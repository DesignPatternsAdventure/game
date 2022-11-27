"""Internal logic for pointing to whichever task code will be loaded."""

from types import ModuleType

from .task01 import task_s_select_character as player_module  # noqa: F401

code_modules: list[ModuleType] = []
