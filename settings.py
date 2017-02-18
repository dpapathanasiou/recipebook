#!/usr/bin/env python

"""
This file defines the configuration settings for this project;
change them according to your environment, or use a local_settings.py
file which is excluded from source control.

"""

ENCODING = 'utf-8'
UA = "recipebook/1.2 +http://github.com/dpapathanasiou/recipebook"

# Define where the scraped and parsed results will be saved
OUTPUT_FOLDER = '/tmp'

# Override any of the above settings for your local environment in a
# separate local_settings.py file which is *not* checked into source
# control

try:
    from local_settings import *
except ImportError:
    pass
