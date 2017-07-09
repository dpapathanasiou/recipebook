#!/usr/bin/env python

"""
crawler.py

For any given site implementation, use the getOtherRecipeLinks()
results to crawl for other recipes automatically.

"""

from Queue import Queue
from threading import Thread
import sys
sys.path.append('sites')

# sites implemented so far
from allrecipes import AllRecipes
from epicurious import Epicurious
from foodnetwork import FoodNetwork
from saveur import Saveur
from sirogohan import SiroGohan
from wsonoma import WilliamsSonoma

AVAILABLE = {
  'AllRecipes' : AllRecipes,
  'Epicurious' : Epicurious,
  'FoodNetwork' : FoodNetwork,
  'SiroGohan' : SiroGohan,
  'Saveur' : Saveur,
  'WilliamsSonoma' : WilliamsSonoma,
}

pending = Queue()
fetched = Queue()

def site (label):
    """Return the site module corresponding to this label,
       defaulting to None if not available"""
    return AVAILABLE.get(label, None)

def fetch (src, save, db, collection, p, f):
    """This is the worker function to get the next recipe from
       the pending queue, save it, and put all the related urls
       on the pending queue for other workers to process"""
    while True:
        url = p.get()
        if url in f.queue:
            p.task_done()
        else:
            try:
                recipe = src(url)
                if save:
                    recipe.save()
                if db is not None and collection is not None:
                    recipe.store(db, collection)
                f.put(url)
                map(lambda x: p.put(x), filter(lambda link: link != url, recipe.getOtherRecipeLinks()))
            except ValueError:
                print '[warning] could not fetch:', url
            p.task_done()

if __name__ == "__main__":
    """Create a command-line main() entry point"""

    if len(sys.argv) < 4:
        # Define the usage
        possibleSources = sorted(AVAILABLE.keys())
        print sys.argv[0], \
          '[site: (' + u'|'.join(possibleSources) +')]', \
          '[file of seed urls]', \
          '[threads]', \
          '[save() (defaults to True)]', \
          '[store() database (defaults to None)]', \
          '[store() collection (defaults to None)]'
    else:
        # Do the deed
        module = site(sys.argv[1])
        if module is None:
            print 'Sorry, that site is not yet available'
        else:
            threads = 1
            try:
                threads = int(sys.argv[3])
            except ValueError:
                pass

            save = True
            try:
                saveReq = sys.argv[4].lower()
                save = saveReq.startswith('t') or saveReq == 'true'
            except IndexError:
                pass

            db = None
            collection = None
            try:
                db = sys.argv[5]
                collection = sys.argv[6]
            except IndexError:
                pass

            for i in range(threads):
                worker = Thread(target=fetch, args=(module, save, db, collection, pending, fetched,))
                worker.setDaemon(True)
                worker.start()

            # load the file of initial urls and seed the pending queue
            with open(sys.argv[2], 'r') as f:
                links = f.read()
                map(lambda link: pending.put(link), links.splitlines())

            pending.join()

            # show the summary
            print 'Fetched and parsed:'
            for i, link in enumerate(set(fetched.queue)):
                print "{:,}".format(1+i), '\t', link
