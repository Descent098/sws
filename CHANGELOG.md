# Changelog

## V0.2.0; TBA

Focus for this release was to revamp the package and add a ton of functionality.

Features:

- Simplified and streamlined `redirect.trace()`
- Added Bash autocomplete for ease of use on *nix systems
- Added ```domains``` module and command
- Added ```dns``` module and command
- Added ```downloads`` module to make handling downlaods simpler
- Added `__main__.py` file for direct cli invocation (`python -m sws`)

Documentation Improvements:
- Added additional source, docs, and roadmap links to ```setup.py``` for PyPi
- Added github templates (for issues and PR's), and testing pipeline
- Added testing suite for majority of library functions
- Moved usage docs to readthedocs https://sws.readthedocs.io
- Added API docs to https://kieranwood.ca/sws

## V0.1.0; February 4th 2020

Initial release went out on github and PyPi. Ported functionality from kuws package.

Features:

- Trace redirects
- Download YouTube videos directly from command line
- Check SSL status information and expiry date
