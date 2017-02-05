#!/usr/bin/env python

"""
scraper.py

This module defines a series of functions to fetch html content from
from any publically-available URL.

"""

import pycurl
from cStringIO import StringIO

from settings import UA

def getUrl (url, user_agent=UA, referrer=None):
    """Make a GET request of the url using pycurl and return the data
    (which is None if unsuccessful)"""

    data = None
    databuffer = StringIO()

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.CONNECTTIMEOUT, 5)
    curl.setopt(pycurl.TIMEOUT, 8)
    curl.setopt(pycurl.WRITEFUNCTION, databuffer.write)
    curl.setopt(pycurl.COOKIEFILE, '')
    if user_agent:
        curl.setopt(pycurl.USERAGENT, user_agent)
    if referrer is not None:
        curl.setopt(pycurl.REFERER, referrer)
    try:
        curl.perform()
        data = databuffer.getvalue()
    except Exception:
        pass
    curl.close()

    return data
