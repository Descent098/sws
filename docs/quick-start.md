# Quick Start

Here is everything you need to get started with sws.



## Script usage

```bash
Super Web Scripts; A command line interface, and set of scripts for web tasks.

Usage:
    sws [-h] [-v]
    sws redirects <url> [-t]
    sws youtube <url> [<path>]
    sws ssl <hostname> [-e] [-c]

Options:
    -h --help               Show this help message and exit
    -v --version            Show program's version number and exit
    -e --expiry             If specified will check the expiry of ssl cert/domain
    -c --cert               If specified will print the full details of the SSL cert
    -t --trace              If specified will show the full trace of the provided url
```



### Commands



#### redirects

Can be used to gather information about http redirects.



**-t or --trace**: When specified will print the train of redirects from the initial url provided. 



#### youtube

Used to download YouTube videos.



**\<url\>**: The YouTube video URL; NOTE: this must be in full form with protocol i.e. [https://www.youtube.com/watch?v=6j1I3mC0BR0](https://www.youtube.com/watch?v=6j1I3mC0BR0)



**\<path\>**: A path to download the YouTube video to (by default it's in the same directory you run the command from).



#### ssl

Used to gather information about a host's SSL certificate (such as expiry etc).



**\<hostname\>**: specify the FQDN to pull information about (URL without the protocol) i.e. kieranwood.ca



**-e or --expiry**: Prints the date and time the SSL cert will expire. 



**-c or --cert**: Prints the full set of available information about the cert (commonName, notBefore etc.). 



## API usage

If you are looking to use sws as an API, first install it. Once installed you can build API docs by installing [pdoc3](https://pdoc3.github.io/pdoc/) (```pip install pdoc3``` or ```sudo pip3 install pdoc3```), and then running ```pdoc sws --http localhost:8080```. Go to a browser and type in [http://localhost:8080/sws/utilities/](http://localhost:8080/sws/utilities/)

