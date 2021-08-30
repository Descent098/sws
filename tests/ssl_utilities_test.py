"""Testing the functionality of sws.ssl_utilities"""

import pytest
from sws.ssl_utilities import *

# NOTE: Due to the dynamic nature of domains I have chosen to test wih kieranwood.ca (my site) because I can be relatively sure it will be stable,
# if this test file fails check the domain SSL cert is still valid manually

def test_valid_ssl_certs():
    # Regular domain
    assert type(get_ssl_cert("kieranwood.ca")) == dict
    assert type(check_ssl_expiry("kieranwood.ca")) == str
    assert type(get_ssl_issuer("kieranwood.ca")) == list

    # Domain with protocols
    assert type(get_ssl_cert("http://kieranwood.ca")) == dict
    assert type(check_ssl_expiry("http://kieranwood.ca")) == str
    assert type(get_ssl_issuer("http://kieranwood.ca")) == list

    assert type(get_ssl_cert("https://kieranwood.ca")) == dict
    assert type(check_ssl_expiry("https://kieranwood.ca")) == str
    assert type(get_ssl_issuer("https://kieranwood.ca")) == list

    # Subdomain
    assert type(get_ssl_cert("mail.google.com")) == dict
    assert type(check_ssl_expiry("mail.google.com")) == str
    assert type(get_ssl_issuer("mail.google.com")) == list

def test_invalid_ssl_certs():
    # Regular domain
    with pytest.raises(ValueError):
        assert type(get_ssl_cert("asdfhkjgaeoiruyfgasadf.ca")) == dict
    with pytest.raises(ValueError):
        assert type(check_ssl_expiry("asdfhkjgaeoiruyfgasadf.ca")) == str
    with pytest.raises(ValueError):
        assert type(get_ssl_issuer("asdfhkjgaeoiruyfgasadf.ca")) == list

    # Domain with protocols
    with pytest.raises(ValueError):
        assert type(get_ssl_cert("http://asdfhkjgaeoiruyfgasadf.ca")) == dict
    with pytest.raises(ValueError):
        assert type(check_ssl_expiry("http://asdfhkjgaeoiruyfgasadf.ca")) == str
    with pytest.raises(ValueError):
        assert type(get_ssl_issuer("http://asdfhkjgaeoiruyfgasadf.ca")) == list

    with pytest.raises(ValueError):
        assert type(get_ssl_cert("https://asdfhkjgaeoiruyfgasadf.ca")) == dict
    with pytest.raises(ValueError):
        assert type(check_ssl_expiry("https://asdfhkjgaeoiruyfgasadf.ca")) == str
    with pytest.raises(ValueError):
        assert type(get_ssl_issuer("https://asdfhkjgaeoiruyfgasadf.ca")) == list

    # Subdomain
    with pytest.raises(ValueError): 
        assert type(get_ssl_cert("mail.asdfhkjgaeoiruyfgasadf.com")) == dict
    with pytest.raises(ValueError):
        assert type(check_ssl_expiry("mail.asdfhkjgaeoiruyfgasadf.com")) == str
    with pytest.raises(ValueError):
        assert type(get_ssl_issuer("mail.asdfhkjgaeoiruyfgasadf.com")) == list
