"""bacon.py

ModuleFinder Official sample

https://docs.python.org/ja/3/library/modulefinder.html#modulefinder-example
"""

import re, itertools

try:
    import baconhameggs
except ImportError:
    pass

try:
    import guido.python.ham
except ImportError:
    pass

