"""Provides a simple way to download YouTube videos.

Functions
---------
download : str
    Primary entrypoint for the sws script.

link_and_path:
    Don't use this function (janky).


Examples
--------
```
>> from sws.utilities.youtube import download

>> download("https://www.youtube.com/watch?v=6j1I3mC0BR0", ".") # Downloads video in current folder
```
"""

from pytube import YouTube
import tkinter as tk
from tkinter import filedialog

def link_and_path():
    """Prompts user for the link to a youtube video, and path of where to download the video to"""
    video_url = input("What is the URL for the video you want to download?: ")
    root = tk.Tk()
    root.withdraw()
    file_path = str(filedialog.askdirectory(
        title="Select Video Output directory",
        mustexist=False))
    return video_url, file_path


def download(video_url, path):
    """Downloads specified video_url to path
    
    Parameters
    ----------
    video_url : (str)
        The full URL you want to download i.e. https://www.youtube.com/watch?v=6j1I3mC0BR0

    path : (str)
        The path on your system to download the video to.

    Examples
    --------
    ```
    >> from sws.utilities.youtube import download

    >> download("https://www.youtube.com/watch?v=6j1I3mC0BR0", ".") # Downloads video in current folder
    ```
    """
    video_title = str(YouTube(video_url).title)
    print(f"Downloading {video_title} to {path}")
    YouTube(video_url).streams.filter(subtype='mp4', progressive=True).order_by('resolution').desc().first().download(path)
    
    return("Downloaded {} to {} as {}.mp4".format(video_title, path, video_title))

