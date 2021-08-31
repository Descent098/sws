"""Get deails about the ssl cert of a hostname such as:

- When the cert will expire
- The issuer of the cert
- A full dict of the details of the cert

Notes
-----
- You should use an FQDN for any ssl_utilties functions, so something like https://www.google.ca becomes google.ca

Examples
--------
### Check when kieranwood.ca SSL cert expires
```
from sws.ssl_utlities import check_ssl_expiry

print(check_ssl_expiry('kieranwood.ca')) # prints: 'Oct  9 12:00:00 2020 GMT'
```

### Print the full cert details of kieranwood.ca
```
from pprint import pprint

from sws.ssl_utlities import check_ssl_expiry

pprint(get_ssl_cert('kieranwood.ca'))
# Prints:
'''
    {'OCSP': ('http://ocsp.digicert.com',),
    'caIssuers': ('http://cacerts.digicert.com/CloudFlareIncECCCA-2.crt',),
    'crlDistributionPoints': ('http://crl3.digicert.com/CloudFlareIncECCCA2.crl',
                            'http://crl4.digicert.com/CloudFlareIncECCCA2.crl'),
    'issuer': ((('countryName', 'US'),),
                (('stateOrProvinceName', 'CA'),),
                (('localityName', 'San Francisco'),),
                (('organizationName', 'CloudFlare, Inc.'),),
                (('commonName', 'CloudFlare Inc ECC CA-2'),)),
    'notAfter': 'Oct  9 12:00:00 2020 GMT',
    'notBefore': 'Jan  8 00:00:00 2020 GMT',
    'serialNumber': '06C5F428AF7D8439EB013216CB300B6A',
    'subject': ((('countryName', 'US'),),
                (('stateOrProvinceName', 'CA'),),
                (('localityName', 'San Francisco'),),
                (('organizationName', 'Cloudflare, Inc.'),),
                (('commonName', 'sni.cloudflaressl.com'),)),
    'subjectAltName': (('DNS', 'kieranwood.ca'),
                        ('DNS', 'sni.cloudflaressl.com'),
                        ('DNS', '*.kieranwood.ca')),
    'version': 3}
'''
```

### Get issuer details of existing hostname
```
from sws.ssl_utilities import get_ssl_issuer

get_ssl_issuer("kieranwood.ca") # Returns [('countryName', 'US'), ('organizationName', 'Cloudflare, Inc.'), ('commonName', 'Cloudflare Inc ECC CA-3')]
```

### Get issuer details of non-existing hostname
```
from sws.ssl_utilities import get_ssl_issuer

get_ssl_issuer("kieranwood.com") # Returns False
```
"""

# Internal Dependencies
import ssl                      # Used to get details about SSL certs
import socket                   # Used to make a request to get SSL cert
import logging                  # Used in logging for debug and info messages
from typing import Union        # Used to help provide more detailed type hints


def check_ssl_expiry(hostname: str) -> str:
    """Allows you to check the SSL expiry for a FQDN;
    More specifically it will return the notAfter for the SSL cert associated with the FQDN.

    Arguments
    ---------
    hostname : str
        A string of a FQDN (root URL with no protocol) for example 'kieranwood.ca'.

    Returns
    -------
    str:
        A the expiry of the domain name in MMM DD HH:MM:SS YYYY TZ format

    Raises
    ------
    ValueError:
        If hostname is not a valid domain

    Example
    -------
    Check when kieranwood.ca SSL cert expires
    ```
    from sws.ssl_utlities import check_ssl_expiry

    print(check_ssl_expiry('kieranwood.ca')) # prints: 'Oct  9 12:00:00 2020 GMT'
    ```
    """
    logging.info(f"check_ssl_expiry(hostname={hostname})")
    try:
        logging.info(f"Getting cert info for {hostname}")
        cert = get_ssl_cert(hostname)
    except socket.gaierror:
        raise ValueError(f"Unable to connect to {hostname}")

    expiry_date = cert["notAfter"]

    logging.info(f"exiting check_ssl_expiry() and returning {expiry_date}")
    return expiry_date


def get_ssl_cert(hostname: str) -> dict:
    """Returns all available SSL information, such as notAfter, commonName etc.

    Arguments
    ---------
    hostname : str
        A string of a FQDN (root URL with no protocol) for example 'kieranwood.ca'

    Raises
    ------
    ValueError:
        If hostname is not a valid domain

    Returns
    -------
    dict:
        The details about the SSL certificate

    Example
    -------
    Print the full cert details of kieranwood.ca
    ```
    from pprint import pprint

    from sws.ssl_utlities import check_ssl_expiry

    pprint(get_ssl_cert('kieranwood.ca'))
    # Prints:
    '''
        {'OCSP': ('http://ocsp.digicert.com',),
        'caIssuers': ('http://cacerts.digicert.com/CloudFlareIncECCCA-2.crt',),
        'crlDistributionPoints': ('http://crl3.digicert.com/CloudFlareIncECCCA2.crl',
                                'http://crl4.digicert.com/CloudFlareIncECCCA2.crl'),
        'issuer': ((('countryName', 'US'),),
                    (('stateOrProvinceName', 'CA'),),
                    (('localityName', 'San Francisco'),),
                    (('organizationName', 'CloudFlare, Inc.'),),
                    (('commonName', 'CloudFlare Inc ECC CA-2'),)),
        'notAfter': 'Oct  9 12:00:00 2020 GMT',
        'notBefore': 'Jan  8 00:00:00 2020 GMT',
        'serialNumber': '06C5F428AF7D8439EB013216CB300B6A',
        'subject': ((('countryName', 'US'),),
                    (('stateOrProvinceName', 'CA'),),
                    (('localityName', 'San Francisco'),),
                    (('organizationName', 'Cloudflare, Inc.'),),
                    (('commonName', 'sni.cloudflaressl.com'),)),
        'subjectAltName': (('DNS', 'kieranwood.ca'),
                            ('DNS', 'sni.cloudflaressl.com'),
                            ('DNS', '*.kieranwood.ca')),
        'version': 3}
    '''
    ```
    """
    logging.info(f"get_ssl_cert(hostname={hostname})")
    # Strip protocols from hostname if they exist
    if hostname.startswith("https://"):
        logging.info(f"Stripping https:// protocol from {hostname}")
        hostname = hostname.replace("https://", "")
    elif hostname.startswith("http://"):
        logging.info(f"Stripping http:// protocol from {hostname}")
        hostname = hostname.replace("http://", "")

    try:
        logging.info("Making SSL socket connection to retrieve info")
        context_socket = _get_ssl_socket(hostname)
        context_socket.connect((hostname, 443))  # Connects to the host over a socket
        cert = context_socket.getpeercert()  # Dictionary containing all the certificate information
    except socket.gaierror:
        raise ValueError(f"Unable to connect to {hostname}")

    logging.info(f"exiting get_ssl_cert() and returning {cert}")
    return cert


def get_ssl_issuer(hostname: str) -> Union[list, bool]:
    """Get's the details for the issuer of the hostname's SSL cert

    Parameters
    ----------
    hostname : str
        The hostname you want to get the issuer for

    Raises
    ------
    ValueError:
        If hostname is not a valid domain

    Returns
    -------
    list[tuple[str,str]] or False
        Returns a list of tuples with details about the SSL issuer,
        or False if there is no SSL cert for associated domain

    Examples
    --------
    Get details of existing hostname
    ```
    from sws.ssl_utilities import get_ssl_issuer

    get_ssl_issuer("kieranwood.ca") # Returns [('countryName', 'US'), ('organizationName', 'Cloudflare, Inc.'), ('commonName', 'Cloudflare Inc ECC CA-3')]
    ```

    Get details of non-existing hostname
    ```
    from sws.ssl_utilities import get_ssl_issuer

    get_ssl_issuer("kieranwood.com") # Returns False
    ```
    """
    logging.info(f"get_ssl_issuer(hostname={hostname})")
    # Strip protocols from hostname if they exist
    if hostname.startswith("https://"):
        logging.info(f"Stripping https:// protocol from {hostname}")
        hostname = hostname.replace("https://", "")
    elif hostname.startswith("http://"):
        logging.info(f"Stripping http:// protocol from {hostname}")
        hostname = hostname.replace("http://", "")
    try:
        cert = get_ssl_cert(hostname)
    except socket.gaierror:
        raise ValueError(f"Unable to connect to {hostname}")
    if cert["issuer"]:
        issuer = [data[0] for data in cert["issuer"]]
        logging.info(f"exiting get_ssl_issuer() and returning {issuer}")
        return issuer
    else:
        logging.info("exiting get_ssl_issuer() and returning False")
        return False


def _get_ssl_socket(hostname: str) -> ssl.SSLSocket:
    """Get's the context for a host over SSL

    Parameters
    ----------
    hostname: (str)
        The hostname to instantiate a SSL socket context to

    Raises
    ------
    ValueError:
        If hostname is not a valid domain

    Returns
    -------
    SSLSocket:
        A socket that can be used to connect to the hostname

    Examples
    --------
    ```
    context_socket = _get_ssl_context(hostname)

    context_socket.connect((hostname, 443)) # Connects to the host over a socket
    ```
    """
    # Strip protocols from hostname if they exist
    if hostname.startswith("http://"):
        hostname = hostname.replace("http://", "")
    elif hostname.startswith("https://"):
        hostname = hostname.replace("https://", "")
    context = ssl.create_default_context()
    context_socket = context.wrap_socket(socket.socket(), server_hostname=hostname)
    return context_socket
