"""The primary entrypoint for the sws script.

This module's main function contains all the argument
parsing for the sws script.

Functions
---------
main:
    Primary entrypoint for the sws script.

Module Variabes
---------------
usage : str
    A variable that defines the argument parsing for the script in standard POSIX format.

"""

# Python Standard library
import sys
import os
from pprint import pprint

# External Dependencies
from docopt import docopt

# Internal Dependencies
from .utilities.youtube import download
from .utilities.redirects import trace
from .utilities.ssl_utilities import check_ssl_expiry, get_ssl_cert
from .utilities.domains import register_key

usage = """Super Web Scripts; A command line interface, and set of scripts for web tasks.

Usage:
    sws [-h] [-v]
    sws redirects <url> [-t]
    sws youtube <url> [<path>]
    sws ssl <hostname> [-e] [-c]

Options:
    -h --help               Show this help message and exit
    -v --version            Show program's version number and exit
    -e --expiry             If specified will check the expiry of ssl cert/domain
    -c --cert               If specified will print the full details of the SSL cert
    -t --trace              If specified will show the full trace of the provided url

"""

def main():
    """Primary entrypoint for the sws script."""
    args = docopt(usage, version="sws V0.0.6") # Grab arguments for parsing

    if len(sys.argv) == 1:
        print(usage)

    if args["ssl"]: # Begin parsing for ssl subcommand
        if args["--expiry"]: # If -e or --expiry is specified
            print(f"Domain {args['<hostname>']} Expires on: {check_ssl_expiry(args['<hostname>'])}")

        if args["--cert"]: # If -c or --cert is specified
            pprint(get_ssl_cert(args['<hostname>']))
    
    if args["redirects"]: # Begin parsing for redirects subcommand
        if args["--trace"]: # If -t or --trace is specified
            if "https://" in args["<url>"]:
                args["<url>"] = args["<url>"].replace("https://", "http://")
            trace(args["<url>"], print_result=True)

    if args["youtube"]:
        if not args["<path>"]:
            args["<path>"] = "."
        download(args["<url>"], args["<path>"])

    # Info for domains command once re-implemented

    # Docopt info
    # sws domains [-k=<whoiskey>]
    # sws domains <domain> [-e] [-k=<whoiskey>]

    # -k --key=<whoiskey>     If specified will register the whois domain key SEE: https://jsonwhois.io/

    # Argument parsing
    # if args["domains"]: # Begin parsing for ssl subcommand
    #     if args["--expiry"]: # If -e or --expiry is specified
    #         pass
    #     if args["--key"]:
    #         register_key(args["--key"])


