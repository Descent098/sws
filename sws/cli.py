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
from sdu.autocomplete import *    # Used to generate bash autocomplete

# Internal Dependencies
from sws.domains import *         # Import all domains utilities
from sws.youtube import *         # Import all youtube utilities
from sws.ssl_utilities import *   # Import all ssl_utilties functions
from sws.redirects import trace   # Import trace from redirect utilities
from sws.dns_utilities import *   # Import all dns utilitites

usage = """Super Web Scripts; A command line interface, API, and set of scripts for web tasks

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
"""

command_list = [  # Used for autocompletion generation
    command("dns", []),
    command("youtube", []),
    command("ssl", ["-e", "--expiry", "-c", "--cert"]),
    command("redirects", []),
    command("domains", ["-e", "--expiry", "-r", "--registrar", "-d", "--details", "-a", "--available"]),
]


def main():
    """Primary entrypoint for the sws script."""
    args = docopt(usage, version="sws V0.2.0")  # Grab arguments for parsing

    if len(sys.argv) == 1:  # if no arguments are provided
        print(usage)
        if not os.name == "nt":  # Generate bash autocomplete
            autocomplete_file_text = generate_bash_autocomplete(command_list)
            try:
                with open("/etc/bash_completion.d/sws.sh", "w") as autocomplete_file:
                    autocomplete_file.write(autocomplete_file_text)
                print("Bash autocompletion file written to /etc/bash_completion.d/sws.sh \nPlease restart shell for autocomplete to update")
            except PermissionError:
                print("Unable to write bash autocompletion file for sws are you sudo?")
        sys.exit()

    if args["dns"]:
        dns_dict = get_dns_records(args['<domain>'], as_dict=True)
        print(dns_result_table(args['<domain>'], dns_dict))

    elif args["ssl"]:  # Begin parsing for ssl subcommand
        if args["--expiry"]:  # If -e or --expiry is specified
            print(f"SSL cert on domain {args['<hostname>']} Expires on: {check_ssl_expiry(args['<hostname>'])}")
        if args["--cert"]:  # If -c or --cert is specified
            pprint(get_ssl_cert(args['<hostname>']))
        if not (args["--expiry"] or args["--cert"]):
            print(usage)
            sys.exit()

    elif args["redirects"]:  # Begin parsing for redirects subcommand
        if args["<ignored>"]:
            if args["<ignored>"].startswith("["):
                args["<ignored>"] = list(args["<ignored>"])
        try:
            trace(args["<url>"], args["<ignored>"], print_result=True)
        except ValueError as e:
            print(e)

    elif args["youtube"]:
        download(args["<url>"], args["<path>"])

    elif args["domains"]:  # Begin parsing for ssl subcommand
        domain_details = get_domain_info(args["<domain>"])

        if args["--expiry"]:  # If -e or --expiry is specified
            expiry_date = domain_details["expiration_date"]
            if expiry_date:
                print(f"Domain {args['<domain>']} set to expire on {expiry_date.strftime('%d-%b-%Y %H:%M:%S')}")
            else:
                print(f"Domain {args['<domain>']} is expired")
        if args["--registrar"]:
            if domain_details["registrar"]:
                print(f"{args['<domain>']} is registered through {domain_details['registrar']}")
            else:
                print(f"{args['<domain>']} is not registered")
        if args["--details"]:
            if not domain_details['creation_date']:
                print(f"Domain {args['<domain>']} was not registered")
            pprint(domain_details)
        if args["--available"]:
            print(f"Domain {args['<domain>']} is available" if domain_availability(domain_details)[1] else f"{domain_availability(domain_details)[0]}")

        if not (args["--expiry"] or args["--registrar"] or args["--details"] or args["--available"]):
            print(usage)
            sys.exit()

    else:
        print(usage)
        if not os.name == "nt":  # Generate bash autocomplete
            autocomplete_file_text = generate_bash_autocomplete(command_list)
            try:
                with open("/etc/bash_completion.d/sws.sh", "w") as autocomplete_file:
                    autocomplete_file.write(autocomplete_file_text)
                print("Bash autocompletion file written to /etc/bash_completion.d/sws.sh \nPlease restart shell for autocomplete to update")
            except PermissionError:
                print("Unable to write bash autocompletion file for sws are you sudo?")
