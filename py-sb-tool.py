#!/usr/bin/env python2.7

import os
import sys
import tarfile
import urllib

from pysquidblacklists import PySquidBlacklistsConfig

print("Parsing configuration file ...")
config = PySquidBlacklistsConfig()
config.get_config()


def download(url, path):
    bl_file = urllib.URLopener()
    bl_file.retrieve(url, path)


def extract(base_dir, archive):
    if not os.path.isdir(base_dir):
        bl_file = tarfile.open(archive)
        bl_file.extractall(base_dir)
    else:
        pass


def usage():
    print("tool.py import : import blacklists using config file")


if len(sys.argv) > 1:
    if sys.argv[1] == "import":
        print("Retrieving %s, storing it to %s ..." % (config.url, config.archive))
        download(config.url, config.archive)
        print("Extracting blacklists to %s" % config.base_dir)
        extract(config.base_dir, config.archive)
else:
    print(usage())