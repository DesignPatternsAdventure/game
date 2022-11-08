"""doit Script.

```py
# Ensure that packages are installed
poetry install
# List Tasks
poetry run doit list
# (Or use a poetry shell)
# > poetry shell
# (shell) doit list

# Run tasks individually (examples below)
(shell) doit run test
(shell) doit run test check
# Or all of the tasks in DOIT_CONFIG
(shell) doit
```

"""

from warnings import filterwarnings

from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

# FYI: https://github.com/beartype/beartype#are-we-on-the-worst-timeline
filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)

from pattern_feedback_tool.doit_tasks import *  # noqa: E402,F401,F403
