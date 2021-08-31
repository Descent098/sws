

![sws-banner](./img/sws-banner.png)

# Welcome to the sws documentation!

## what is sws?

sws is a utility I wrote with the intention of implementing some common web scripts into one cohesive library. it is primarily intended to be used as a standalone script, but it can also be used as an API. 

## Installation

### From PyPi

run ```pip install sws``` or ```sudo pip3 install sws```.

### From source

1. Clone the github repo ([https://github.com/Descent098/sws](https://github.com/Descent098/sws))
2. cd into the 'sws' root directory (where setup.py is) and run ```pip install .``` or ```sudo pip3 install . ```


## Script Usage
You can validate it is installed properly by typing ```sws``` into your terminal, the output should look like this:

Additional details can be found at the documentation available on [https://sws.readthedocs.io/](https://sws.readthedocs.io/).

You can validate it is installed properly by typing ```sws``` into your terminal, the output should look like this:

```bash
Super Web Scripts; A command line interface, and set of scripts for web tasks.

Usage:
    sws [-h] [-v]
    sws dns <domain>
    sws youtube <url> [<path>]
    sws ssl <hostname> [-e] [-c]
    sws redirects <url> [<ignored>]
    sws domains <domain> [-e] [-r] [-d] [-a]
    

Options:
    -h --help               Show this help message and exit
    -v --version            Show program's version number and exit
    -e --expiry             If specified will check the expiry of ssl cert/domain
    -c --cert               If specified will print the full details of the SSL cert
    -r --registrar          Tells you who the domain is registered through
    -d --details            If specified will show full domain details
    -a --available          Gives information on whether a specific domain is available
```

<u>Required Positional Arguments:</u>

- *\<url\>*;  This is a **positional** placeholder value for a url you want to act upon. This should include a protocol (http:// or https://).

- *\<hostname\>*;  This is a **positional** placeholder value for the FQDN you want to run a command on, this is the root of a website without a protocol. For example the site http://kieranwood.ca would have an FQDN of kieranwood.ca

- *\<domain\>*;  This is a **positional** placeholder value for the FQDN you want to run a command on, this is the root of a website without a protocol. For example the site http://kieranwood.ca would have an FQDN of kieranwood.ca

### dns

Prints a table of the DNS records for a given domain

#### Examples

*Get dns records for kieranwood.ca*

`sws dns kieranwood.ca`

which prints:

```text
DNS records for kieranwood.ca

| Record Type | Record Value |
|-------------|--------------|
|      A      | 104.21.47.45 |
|             |172.67.144.116|
|=============|==============|
|     NS      |kevin.ns.cloudflare.com.|
|             |sharon.ns.cloudflare.com.|
|=============|==============|
|     SOA     |kevin.ns.cloudflare.com. dns.cloudflare.com. 2036568886 10000 2400 604800 3600|
|=============|==============|
|    AAAA     |2606:4700:3037::ac43:9074|
|             |2606:4700:3035::6815:2f2d|
|=============|==============|
|    HTTPS    |  alpn="h2"   |
|             |ipv4hint="104.21.47.45,172.67.144.116"|
|             |ipv6hint="2606:4700:3035::6815:2f2d,2606:4700:3037::ac43:9074"|
|=============|==============|
```

### domains

Used to pull details about a domain name

- \-e or \-\-expiry; If specified will check the expiry of ssl cert/domain
- \-r or \-\-registrar; Tells you who the domain is registered through
- \-d or \-\-details; If specified will show full domain details
- \-a or \-\-available; Gives information on whether a specific domain is available

#### Examples

*Get expiry date for kieranwood.ca*

`sws domains kieranwood.ca -e`

Which prints:

```Domain kieranwood.ca set to expire on 06-Nov-2022 05:09:47```

*Get all available details about kieranwood.ca*

`sws domains kieranwood.ca -d`

Which prints:

```
{'creation_date': datetime.datetime(2018, 11, 6, 5, 9, 47),
 'expiration_date': datetime.datetime(2022, 11, 6, 5, 9, 47),
 'last_updated': datetime.datetime(2020, 11, 7, 14, 52, 12),
 'name': 'kieranwood.ca',
 'name_servers': {'sharon.ns.cloudflare.com', 'kevin.ns.cloudflare.com'},
 'registrant_cc': 'redacted for privacy',
 'registrar': 'Go Daddy Domains Canada, Inc'}
```

### redirects

Allows you to trace and validate redirects

<u>Optional Arguments:</u>

- *\<ignored\>*;  A list of domains to ignore. i.e. ["google.com"] would skip any redirects that include "google.com"

#### Examples

`sws redirects http://kieranwood.ca`

Which prints

```
Printing response for http://kieranwood.ca

Redirect level:1
URL: http://kieranwood.ca/
HTTP Code: 301

Redirect level:2
URL: https://kieranwood.ca/
HTTP Code: 200
```

### youtube

Allows you to get youtube video metadata and download videos

<u>Optional Arguments:</u>

- *\<path\>*;  This is a **positional** placeholder value for the path that you want to store the video to.


#### Examples

*Downloads video to current working directory*

`sws youtube https://www.youtube.com/watch?v=6j1I3mC0BR0 .`

Which prints

`Downloading Python Packaging Template usage documentation to C:\Users\Kieran\Desktop`

### ssl

Get deails about the ssl cert of a hostname

<u>Optional Arguments:</u>

- *\-e or \-\-expiry*: Print the expiry of the cert
- *\-c or \-\-cert*: Print the full list of info about a ssl cert

#### Examples

*Check expiry of ssl cert*

`sws ssl kieranwood.ca -e`

Which prints

`SSL cert on domain kieranwood.ca Expires on: Jun 24 23:59:59 2022 GMT`

*Check details of ssl cert*

`sws ssl kieranwood.ca -c`

Which prints

```
{'OCSP': ('http://ocsp.digicert.com',),
 'caIssuers': ('http://cacerts.digicert.com/CloudflareIncECCCA-3.crt',),
 'crlDistributionPoints': ('http://crl3.digicert.com/CloudflareIncECCCA-3.crl',
                           'http://crl4.digicert.com/CloudflareIncECCCA-3.crl'),
 'issuer': ((('countryName', 'US'),),
            (('organizationName', 'Cloudflare, Inc.'),),
            (('commonName', 'Cloudflare Inc ECC CA-3'),)),
 'notAfter': 'Jun 24 23:59:59 2022 GMT',
 'notBefore': 'Jun 25 00:00:00 2021 GMT',
 'serialNumber': '07FB54A58560923CE9261742D4E4112D',
 'subject': ((('countryName', 'US'),),
             (('stateOrProvinceName', 'California'),),
             (('localityName', 'San Francisco'),),
             (('organizationName', 'Cloudflare, Inc.'),),
             (('commonName', 'sni.cloudflaressl.com'),)),
 'subjectAltName': (('DNS', 'sni.cloudflaressl.com'),
                    ('DNS', '*.kieranwood.ca'),
                    ('DNS', 'kieranwood.ca')),
 'version': 3}
```

## API usage

Details on API usage can be found here [https://kieranwood.ca/sws/](https://kieranwood.ca/sws/). All functions include logging and can be attached to with a standard logger for debugging assitance.


You can also build local API docs by installing [pdoc3](https://pdoc3.github.io/pdoc/) (```pip install pdoc3``` or ```sudo pip3 install pdoc3```), and then running ```pdoc sws --http localhost:8080```. Go to a browser and type in [http://localhost:8080/sws/utilities/](http://localhost:8080/sws/utilities/)

