"""Provides functionality for working with YouTube videos such as:

- Downloading youtube videos
- Pulling video metadata

Examples
--------
### Download youtube video to current folder
```
from sws.youtube import download

download("https://www.youtube.com/watch?v=6j1I3mC0BR0", ".") # Downloads video in current folder
```
"""

# Standard library Dependencies
import os                       # Used for path validation
import logging                  # Used in logging debug and info messages
import tkinter as tk            # Used to setup a gui for selecting files
from typing import Union        # Used for type hints with multiple types
from tkinter import filedialog  # Used to setup a gui for selecting files

# External Dependencies
from pytube import YouTube      # Used to download and get youtube video info
import pytube.exceptions


def _request_path():
    """Prompts user for the link to a youtube video, and path of where to download the video to"""
    logging.info("Entering _request_path()")
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = str(filedialog.askdirectory(
            title="Select Video Output directory",
            mustexist=False))
    except Exception as e:
        print(f"Unable to start path selection GUI due to {e}, defualting downloading to current working directory {os.path.abspath('.')}")
        file_path = os.path.abspath(".")
    return file_path


def get_video_metadata(video_url:str) -> dict:
    """Gets the metadata of a youtube video

    Parameters
    ----------
    video_url : str
        The URL of the video

    Notes
    -----
    - Keys include:
        - title; The title of the video
        - id;  The id of the video
        - publish_date; The publishing date of the video (as a `datetime.datetime` object)
        - age_restricted; A boolean that is True if the video is age restricted
        - creator; A string representation of the channel name
        - metadata; A raw `pytube.metadata.YouTubeMetadata` object of video metadata

    Returns
    -------
    dict
        A dictionary of results (see notes for keys)

    Raises
    ------
    ValueError
        If the video is inaccessible for any reason
    """
    logging.info(f"Entering get_video_metadata(video_url={video_url})")
    result = {}
    try:
        logging.info("Getting video metadata")
        video_data = YouTube(video_url)
        result["title"] = video_data.title
        result["id"] = video_data.video_id
        result["publish_date"] = video_data.publish_date
        result["age_restricted"] = video_data.age_restricted
        result["creator"] = video_data.author
        result["metadata"] = video_data.metadata
    except pytube.exceptions.RegexMatchError:
        raise ValueError(f"Video URL {video_url} does not exist")
    except pytube.exceptions.VideoPrivate:
        raise ValueError(f"Video URL {video_url} is private")
    except pytube.exceptions.MembersOnly:
        raise ValueError(f"Video URL {video_url} is Members Only")
    except pytube.exceptions.RecordingUnavailable:
        raise ValueError(f"Video URL {video_url} does not have a recording for the livestream")
    except pytube.exceptions.VideoUnavailable:
        raise ValueError(f"Video URL {video_url} does not have an available video")
    except pytube.exceptions.LiveStreamError:
        raise ValueError(f"Video URL {video_url} is a livestream and cannot be downloaded")
    logging.info(f"Exiting get_video_metadata() and returning {result}")
    return result


def download(video_url: str, path: Union[str, bool]) -> str:
    """Downloads specified video_url to path

    Parameters
    ----------
    video_url : (str)
        The full URL you want to download i.e. https://www.youtube.com/watch?v=6j1I3mC0BR0

    path : (str or bool)
        The path on your system to download the video to, or False to start pathfinding function

    Raises
    ------
    ValueError:
        If the video is inaccessible for any reason

    Returns
    -------
    str:
        A string with 'Downloaded <video title> to <path> as <video_title>.mp4' if file was downloaded, or message 'File <filepath> already exists' if file already existed

    Examples
    --------
    Download youtube video to current folder
    ```
    from sws.youtube import download

    download("https://www.youtube.com/watch?v=6j1I3mC0BR0", ".") # Downloads video in current folder
    ```
    """
    logging.info(f"Entering download(video_url={video_url}, path={path})")
    if not path:
        logging.info("No path found, entering _request_path()")
        path = os.path.realpath(f"{_request_path()}")
    else:
        logging.info(f"Path found {path}, converting to abspath {os.path.abspath(path)}")
        path = os.path.abspath(path)

    # Get video title if video exists
    try:
        logging.info("Requesting video data")
        video_title = str(YouTube(video_url).title)
    except pytube.exceptions.RegexMatchError:
        raise ValueError(f"Video URL {video_url} does not exist")
    except pytube.exceptions.VideoPrivate:
        raise ValueError(f"Video URL {video_url} is private")
    except pytube.exceptions.MembersOnly:
        raise ValueError(f"Video URL {video_url} is Members Only")
    except pytube.exceptions.RecordingUnavailable:
        raise ValueError(f"Video URL {video_url} does not have a recording for the livestream")
    except pytube.exceptions.VideoUnavailable:
        raise ValueError(f"Video URL {video_url} does not have an available video")
    except pytube.exceptions.LiveStreamError:
        raise ValueError(f"Video URL {video_url} is a livestream and cannot be downloaded")

    logging.info("Checking if ouput file already exists")
    if os.path.exists(os.path.join(path, video_title)):
        logging.info(f"Found existing output file, exiting download() and returning 'File {os.path.join(path, video_title)} already exists'")
        return f"File {os.path.join(path, video_title)} already exists"

    print(f"Downloading {video_title} to {path}")
    YouTube(video_url).streams.get_highest_resolution().download(path)

    logging.info(f"Found existing output file, exiting download() and returning 'Downloaded {video_title} to {path} as {video_title}.mp4'")
    return f"Downloaded {video_title} to {path} as {video_title}.mp4"
