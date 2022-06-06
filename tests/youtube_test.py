"""Testing the functionality of sws.youtube"""

from tempfile import TemporaryDirectory

import pytest
import datetime
from sws.youtube import *
from pytube.metadata import YouTubeMetadata


def test_valid_metadata():
    data = get_video_metadata("https://www.youtube.com/watch?v=6j1I3mC0BR0")

    assert type(data) == dict
    assert data["title"] == "Python Packaging Template usage documentation"
    assert data["id"] == "6j1I3mC0BR0"
    assert data["publish_date"] == datetime.datetime(2020, 1, 28, 0, 0)
    assert data["age_restricted"] == False
    assert data["creator"] == "Canadian Coding"
    assert type(data["metadata"]) == YouTubeMetadata

    # Age restricted video
    assert get_video_metadata("https://www.youtube.com/watch?v=-THmRGelP_o")["age_restricted"] == True


def test_invalid_metadata():
    # Non existant video
    with pytest.raises(ValueError):
        get_video_metadata("https://www.youtube.com/watch?v=aaaaaaaaa")

    # Test private video
    with pytest.raises(ValueError):
        get_video_metadata("https://www.youtube.com/watch?v=mLrSNOz_2IQ")


def test_valid_download():
    download("https://www.youtube.com/watch?v=QVV_bUxxiZ8", ".")
    assert os.path.exists("Animated Explanation of the one-time pad.mp4")

    with TemporaryDirectory() as temp_directory:
        download("https://www.youtube.com/watch?v=QVV_bUxxiZ8", temp_directory)
        assert os.path.exists(os.path.join(temp_directory, "Animated Explanation of the one-time pad.mp4"))

    # Run download twice
    download("https://www.youtube.com/watch?v=QVV_bUxxiZ8", ".")
    assert os.path.exists("Animated Explanation of the one-time pad.mp4")

    # Cleanup
    os.remove("Animated Explanation of the one-time pad.mp4")


def test_invalid_download():
    # Non existant video
    with pytest.raises(ValueError):
        download("https://www.youtube.com/watch?v=aaaaaaaaa", ".")

    # Test private video
    with pytest.raises(ValueError):
        download("https://www.youtube.com/watch?v=mLrSNOz_2IQ", ".")
