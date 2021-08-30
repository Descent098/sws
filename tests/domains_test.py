"""Testing the functionality of sws.domains"""

import pytest
from sws.domains import *
from sws.domains import _install_whois

# NOTE: Due to the dynamic nature of domains I have chosen to test wih kieranwood.ca (my site) because I can be relatively sure it will be stable,
# if this test file fails check the domain is still valid

def test_install_whois():
    _install_whois()

def test_valid_domains():
    # Unavailable but valid domain
    domain_details = get_domain_info('kieranwood.ca')
    availability = domain_availability(domain_details)

    assert availability[1] == False
    assert domain_details["name"] == "kieranwood.ca"
    assert domain_details["last_updated"] != False
    assert domain_details["creation_date"] != False
    assert domain_details["expiration_date"] != False
    assert domain_details["name_servers"] != False
    assert domain_details["registrant_cc"] != False
    assert domain_details["registrar"] != False

    # Available and valid domain
    domain_details = get_domain_info('asweifgdasfgj.ca')
    availability = domain_availability(domain_details)

    assert type(domain_details) == dict
    assert availability[1] == True
    assert domain_details["name"] == "asweifgdasfgj.ca"
    assert domain_details["last_updated"] == False
    assert domain_details["creation_date"] == False
    assert domain_details["expiration_date"] == False
    assert domain_details["name_servers"] == False
    assert domain_details["registrant_cc"] == False
    assert domain_details["registrar"] == False

def test_invalid_domains():
    # Unavailable but valid domain(s) with protocol
    domain_details = get_domain_info('http://kieranwood.ca')
    availability = domain_availability(domain_details)

    assert availability[1] == False
    assert domain_details["name"] == "kieranwood.ca"
    assert domain_details["last_updated"] != False
    assert domain_details["creation_date"] != False
    assert domain_details["expiration_date"] != False
    assert domain_details["name_servers"] != False
    assert domain_details["registrant_cc"] != False
    assert domain_details["registrar"] != False

    domain_details = get_domain_info('https://kieranwood.ca')
    availability = domain_availability(domain_details)

    assert availability[1] == False
    assert domain_details["name"] == "kieranwood.ca"
    assert domain_details["last_updated"] != False
    assert domain_details["creation_date"] != False
    assert domain_details["expiration_date"] != False
    assert domain_details["name_servers"] != False
    assert domain_details["registrant_cc"] != False
    assert domain_details["registrar"] != False

    # URL, not domain
    with pytest.raises(ValueError):
        domain_details = get_domain_info('asweifgdasfgj.ca/yeet')

    # Invalid TLD
    with pytest.raises(ValueError):
        domain_details = get_domain_info('google.co.yeet')

    # Subdomain
    with pytest.raises(ValueError):
        domain_details = get_domain_info('profile.kieranwood.ca')
