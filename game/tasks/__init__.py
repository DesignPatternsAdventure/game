"""Internal logic for pointing to whichever task code will be loaded."""

from . import task01_S_player as player_module  # noqa: F401
from . import task02_O_TBD, task03_L_TBD, task04_I_TBD, task05_D_TBD

code_modules = [task02_O_TBD, task03_L_TBD, task04_I_TBD, task05_D_TBD]
