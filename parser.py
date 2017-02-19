#!/usr/bin/env python

"""
parser.py

This module defines an abstract RecipeParser class, which provides
some basic parsing infrastructure, but ultimately requires each
source class to implement, since each recipe site adheres to hRecipe
somewhat differently.

"""

from lxml import etree
from urlparse import urlsplit
import json
import codecs
import os

from scraper import getUrl
from settings import ENCODING, OUTPUT_FOLDER

class RecipeParser:
    def __init__(self, url, pageEncoding=ENCODING):
        self.url  = url
        self.html = getUrl(self.url)
        if self.html is not None:
            self.valid  = True
            self.encode = pageEncoding
            self.parser = etree.HTMLParser(encoding=self.encode)
            self.tree   = etree.HTML(self.html, parser=self.parser)
        else:
            self.valid = False
            raise ValueError('could not fetch data from: ""'+self.url+'""')

    def setSource(self):
        """Defaults to the 'netloc' portion of the url (can be overridden)"""
        self.source = urlsplit(self.url).netloc

    def setLanguage(self):
        """Define the IETF language tag of the site contents (defaults to 'en-US' but can be overridden)"""
        self.language = 'en-US'

    def setFilename(self):
        """Defaults to the last string in the url path, minus '.html|.htm' (can be overridden)"""
        self.filename = filter(None, urlsplit(self.url).path.split('/'))[-1:][0].lower().replace('.html', '').replace('.htm', '')+'.json'

    def compose(self):
        """Compose the json object of the recipe data"""

        self.setSource()
        self.setLanguage()
        return {
          'source': self.source,
          'language': self.language,
          'title': self.getTitle(),
          'ingredients': self.getIngredients(),
          'directions': self.getDirections(),
          'tags': self.getTags(),
          'url': self.url
        }

    def save(self, folder=OUTPUT_FOLDER):
        """Attempt to write the resulting json data to a text file"""

        data = json.dumps(self.compose(), indent=4, sort_keys=True)
        if not self.valid:
            print '[error] invalid data at:', self.url
        else:
            self.setFilename()
            try:
                with codecs.open(os.path.join(folder, self.filename), 'w', self.encode) as f:
                    f.write(data)
            except (OSError, IOError):
                print '[error] could not write recipe json in:', os.path.join(folder, self.filename)

    def getTitle(self):
        """Defaults to the <title> string in the html (can be overridden)"""
        return self.tree.xpath('//title')[0].text.strip()

    def getIngredients(self):
        """Return a list or a map of the recipe ingredients"""
        raise NotImplementedError('subclasses must override getIngredients()')

    def getDirections(self):
        """Return a list or a map of the preparation instructions"""
        raise NotImplementedError('subclasses must override getDirections()')

    def getTags(self):
        """Return a list of tags for this recipe"""
        raise NotImplementedError('subclasses must override getTags()')

    def getOtherRecipeLinks(self):
        """Return a list of other recipes found in the page"""
        raise NotImplementedError('subclasses must override getOtherRecipeLinks()')
