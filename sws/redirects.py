"""Utilities to get information about http redirects

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

# External Dependencies
import requests

def trace(url:str, ignored_domains:list, print_result:bool = True) -> list:
    """Trace all redirects associated with a URL.

    Arguments
    ---------
    url : str
        The URL to trace, can include or not include a protocol
    
    ignored_domains : list[str]
        A list of domains (without protocols) to ignore in the trace

    print_result : bool
        If true then the value will be printed in a human readable format

    Notes
    -----
    url argument can include or not include a protocol

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
    # Checks if protocols are present
    if "https://" in url: 
        None # Continue
    elif "http://" in url:
        None # Continue
    else: # Add a protocol to URL
        url = "http://" + url

    try:
        trace = requests.get(url)
    except Exception as identifier:
        if print_result == True:
            print(f"Error while checking {url} \nError Code: {identifier}")
        return([f"Error while checking {url} \nError Code: {identifier}"])

    output = [] # The result of the trace
    if trace.history: # If the request was redirected
        if ignored_domains:
            trace = _skip_ignored_domains(trace.history, ignored_domains)
        if (print_result == True):
            print(f"\nPrinting trace for {url}")
        for level, redirect in enumerate(trace.history):
            output.append([level+1, redirect.url, redirect.status_code])
        output.append([len(output)+1,trace.url, trace.status_code])
        if (print_result == True):
            for redirect in output:
                print("\nRedirect level:{} \nURL: {} \nHTTP Code: {}".format(redirect[0], redirect[1], redirect[2]))
        return output
    else: # If the request was not redirected
        if (print_result == True):
            print("Request was not redirected")
        return(["Request was not redirected"])

def _skip_ignored_domains(response_trace, ignored_domains:list):
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
    for domain in ignored_domains:
        for count, response in enumerate(response_trace):
            if domain in response.url:
                response_trace.remove(response)
            else:
                continue
    return response_trace
