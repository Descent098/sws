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
import tkinter as tk            # Used to setup a gui for selecting files
from typing import Union        # Used for type hints with multiple types
from tkinter import filedialog  # Used to setup a gui for selecting files

# External Dependencies
from pytube import YouTube      # Used to download and get youtube video info



def _request_path():
    """Prompts user for the link to a youtube video, and path of where to download the video to"""
    root = tk.Tk()
    root.withdraw()
    file_path = str(filedialog.askdirectory(
        title="Select Video Output directory",
        mustexist=False))
    return file_path


def download(video_url: str, path: Union[str, bool]) -> str:
    """Downloads specified video_url to path

    Parameters
    ----------
    video_url : (str)
        The full URL you want to download i.e. https://www.youtube.com/watch?v=6j1I3mC0BR0

    path : (str or bool)
        The path on your system to download the video to, or False to start pathfinding function

    Examples
    --------
    Download youtube video to current folder
    ```
    from sws.youtube import download

    download("https://www.youtube.com/watch?v=6j1I3mC0BR0", ".") # Downloads video in current folder
    ```
    """
    if not path:
        path = os.path.realpath(f"{_request_path()}")

    video_title = str(YouTube(video_url).title)
    print(f"Downloading {video_title} to {path}")
    YouTube(video_url).streams.filter(subtype='mp4', progressive=True).order_by('resolution').desc().first().download(path)

    return f"Downloaded {video_title} to {path} as {video_title}.mp4"
