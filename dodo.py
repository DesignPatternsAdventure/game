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

from warnings import filterwarnings

from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

# FYI: https://github.com/beartype/beartype#are-we-on-the-worst-timeline
filterwarnings('ignore', category=BeartypeDecorHintPep585DeprecationWarning)

from beartype import beartype  # noqa: E402
from calcipy.doit_tasks import *  # noqa: F401,F403,H303 (Run 'doit list' to see tasks)
from calcipy.doit_tasks import DOIT_CONFIG_RECOMMENDED  # noqa: E402
from calcipy.doit_tasks.base import debug_task  # noqa: E402
from calcipy.doit_tasks.doit_globals import DoitTask  # noqa: E402
from calcipy.log_helpers import activate_debug_logging  # noqa: E402
from doit.tools import Interactive  # noqa: E402

from game import __pkg_name__  # noqa: E402

activate_debug_logging(pkg_names=[__pkg_name__])

DOIT_CONFIG_RECOMMENDED['default_tasks'] = ['auto_format', 'test_all', 'lint_project', 'check_types']

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
