# Glossary

Throughout the library there are many obscure terms and abbreviations used, this glossary is here to help make those terms clear.

## Protocol

This could mean a few things, but in most contexts used in this library it refers to the method used to do a specific task (i.e. steps taken to connect to a site uses the Hypertext Transfer **Protocol**). It does have another use refering to the connection method used in a browser. Whenever you go to a website you will see something like  `http://` in front of the url. This is because you are connecting using the `http` protocol. Other protocols exist like [https](#httphttps), [ftp](https://en.wikipedia.org/wiki/File_Transfer_Protocol), and [many more](https://www.w3schools.in/types-of-network-protocols-and-their-uses/).

## HTTP/HTTPS

[Hypertext Transfer Protocol (http)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) is the [protocol](#protocol) that is used to allow connections to websites/webapps. Whenever you go to a website you will see either `http://` or `https://` in front, because that is what allows you to connect to a site.  Hypertext Transfer Protocol Secure (https), is used more commonly these days and is essentially the same as `http`, except it is encrypted (with [SSL](#ssltls), or [TLS](#ssltls)) to avoid leaking data.

## SSL/TLS

[Secure-Socket Layer (SSL)](https://www.ssl.com/faqs/faq-what-is-ssl/) and [Transport Layer Security (TLS)](https://www.cloudflare.com/en-ca/learning/ssl/transport-layer-security-tls/)  are standards by which websites and webapps traffic between server and client are encrypted. It is what allows connections over [https](#httphttps), and is considered essential in modern web development. Failure to have a valid SSL or TLS certificate means at minimum the data exchanged over `http` is vulnerable to attack (can be read in plaintext), and also in many cases sites/apps without it won't be indexed by search engines, or even load in some browsers.

## Requests/traffic

Request typically refers to an [http request](https://www.ibm.com/docs/en/cics-ts/5.3?topic=protocol-http-requests), or the package used in some of the modules that actually creates http requests, called [requests](https://docs.python-requests.org/en/master/). An http request is used to request an [http response](https://www.ibm.com/docs/en/cics-ts/5.3?topic=protocol-http-responses) from a server, which contains the data that a client is looking for. So basically you send a request in order to get a response with your data (i.e. image, webpage etc.). This back and forth request and response is often called **traffic**.

## IP Address

An IP address can be thought of like coordinates, it is the **exact** "location" where you can "find" a server. Every computer has an IP address, and it can be used to connect to a computer. The way this happens is you use an IP address in conjunction with a [port](https://www.cloudflare.com/en-ca/learning/network-layer/what-is-a-computer-port/) to connect to an app/website. For example if your computer had an IP address of `127.0.0.1`, and you were running a web server on port `5000` you could open a browser and go to `http://127.0.0.1:5000` to access the site. Typically [domains](#domainfqdn), are just a mask for an IP address. They allow you to type in `google.ca` instead of `172.217.14.227:80`. 

## Domain/FQDN/PQDN

A domain is a name used to point to a service. For example `google.ca` is a domain that points to one of google's search engine servers. A domain most commonly is used to allow you to connect to a web service without having to use it's [IP address](#ip-address). The domain `google.ca` (in conjunction with [dns records](#dns-records)), are what allow you to go to `google.ca` instead of `172.217.14.227:80`. A [Fully Qualified Domain Name (FQDN)](https://www.networksolutions.com/blog/establish/domains/what-is-a-fully-qualified-domain-name--fqdn--#:~:text=An%20FQDN%20is%20a%20complete,ending%20with%20a%20trailing%20period.) is the name given to when you write a domain and **not a URL**. For example `https://www.google.ca` is a URL, whereas `www.google.ca` is a FQDN and `google.ca` is also often called an FQDN, but is technically a [Partially Qualified Domain Name (PQDN)](https://en.wikipedia.org/wiki/Fully_qualified_domain_name) or root domain name.

A domain differs from a URL in that a domain in and of itself just says if you own the name or not (going through a [Domain Name Registrar](#domain-name-registrarregistrar)). Once you own the domain you will need to setup your [dns](#dns) to have working URL's that people can use.

## Subdomains

A subdomain is anything that takes the [root domain](#domainfqdnpqdn), and prefixes it. So for example if you have the domain `google.ca` then you might have the subdomain `mail.google.ca` for a mail service. Like a regular domain what this is used for depends on the [DNS](#dns).

## DNS

The dns of a [domain](#domainfqdnpqdn) refers to the set of [DNS records](#dns-records), that tell browsers what to do when they go to any URL's associated with your domain. So for example when you go to `https://google.ca`, the DNS records are pulled up in order to determine where the browser should send people. In this case the browser would see (based on current config), that it should connect to `172.217.14.227:80` in the background while still showing people the `https://google.ca` URL in their browser.

## DNS Records

These are the individual records that make up a [domain's](#domainfqdnpqdn) configured [dns](#dns). For example when you connect to `https://google.ca`, there is an [A Record](https://support.dnsimple.com/articles/a-record/) that tells the browser that the IP address of the server is `172.217.14.227` and to connect on the defualt port `80`. There is a [long list](https://en.wikipedia.org/wiki/List_of_DNS_record_types) of record types and values that allow for proper conenctions to different types of services, and also are used in many cases in the process of setting up [SSL/TLS](#ssltls).

## Domain Name Registrar/Registrar

A [Domain Name Registrar](https://www.cloudflare.com/en-ca/learning/dns/glossary/what-is-a-domain-name-registrar/#:~:text=A%20domain%20name%20registrar%20is,1.1.) is a company/organization that allows people to purchase [domains](#domainfqdnpqdn). Essentially these companies/organizations keep a list of who owns what domain, and sometimes either does the [dns](#dns) or tells browsers where to go to find the [dns](#dns).

## Metadata

A broad name given to the data surrounding something. For example metadata of a YouTube video might include it's title, or channel name whereas the metadata of a book might be also it's title and author along with it's ISBN etc.

## Redirects

A redirect or [http redirect](https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections) is a [http response](#httphttps) that forwards your [http request](#httphttps) on to another URL. For example let's say you change the URL an item in an online store from `https://example.com/store/items/shoe` to `https://example.com/store/shoe`, you could put a redirect in that sends people from the old URL to the new one.
