"""A module for dealing with getting domain information such as:

- If a domain is available
- Who a domain is registered with
- Other domain details such as, creation_date, name_servers etc.

Notes
-----
- If whois is not installed, the package/executable will be installed

Examples
--------
### Getting details about an available domain
```
from sws.domains import get_domain_info, domain_availability

domain_details = get_domain_info('kieranwood.com')
domain_availability(domain_details) # ('Domain available', True)
```

### Getting details of an unavailable domain
```
from sws.domains import get_domain_info, domain_availability

domain_details = get_domain_info('kieranwood.ca')
domain_availability(domain_details) # ('Domain unavailable until 6/November/2020', False)
```

### Getting details about an unregistered domain
```
from sws.domains import get_domain_info

print(get_domain_info('kieranwood.com')) # {'creation_date': False, 'expiration_date': False, 'last_updated': False, 'name': domain, 'name_servers': False, 'registrant_cc': False, 'registrar': False}
```

### Getting details of a registered domain
```
from sws.domains import get_domain_info

print(get_domain_info('kieranwood.ca')) # {'creation_date': datetime.datetime(2018, 11, 6, 5, 9, 47), 'expiration_date': datetime.datetime(2020, 11, 6, 5, 9, 47), 'last_updated': datetime.datetime(2020, 1, 8, 8, 9, 44), 'name': 'kieranwood.ca', 'name_servers': {'kevin.ns.cloudflare.com', 'sharon.ns.cloudflare.com'}, 'registrant_cc': 'redacted for privacy', 'registrar': 'Go Daddy Domains Canada, Inc'}
```
"""

# Standard Library Dependencies
import os                        # Used for path manipulation
import sys                       # Used to exit safely during errors
import logging                   # Used for logging in debugging etc.
import subprocess                # Used to execute existing binaries
from shutil import move          # Used to move folders within the os
from datetime import datetime    # Used for interpreting dates and times
from calendar import month_name  # Used to convert integer month representations to string representations

# Third Party Dependencies
import whois  # Used to pull domain information
from pystall.core import build, ZIPResource, _add_to_path, APTResource  # Used to install whois binary


def get_domain_info(domain: str) -> dict:
    """Returns a dictionary of all domain information

    Parameters
    ----------
    domain : str
        The domain you want the details for

    Returns
    -------
    dict
        A dictionary of a whois.Domain query

    Notes
    -----
    - If whois is not installed, the package/executable will be installed
    - Make sure to use the domain, and not just a url for example https://kieranwood.ca/hello is a url but kieranwood.ca is a domain
    - In the case that a protocol (http:// or https://) is provided it will be stripped, be aware this can cause comparison issues to the 'name' parameter of the dictionary
    
    Raises
    ------
    ValueError:
        If provided domain is not a valid domain (i.e. Subdomain, or URL instead of domain)

    Examples
    --------
    Getting details about an unregistered domain
    ```
    from sws.domains import get_domain_info

    print(get_domain_info('kieranwood.com')) # {'creation_date': False, 'expiration_date': False, 'last_updated': False, 'name': domain, 'name_servers': False, 'registrant_cc': False, 'registrar': False}
    ```

    Getting details of a registered domain
    ```
    from sws.domains import get_domain_info

    print(get_domain_info('kieranwood.ca')) # {'creation_date': datetime.datetime(2018, 11, 6, 5, 9, 47), 'expiration_date': datetime.datetime(2020, 11, 6, 5, 9, 47), 'last_updated': datetime.datetime(2020, 1, 8, 8, 9, 44), 'name': 'kieranwood.ca', 'name_servers': {'kevin.ns.cloudflare.com', 'sharon.ns.cloudflare.com'}, 'registrant_cc': 'redacted for privacy', 'registrar': 'Go Daddy Domains Canada, Inc'}
    ```
    """
    logging.info(f"Entering get_domain_info(domain={domain})")
    _install_whois()  # Verify/install whois

    # Validation

    ## Strip protocols
    if domain.startswith("https://"):
        logging.info(f"Stripping https:// protocol from {domain}")
        domain = domain.replace("https://", "")
    elif domain.startswith("http://"):
        logging.info(f"Stripping http:// protocol from {domain}")
        domain = domain.replace("http://", "")

    ## Raise error if subdomain
    logging.info(f"Confirming domain {domain} is not a subdomain")
    if len(domain.split(".")) > 2: # If domain is subdomain
        raise ValueError(f"Provided domain {domain} is likely a subdomain")
    
    ## Raise Error if invalid TLD
    try:
        logging.info(f"Querying {domain} with whois")
        domain_details = whois.query(domain)
    except Exception as e:
        if "Unknown TLD:" in str(e):
            raise ValueError(f"Domain {domain} is not a valid domain")

    # ## TODO: When new version of python-whois-extended releases uncomment below code
    # try:
        
    #     if os.name == "nt" and os.path.exists(os.path.realpath(f"{os.getenv('USERPROFILE')}\\..\\..\\whois")):
    #         INSTALL_FOLDER = os.path.realpath(f"{os.getenv('USERPROFILE')}\\..\\..\\whois\\whois.exe")
    #         domain_details = whois.query(domain, executable=INSTALL_FOLDER)
    #     else:
    #         domain_details = whois.query(domain)
    # except Exception as e:
    #     if "Unknown TLD:" in str(e):
    #         raise ValueError(f"Domain {domain} is not a valid domain")
    #     else:
    #         raise e

    # Parse response
    try:
        if domain_details is None:  # If the domain is not registered and query completely failed
            logging.info(f"""Exiting get_domain_info() and returning {{'creation_date': False,
                    'expiration_date': False,
                    'last_updated': False,
                    'name': {domain},
                    'name_servers': False,
                    'registrant_cc': False,
                    'registrar': False}}""")
            return {'creation_date': False,
                    'expiration_date': False,
                    'last_updated': False,
                    'name': domain,
                    'name_servers': False,
                    'registrant_cc': False,
                    'registrar': False}

        elif not domain_details:  # If the domain is not registered
            logging.info(f"""Exiting get_domain_info() and returning {{'creation_date': False,
                    'expiration_date': False,
                    'last_updated': False,
                    'name': {domain},
                    'name_servers': False,
                    'registrant_cc': False,
                    'registrar': False}}""")
            return {'creation_date': False,
                    'expiration_date': False,
                    'last_updated': False,
                    'name': domain,
                    'name_servers': False,
                    'registrant_cc': False,
                    'registrar': False}

        else:  # If there was domain info
            logging.info(f"Exiting get_domain_info() and returning {vars(domain_details)}")
            return vars(domain_details)

    except UnboundLocalError: # When the variable never gets assigned after a failure
        logging.info(f"""Exiting get_domain_info() and returning {{'creation_date': False,
                    'expiration_date': False,
                    'last_updated': False,
                    'name': {domain},
                    'name_servers': False,
                    'registrant_cc': False,
                    'registrar': False}}""")
        return {'creation_date': False,
                    'expiration_date': False,
                    'last_updated': False,
                    'name': domain,
                    'name_servers': False,
                    'registrant_cc': False,
                    'registrar': False}


def domain_availability(domain_query: dict) -> tuple:
    """Checks the availability of a domain

    Parameters
    ----------
    domain_query : dict
        The dictionary representation of a whois.Domain object

    Returns
    -------
    tuple[str, bool]
        Returns a tuple with a printable string about availability, 
        and a bool that's True if it's available and False if not

    Examples
    --------
    Getting details about an available domain
    ```
    from sws.domains import get_domain_info, domain_availability

    domain_details = get_domain_info('kieranwood.com')
    domain_availability(domain_details) # ('Domain available', True)
    ```

    Getting details of an unavailable domain
    ```
    from sws.domains import get_domain_info, domain_availability

    domain_details = get_domain_info('kieranwood.ca')
    domain_availability(domain_details) # ('Domain unavailable until 6/November/2020', False)
    ```
    """
    logging.info(f"Entering get_domain_info(domain_query={domain_query})")
    if not domain_query["expiration_date"] or domain_query["expiration_date"] < datetime.today():
        logging.info("Domain available, returning ('Domain available', True)")
        return "Domain available", True
    else:
        logging.info(f"Domain unavailable, returning ('Domain {domain_query['name']} unavailable until {domain_query['expiration_date'].day}/{month_name[domain_query['expiration_date'].month]}/{domain_query['expiration_date'].year}', False)")
        return f"Domain {domain_query['name']} unavailable until {domain_query['expiration_date'].day}/{month_name[domain_query['expiration_date'].month]}/{domain_query['expiration_date'].year}", False


def _install_whois():
    """Used to install whois binary if it isn't available"""
    logging.info("Entering _install_whois()")
    # Setting up default downloads folder based on OS
    if os.name == "nt":
        DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads"
        INSTALL_FOLDER = os.path.realpath(f"{os.getenv('USERPROFILE')}\\..\\..\\whois")
    else:  # PORT: For *Nix systems
        DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads"
        INSTALL_FOLDER = f"{os.getenv('HOME')}/whois"
    if not os.path.exists(INSTALL_FOLDER):
        try:
            subprocess.Popen("whois")  # Check if binary is installed
        except FileNotFoundError:
            if os.name == "nt":  # Install windows version of whois
                logging.info(f"System is windows manually installing: DOWNLOAD_FOLDER = {DOWNLOAD_FOLDER}, INSTALL_FOLDER = {INSTALL_FOLDER}")
                logging.info(f"Downloading whois from https://download.sysinternals.com/files/WhoIs.zip and installing to {INSTALL_FOLDER}")
                build(ZIPResource("whois", "https://download.sysinternals.com/files/WhoIs.zip", overwrite_agreement=True))
                move(f"{DOWNLOAD_FOLDER}{os.sep}whois", INSTALL_FOLDER)
                logging.warning("Beginning adding whois to path variable")
                _add_to_path(INSTALL_FOLDER) # TODO: When new version of python-whois-extended releases remove this call
                print("Whois has been installed, restart script") # TODO: When new version of python-whois-extended releases remove this call
                sys.exit()
            else:  # Linux Installation
                try:
                    logging.info(f"System is nix, installing with APT: DOWNLOAD_FOLDER = {DOWNLOAD_FOLDER}, INSTALL_FOLDER = {INSTALL_FOLDER}")
                    build(APTResource("whois", "whois", overwrite_agreement=True))
                except:
                    raise Exception("Unable to find or install whois, please install binary and try again")
