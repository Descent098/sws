"""Utilities to handle redirects and redirect histories, also some proxy info

Functions
---------
trace : list[responses]
    Primary entrypoint for the sws script.

_skip_ignored_domains : list[responses]
    Takes a list of responses and removes any responses that
    have domains that are in the ignored_domains variable

Module Variabes
---------------
ignored_domains : list[str]
    A list of domains to ignore in trace

Examples
--------
```
>> from sws.utilities.redirects import trace

>> trace('kieranwood.ca', print_result = True)
```

"""

# External Dependencies
import requests

ignored_domains = ["safelinks.protection.outlook.com", "can01.safelinks.protection.outlook.com"] # A list of domains to ignore in trace

def trace(url, print_result = True):
    """Trace all redirects associated with a URL.

    Arguments
    ---------
    url : str
        The URL to trace, can include or not include a protocol.
    
    print_result : bool
        If true then the value will be printed in a human readable format.

    Notes
    -----
    url argument can include or not include a protocol.

    Returns
    -------
    list[responses]:
        The list of traced responses

    Examples
    --------
    ```
    >> from sws.utilities.redirects import trace

    >> trace('kieranwood.ca', print_result = True)

    >> '''Prints:

    Printing trace for http://kieranwood.ca

    Redirect level:1
    URL: http://kieranwood.ca/
    HTTP Code: 301

    Redirect level:2
    URL: https://portfolio.kieranwood.ca
    HTTP Code: 200'''
    ```

    """
    if "https://" in url: # Checks if protocols are present
        None
    if "http://" in url:
        None
    else: # Add a protocol to URL
        url = "http://" + url

    try:
        trace = requests.get(url)
    except Exception as identifier:
        if print_result == True:
            print("Error while checking {} \nError Code: {}".format(url, identifier))
        return(["Error while checking {} \nError Code: {}".format(url, identifier)])

    
    if trace.history:
        output = []
        _skip_ignored_domains(trace.history)
        if (print_result == True):
            print("\nPrinting trace for {}".format(url))
        for level, redirect in enumerate(trace.history):
            output.append([level+1, redirect.url, redirect.status_code])
        output.append([len(output)+1,trace.url, trace.status_code])
        if (print_result == True):
            for redirect in output:
                print("\nRedirect level:{} \nURL: {} \nHTTP Code: {}".format(redirect[0], redirect[1], redirect[2]))
        return output
    else:
        if (print_result == True):
            print("Request was not redirected")
        return(["Request was not redirected"])

def _skip_ignored_domains(response_trace):
    """Takes a list of responses and removes any responses that
    have domains that are in the ignored_domains variable

    Arguments
    ---------
    response_trace : list[responses]
        List of responses to strip domain results from

    Notes
    -----
    url argument can include or not include a protocol.

    Returns
    -------
    list[responses]:
        The stripped list of responses

    Examples
    --------
    ```
    >> from sws.utilities.redirects import ignored_domains

    >> ignored_domains = ["safelinks.protection.outlook.com", "can01.safelinks.protection.outlook.com"]

    >> from sws.utilities.redirects import trace

    >> trace('kieranwood.ca', print_result = True)
    ```

    """
    for domain in ignored_domains:
        for count, response in enumerate(response_trace):
            if domain in response.url:
                response_trace.remove(response)
            else:
                continue
    return response_trace
