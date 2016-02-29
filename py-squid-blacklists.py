#!/usr/bin/env python2.7
from pysquidblacklists import *

config = PySquidBlacklistsConfig()
config.get_config(__file__)

bli = PySquidBlacklistsImporter(config)
bl = PySquidBlacklistsRunner(config, bli)
bl.loop()