#!/usr/bin/env python

"""
wsonoma.py

This module inherits from RecipeParser, and provides an implementation
for parsing recipes from the williams-sonoma.com site.

"""

from lxml import etree
from urlparse import urlsplit

from parser import RecipeParser

class WilliamsSonoma(RecipeParser):
    def getTitle(self):
        """The title format is:

        <title>Recipe | Williams Sonoma</title>

        we want just 'Recipe'
        """
        return self.tree.xpath('//title')[0].text.split('|')[0].strip()

    def getIngredients(self):
        """Return a list or a map of the recipe ingredients"""
        data = []
        for node in self.tree.xpath('//li[@itemprop="ingredient"]'):
            data.append( ''.join(node.xpath('descendant-or-self::text()')).strip() )
        return data

    def getDirections(self):
        """Return a list or a map of the preparation instructions"""
        data = []
        for node in self.tree.xpath('//div[@class="directions"]'):
            data.append( node.xpath('descendant-or-self::text()') )
        return filter(None, map(lambda x: x.strip(), data[0]))

    def getTags(self):
        """Return a list of tags for this recipe"""
        return []

    def getOtherRecipeLinks(self):
        """Return a list of other recipes found in the page: while single recipe
        pages do not have links, the various categories at
        http://www.williams-sonoma.com/recipe/ do.

        For example,
        http://www.williams-sonoma.com/search/results.html?activeTab=recipes&words=winter_weeknight_dinners
        has a collection of individual recipe links, and this method will find them.

        """
        data = []
        for link in self.tree.xpath('//ul[@class="recipe-list"]/li/a'):
            if 'href' in link.keys():
                href = urlsplit(link.get('href'))
                if 'cm_src=RECIPESEARCH' == href.query:
                    data.append(href.scheme + '://' + href.netloc + href.path)
        return data
