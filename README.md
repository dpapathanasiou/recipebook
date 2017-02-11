# About

This is a simple application for scraping and parsing food recipe data found on the web in [hRecipe](http://microformats.org/wiki/hrecipe) format, producing results in [json](http://json.org/).

This project was inspired by [this answer](http://opendata.stackexchange.com/a/4286) to a query for an open database of recipes.

# Usage

## Individual recipes

Import the class corresponding to the site you want, and use the recipe URL in its constructor.

Here's an example to fetch and parse the [Chocolate, Almond, and Banana Parfaits](http://www.epicurious.com/recipes/food/views/Chocolate-Almond-and-Banana-Parfaits-357369) recipe from [Epicurious](http://www.epicurious.com/):

```python
>>> from epicurious import Epicurious
>>> recipe = Epicurious("http://www.epicurious.com/recipes/food/views/Chocolate-Almond-and-Banana-Parfaits-357369")
```

Use the <tt>save()</tt> method to create a file of the recipe in json object.

The file name is determined from the URL, and the output folder is defined in the [settings.py](settings.py) file (it is <tt>/tmp/</tt> by default)):

```python
>>> recipe.save()
```

Results in the creation of <tt>/tmp/chocolate-almond-and-banana-parfaits-357369.json</tt> with these contents:

```json
{
    "directions": [
        "Heat chocolate chips and 4 tablespoons cream in microwave in 1-cup glass measuring cup at 50 percent power just until chocolate is melted, about 30 to 35 seconds. Stir to blend; cool chocolate sauce to lukewarm. Whisk mascarpone, amaretto, sugar, and remaining 2 tablespoons cream in medium bowl until blended and mixture just starts to thicken.",
        "Using 2 1/2-inch-diameter cookie cutter, cut out round from each angel food cake slice. Place 1 cake round in each of 4 wine goblets or old-fashioned glasses. Top each cake round with 3 banana slices, 1 heaping tablespoon mascarpone mixture, bittersweet chocolate sauce, and sprinkling of almonds. Repeat parfait layering 1 more time and serve."
    ],
    "ingredients": [
        "1/2 cup bittersweet chocolate chips",
        "6 tablespoons heavy whipping cream, divided",
        "3/4 cup mascarpone cheese",
        "3 tablespoons amaretto",
        "2 tablespoons sugar",
        "8 1/2-inch-thick angel food cake slices",
        "24 1/3-inch-thick diagonal banana slices (from about 3 bananas)",
        "1/3 cup (about) sliced almonds, toasted"
    ],
    "source": "www.epicurious.com",
    "tags": [
        "Chocolate",
        "Dessert",
        "Quick & Easy",
        "High Fiber",
        "Banana",
        "Almond",
        "Amaretto",
        "Shower",
        "Party",
        "Vegetarian",
        "Pescatarian",
        "Peanut Free",
        "Soy Free",
        "Kosher"
    ],
    "title": "Chocolate, Almond, and Banana Parfaits",
    "url": "http://www.epicurious.com/recipes/food/views/Chocolate-Almond-and-Banana-Parfaits-357369"
}
```

## Crawling

The better sites, such as Epicurious and [FoodNetwork](http://www.foodnetwork.com), offer related links within each recipe.

It is easy to use those to crawl the entire site automatically.

From the example above, the <tt>getOtherRecipeLinks()</tt> method produces more URLs to fetch:

```python
>>> recipe.getOtherRecipeLinks()
['http://www.epicurious.com/recipes/food/views/chocolate-amaretto-souffles-104730', 'http://www.epicurious.com/recipes/food/views/coffee-almond-ice-cream-cake-with-dark-chocolate-sauce-11036', 'http://www.epicurious.com/recipes/food/views/toasted-almond-mocha-ice-cream-tart-12550', 'http://www.epicurious.com/recipes/food/views/chocolate-marble-cheesecake-241488', 'http://www.epicurious.com/recipes/food/views/hazelnut-dome-cake-4246']
```

Each of those links will also have related links. By keeping track of which have already been visited, a simple crawler can pull most of the recipes on the site with one command.
