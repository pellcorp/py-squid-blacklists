#!/usr/bin/env python2.7

import sys
import os
import re
import time
from urlparse import urlparse

try:
    import config
except ImportError:
    print("Please create config.py using config.py.sample")
    exit()
try:
    import cdb
except ImportError:
    print("Please install python-cdb from pypi or via package manager")
    exit()


class PySquidBlacklists:
    def __init__(self, config):
        self.db_backend = config.db_backend
        self.categories = config.categories
        self.base_dir = config.base_dir
        self.domain_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(self.base_dir)) for f in
                             fn if re.match(r"domains*", f)]
        self.blacklist_files = self.make_list()
        self.cache = self.make_db()

    def make_list(self):
        blacklists = []
        for l in self.domain_files:
            splitlist = l.split("/")
            list_type = splitlist[len(splitlist) - 2]
            blacklists.append([list_type, l])
        return blacklists

    def make_db(self):
        lib = dict()
        for bls in self.blacklist_files:
            if self.db_backend == "ram":
                if bls[0] in self.categories:
                    cache = dict()
                    f = open(bls[1], "r")
                    for l in f:
                        cache[l.strip("\n")] = True
                    lib[bls[0]] = cache
                    del cache
        return lib

    def compare(self, outline):
        result = False
        for blacklist in self.cache:
            tmpline = outline
            while not result and tmpline != "":
                try:
                    result = self.cache[blacklist][tmpline]
                    pass
                except KeyError:
                    pass
                tmpline = tmpline.partition('.')[2]
        return result

    @staticmethod
    def response(r):
        sys.stdout.write("%s\n" % r)
        sys.stdout.flush()


class PySquidBlacklistsImporter:
    def __init__(self, conf):
        self.test = True
        self.db = conf.db_backend


bli = PySquidBlacklistsImporter(config)
bl = PySquidBlacklists(config)
while True:
    try:
        line = sys.stdin.readline().strip()
        if line == "":
            exit()
        outline = urlparse(line).netloc
        if line:
                if bl.compare(outline):
                    bl.response("OK")
                else:
                    bl.response("ERR")
    except IOError:
        pass