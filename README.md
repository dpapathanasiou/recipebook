# About

This is a simple application for scraping and parsing food recipe data found on the web in [hRecipe](http://microformats.org/wiki/hrecipe) format, producing results in [json](http://json.org/).

This project was inspired by [this answer](http://opendata.stackexchange.com/a/4286) to a query for an open database of recipes.

# Contribute

Add your favorite site by implementing a [RecipeParser](parser.py) class with appropriate [lxml etree](http://lxml.de/tutorial.html) definitions of the <tt>getIngredients()</tt>, <tt>getDirections()</tt>, <tt>getTags()</tt>, and <tt>getOtherRecipeLinks()</tt> methods.

Few sites implement hRecipe exactly, though, so study the site's html source code to understand its structure. Also see how the current implementations for [AllRecipes](allrecipes.py), [Epicurious](epicurious.py), [FoodNetwork](foodnetwork.py), and [Williams Sonoma](wsonoma.py) were written.

[Pull requests](https://help.github.com/articles/about-pull-requests/) are welcome!

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
    "language": "en-US",
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

Most sites offer related links within each recipe.

From the example above, the <tt>getOtherRecipeLinks()</tt> method produces more URLs to fetch:

```python
>>> recipe.getOtherRecipeLinks()
['http://www.epicurious.com/recipes/food/views/chocolate-amaretto-souffles-104730', 'http://www.epicurious.com/recipes/food/views/coffee-almond-ice-cream-cake-with-dark-chocolate-sauce-11036', 'http://www.epicurious.com/recipes/food/views/toasted-almond-mocha-ice-cream-tart-12550', 'http://www.epicurious.com/recipes/food/views/chocolate-marble-cheesecake-241488', 'http://www.epicurious.com/recipes/food/views/hazelnut-dome-cake-4246']
```

The [crawler.py](crawler.py) application takes advantage of this by visiting each related recipe link in parallel, getting even more recipe links, fetching each of those, and so on.

Kick it off with a specific site and an initial seed link, and it will automatically fetch and parse all the related links it finds, without repeating the same link twice.

From the example above, here is how to start the crawler with four parallel worker threads:

```sh
python crawler.py Epicurious "http://www.epicurious.com/recipes/food/views/Chocolate-Almond-and-Banana-Parfaits-357369" 4
```

By default, all the json files are written to the <tt>/tmp</tt> folder, but this can be changed by passing a fourth argument.

Here is the crawler usage:

```sh
python crawler.py [site: (AllRecipes|Epicurious|FoodNetwork|SiroGohan|WilliamsSonoma)] [seed url (containing other links)] [threads] [output folder (optional: defaults to "/tmp")]
```
