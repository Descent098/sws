"""Provides a function for tracing redirects

Examples
--------
### Trace the redirects from kieranwood.ca
```
from sws.redirects import trace

trace('kieranwood.ca', print_result = True) '''Prints:

Printing trace for http://kieranwood.ca

Redirect level:1
URL: http://kieranwood.ca/
HTTP Code: 301

Redirect level:2
URL: https://kieranwood.ca
HTTP Code: 200'''
```
"""

# Standard library Dependencies
import logging                  # Used for logging
from typing import Union        # Used for type hints with multiple types

# External Dependencies
import requests                 # Used to make http requests for redirect tracing


def trace(url: str, ignored_domains: Union[list, bool], print_result: bool = True) -> list:
    """Trace all redirects associated with a URL.

    Arguments
    ---------
    url : str
        The URL to trace, can include or not include a protocol

    ignored_domains : list[str] or bool
        A list of domains (without protocols) to ignore in the trace; False
        can be passed in if no domains should be ignored

    print_result : bool
        If true then the value will be printed in a human readable format

    Notes
    -----
    url argument can include or not include a protocol

    Raises
    ------
    ValueError:
        If url cannot be connected to a ValueError will be raised

    Returns
    -------
    list[responses]:
        The list of traced responses

    Examples
    --------
    Trace the redirects from kieranwood.ca
    ```
    from sws.redirects import trace

    trace('kieranwood.ca', print_result = True) '''Prints:

    Printing trace for http://kieranwood.ca

    Redirect level:1
    URL: http://kieranwood.ca/
    HTTP Code: 301

    Redirect level:2
    URL: https://kieranwood.ca
    HTTP Code: 200'''
    ```
    """
    logging.info(f"Entering trace(url={url}, ignored_domains={ignored_domains}, print_result={print_result})")

    logging.info(f"Checking protocol is present on {url}")
    # Checks if protocols are present
    if "https://" in url:
        ...  # Continue
    elif "http://" in url:
        ...  # Continue
    else:  # Add a protocol to URL
        url = "http://" + url
        logging.info(f"Changed url to {url}")

    # Try going to the provided URL
    logging.info("Starting HTTP request")
    try:
        response = requests.get(url)

    except requests.exceptions.ConnectionError:
        if print_result:
            print(f"Could not connect to {url}, please ensure there are no spelling mistakes")
        raise ValueError(f"Could not connect to {url}, please ensure there are no spelling mistakes")
    except Exception as identifier:
        if print_result:
            print(f"Error while checking {url} \nError Code: {identifier}")
        return [f"Error while checking {url} \nError Code: {identifier}"]

    output = []  # The result of the response
    if response.history:  # If the request was redirected
        if ignored_domains:
            logging.debug("Skipping ignored domains")
            response.history = _skip_ignored_domains(response.history, ignored_domains)
        if print_result:
            print(f"\nPrinting response for {url}")
        for level, redirect in enumerate(response.history):
            logging.debug(f"Appending redirect {redirect.url} to output")
            output.append([level+1, redirect.url, redirect.status_code])
        output.append([len(output)+1, response.url, response.status_code])
        if print_result:
            logging.debug("Printing result(s)")
            for redirect in output:
                print(f"\nRedirect level:{redirect[0]} \nURL: {redirect[1]} \nHTTP Code: {redirect[2]}")
        logging.info(f"Exiting trace() and returning {output}") 
        return output
    else:  # If the request was not redirected
        if print_result:
            print("Request was not redirected")
        logging.info("Exiting trace() and returning ['Request was not redirected']") 
        return ["Request was not redirected"]


def _skip_ignored_domains(response_trace: list, ignored_domains: list) -> list:
    """Takes a list of responses and removes any responses that
    have domains that are in the ignored_domains variable

    Arguments
    ---------
    response_trace : list[responses]
        List of responses to strip domain results from

    Notes
    -----
    ignored_domains argument can include or not include a protocol

    Returns
    -------
    list[responses]:
        The stripped list of responses

    Examples
    --------
    Skip all domains with safelinks.protection.outlook.com or can01.safelinks.protection.outlook.com in the responses
    ```
    from sws.utilities.redirects import trace

    trace('kieranwood.ca', ["safelinks.protection.outlook.com", "can01.safelinks.protection.outlook.com"], print_result = True)
    ```
    """
    # Remove instances of ignored domains from the response trace
    for domain in ignored_domains:
        for response in response_trace:
            if domain in response.url:
                response_trace.remove(response)
            else:
                continue
    return response_trace
