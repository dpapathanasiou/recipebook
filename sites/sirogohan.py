#!/usr/bin/env python
# coding: utf-8

"""
sirogohan.py

This module inherits from RecipeParser, and provides an implementation
for parsing recipes from the sirogohan.com site.

"""

from lxml import etree
import re

from parser import RecipeParser

class SiroGohan(RecipeParser):

    # define some patterns to match/filter
    otherURL = re.compile(r'^/recipe/', re.I)

    def setLanguage(self):
        self.language = 'ja-JP'

    def getTitle(self):
        """The title format is:

        <title>Recipe：白ごはん.com</title>

        we want just 'Recipe'
        """
        return self.tree.xpath('//title')[0].text.split(u'：')[0].strip()

    def getImage(self):
        """The image format is:

        <meta property="og:image" content="IMG_URL">

        we want just 'IMG_URL'
        """
        return self.tree.xpath('//meta[@property="og:image"]')[0].get('content')

    def getIngredients(self):
        """Return a list or a map of the recipe ingredients"""
        data = []
        # the basic ingredients
        for node in self.tree.xpath('//div[@class="material-halfbox"]//ul[@class="disc-list"]/li'):
            data.append( u''.join(node.xpath('descendant-or-self::text()')).strip() )
        # the 'maru' ingredients
        for node in self.tree.xpath('//ul[@class="circle-list"]/li'):
            data.append(u'○ ' + u''.join(node.xpath('descendant-or-self::text()')).strip() )
        # the 'A' ingredients
        for node in self.tree.xpath('//ul[@class="a-list"]/li'):
            data.append(u'A ' + u''.join(node.xpath('descendant-or-self::text()')).strip() )
        return data

    def getDirections(self):
        """Return a list or a map of the preparation instructions"""
        data = []
        # the basic instructions
        for node in self.tree.xpath('//div[@class="howto-block"]/*'):
            data.append( u''.join(node.xpath('descendant-or-self::text()')).strip() )
        # plus any hints
        for node in self.tree.xpath('//div[@class="point-text"]/*/li'):
            data.append( u''.join(node.xpath('descendant-or-self::text()')).strip() )
        return list(filter(None, data))

    def getTags(self):
        """Return a list of tags for this recipe"""
        data = []
        for node in self.tree.xpath('//dt[@class="icon-keyword"]'):
            for link in node.xpath('//dd/a'):
                data.append( ''.join(link.xpath('descendant-or-self::text()')).strip() )
        return list(filter(None, data))

    def getOtherRecipeLinks(self):
        """Return a list of other recipes found in the page"""
        data = []
        for link in self.tree.xpath('//div[@class="ranking-box"]/a'):
            if 'href' in link.keys():
                href = link.get('href')
                if self.otherURL.search(href):
                    l = 'http://www.sirogohan.com' + href
                    if self.url != l and l not in data:
                        data.append(l)
        return data
