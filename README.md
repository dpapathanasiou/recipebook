# About

This is a simple application for scraping and parsing food recipe data found on the web in [hRecipe](http://microformats.org/wiki/hrecipe) format, producing results in [json](http://json.org/).

This project was inspired by [this answer](http://opendata.stackexchange.com/a/4286) to a query for an open database of recipes.

[Contribute](sites/README.md) your favorite site by implementing a [RecipeParser](parser.py) class for it, and make a [pull request](https://help.github.com/articles/about-pull-requests/).

# Data

Recipes collected using the crawler are now available in a [parallel repository](https://github.com/dpapathanasiou/recipes): https://github.com/dpapathanasiou/recipes

# Usage

## Individual recipes

Import the class corresponding to the site you want, and use the recipe URL in its constructor.

Here's an example to fetch and parse the [Chocolate, Almond, and Banana Parfaits](http://www.epicurious.com/recipes/food/views/Chocolate-Almond-and-Banana-Parfaits-357369) recipe from [Epicurious](http://www.epicurious.com/):

```python
>>> import sys; sys.path.append('sites')
>>> from epicurious import Epicurious
>>> recipe = Epicurious("http://www.epicurious.com/recipes/food/views/Chocolate-Almond-and-Banana-Parfaits-357369")
```

Use the <tt>save()</tt> method to create a file of the recipe in json object.

The file name is determined from the URL, and the output folder is defined in the [settings.py](settings.py) file as <tt>OUTPUT_FOLDER</tt>, and can be overridden by creating a local_settings.py file:

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

Kick it off with a specific site and a file of initial seed links, and it will automatically fetch and parse all the related links it finds, without repeating the same link twice.

From the example above, here is how to start the crawler with four parallel worker threads.

The file <tt>/tmp/epi.link</tt> passed in the second argument contains the seed URL <tt>http://www.epicurious.com/recipes/food/views/Chocolate-Almond-and-Banana-Parfaits-357369</tt> for this example, though it could contain more links, too.

It is also a good idea to capture the output into a log file, as shown here, in order to see the full list of parsed recipes, along with any error messages.

```sh
python crawler.py Epicurious /tmp/epi.link 4 > epicurious.log 2>&1
```

By default, all the json files are written to the <tt>OUTPUT_FOLDER</tt> folder specified in [settings.py](settings.py) local_settings.py, but this can be changed by passing a fourth argument: "False" or "F" (in either upper or lower case) will prevent the individual recipes from being written to to the <tt>OUTPUT_FOLDER</tt> folder at all.

Similarly, storing the results to a [ARMS mongo service](https://github.com/dpapathanasiou/ARMS) is off by default, but if the fifth and sixth arguments specify a database and collection, respectively, the crawler will attempt to store them, using the <tt>ARMS</tt> server, api key and seed definitions in [settings.py](settings.py) or local_settings.py.

### Avoiding server blocks

The crawler can also be configured to pause a random number of seconds in between fetches, to prevent recipe hosts from blocking it for too many requests.

The pause default configuration is defined in lines 12 and 13 of the [settings.py](settings.py) file, which can be overridden in a local_settings.py definition.

Another strategy, which can done in conjunction with pausing, is to change the [user agent](https://en.wikipedia.org/wiki/User_agent) from the default defined in line 11 of the [settings.py](settings.py) file to something resembling a human user.

[MDN maintains a list](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) of current common browser agent strings, which can be used in a local_settings.py definition of the <tt>UA</tt> variable.

### Usage
Here is the crawler usage in full:

```sh
python crawler.py [site: (AllRecipes|Epicurious|FoodNetwork|Saveur|SiroGohan|WilliamsSonoma)] [file of seed urls] [threads] [save() (defaults to True)] [store() database (defaults to None)] [store() collection (defaults to None)]
```
