# Standard lib dependencies
import os

# Internal Dependencies
from sws.downloads import Download

# Third party dependencies
import pytest


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
    with pytest.raises(ValueError):
        test_download = Download("https://github.com/Descent098/sws/archive/master.zip")

