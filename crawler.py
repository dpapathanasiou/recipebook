#!/usr/bin/env python

"""
crawler.py

For any given site implementation, use the getOtherRecipeLinks()
results to crawl for other recipes automatically.

"""

from Queue import Queue
from threading import Thread
import sys
import time

# sites implemented so far
from allrecipes import AllRecipes
from epicurious import Epicurious
from foodnetwork import FoodNetwork
from sirogohan import SiroGohan
from wsonoma import WilliamsSonoma

AVAILABLE = {
  'AllRecipes' : AllRecipes,
  'Epicurious' : Epicurious,
  'FoodNetwork' : FoodNetwork,
  'SiroGohan' : SiroGohan,
  'WilliamsSonoma' : WilliamsSonoma,
}

class UniqueQueue(Queue):
    def _init(self, maxsize):
        Queue._init(self, maxsize)
        self.all_items = set()

    def _put(self, item):
        if item not in self.all_items:
            Queue._put(self, item)
            self.all_items.add(item)

    def _get(self):
        return self.queue.pop()

    def has(self, item):
        item in self.all_items

pending = UniqueQueue()
fetched = UniqueQueue()

def site (label):
    """Return the site module corresponding to this label,
       defaulting to None if not available"""
    return AVAILABLE.get(label, None)

def fetch (src, folder, p, f):
    """This is the worker function to get the next recipe from
       the pending queue, save it, and put all the related urls
       on the pending queue for other workers to process"""
    while True:
        url = p.get()
        if f.has(url):
            p.task_done()
        else:
            recipe = src(url)
            recipe.save(folder)
            f.put(url)
            map(lambda x: p.put(x), filter(lambda link: link != url, recipe.getOtherRecipeLinks()))
            p.task_done()

if __name__ == "__main__":
    """Create a command-line main() entry point"""

    if len(sys.argv) < 4:
        # Define the usage
        print sys.argv[0], \
          '[site: (AllRecipes|Epicurious|FoodNetwork|SiroGohan|WilliamsSonoma)]', \
          '[seed url (containing other links)]', \
          '[threads]', \
          '[output folder (optional: defaults to "/tmp")]'
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

            folder ='/tmp'
            try:
                folder = sys.argv[4]
            except IndexError:
                pass

            pending.put(sys.argv[2])
            for i in range(threads):
                worker = Thread(target=fetch, args=(module, folder, pending, fetched,))
                worker.setDaemon(True)
                worker.start()

            # give the first worker time to parse the seed url
            # and put other links on the pending queue
            time.sleep(10)

            pending.join()
            print 'Fetched and parsed:'
            for i, link in enumerate(fetched.get()):
                print i, link
