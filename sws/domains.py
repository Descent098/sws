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
    _install_whois()  # Verify/install whois
    domain = whois.query(domain)
    if not domain:  # If the domain is not registered
        return {'creation_date': False,
                'expiration_date': False,
                'last_updated': False,
                'name': domain,
                'name_servers': False,
                'registrant_cc': False,
                'registrar': False}
    else:  # If there was domain info
        return vars(domain)


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
    if not domain_query["expiration_date"] or domain_query["expiration_date"] < datetime.today():
        return "Domain available", True
    else:
        return f"Domain unavailable until {domain_query['expiration_date'].day}/{month_name[domain_query['expiration_date'].month]}/{domain_query['expiration_date'].year}", False


def _install_whois():
    """Used to install whois binary if it isn't available"""
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
                build(ZIPResource("whois", "https://download.sysinternals.com/files/WhoIs.zip", overwrite_agreement=True))
                move(f"{DOWNLOAD_FOLDER}{os.sep}whois", INSTALL_FOLDER)
                _add_to_path(INSTALL_FOLDER)
                print("Whois has been installed, restart script")
                sys.exit()
            else:  # Linux Installation
                build(APTResource("whois", "whois", overwrite_agreement=True))
