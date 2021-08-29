"""A module for getting DNS configurations on a domain

Notes
-----
- If http or https is passed to any function it will be stripped

Examples
--------
### Printing the values of 'kieranwood.ca' when as_dict is True
```
from sws.dns_utilities import get_dns_records

print(get_dns_records("kieranwood.ca", as_dict=True)) # {'A': ['104.21.47.45', '172.67.144.116'], 'SOA': 'kevin.ns.cloudflare.com. dns.cloudflare.com. 2036568886 10000 2400 604800 3600'}
```
"""
# Standard Library Dependencies
from math import floor, ceil                # Used to normalize padding
from typing import Dict, List, Tuple, Union # Used to provide useful typehints in functions

# Third Party Library Dependencies
import dns.resolver     # Used to get domain information
import dns.rdatatype    # Used to determine record types

# Includes deprecated record types (more canonical)
RECORD_TYPES = dns.rdatatype.RdataType

# More human-readable and workable list that axes unused record types taken from https://en.wikipedia.org/wiki/List_of_DNS_record_types
RECORD_TYPES_TUPLE:Tuple[str] = ( 
    # Alias/resource records
    'A',
    'AAAA',
    'CNAME',
    'DNAME',
    'URI',
    'PTR',
    'LOC',
    'GPOS',

    # Nameservers/Name registrar config
    'NS',
    'SOA',
    'CSYNC',
    'NSEC',
    'NSEC3',
    'NSEC3PARAM',
    'CAA',
    'RP',
    'DHCID',

    # Mailservers/Communications
    'MX',
    'SPF',
    'SRV',
    'MD',  # Technically obsoleted by RFC 973
    'MF',  # Technically obsoleted by RFC 973

    #Mailing lists (mostly obsolete at this point but unfortunately not dead)
    'MB',
    'MG',
    'MR',
    'MAILA',
    'MAILB',
    'MINFO',

    # Cert info/configuration/misc
    'TXT',
    'CERT',
    'DNSKEY',
    'KEY',      # Somewhat obsoleted by RFC 3445
    'CDNSKEY',
    'HINFO',    # Unobsoleted by RFC 8482
    'AFSDB',
    'NAPTR',
    'KX',
    'OPT',
    'DS',
    'SSHFP',
    'IPSECKEY',
    'RRSIG',
    'TLSA',
    'HIP',
    'CDS',
    'EUI48',
    'EUI64',
    'TKEY',
    'TSIG',
    'IXFR',
    'AXFR',
    'TA',
    'DLV',
)

def get_dns_records(domain:str, as_dict:bool=False) -> Union[List[str], Dict[str, Union[str, List[str]]]]:
    """Takes in a domain and returns either a list or dictionary of the records of the domain

    Notes
    -----
    - A list of supported record types can be found by importing `sws.dns.RECORD_TYPES` or `sws.dns.RECORD_TYPES_TUPLE` (a tuple not an enum so you can do index lookups)

    Parameters
    ----------
    domain : str
        [description]

    as_dict : bool, optional
        Whether to return a list of strings (False) or dictionary (True), by default False

    Returns
    -------
    Union[List[str], Dict[str, str]]
        If as_dict is False will return a list of printable strings (i.e. ['A: 127.0.0.1']), \n
        if as_dict is True will return a dict with record:str->record_data:str mapping (i.e. {'A':'127.0.0.1'})

    Raises
    ------
    ValueError
        If the domain has no valid records

    Examples
    --------
    ### Printing the values of 'kieranwood.ca'
    ```
    from sws.dns import get_dns_records

    print(get_dns_records("kieranwood.ca")) # ['A: 127.0.0.1', 'A: 106.23.49.45', 'NS: kevin.ns.cloudflare.com.']
    ```

    ### Printing the values of 'kieranwood.ca' when as_dict is True
    ```
    from sws.dns_utilities import get_dns_records

    print(get_dns_records("kieranwood.ca", as_dict=True)) # {'A': ['104.21.47.45', '172.67.144.116'], 'SOA': 'kevin.ns.cloudflare.com. dns.cloudflare.com. 2036568886 10000 2400 604800 3600'}
    ```
    """
    if domain.startswith("https://"):
        domain = domain.replace("https://", "")
    elif domain.startswith("http://"):
        domain = domain.replace("http://", "")
        
    if as_dict:
        result = {}
        for record_type in RECORD_TYPES:
            try:
                response = dns.resolver.resolve(domain, rdtype=record_type)
                for record_data in response:
                    if record_type == dns.rdatatype.RdataType.HTTPS:
                        result[record_type.name] = record_data.to_text().split(" ")[2:] # Remove 1 . from entries
                        continue
                    if result.get(record_type.name, False): # If multiple values of same record_type (i.e. 2+ A records on a domain)

                        if type(result.get(record_type.name, False)) == str: # If this is the second of same record_type
                            result[record_type.name] = [result[record_type.name], record_data.to_text()] # Convert string to list, and append new record data

                        elif type(result.get(record_type.name, False)) == list: # If 3+ of same record_type
                            result[record_type.name].append(record_data.to_text())

                    else: # If new record without existing value
                        result[record_type.name] = record_data.to_text()
            except Exception as e:
                ... # Record doesn't exist
    else:
        result = []
        for record_type in RECORD_TYPES:
            try:
                response = dns.resolver.resolve(domain, rdtype=record_type)
                for record_data in response:
                    result.append(f"{record_type.name}: {record_data.to_text()}")
            except Exception as e:
                ... # Record doesn't exist
    if not result:
        raise ValueError("Domain {} did not have any configured records, please check ")
    return result


def dns_result_table(domain:str, dns_dict:dict) -> str:
    """Takes in a dictionary of dns values and returns a human-readable table

    Parameters
    ----------
    domain:str
        The domain used to generate the dns_dict

    dns_dict : dict
        A dictionary with all the dns records in a record_type(str)->record_value(str or list) mapping

    Returns
    -------
    str
        A table of dns records and their values for the domain
    """    
    if domain.startswith("https://"):
        domain = domain.replace("https://", "")
    elif domain.startswith("http://"):
        domain = domain.replace("http://", "")
    # add header
    result = f"""\nDNS records for {domain} \n
| Record Type | Record Value |
|-------------|--------------|\n"""
    for record in dns_dict:

        # Add in Record Type column
        record_type = _even_padding(record, 13)
        current_row = f"|{record_type}|"

        # Add in Record Value column
        if type(dns_dict[record]) == list: # Need to render multiple result rows
            for index, record_value in enumerate(dns_dict[record]):
                if index == 0: # The first row
                    value = _even_padding(record_value, 14)
                    current_row += f"{value}|\n"
                elif index == len(dns_dict[record])-1: # Last row for current record
                    value = _even_padding(record_value, 14)
                    current_row += f"|{' '* 13}|{value}|\n|{'='* 13}|{'='* 14}|\n"

                else: # Middle row(s) for current record
                    value = _even_padding(record_value, 14)
                    current_row += f"|{' '* 13}|{value}|\n"

        else: # Just a single string for the current record so only takes a single row
            value = _even_padding(dns_dict[record], 14)
            current_row += f"{value}|\n|{'='* 13}|{'='* 14}|\n"
    
        result += current_row
    return result

def _even_padding(value:str, size:int, spacer:str= " ") -> str:
    """Creates even padding for a string value within a set size

    Parameters
    ----------
    value : str
        The value to pad

    size : int
        The size (number of characters) total that are available

    spacer : str, optional
        What character to space with, by default " "

    Returns
    -------
    str
        The value with padding to make it even spaced within size,
        just returns original value if it's larger than size

    Examples
    --------
    ### Passing a value that is shorter or equal to size
    ```
    # Value same length as size
    value = '192.85.111.115'
    padded_value = even_padding(value, 14)
    print("|{padded_value}|") # Prints |192.85.111.115|
    
    # Value smaller than size
    value = '192.33.22.55'
    padded_value = even_padding(value, 14)
    print("|{padded_value}|") # Prints | 192.33.22.55 |
    ```

    ### Passing a value that larger than size
    ```
    value = 'karen.ns.cloudflare.com'
    padded_value = even_padding(value, 14)
    
    print("|{padded_value}|") # Never get's called cause value is too large
    ```
    """

    if len(value) > size:
        return value
    padding = abs(len(value) - size)/2
    if not padding.is_integer():
        padding_left = spacer * floor(padding)
        padding_right = spacer * ceil(padding)
    else:
        padding_left = spacer * int(padding)
        padding_right = spacer * int(padding)
    
    return f"{padding_left}{value}{padding_right}"

if __name__ == "__main__":
    result = get_dns_records("kieranwood.ca", as_dict=True)
    print(dns_result_table("kieranwood.ca", result))
