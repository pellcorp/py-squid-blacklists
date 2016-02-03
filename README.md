# py-squid-blacklists
Squid helper handling squidguard blacklists written in python

* Only supports domains blacklists actually (ie : google.com, www.google.com, api.google.com, etc.)
* All specified blacklists are loaded in RAM
* Usable as an external acl plugin of squid
* Written because of poor developpement on squidguard and bad support of blacklists files using squid3
* Tested on Debian 8 / python 2.7.9

## Usage

Add this configuration to squid.conf :
```
external_acl_type urlblacklist_lookup ttl=5 %URI /usr/bin/python /usr/local/blacklists/py-squid-blacklists.py
...
acl urlblacklist external urlblacklist_lookup
...
http_access deny urlblacklist
```
