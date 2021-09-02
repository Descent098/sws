"""Contains all the configuration for the package on pip"""
import setuptools

def get_content(*filename:str) -> str:
    """ Gets the content of a file or files and returns
    it/them as a string

    Parameters
    ----------
    filename : (str)
        Name of file or set of files to pull content from 
        (comma delimited)
    
    Returns
    -------
    str:
        Content from the file or files
    """
    content = ""
    for file in filename:
        with open(file, "r") as full_description:
            content += full_description.read()
    return content


setuptools.setup(
    name="sws",
    version="0.2.2",
    author="Kieran Wood",
    author_email="kieran@canadiancoding.ca",
    description="An API & command line interface, for common web tasks",
    long_description = get_content("README.md", "CHANGELOG.md"),
    long_description_content_type="text/markdown",
    project_urls={
        'API Docs': 'http://kieranwood.ca/sws',
        'CLI Docs': 'http://sws.readthedocs.io/',
        'Bug Reports': 'https://github.com/Descent098/sws/issues/new?assignees=Descent098&labels=bug&template=bug_report.md&title=%5BBUG%5D',
        'Source': 'https://github.com/Descent098/sws',
        'Roadmap': 'https://github.com/Descent098/sws/projects',
    },
    packages=setuptools.find_packages(),
    entry_points={
            'console_scripts': ['sws = sws.cli:main']
        },
    install_requires=[
    "requests",                 # Used in various modules for http connections and header parsing
    "pytube",                   # Used for youtube downloading
    "docopt",                   # Used for argument parsing in CLI
    "pystall",                  # Used to install ad-hoc binaries
    "python-whois-extended",    # Used to gather domain name info
    "dnspython",                # Used to gather dns info
    "locust",                   # Used to do loadtesting
    "sdu",                      # Allows for use of autocomplete on nix systems
    ],
    extras_require = {
        "dev" : ["nox",   # Used to run automated processes
                "pytest", # Used to run the test code in the tests directory
                "mkdocs", # Used to create HTML versions of the markdown docs in the docs directory
                ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
)