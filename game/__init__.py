"""game."""

from warnings import filterwarnings

from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

__version__ = '0.0.1'
__pkg_name__ = 'game'

# FYI: https://github.com/beartype/beartype#are-we-on-the-worst-timeline
filterwarnings('ignore', category=BeartypeDecorHintPep585DeprecationWarning)
