# Developer Notes

## Local Development

```sh
git clone https://github.com/DesignPatternsAdventure/game.git
cd game
poetry install

# See the available tasks
poetry run doit list

# Run the default task list (lint, auto-format, test coverage, etc.)
poetry run doit --continue

# Make code changes and run specific tasks as needed:
poetry run doit run test
```

## Publishing

For testing, create an account on [TestPyPi](https://test.pypi.org/legacy/). Replace `...` with the API token generated on TestPyPi or PyPi respectively

```sh
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi ...

poetry run doit run publish_test_pypi
# If you didn't configure a token, you will need to provide your username and password to publish
```

To publish to the real PyPi

```sh
poetry config pypi-token.pypi ...
poetry run doit run publish

# For a full release, triple check the default tasks, increment the version, rebuild documentation (twice), and publish!
poetry run doit run --continue
poetry run doit run cl_bump lock document deploy_docs publish

# For pre-releases use cl_bump_pre
poetry run doit run cl_bump_pre -p rc
poetry run doit run lock document deploy_docs publish
```

## Current Status

<!-- {cts} COVERAGE -->
| File                                         |   Statements |   Missing |   Excluded | Coverage   |
|----------------------------------------------|--------------|-----------|------------|------------|
| `game/__init__.py`                           |            2 |         0 |          0 | 100.0%     |
| `game/_example_code/11_animate_character.py` |          261 |       261 |          0 | 0.0%       |
| `game/_example_code/__init__.py`             |            0 |         0 |          0 | 100.0%     |
| `game/_example_code/line_of_sight.py`        |          119 |       119 |          0 | 0.0%       |
| `game/_example_code/pymunk_demo_top_down.py` |          163 |       163 |          0 | 0.0%       |
| `game/_example_code/sprite_rooms.py`         |          117 |       117 |          0 | 0.0%       |
| `game/core/__init__.py`                      |            1 |         1 |          0 | 0.0%       |
| `game/core/models/__init__.py`               |            1 |         1 |          0 | 0.0%       |
| `game/core/models/sprite_state.py`           |           10 |        10 |          0 | 0.0%       |
| `game/core/pressed_keys.py`                  |           30 |        30 |          0 | 0.0%       |
| `game/core/registration.py`                  |           29 |        29 |          0 | 0.0%       |
| `game/core/settings.py`                      |            9 |         9 |          0 | 0.0%       |
| `game/core/view_strategies/__init__.py`      |            0 |         0 |          0 | 100.0%     |
| `game/core/view_strategies/movement.py`      |           30 |        30 |          0 | 0.0%       |
| `game/core/views/__init__.py`                |            1 |         1 |          0 | 0.0%       |
| `game/core/views/game_sprite.py`             |           20 |        20 |          0 | 0.0%       |
| `game/core/window.py`                        |           84 |        84 |          0 | 0.0%       |
| `game/play.py`                               |           11 |        11 |          0 | 0.0%       |
| `game/tasks/__init__.py`                     |            0 |         0 |          0 | 100.0%     |
| `game/tasks/task01_player.py`                |           31 |        31 |          0 | 0.0%       |
| **Totals**                                   |          919 |       917 |          0 | 0.2%       |

Generated on: 2022-11-04
<!-- {cte} -->
