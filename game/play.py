"""Play the game!

Run with `poetry run doit play`

"""

import arcade
from beartype import beartype

from .core.window import Window


@beartype
def main() -> None:
    Window(
        width=500,
        height=500,
        title='Experimenting with Module Reload and Dependency Inversion',
    )
    arcade.run()  # type: ignore[no-untyped-call]


if __name__ == '__main__':
    main()
