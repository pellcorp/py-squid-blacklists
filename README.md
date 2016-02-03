# py-squid-blacklists
Squid helper handling squidguard blacklists written in python

* Only supports domains blacklists actually (ie : google.com, www.google.com, api.google.com, etc.)
* All blacklists are loaded in RAM
* Usable as an external acl plugin of squid
* Written because of poor developpement on squidguard and bad support of blacklists files using squid3
* Tested on Debian 8 / python 2.7.9
