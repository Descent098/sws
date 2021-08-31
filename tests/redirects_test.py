"""Testing the functionality of sws.redirects"""

import pytest
from sws.redirects import *

def test_valid_redirects():
    assert type(trace("https://youtube.com", False)) == list
    assert len(trace("https://youtube.com", False)) == 2 # Should be redirected twice

    # Ignored domains
    assert type(trace("https://youtube.com", ignored_domains=["youtube.com"])) == list
    assert len(trace("https://youtube.com", ignored_domains=["youtube.com"])) == 1

def test_invalid_redirects():
    # Non existent path that still connects
    assert len(trace("https://kieranwood.ca/sadf/sadfasdf", False)) == 1

    # Non existent subdomain
    with pytest.raises(ValueError):
        trace("https://profile.kieranwood.ca", False)

    # Non existent path with ignored domains
    assert len(trace("https://kieranwood.ca/sadf/sadfasdf", ["kieranwood.ca"])) == 1

    # Non existent subdomain with ignored domains
    with pytest.raises(ValueError):
        trace("https://profile.kieranwood.ca", ["kieranwood.ca"])
