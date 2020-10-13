"""The primary entrypoint for the sws script.

This module's main function contains all the argument
parsing for the sws script.

Module Variabes
---------------
usage : str
    A variable that defines the argument parsing for the script in standard POSIX format.
"""

# Python Standard library
import sys                       # Used to validate arguments are given at the command line
from pprint import pprint        # Used to pretty-print to command line


# External Dependencies
from docopt import docopt        # Used to parse CLI arguments

# Internal Dependencies
from sws.domains import *        # Import domain utilities
from sws.ssl_utilities import *  # Import SSL utilities
from sws.redirects import trace  # Import redirect utilities
from sws.youtube import download # Import youtube utilities

usage = """Super Web Scripts; A command line interface, and set of scripts for web tasks.

Usage:
    sws [-h] [-v]
    sws redirects <url> [-t]
    sws youtube <url> [<path>]
    sws ssl <hostname> [-e] [-c]
    sws domains <domain> [-e] [-r] [-d] [-a] [-t]

Options:
    -h --help               Show this help message and exit
    -v --version            Show program's version number and exit
    -e --expiry             If specified will check the expiry of ssl cert/domain
    -c --cert               If specified will print the full details of the SSL cert
    -t --trace              If specified will show the full trace of the provided url
    -r --registered         Tells you if the domain has been registered
    -d --details            If specified will show full domain details
    -a --available          Show this help message and exit
"""

def main():
    """Primary entrypoint for the sws script."""
    args = docopt(usage, version="sws V0.2.0")  # Grab arguments for parsing

    if len(sys.argv) == 1: # if no arguments are provided
        print(usage)

    if args["ssl"]:  # Begin parsing for ssl subcommand
        if args["--expiry"]:  # If -e or --expiry is specified
            print(f"Domain {args['<hostname>']} Expires on: {check_ssl_expiry(args['<hostname>'])}")

        if args["--cert"]:  # If -c or --cert is specified
            pprint(get_ssl_cert(args['<hostname>']))

    if args["redirects"]:  # Begin parsing for redirects subcommand
        if args["--trace"]:  # If -t or --trace is specified
            if "https://" in args["<url>"]:
                args["<url>"] = args["<url>"].replace("https://", "http://")
            trace(args["<url>"], [], print_result=True)

    if args["youtube"]:
        if not args["<path>"]:
            args["<path>"] = "."
        download(args["<url>"], args["<path>"])

    if args["domains"]:  # Begin parsing for ssl subcommand
        domain_details = get_domain_info(args["<domain>"])
        if args["--expiry"]:  # If -e or --expiry is specified
            pprint(domain_details["expiration_date"])
        if args["--registered"]:
            if domain_details["registrar"]:
                print(f"{args['<domain>']} is registered through {domain_details['registrar']}")
            else:
                print(f"{args['<domain>']} is not registered")
        if args["--details"]:
            pprint(domain_details)
        if args["--available"]:
            print(domain_availability(domain_details)[0])
