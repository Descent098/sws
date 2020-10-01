

![sws-banner](./img/sws-banner.png)

# Welcome to the sws documentation!



## what is sws?

sws is a utility I wrote with the intention of implementing some common web scripts into one cohesive library. it is primarily intended to be used as a standalone script, but it can also be used as an API. 



## Installation

### From PyPi

run ```pip install sws``` or ```sudo pip3 install sws```.



### From source

1. Clone the github repo ([https://github.com/Descent098/sws](https://github.com/Descent098/sws))
2. cd into the 'sws' root directory (where setup.py is) and run ```pip install .``` or ```sudo pip3 install . ```


## Script Usage
You can validate it is installed properly by typing ```sws``` into your terminal, the output should look like this:

Additional details can be found at the documentation available on [https://kieranwood.ca/sws](https://kieranwood.ca/sws).

You can validate it is installed properly by typing ```sws``` into your terminal, the output should look like this:

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

<u>Required Arguments:</u>

- *\<url\>*;  This is a **positional** placeholder value for a url you want to act upon. This should include a protocol (http:// or https://).

- *\<hostname\>*;  This is a **positional** placeholder value for the FQDN you want to run a command on, this is the root of a website without a protocol. For example the site http://kieranwood.ca would have an FQDN of kieranwood.ca

### redirects

Allows you to trace and validate redirects

<u>Optional Arguments:</u>

- *\-t or \-\-trace*: Trace redirect from the starting url provided to the end-of-the-line and print the result

### youtube

Allows you to get youtube video metadata and download videos

<u>Optional Arguments:</u>

- *\<path\>*;  This is a **positional** placeholder value for the path that you want to store the video to.


### ssl

Get deails about the ssl cert of a hostname

<u>Optional Arguments:</u>

- *\-e or \-\-expiry*: Print the expiry of the cert
- *\-c or \-\-cert*: Print the full list of info about a ssl cert

