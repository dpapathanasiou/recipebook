# About

These are the implementations made so far for recipe sites which support the [hRecipe](http://microformats.org/wiki/hrecipe) format for their data:

* [AllRecipes](allrecipes.py)
* [Epicurious](epicurious.py)
* [FoodNetwork](foodnetwork.py)
* [Saveur](saveur.py)
* [SiroGohan](sirogohan.py)
* [WilliamsSonoma](wsonoma.py)

# Contribute

Add your favorite site by implementing a [RecipeParser](../parser.py) class with appropriate [lxml etree](http://lxml.de/tutorial.html) definitions of the <tt>getIngredients()</tt>, <tt>getDirections()</tt>, <tt>getTags()</tt>, and <tt>getOtherRecipeLinks()</tt> methods.

Few sites implement hRecipe exactly, though, so study the site's html source code to understand its structure. Also see how the current implementations for [AllRecipes](allrecipes.py), [Epicurious](epicurious.py), [FoodNetwork](foodnetwork.py), and [Williams Sonoma](wsonoma.py) were written.

[Pull requests](https://help.github.com/articles/about-pull-requests/) are welcome!
