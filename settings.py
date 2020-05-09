#!/usr/bin/env python

"""
This file defines the configuration settings for this project;
change them according to your environment, or use a local_settings.py
file which is excluded from source control.

"""

ENCODING = 'utf-8'
UA = "recipebook/1.5 +http://github.com/dpapathanasiou/recipebook"
PAUSE_CRAWLER = True
PAUSE_TIME_RANGE = (10, 60)

# Define where the scraped and parsed results will be saved
OUTPUT_FOLDER = '/tmp'

# Define credentials for using a service running ARMS (http://github.com/dpapathanasiou/ARMS)
ARMS = {
    'SERVER': None,
    'API-KEY': None,
    'API-SEED': None
}

# Override any of the above settings for your local environment in a
# separate local_settings.py file which is *not* checked into source
# control

try:
    from local_settings import *
except ImportError:
    pass
