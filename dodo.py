# pylint: disable=C0413,W0614
"""doit Script.

```py
# Ensure that packages are installed
poetry install
# List Tasks
poetry run doit list
# (Or use a poetry shell)
# > poetry shell
# (game-py3.10) doit list

# Run tasks individually (examples below)
(game-py3.10) doit run test
(game-py3.10) doit run test check
# Or all of the tasks in DOIT_CONFIG
(game-py3.10) doit
```

"""

from warnings import filterwarnings

from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

# FYI: https://github.com/beartype/beartype#are-we-on-the-worst-timeline
filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)

from beartype import beartype  # noqa: E402,F403
from calcipy.doit_tasks.base import debug_task  # noqa: E402,F403
from calcipy.doit_tasks.doit_globals import DoitTask  # noqa: E402,F403
from doit.tools import Interactive  # noqa: E402,F403
from pattern_feedback_tool.doit_tasks import *  # noqa: E402,F401,F403


@beartype
def task_update() -> DoitTask:
    """Run update operations and update the requirements file.

    Returns:
        DoitTask: DoIt task

    """
    return debug_task(
        [
            Interactive("poetry lock --no-update"),
            Interactive(
                "poetry export --format=requirements.txt --output=requirements.txt --without-hashes"
            ),
        ]
    )
