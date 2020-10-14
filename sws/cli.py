"""The primary entrypoint for the sws script.

This module's main function contains all the argument
parsing for the sws script.

Module Variabes
---------------
usage : str
    A variable that defines the argument parsing for the script in standard POSIX format.
"""

# Python Standard library
import sys                        # Used to check number of arguments
from pprint import pprint         # Used to pretty-print to command line

# External Dependencies
from docopt import docopt         # Used to parse CLI arguments

# Internal Dependencies
from sws.domains import *         # Import all domains utilities
from sws.youtube import *         # Import all youtube utilities
from sws.ssl_utilities import *   # Import all ssl_utilties functions
from sws.redirects import trace   # Import trace from redirect utilities

usage = """Super Web Scripts; A command line interface, and set of scripts for web tasks.

Usage:
    sws [-h] [-v]
    sws youtube <url> [<path>]
    sws ssl <hostname> [-e] [-c]
    sws redirects <url> [<ignored>]
    sws domains <domain> [-e] [-r] [-d] [-a] [-t]

Options:
    -h --help               Show this help message and exit
    -v --version            Show program's version number and exit
    -e --expiry             If specified will check the expiry of ssl cert/domain
    -c --cert               If specified will print the full details of the SSL cert
    -r --registrar          Tells you who the domain is registered through
    -d --details            If specified will show full domain details
    -a --available          Gives information on whether a specific domain is available
"""

def main():
    """Primary entrypoint for the sws script."""
    args = docopt(usage, version="sws V0.2.0")  # Grab arguments for parsing

    if len(sys.argv) == 1:  # if no arguments are provided
        print(usage)

    if args["ssl"]:  # Begin parsing for ssl subcommand
        if args["--expiry"]:  # If -e or --expiry is specified
            print(f"Domain {args['<hostname>']} Expires on: {check_ssl_expiry(args['<hostname>'])}")
        if args["--cert"]:  # If -c or --cert is specified
            pprint(get_ssl_cert(args['<hostname>']))

    if args["redirects"]:  # Begin parsing for redirects subcommand
        print(args["<ignored>"])
        if args["<ignored>"]:
            if args["<ignored>"].startswith("["):
                args["<ignored>"] = list(args["<ignored>"])
        trace(args["<url>"], args["<ignored>"], print_result=True)

    if args["youtube"]:
        download(args["<url>"], args["<path>"])

    if args["domains"]:  # Begin parsing for ssl subcommand
        domain_details = get_domain_info(args["<domain>"])
        if args["--expiry"]:  # If -e or --expiry is specified
            pprint(domain_details["expiration_date"])
        if args["--registrar"]:
            if domain_details["registrar"]:
                print(f"{args['<domain>']} is registered through {domain_details['registrar']}")
            else:
                print(f"{args['<domain>']} is not registered")
        if args["--details"]:
            pprint(domain_details)
        if args["--available"]:
            print(domain_availability(domain_details)[0])
