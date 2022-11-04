"""doit Script.

```python3
# Ensure that packages are installed
poetry install
# List Tasks
poetry run doit list
# (Or use a poetry shell)
# > poetry shell
# > doit list

# Run tasks individually (examples below)
poetry run doit run ptw_ff
poetry doit run coverage open_test_docs
# Or all of the tasks in DOIT_CONFIG
poetry run doit
```

"""

from beartype import beartype
from calcipy.doit_tasks import *  # noqa: F401,F403,H303 (Run 'doit list' to see tasks)
from calcipy.doit_tasks import DOIT_CONFIG_RECOMMENDED
from calcipy.doit_tasks.base import debug_task
from calcipy.doit_tasks.doit_globals import DoitTask
from calcipy.log_helpers import activate_debug_logging
from doit.tools import Interactive

from game import __pkg_name__

activate_debug_logging(pkg_names=[__pkg_name__])

# Create list of all tasks run with `poetry run doit`
DOIT_CONFIG = DOIT_CONFIG_RECOMMENDED


@beartype
def task_play() -> DoitTask:
    """Launch and play the game!

    Returns:
        DoitTask: doit task

    """
    return debug_task([
        Interactive('poetry run python -m game.play'),
    ])
