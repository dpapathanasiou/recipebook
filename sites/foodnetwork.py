#!/usr/bin/env python

"""
foodnetwork.py

This module inherits from RecipeParser, and provides an implementation
for parsing recipes from the foodnetwork.com site.

"""

from lxml import etree
import re
import json

from parser import RecipeParser
from settings import ENCODING

class FoodNetwork(RecipeParser):
    def __init__(self, url, pageEncoding=ENCODING):
        RecipeParser.__init__(self, url, pageEncoding)
        # this site now has all the recipe data available as an embedded json object
        for node in self.tree.xpath('//*[@type="application/ld+json"]'):
            self.recipeJSON = json.loads( u''.join(node.xpath('descendant-or-self::text()')) )

    # define some patterns to match/filter
    otherURL  = re.compile(r'/recipes/', re.I)
    seriesURL = re.compile(r'recipes$', re.I)
    sectionURL = re.compile(r'#', re.I)

    def getTitle(self):
        """The title format is:

        <title>Recipe | Contributor Name | Food Network</title>

        we want just 'Recipe'
        """
        try:
            # use the json object data
            return self.recipeJSON['name']
        except (AttributeError, KeyError) as e:
            print '[warning]: likely no recipe at', self.url
            # fall back to parsing the html title, which is colon-separated
            return self.tree.xpath('//title')[0].text.split(':')[0].strip()

    def getIngredients(self):
        """Return a list or a map of the recipe ingredients"""
        try:
            return filter(None, map(lambda x: x.strip(), self.recipeJSON['recipeIngredient']))
        except (AttributeError, KeyError):
            self.valid = False
            return []

    def getDirections(self):
        """Return a list or a map of the preparation instructions"""
        try:
            return filter(None, map(lambda x: x.strip(), self.recipeJSON['recipeInstructions']))
        except (AttributeError, KeyError):
            self.valid = False
            return []

    def getTags(self):
        """Return a list of tags for this recipe"""
        try:
            return filter(None, map(lambda x: x.strip(), self.recipeJSON['recipeCategory']))
        except (AttributeError, KeyError):
            self.valid = False
            return []

    def getOtherRecipeLinks(self):
        """Return a list of other recipes found in the page"""
        data = []
        for link in self.tree.xpath('//div[contains(@class,"m-MediaBlock__m-MediaWrap")]/a'):
            if 'href' in link.keys():
                l = link.get('href')
                if self.otherURL.search(l) and \
                  not self.seriesURL.search(l) and \
                  not self.sectionURL.search(l):
                    data.append(l)
        return data
