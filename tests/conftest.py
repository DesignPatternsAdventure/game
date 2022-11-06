"""PyTest configuration.

Note: the calcipy imports are required for a nicer test HTML report

"""

from pathlib import Path

import arcade
import pytest
from calcipy.dev.conftest import pytest_configure  # noqa: F401
from calcipy.dev.conftest import pytest_html_results_table_header  # noqa: F401
from calcipy.dev.conftest import pytest_html_results_table_row  # noqa: F401
from calcipy.dev.conftest import pytest_runtest_makereport  # noqa: F401

from .configuration import TEST_TMP_CACHE, clear_test_cache


@pytest.fixture()
def fix_test_cache() -> Path:
    """Fixture to clear and return the test cache directory for use.

    Returns:
        Path: Path to the test cache directory

    """
    clear_test_cache()
    return TEST_TMP_CACHE


# ---------- Arcade Test Configuration ----------
# Copied from: https://github.com/pythonarcade/arcade/blob/a25940fe78a2d286fd0f27e6b2fc52318189fe21/tests/conftest.py


# Reduce the atlas size
arcade.ArcadeContext.atlas_size = (2048, 2048)

WINDOW = None


def create_window() -> arcade.Window:
    global WINDOW
    if not WINDOW:
        WINDOW = arcade.Window(title='Testing', vsync=False, antialiasing=False)
        WINDOW.set_vsync(False)
    return WINDOW


def prepare_window(window: arcade.Window) -> None:
    # Check if someone has been naughty
    if window.has_exit:
        raise RuntimeError('Please do not close the global test window :D')

    window.switch_to()
    _ctx = window.ctx
    _ctx._default_atlas = None  # Clear the global atlas
    window.hide_view()  # Disable views if any is active

    # Reset context (various states)
    _ctx.reset()
    window.set_vsync(False)
    window.flip()
    window.clear()
    _ctx.gc_mode = 'context_gc'

    # Ensure no old functions are lingering
    window.on_draw = lambda: None
    window.on_update = lambda _dt: None
    window.update = lambda _dt: None


@pytest.fixture(scope='function')
def window():
    win = create_window()
    arcade.set_window(win)
    try:
        prepare_window(win)
        yield win
    finally:
        win.flip()
