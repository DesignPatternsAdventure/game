"""Check that all imports work as expected.

Primarily checking that:

1. No optional dependencies are required

"""

from pprint import pprint

from game.play import main  # noqa: F401

pprint(locals())  # noqa: T003
