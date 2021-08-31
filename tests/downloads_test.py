# Standard lib dependencies
import os

# Internal Dependencies
from sws.downloads import Download

# Third party dependencies
import pytest


# NOTE: Due to the dynamic nature of downloads I have chosen to test wih the github source code because I can be relatively sure it will be stable,
# if this test file fails check the repo is still valid

def test_valid_url():
    test_download = Download("https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png", ".")
    
    assert "sws-banner.png" == test_download.filename
    assert "https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png" == test_download.url
    assert "sws-banner.png" == test_download.filename
    assert 19 == test_download.size
    test_download.download()

    # Cleanup
    assert os.path.exists("sws-banner.png")
    os.remove("sws-banner.png")


def test_invalid_url():
    # URL with no download
    with pytest.raises(ValueError):
        Download("https://github.com")

    # 404 URL
    with pytest.raises(ValueError):
        Download("https://kieranwood.ca/yeetyeet.pdf")

    # Non existent site
    with pytest.raises(ValueError):
        Download("https://asdlfjkhasldkjfhasdflgkhsdaflghasdlkjfgadfsohjgfhasdl.ca/yeetyeet.pdf")
