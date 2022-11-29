"""Internal logic for pointing to whichever task code will be loaded."""

from types import ModuleType

from .task01 import task_s_select_character as player_module  # noqa: F401
from .task02 import task_o_inventory as task_2  # noqa: F401
from .task03 import task_l_crafting as task_3  # noqa: F401

# from .task04 import task_s_select_character as task_4  # noqa: F401
# from .task05 import task_s_select_character as task_5  # noqa: F401

code_modules: list[ModuleType] = [task_2, task_3]
