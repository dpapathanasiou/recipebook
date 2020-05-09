#!/usr/bin/env python

"""
restClient.py

This module defines a series of functions to perform basic http
actions using pycurl.

"""

import pycurl
from io import StringIO
from io import BytesIO

from settings import UA


def get(url, encoding, user_agent=UA, referrer=None):
    """Make a GET request of the url using pycurl and return the data
    (which is None if unsuccessful)"""

    data = None
    databuffer = BytesIO()

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.CONNECTTIMEOUT, 5)
    curl.setopt(pycurl.TIMEOUT, 8)
    curl.setopt(pycurl.WRITEDATA, databuffer)
    curl.setopt(pycurl.COOKIEFILE, '')
    if user_agent:
        curl.setopt(pycurl.USERAGENT, user_agent)
    if referrer is not None:
        curl.setopt(pycurl.REFERER, referrer)
    try:
        curl.perform()
        data = databuffer.getvalue().decode(encoding)
    except Exception:
        pass
    curl.close()

    return data


def put(url, data, headers=None):
    """Make a PUT request to the url, using data in the message body,
    with the additional headers, if any"""

    if headers is None:
        headers = {}
    reply = -1  # default, non-http response

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    if len(headers) > 0:
        curl.setopt(pycurl.HTTPHEADER, [k + ': ' + v for k, v in list(headers.items())])
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
