# py-squid-blacklists
Squid helper handling squidguard blacklists written in python

* Only supports domains blacklists actually (ie : google.com, www.google.com, mail.google.com, etc.)
* In config specified blacklists are loaded in RAM or CDB backend using https://github.com/acg/python-cdb (testing flavour is available)
* Usable as an external acl plugin of squid
* Written because of poor developpement on squidguard and bad support of blacklists files using squid3
* Tested on Debian 8 / python 2.7.9 / squid 3.4.8

## Usage

Add this configuration to squid.conf :
```
external_acl_type urlblacklist_lookup ttl=5 %URI /usr/bin/python /usr/local/py-squid-blacklists/py-squid-blacklists.py
...
acl urlblacklist external urlblacklist_lookup
...
http_access deny urlblacklist
```

config.py file must be include following statements
```
url = "http://dsi.ut-capitole.fr/blacklists/download/blacklists.tar.gz"
base_dir = "/usr/local/py-squid-blacklists/blacklists/"
categories = ["adult","malware"]
db_backend = "ram"
```

* url : squidguard-like blacklists files, this variable is not already usable
* categories : blacklists to use for filtering
* base_dir : path containing blacklists files
* db_backend : database flavour (ram|cdb)

## TODO

* Auto-fetcher using url if blacklists are not already downloaded or stored on the squid machine
* Compatibility with python3 only
* Filters for regex urls
* Reduce memory footprint (wip with CDB backend alternative)
* Code optimisation (wip)
* Object oriented programming (wip)
* Tests (wip)
* ...

## DBs support ideas

* High performance but heavy RAM usage when using dict()
* Sqlite3 tested, small memory footprint, but very slow
* CDB backend seems to be as fast as attended, with a very small footprint
