# Development-Contribution guide

## Installing development dependencies

There are a few dependencies you will need to use this package fully, they are specified in the extras require parameter in setup.py but you can install them manually:

```
nox   	# Used to run automated processes
pytest 	# Used to run the test code in the tests directory
mkdocs	# Used to create HTML versions of the markdown docs in the docs directory
pdoc3   # Used to generate API documentation
```

Just go through and run ```pip install <name>``` or ```sudo pip3 install <name>```. These dependencies will help you to automate documentation creation, testing, and build + distribution (through PyPi) automation.

## Building "API" docs

API docs are useful if you want an easily navigatable version of the in-line documentation. 
The best way to do this currently is to:

1.  download [pdoc3](https://pdoc3.github.io/pdoc/doc/pdoc/); ```pip install pdoc3``` 
2.  Install your current sws code by going to the root directory and running ```pip install .```
3.  Run ````pdoc sws --http localhost:8080```
4.  Go to a browser and type in [http://localhost:8080/sws](http://localhost:8080/sws).

## Building "user" docs

User docs detail primarily the CLI usage. To build them locally install mkdocs and run ```mkdocs serve``` on the root directory and navigate to [http://localhost:8000](http://localhost:8000)

## Nox integration

If you have never used [nox](https://nox.readthedocs.io/) before it is a great system for automating tedius tasks (builds, distributions, testing etc). This project uses nox for a number of things and in the following sections I will explain each. 

## Running tests

Testing is implemented using [pytest](https://docs.pytest.org/en/latest/), and can be run 1 of 2 ways:

1. Run the tests through nox using ```nox -s tests```, this will automatically run the tests against python 3.5-3.8 (assuming they are installed on system).
2. Go to the root directory and run ```pytest```, this should automatically detect the /tests folder and run all tests.

## Building the package

This is not necessary for pull requests, or even development but if you want to validate that it doesn't break buildability here is how to do it. You can use ```nox -s build```, this will create a source distribution for you using pythons [setuptools module](https://setuptools.readthedocs.io/en/latest/).

## Pull requests and issues guide

### TLDR

1. Commenting/documentaion is **not** optional
2. Breaking platform compatability is **not** acceptable
3. Do **everything** through [github](https://github.com/Descent098/sws) (don't email me), and (mostly) everything has been setup for you.

### Bug Reports & Feature Requests

Submit all bug reports and feature requests on [github](https://github.com/Descent098/sws/issues/new/choose), the format for each is pre-defined so just follow the outlined format

### Pull requests

Pull requests should be submitted through github and follow the default pull request template specified. If you want the rundown of what needs to be present:

1. Provide a clear explination of what you are doing/fixing
2. Feature is tested on Windows & *nix (unless explicitly incompatable)
3. All Classes, modules, and functions must have docstrings that follow the [numpy-style guide](https://numpydoc.readthedocs.io/en/latest/format.html).
4. Unless feature is essential it cannot break backwards compatability

## Folder Structure

*A Brief explanation of how the project is set up for people trying to get into developing for it*

### /sws

Contains all of the modules that implement the functionality for the CLI and API.

### /docs

*Contains markdown source files to be used with [mkdocs](https://www.mkdocs.org/) to create html/pdf documentation.* 

**Before you can use this you will need to setup the mkdocs.yml file **

### /tests

*Contains tests to be run before release* 

### Root Directory

**setup.py**: Contains all the configuration for installing the package via pip.

**LICENSE**: This file contains the licensing information about the project.

**CHANGELOG.md**: Used to create a changelog of features you add, bugs fixed for each release

**CONTRIBUTING.md**: Contains development details for how to contribute to sws

**mkdocs.yml**: Used to specify how to build documentation from the source markdown files.

**.gitignore**: A preconfigured gitignore file (info on .gitignore files can be found here: https://www.atlassian.com/git/tutorials/saving-changes/gitignore)
