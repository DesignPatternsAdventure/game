"""Play the game!

Run with `poetry run doit play`

"""

import arcade
from beartype import beartype

from .core.game_view import GameView
from .core.settings import SETTINGS
from .tasks import code_modules, player_module


@beartype
def main() -> None:  # pragma: no cover
    window = arcade.Window(
        width=SETTINGS.WIDTH,
        height=SETTINGS.HEIGHT,
        title="Design Patterns Adventure!",
        center_window=True,
    )
    game_view = GameView(player_module=player_module, code_modules=code_modules)
    window.show_view(game_view)
    arcade.run()  # type: ignore[no-untyped-call]


if __name__ == "__main__":  # pragma: no cover
    main()
