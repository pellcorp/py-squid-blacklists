#!/usr/bin/env python2.7

import sys
import os
import re
import urllib
from urlparse import urlparse

try:
    import config
except ImportError:
    print("Please create config.py using config.py.sample")
    exit()


def make_list(files):
    blacklists = []
    for l in files:
        splitlist = l.split("/")
        list_type = splitlist[len(splitlist) - 2]
        blacklists.append([list_type, l])
    return blacklists


def make_db(blacklist_files, config):
    lib = dict()
    for bl in blacklist_files:
        if (bl[0] in config.blacklists):
            cache = dict()
            f = open(bl[1], "r")
            for line in f:
                cache[line.strip("\n")] = True
            lib[bl[0]] = cache
            del cache
    return lib


def compare(outline, blacklist_cache):
    result = False
    for blacklist in blacklist_cache:
        tmpline = outline
        while not result and tmpline != "":
            try:
                result = blacklist_cache[blacklist][tmpline]
                pass
            except KeyError:
                pass
            tmpline = tmpline.partition('.')[2]
    return result


def squid_response(response):
    sys.stdout.write("%s\n" % response)
    sys.stdout.flush()


domain_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(config.blacklists_dir)) for f in fn if re.match(r"domains*", f)]

blacklist_files = make_list(domain_files)
blacklist_cache = make_db(blacklist_files, config)

while True:
    try:
     line = sys.stdin.readline().strip()
     outline = urlparse(line).netloc
     if line:
         if compare(outline, blacklist_cache):
             squid_response("OK")
         else:
             squid_response("ERR")
    except KeyboardInterrupt:
        break
