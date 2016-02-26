#!/usr/bin/env python2.7

import sys
import os
import re
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
    def __init__(self, config, bli):
        self.base_dir = config.base_dir
        self.db_backend = config.db_backend
        self.cache = bli.cache
        self.cdb_cache = dict()
        for blacklist in self.cache:
            if self.db_backend == "ram":
                pass
            elif self.db_backend == "cdb":
                self.cdb_cache[blacklist] = cdb.init(blacklist)
        self.loop()

    def domain_compare(self):
        result = False
        for blacklist in self.cache:
            tmpline = self.outline
            while not result and tmpline != "":
                try:
                    if self.db_backend == "ram":
                        result = self.cache[blacklist][tmpline]
                    elif self.db_backend == "cdb":
                        result = self.cdb_cache[blacklist][tmpline]
                    pass
                except KeyError:
                    pass
                tmpline = tmpline.partition('.')[2]
        return result

    def loop(self):
        while True:
            try:
                line = sys.stdin.readline().strip()
                if line == "":
                    exit()
                self.outline = urlparse(line).netloc
                if line:
                    if self.domain_compare():
                        self.response("OK")
                    else:
                        self.response("ERR")
            except IOError:
                pass

    @staticmethod
    def response(r):
        sys.stdout.write("%s\n" % r)
        sys.stdout.flush()


class PySquidBlacklistsImporter:
    def __init__(self, conf):
        self.db_backend = config.db_backend
        self.categories = config.categories
        self.base_dir = config.base_dir
        self.domain_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(self.base_dir)) for f in
                             fn if re.match(r"domains*", f)]
        self.blacklist_files = self.make_list()
        self.cache = None
        if self.db_backend == "ram":
            self.make_ram_db()
        elif self.db_backend == "cdb":
            self.make_cdb_db()

    def make_list(self):
        blacklists = []
        for l in self.domain_files:
            splitlist = l.split("/")
            list_type = splitlist[len(splitlist) - 2]
            blacklists.append([list_type, l])
        return blacklists

    def make_ram_db(self):
        lib = dict()
        for bls in self.blacklist_files:
            if bls[0] in self.categories:
                blcache = dict()
                f = open(bls[1], "r")
                for l in f:
                    blcache[l.strip("\n")] = True
                lib[bls[0]] = blcache
                del blcache
        self.cache = lib

    def make_cdb_db(self):
        lib = []
        for bl in self.blacklist_files:
            bl_cdb_file = ("%s/%s.cdb" % (self.base_dir, bl[0]))
            bl_cdb_file_tmp = ("%s/%s.tmp" % (self.base_dir, bl[0]))
            if bl[0] in self.categories:
                if not os.path.isfile(bl_cdb_file):
                    cdb_file = cdb.cdbmake(bl_cdb_file, bl_cdb_file_tmp)
                    f = open(bl[1], "r")
                    for line in f:
                        cdb_file.add(line.strip("\n"), "True")
                    cdb_file.finish()
                lib.append(bl_cdb_file)
        self.cache = lib


bli = PySquidBlacklistsImporter(config)
bl = PySquidBlacklists(config, bli)
