"""Module that provides a class for doing downloads that feature:

- 4xx and 5xx error catching
- Progress bars for downloads
- Additional download metadata
- Easy printable debugging

Examples
--------
### Downloading image to current folder using original filename
```
from sws.downloads import Download

d = Download('https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png') 
d.download() # Downloads to ./sws-banner.png
``` 

### Downloading image to downloads folder
```
import os
from sws.downloads import Download

d = Download('https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png', download_path=os.path.join(os.getenv('USERPROFILE'),'Downloads'))
d.download() # Downloads to <downloads folder>/sws-banner.png
``` 

### Downloading image to current folder with custom name
```
from sws.downloads import Download

d = Download('https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png' , filename='image.png') 
d.download() # Downloads to ./image.png
``` 

### Using Debug printing
```
from sws.downloads import Download
d = Download('https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png')
print(d) '''Prints:
Details for image.png
size: 19kb
downloaded: False
url: https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png
download path: C:\\Users\\Kieran\\Desktop
'''

print(repr(d)) # Prints: Download for https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png to download image.png to C:\\Users\\Kieran\\Desktop and has not been downloaded yet
```
"""

import os                 # Used to validate paths
import re                 # Used to parse for filename(s)
import logging            # Used to log errors and debug info
from typing import Union  # Used to specify multi-type parameters

# Third Party Dependencies
import requests           # Used to download Files, and get file metadata
from tqdm import tqdm     # Used to create a progress bar for active downloads


class Download:
    """Class used to help download files

    Attributes
    ----------
    url: str
        The URL for the download

    size: Union[bool, int]
        The size of the file in kb

    download_path: Union[bool, str]
        The path to download the file to (the folder where the file will download to)

    filename: Union[bool, str]
        The name of the file to download, defaults to headers where available

    downloaded:bool = False
        Set to True when file has been downloaded, and keeps files from being redownloaded

    Notes
    -----
    - Download also has custom `__repr__()` and `__str__()` functions to help with debugging. Calling `print()` on an instance gives a readable multiline string, and using `repr()` on an instance gives a good debugging string that is single-line.
    - Each instance can only be used to download ONE file, once `self.downloaded` has been set to True (which happens in `download()`)you cannot use it to download again

    Examples
    --------
    ### Downloading image to current folder using original filename
    ```
    from sws.downloads import Download

    d = Download('https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png') 
    d.download() # Downloads to ./sws-banner.png
    ``` 

    ### Downloading image to downloads folder
    ```
    import os
    from sws.downloads import Download

    d = Download('https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png', download_path=os.path.join(os.getenv('USERPROFILE'),'Downloads'))
    d.download() # Downloads to <downloads folder>/sws-banner.png
    ``` 

    ### Downloading image to current folder with custom name
    ```
    from sws.downloads import Download

    d = Download('https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png' , filename='image.png') 
    d.download() # Downloads to ./image.png
    ``` 

    ### Using Debug printing
    ```
    from sws.downloads import Download
    d = Download('https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png')
    print(d) '''Prints:
    Details for image.png
    size: 19kb
    downloaded: False
    url: https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png
    download path: C:\\Users\\Kieran\\Desktop
    '''

    print(repr(d)) # Prints: Download for https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png to download image.png to C:\\Users\\Kieran\\Desktop and has not been downloaded yet
    ```
    """   

    def __init__(self, url: str, download_path: Union[bool, str] = False, filename: Union[bool, str] = False):
        self.url = url
        self.downloaded = False
        self.size = self._get_size()

        # Setup filename variable
        if not filename:
            self._get_filename()
        else:
            self.filename = filename

        # Setup download_path variable
        if not download_path:
            self.download_path = os.path.realpath(".")
        else:
            if os.path.exists(download_path):
                self.download_path = download_path
            else:
                raise ValueError(f"Provided download path {download_path} does not exist")


    def _get_filename(self):
        """Check http headers for filename"""
        logging.info("No filename provided, checking headers")
        if "Content-Disposition" in requests.get(self.url).headers.keys():
            self.filename = re.findall("filename=(.+)", requests.get(self.url).headers["Content-Disposition"])[0]
            logging.info(f"Found filename {self.filename}")
        else:
            self.filename = self.url.split("/")[-1]
            logging.info(f"Could not find filename, falling back to {self.filename}")


    def _get_size(self) -> int:
        """Get the size of the file download

        Returns
        -------
        int
            The size of the download in KB
        """
        try:
            response = requests.get(self.url)
            if response.status_code//100 in [4,5]: # 4xx or 5xx status codes
                raise ValueError(f"{self.url} is not a valid download link and returned response code {response.status_code}")
            size = response.headers.get('content-length')
            if size:
                return int(size)//1024
            else:
                raise ValueError(f"{self.url} is not a valid download link")
        except ValueError as e:
            raise e # Reraise the error
        except Exception as e: # Have to do catchall and re-raise as ValueError because hundreds of exception types can be raised 
            raise ValueError(f"{self.url} is not a valid url, connection failed to establish with error {e}")


    def download(self):
        """Download a file from self.url"""
        file_path = os.path.realpath(f"{self.download_path}{os.sep}{self.filename}")
        if not self.downloaded: # If file is not downloaded
            logging.info("Starting binary download")

            # Setting up necessary download variables
            file_stream = requests.get(self.url, stream=True) # The open http request for the file
            chunk_size = 1024 # Setting the progress bar chunk size to measure in kb

            # Setting up the download progress bar
            progress_bar = tqdm(total=self.size, unit='iB', unit_scale=True)
            progress_bar.set_description(f"Download progress for {self.filename}")

            # Write the incoming data stream to a file and update progress bar as it downloads
            with open(file_path, 'wb') as download_file: 
                for chunk in file_stream.iter_content(chunk_size): 
                    if chunk:
                        progress_bar.update(len(chunk))
                        download_file.write(chunk)
            progress_bar.close()
            self.downloaded = True


    def __str__(self):
        return f"""Details for {self.filename}
    size: {self.size}kb
    downloaded: {self.downloaded}
    url: {self.url}
    download path: {self.download_path}"""


    def __repr__(self):
        return f"Download for {self.url} to download {self.filename} to {self.download_path} {'and has been downloaded' if self.downloaded else 'and has not been downloaded yet'}"


if __name__ == "__main__":
    d = Download("https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png")
    print(d)
    print(str(d))
