"""An api and cli for doing common web development tasks

Goals
-----
This project has several goals:

1. Provide cross-platform implementations of functions (where possible)
2. Serve as a repository of general knowledge to share solutions to issues with people
3. Give people access to source code to learn how the functions work and just pull what's needed
4. Provide a useful API for well developed functions with error catching and testing for commonly annoying situations

Installation
------------
### From PyPi

run ```pip install sws``` or ```sudo pip3 install sws```.

### From source

1. Clone the github repo ([https://github.com/Descent098/sws](https://github.com/Descent098/sws))
2. cd into the 'sws' root directory (where setup.py is) and run ```pip install .``` or ```sudo pip3 install . ```

Modules
-------
### domains
A module for dealing with getting domain information such as:

- If a domain is available
- Who a domain is registered with
- Other domain details such as, creation_date, name_servers etc.

### dns_utilities
A module for getting DNS configurations on a domain

### downloads
Module that provides a class for doing downloads that feature:

- 4xx and 5xx error catching
- Progress bars for downloads
- Additional download metadata
- Easy printable debugging

### redirects
Provides a function for tracing redirects

### ssl_utilities
Get deails about the ssl cert of a hostname such as:

- When the cert will expire
- The issuer of the cert
- A full dict of the details of the cert

### youtube
Provides functionality for working with YouTube videos such as:

- Downloading youtube videos
- Pulling video metadata

Notes
-----
- When using the domain module if ```whois``` is not installed, the package/executable will be installed
- You should use an FQDN for any ```ssl_utilties``` or ```domains``` functions, so something like https://www.google.ca becomes google.ca
- All functions include logging and can be attached to for debugging assitance
"""


__pdoc__ = {"sws.cli": False} # Ignore the CLI in the API docs
