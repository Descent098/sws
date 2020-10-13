"""A module for dealing with getting domain information such as:

- If a domain is available
- WHo a domain is registered with
- Other domain details such as, creation_date, name_servers etc.

Notes
-----
- If whois is not installed, the package/executable will be installed

Examples
-----------
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

print(get_domain_info('kieranwood.ca')) # {'creation_date': datetime.datetime(2018, 11, 6, 5, 9, 47), 'expiration_date': datetime.datetime(2020, 11, 6, 5, 9, 47), 'last_updated': datetime.datetime(2020, 1, 8, 8, 9, 44), 'name': 'kieranwood.ca', 'name_servers': {'kevin.ns.cloudflare.com\r', 'sharon.ns.cloudflare.com\r'}, 'registrant_cc': 'redacted for privacy', 'registrar': 'Go Daddy Domains Canada, Inc'}
```

"""

import os
import subprocess
from shutil import move
from datetime import datetime
from calendar import month_name

# Third Party Dependencies
import whois
from pystall.core import build, ZIPResource, _add_to_path


def get_domain_info(domain:str) -> dict:
    """[summary]

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

    print(get_domain_info('kieranwood.ca')) # {'creation_date': datetime.datetime(2018, 11, 6, 5, 9, 47), 'expiration_date': datetime.datetime(2020, 11, 6, 5, 9, 47), 'last_updated': datetime.datetime(2020, 1, 8, 8, 9, 44), 'name': 'kieranwood.ca', 'name_servers': {'kevin.ns.cloudflare.com\r', 'sharon.ns.cloudflare.com\r'}, 'registrant_cc': 'redacted for privacy', 'registrar': 'Go Daddy Domains Canada, Inc'}
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


def domain_availability(domain_query:dict) -> tuple:
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
    # Setting up default downloads folder based on OS
    if os.name == "nt":
        DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads"
        INSTALL_FOLDER = os.path.realpath(f"{os.getenv('USERPROFILE')}\\..\\..\\whois")
    else:  # PORT: For *Nix systems
        DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads"
        INSTALL_FOLDER = f"{os.getenv('HOME')}/whois"
    if not os.path.exists(INSTALL_FOLDER):
        try:
            subprocess.Popen("whois")
        except FileNotFoundError:
            if os.name == "nt":
                build(ZIPResource("whois", "https://download.sysinternals.com/files/WhoIs.zip", overwrite_agreement = True))
                move(f"{DOWNLOAD_FOLDER}{os.sep}whois", INSTALL_FOLDER)
                _add_to_path(INSTALL_FOLDER)
                print("Whois has been installed, restart script")
                exit()
            else:
                ...  #TODO: Figure out linux installation
