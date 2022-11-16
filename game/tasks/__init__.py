"""Internal logic for pointing to whichever task code will be loaded."""

# FIXME: Rename files and separate lesson code from editable task code (maybe t01_l_lesson and t01_l_task?)

from . import task01_s_select_player as player_module  # noqa: F401
from . import task04_i_the_raft, task05_d_the_new_island

code_modules = [task04_i_the_raft, task05_d_the_new_island]
