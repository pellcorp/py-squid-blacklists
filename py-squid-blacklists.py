#!/usr/bin/python

import sys
import os
import re
import logging
import time
from urlparse import urlparse
from config import *

domain_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(blacklists_dir)) for f in fn if re.match(r"domains*", f)]

def make_list(files):
	blacklists=[]
	for f in files:
		splitlist = f.split("/")
		list_type = splitlist[len(splitlist)-2]
		blacklists.append([list_type,f])
	return blacklists

def make_db(blacklist_files):
	lib = dict()
	for blacklist in blacklist_files:
		cache= dict()
		values=[]
		f = open(blacklist[1], "r")
		for line in f:
			cache[line.strip("\n")] = True
		lib[blacklist[0]]=cache
	return lib

def compare(outline,blacklist_cache):
	result = False
	while not result and outline != "":
		try:
			result=blacklist_cache['adult'][outline]
		except KeyError:
			pass
		outline = outline.partition('.')[2]
	return result

def grant():
	sys.stdout.write( 'OK\n' )
	sys.stdout.flush()

def deny():
	sys.stdout.write( 'ERR\n' )
	sys.stdout.flush()


blacklist_cache=[]

blacklist_files = make_list(domain_files)
blacklist_cache = make_db(blacklist_files)

while True:
	line = sys.stdin.readline().strip()
	outline = urlparse(line).netloc
	if line:
		if compare(outline,blacklist_cache):
			grant()
		else:
			deny()
