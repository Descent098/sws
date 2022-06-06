# Changelog

## V0.3.0; TBA

**Features**:

- Added `loadtest` module and command
- Added `frameworks` module and command

**Bug fixes**:

- Fixed the `domains -d` command output to be human readable
- Changed whois binary install on windows to no longer require path variable updating

**Documentation Improvements**:

- Added documentation for new features
- improved readme

## V0.2.2; September 2nd 2021

More bug fixes

**Bug fixes**:

- Fixed a bug where installing whois would fail out midway through
- Added additional error catching on whois binary installation
- Fixed boolean type conversion bug on `get_domain_info()`

## V0.2.1; September 1st 2021

Fixing bugs found after release

**Bug fixes**:

- Fixed error on ```sws.youtube._request_path()``` where it would fail if no tkinter display variable is set
- Fixed bug with retrieval of domain records where an unbound variable would exist if the request hung
- Fixed issue where no usage would print when using DNS command without any args
- Fixed issue where no usage would print when using SSL command without any args
- Fixed issue with DNS lookups where on slow connections it would hang waiting for records to load

**Documentation Improvements**:

- Fixed some spelling errors and text duplication
- Improved some of the readme and Usage docs explanations

## V0.2.0; September 1st 2021

Focus for this release was to revamp the package and add a ton of functionality.

**Features**:

- Simplified and streamlined `redirect.trace()`
- Added Bash autocomplete for ease of use on *nix systems
- Added ```domains``` module and command
- Added ```dns``` module and command
- Added ```downloads`` module to make handling downlaods simpler
- Added `__main__.py` file for direct cli invocation (`python -m sws`)
- Added logging to existing functions, and all new functions

**Documentation Improvements**:
- Added additional source, docs, and roadmap links to ```setup.py``` for PyPi
- Added github templates (for issues and PR's), and testing pipeline
- Added testing suite for majority of library functions
- Moved usage docs to readthedocs https://sws.readthedocs.io
- Added API docs to https://kieranwood.ca/sws

## V0.1.0; February 4th 2020

Initial release went out on github and PyPi. Ported functionality from kuws package.

**Features**:

- Trace redirects
- Download YouTube videos directly from command line
- Check SSL status information and expiry date
