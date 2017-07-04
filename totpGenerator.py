#!/usr/bin/env python

"""
totpGenerator.py

Produces a Time Based One-Time Password (TOTP) given a secret seed
string, as defined by RFC 6238 (https://tools.ietf.org/html/rfc6238)

"""

from oath import totp
import hashlib

def stringToHex (s):
    """Convert the given string to a hexadecimal version of itself,
       since the seed passed to totp() needs it in this form."""

    return ''.join("{:02x}".format(ord(c)) for c in s)

def create (seed, hash=hashlib.sha512):
    """Create a new TOTP for the given secret seed and hash,
       using the default 30 second time step period."""

    return totp(stringToHex(seed), format='dec8', hash=hash)
