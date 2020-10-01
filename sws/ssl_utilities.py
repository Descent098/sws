"""Get deails about the ssl cert of a hostname such as:
- When the cert will expire
- The issuer of the cert
- A full dict of the details of the cert

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
"""

# Internal Dependencies
import ssl                      # Used to get details about SSL certs
import socket                   # Used to make a request to get SSL cert
from datetime import datetime   # Used to make simple datetime representations of expiries

def check_ssl_expiry(hostname):
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

    Example
    -------
    Check when kieranwood.ca SSL cert expires
    ```
    from sws.ssl_utlities import check_ssl_expiry

    print(check_ssl_expiry('kieranwood.ca')) # prints: 'Oct  9 12:00:00 2020 GMT'
    ```
    """
    cert = get_ssl_cert(hostname)

    expiry_date = cert["notAfter"]

    return expiry_date

def get_ssl_cert(hostname):
    """Returns all available SSL information, such as notAfter, commonName etc.

    Arguments
    ---------
    hostname : str
        A string of a FQDN (root URL with no protocol) for example 'kieranwood.ca'.

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
    context_socket = _get_ssl_socket(hostname)
    context_socket.connect((hostname, 443)) # Connects to the host over a socket
    cert = context_socket.getpeercert() # Dictionary containing all the certificate information

    return cert

def get_ssl_issuer()->str:
    #TODO
    pass

def _get_ssl_socket(hostname):
    """Get's the context for a host over SSL

    Parameters
    ----------
    hostname: (str)
        The hostname to instantiate a SSL socket context to

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
    context = ssl.create_default_context()
    context_socket = context.wrap_socket(socket.socket(), server_hostname=hostname)
    return context_socket