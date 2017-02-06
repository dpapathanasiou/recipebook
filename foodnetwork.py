#!/usr/bin/env python

"""
foodnetwork.py

This module inherits from RecipeParser, and provides an implementation
for parsing recipes from the foodnetwork.com site.

"""

from lxml import etree
from urlparse import urlsplit
import json
import re

from parser import RecipeParser

class FoodNetwork(RecipeParser):
    
    # define some patterns to match/filter
    credits  = re.compile(r'photograph by', re.I)
    otherURL = re.compile(r'^/recipes/', re.I)

    def getTitle(self):
        """The title format is:

        <title>Recipe : Contributor Name : Food Network</title>

        we want just 'Recipe'
        """
        return self.tree.xpath('//title')[0].text.split(':')[0].strip()

    def getIngredients(self):
        """Return a list or a map of the recipe ingredients"""
        data = []
        for node in self.tree.xpath('//li[@itemprop="ingredients"]'):
            data.append( ''.join(node.xpath('descendant-or-self::text()')).strip() )
        return data

    def getDirections(self):
        """Return a list or a map of the preparation instructions"""
        data = []
        for node in self.tree.xpath('//div[@itemprop="recipeInstructions"]'):
            for item in node.xpath('//ul[@class="recipe-directions-list"][li]'):
                for p in item:
                    data.append( ''.join(p.xpath('descendant-or-self::text()')).strip() )
        return filter(lambda x: self.credits.search(x) is None, data)

    def getTags(self):
        """Return a list of tags for this recipe"""
        data = []
        for node in self.tree.xpath('//li[@itemprop="recipeCategory"]'):
            data.append( ''.join(node.xpath('descendant-or-self::text()')).strip() )
        return data

    def getOtherRecipeLinks(self):
        """Return a list of other recipes found in the page"""
        data = []
        for link in self.tree.xpath('//div[contains(@class,"more-ideas")]/div[contains(@class,"recipes")]/div[contains(@class,"group")]/*/a'):
            if 'href' in link.keys():
                l = link.get('href')
                if self.otherURL.search(l):
                    data.append( 'http://www.foodnetwork.com'+l )
        return data
