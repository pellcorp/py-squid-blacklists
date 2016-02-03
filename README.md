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

config.py file must be include following statements
```
blacklists_fetch = "http://dsi.ut-capitole.fr/blacklists/download/blacklists.tar.gz"
blacklists_dir = "/usr/local/py-squid-blacklists/blacklists/"
blacklists = ["adult","malware"]
```

blacklists_fetch : squidguard-like blacklists files, this variable is not already usable
blacklists_dir : path containing blacklists files
blacklists : blacklists to use for filtering

## TODO

* Auto-fetcher using blacklists_fetch if blacklists are not already downloaded or stored on the squid machine
* Compatibility with python3 only
* Filters for regex urls
* Tests
* ...
