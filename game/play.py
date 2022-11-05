"""Play the game!

Run with `poetry run doit play`

"""

import arcade
from beartype import beartype

from .core.settings import SETTINGS
from .core.window import Window
from .tasks import task01_player


@beartype
def main() -> None:
    Window(
        code_modules=[task01_player],
        height=SETTINGS.HEIGHT,
        title='Design Patterns Adventure!',
        width=SETTINGS.WIDTH,
    )
    arcade.run()  # type: ignore[no-untyped-call]


if __name__ == '__main__':
    main()
