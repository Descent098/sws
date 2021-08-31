"""Testing the functionality of sws.dns_utilities"""

import pytest
from sws.dns_utilities import *

# NOTE: Due to the dynamic nature of domains I have chosen to test wih kieranwood.ca (my site) because I can be relatively sure it will be stable,
# if this test file fails check the domain DNS is still valid

def test_valid_domain_list():
    a = get_dns_records("kieranwood.ca")

    # Unsure this works with protocols
    b = get_dns_records("http://kieranwood.ca")
    c = get_dns_records("https://kieranwood.ca")

    for index, record in enumerate(a):
        if record.startswith("A:"):
            break
        if index == len(a) -1: # IF you hit the last item in the list and for loop hasn't been broken yet
            raise ValueError("Valid domain test failed, didn't find A record in list")

    for index, record in enumerate(a):
        if record.startswith("NS:"):
            break
        if index == len(a) -1: # IF you hit the last item in the list and for loop hasn't been broken yet
            raise ValueError("Valid domain test failed, didn't find NS record in list")

    for index, record in enumerate(b):
        if record.startswith("A:"):
            break
        if index == len(b) -1: # IF you hit the last item in the list and for loop hasn't been broken yet
            raise ValueError("Valid domain test failed, didn't find A record in list")

    for index, record in enumerate(b):
        if record.startswith("NS:"):
            break
        if index == len(b) -1: # IF you hit the last item in the list and for loop hasn't been broken yet
            raise ValueError("Valid domain test failed, didn't find NS record in list")

    for index, record in enumerate(c):
        if record.startswith("A:"):
            break
        if index == len(c) -1: # IF you hit the last item in the list and for loop hasn't been broken yet
            raise ValueError("Valid domain test failed, didn't find A record in list")

    for index, record in enumerate(c):
        if record.startswith("NS:"):
            break
        if index == len(c) -1: # IF you hit the last item in the list and for loop hasn't been broken yet
            raise ValueError("Valid domain test failed, didn't find NS record in list")


def test_invalid_domain_list():
    # Nonexistent domain
    with pytest.raises(ValueError):
        get_dns_records("asdfjhkg.com")

    # Nonexistent domain with protocol
    with pytest.raises(ValueError):
        get_dns_records("http://asdfjhkg.com")
    with pytest.raises(ValueError):
        get_dns_records("https://asdfjhkg.com")

    # URL not a domain
    with pytest.raises(ValueError):
        get_dns_records("https://google.com/blah/blah")
    
    # Nonexistent subdomain
    with pytest.raises(ValueError):
        get_dns_records("https://yeet.kieranwood.ca")


def test_valid_domain_dict():
    a = get_dns_records("kieranwood.ca", as_dict=True)

    # Unsure this works with protocols
    b = get_dns_records("http://kieranwood.ca", as_dict=True)
    c = get_dns_records("https://kieranwood.ca", as_dict=True)

    a["A"] # Check to make sure an A record exists
    b["A"] # Check to make sure an A record exists
    c["A"] # Check to make sure an A record exists
    a["NS"] # Check to make sure a NS record exists
    b["NS"] # Check to make sure a NS record exists
    c["NS"] # Check to make sure a NS record exists


def test_invalid_domain_dict():
    # Nonexistent domain
    with pytest.raises(ValueError):
        get_dns_records("asdfjhkg.com", as_dict=True)

    # Nonexistent domain with protocol
    with pytest.raises(ValueError):
        get_dns_records("http://asdfjhkg.com", as_dict=True)
    with pytest.raises(ValueError):
        get_dns_records("https://asdfjhkg.com", as_dict=True)

    # URL not a domain
    with pytest.raises(ValueError):
        get_dns_records("https://google.com/blah/blah", as_dict=True)
    
    # Nonexistent subdomain
    with pytest.raises(ValueError):
        get_dns_records("https://yeet.kieranwood.ca", as_dict=True)
