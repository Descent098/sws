import os                 # Used to validate paths
import re                 # Used to parse for filename(s)
import logging            # Used to log errors and debug info
from typing import Union  # Used to specify multi-type parameters

# Third Party Dependencies
import requests           # Used to download Files, and get file metadata
from tqdm import tqdm     # Used to create a progress bar for active downloads

class Download:
    """
    Attributes
    ----------
    url: str
        The URL for the download

    size: Union[bool, int]
        The size of the file in kb

    download_path: Union[bool, str]
        The path to download the file to

    filename: Union[bool, str]
        The name of the file to download, defaults to headers where available

    downloaded:bool = False
        Set to True when file has been downloaded
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
        size = requests.get(self.url).headers.get('content-length')
        if size:
            return int(size)//1024
        else:
            raise ValueError(f"{self.url} is not a valid download link")

    def download(self):
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

    def __repr__(self):
        return f"""Details for {self.filename}
    size: {self.size}kb
    downloaded: {self.downloaded}
    url: {self.url}
    download path: {self.download_path}"""


if __name__ == "__main__":
    d = Download("https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png")
    print(d)
    d.download()