#!/usr/bin/env python

"""
epicurious.py

This module inherits from RecipeParser, and provides an implementation
for parsing recipes from the saveur.com site.

"""

import re

from parser import RecipeParser


class Saveur(RecipeParser):
    # define some patterns to match/filter
    issueTag = re.compile(r'Issue', re.I)
    tagHREF = re.compile(r'^/tags/', re.I)

    def getTitle(self):
        """The title format is:

        <title>Recipe | SAVEUR</title>

        we want just 'Recipe'
        """
        return u' '.join(self.tree.xpath('//title')[0].text.split('|')[0].strip().split()[:-1])

    def getImage(self):
        """The image format is:

        <meta property="og:image" content="IMG_URL">

        we want just 'IMG_URL'
        """
        return self.tree.xpath('//meta[@property="og:image"]')[0].get('content')

    def getIngredients(self):
        """Return a list or a map of the recipe ingredients"""
        data = []
        for node in self.tree.xpath('//div[@property="ingredients"]'):
            data.append(''.join(node.xpath('descendant-or-self::text()')).strip())
        return data

    def getDirections(self):
        """Return a list or a map of the preparation instructions"""
        data = []
        for node in self.tree.xpath('//div[@property="recipeInstructions"]'):
            data.append(''.join(node.xpath('descendant-or-self::text()')).strip())
        return data

    def getTags(self):
        """Return a list of tags for this recipe"""
        data = []
        for node in self.tree.xpath('//div[contains(@class,"field-tags")]/ul/li/a'):
            if 'href' in node.keys():
                link = node.get('href')
                if self.tagHREF.search(link):
                    tag = u''.join(node.xpath('descendant-or-self::text()')).strip()
                    if not self.issueTag.search(tag):
                        data.append(tag)
        return list(filter(None, data))

    def getOtherRecipeLinks(self):
        """Return a list of other recipes found in the page"""
        return []  # unfortunately these are javascript-enabled by user interaction
