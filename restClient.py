#!/usr/bin/env python

"""
restClient.py

This module defines a series of functions to perform basic http
actions using pycurl.

"""

import pycurl
from cStringIO import StringIO

from settings import UA

def get (url, user_agent=UA, referrer=None):
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

def put (url, data, headers={}):
    """Make a PUT request to the url, using data in the message body,
    with the additional headers, if any"""

    reply = -1 # default, non-http response

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    if len(headers) > 0:
        curl.setopt(pycurl.HTTPHEADER, [k+': '+v for k,v in headers.items()])
    curl.setopt(pycurl.PUT, 1)
    curl.setopt(pycurl.INFILESIZE, len(data))
    databuffer = StringIO(data)
    curl.setopt(pycurl.READFUNCTION, databuffer.read)
    try:
        curl.perform()
        reply = curl.getinfo(pycurl.HTTP_CODE)
    except Exception:
        pass
    curl.close()

    return reply
