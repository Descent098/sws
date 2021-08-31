![sws-banner](https://raw.githubusercontent.com/Descent098/sws/master/docs/img/sws-banner.png)

## Table of Contents
- [Additional Documentation](#additional-documentation)
- [What does sws do?](#what-does-sws-do)
- [Features & Roadmap](#features--roadmap)
    - [Domain names](#domain-names)
    - [Redirects](#redirects)
    - [SSL](#ssl)
    - [YouTube](#youtube)
    - [DNS](#dns)
    - [Roadmap](#roadmap)
- [Why should I use sws?](#why-should-i-use-sws)
- [Who is sws for?](#who-is-sws-for)
- [Quick-start](#quick-start)
    - [Installation](#installation)
        - [From PyPi](#from-pypi)
        - [From source](#from-source)
- [Development-Contribution guide](#development-contribution-guide)

# Super Web Scripts

A command line interface, and set of scripts for common web tasks.

## Additional Documentation

API Documentation can be found at [https://kieranwood.ca/sws/](https://kieranwood.ca/sws/)

User Documentation for the cli can be found at [https://sws.readthedocs.io](https://sws.readthedocs.io)

## What does sws do?

sws is both a cli, and an API with the goal of making common web development tasks simple.

## Features & Roadmap

### Domain names

Get information about domain names including:
- Who is the registrar
- When the domain expires

### Redirects

Get information about the trace of http redirects

### SSL

Get deails about the ssl cert of a hostname such as:
- When the cert will expire
- The issuer of the cert
- A full dict of the details of the cert

### YouTube

Allows for the download of videos as well as geting metadata

### dns

Prints a table of the DNS records for a given domain

### Roadmap

A full roadmap for each project version can be found here: https://github.com/Descent098/sws/projects

## Why should I use sws?

The best marketing pitch that I can give you is that it's easy to use, free, and open source. The project really is here so that people don't have to keep writing the same implementations of basic tasks, and can instead use a tested package that contains a ton of functionality. Additionally if you don't want to use all of sws's features, because it is MIT liscenced you can feel free to vendor functions within your own project.

## Who is sws for?

Really it can be used by anyone, but here are the most typial use cases:
- Web developers; tools provided in sws can help with debugging and validating web servers
- Devops Specialists & testers; can use sws api to automate validation that servers are running how they should be
- People learning webdev; Sometimes getting access to tooling while learning webdev can be difficult, this can be a one-stop shop for lots of functionality
- Scripters; people who are looking to use sws functionality in their own projects

## Quick-start

### Installation

#### From PyPi

run ```pip install sws``` or ```sudo pip3 install sws```.

#### From source

1. Clone the github repo ([https://github.com/Descent098/sws](https://github.com/Descent098/sws))
2. cd into the 'sws' root directory (where setup.py is) and run ```pip install .``` or ```sudo pip3 install . ```

## Development-Contribution guide

See [Contribution guide](https://sws.readthedocs.io/contribution-guide/) for details about helping with development.
