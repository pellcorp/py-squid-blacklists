#!/usr/bin/env python2.7

import sys
import os
import re
import logging
import time
import urllib
from urlparse import urlparse
try:
	from config import *
except ImportError:
	print("Please create config.py using config.py.sample")
	exit()

domain_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(blacklists_dir)) for f in fn if re.match(r"domains*", f)]

def make_list(files):
	blacklists = []
	for f in files:
		splitlist = f.split("/")
		list_type = splitlist[len(splitlist)-2]
		blacklists.append([list_type,f])
	return blacklists

def make_db(blacklist_files):
	lib = dict()
	for blacklist in blacklist_files:
		cache = dict()
		values = []
		f = open(blacklist[1], "r")
		for line in f:
			cache[line.strip("\n")] = True
		lib[blacklist[0]] = cache
	return lib

def compare(outline,blacklist_cache,blacklists):
	result = False
	for blacklist in blacklists:
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


blacklist_cache=[]
blacklist_files = make_list(domain_files)
blacklist_cache = make_db(blacklist_files)

while True:
	line = sys.stdin.readline().strip()
	outline = urlparse(line).netloc
	if line:
		if compare(outline,blacklist_cache,blacklists):
			squid_response("OK")
		else:
			squid_response("ERR")
