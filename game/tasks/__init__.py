"""Internal logic for pointing to whichever task code will be loaded."""

from . import task01_s_select_player as player_module  # noqa: F401
from . import (
    task02_o_inventory,
    task03_l_crafting,
    task04_i_the_raft,
    task05_d_the_new_island,
)

code_modules = [
    task02_o_inventory,
    task03_l_crafting,
    task04_i_the_raft,
    task05_d_the_new_island,
]
