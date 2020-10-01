"""WIP module, will eventually enable whois style lookups of domains"""

import os
import json
import requests


def register_key(key):
    """
    """
    with open(f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}whoiskey.txt", 'w') as key_file:
        key_file.write(key)


def whois_lookup(domain, key=None):
    """
    """
    if not key:
        try:
            with open(f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}whoiskey.txt", 'r') as key_file:
                key = key_file.read()
        except FileNotFoundError as e:
            print("No key file found please add/update key file using: sws domains --key=<key here>")
            return
        except Exception as e:
            print(f"Error when retrieving API key: {e}")
    API_ENDPOINT = f"http://api.jsonwhois.io/domain?key={key}&domain={domain}"
    response = requests.get(API_ENDPOINT)
    response = json.loads(response.text)

    return response
