#!/usr/bin/env python

"""
allrecipes.py

This module inherits from RecipeParser, and provides an implementation
for parsing recipes from the allrecipes.com site.

"""

import json
import re

from parser import RecipeParser


class AllRecipes(RecipeParser):
    # define some patterns to match/filter
    otherURL = re.compile(r'^/recipe/', re.I)

    def getTitle(self):
        """The title format is:

        <title>'Recipe' Recipe - Allrecipes.com</title>

        we want just 'Recipe'
        """
        return self.tree.xpath('//title')[0].text.split(' Recipe ')[0].strip()

    def getImage(self):
        """The image format is:

        <meta property="og:image" content="IMG_URL">

        we want just 'IMG_URL'
        """
        return self.tree.xpath('//meta[@property="og:image"]')[0].get('content')

    def getIngredients(self):
        """Return a list or a map of the recipe ingredients"""
        data = []
        for node in self.tree.xpath('//span[@itemprop="recipeIngredient"]'):
            data.append(''.join(node.xpath('descendant-or-self::text()')).strip())
        return data

    def getDirections(self):
        """Return a list or a map of the preparation instructions"""
        data = []
        for node in self.tree.xpath('//ol[@itemprop="recipeInstructions"][li]'):
            for item in node:
                data.append(''.join(item.xpath('descendant-or-self::text()')).strip())
        return data

    def getTags(self):
        """Return a list of tags for this recipe"""
        return []

    def getOtherRecipeLinks(self):
        """Return a list of other recipes found in the page"""
        data = {}  # k = recipe id, v = recipe url

        # type one: similar recipes carousel (page bottom)
        for link in self.tree.xpath('//ul[@class="recipe-carousel"]/li[@class="slider-card"]/*/a'):
            if 'href' in link.keys():
                href = link.get('href')
                if self.otherURL.search(href):
                    parts = href.split('/')
                    try:
                        data[parts[2]] = 'http://allrecipes.com' + href
                    except IndexError:
                        pass

        # type two: json embedded in the right side panel
        for node in self.tree.xpath('//right-rail-feed'):
            if 'my-feed-data' in node.keys():
                feed = json.loads(node.get('my-feed-data'))
                for item in feed['items']:
                    if 'id' in item:
                        recipeId = str(item['id'])
                        if recipeId not in data:
                            # these links are less descriptive,
                            # so we do not want them over-writing
                            # any pre-existing with the same id
                            data[recipeId] = 'http://allrecipes.com/recipe/' + recipeId

        return data.values()
