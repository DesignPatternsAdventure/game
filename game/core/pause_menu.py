"""Pause menu."""

import arcade
from arcade.gui import UIAnchorWidget, UIBoxLayout, UIFlatButton, UIManager
from beartype import beartype

from . import remove_saved_data


class PauseMenu(arcade.View):
    """Class to manage pause menu."""

    def __init__(self, game_view) -> None:  # type: ignore[no-untyped-def]
        super().__init__()
        arcade.set_background_color(arcade.color.ALMOND)

        self.game_view = game_view
        self.manager = UIManager()
        self.manager.enable()  # type: ignore[no-untyped-call]
        self.v_box = UIBoxLayout()

        resume_button = UIFlatButton(text="Resume Game", width=200)
        self.v_box.add(resume_button.with_space_around(bottom=20))
        resume_button.on_click = self.on_click_resume  # type: ignore[assignment]

        new_game_button = UIFlatButton(text="New Game", width=200)
        self.v_box.add(new_game_button.with_space_around(bottom=20))
        new_game_button.on_click = self.on_click_new_game  # type: ignore[assignment]

        quit_button = UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))
        quit_button.on_click = self.on_click_quit  # type: ignore[assignment]

        self.manager.add(
            UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box)
        )

    def on_draw(self):  # type: ignore[no-untyped-def]
        self.clear()
        self.manager.draw()  # type: ignore[no-untyped-call]

    def on_click_resume(self, event):  # type: ignore[no-untyped-def]
        self.window.show_view(self.game_view)  # type: ignore[has-type]

    def on_click_new_game(self, event):  # type: ignore[no-untyped-def]
        remove_saved_data()
        self.game_view.restart()

    def on_click_quit(self, event):  # type: ignore[no-untyped-def]
        arcade.exit()  # type: ignore[no-untyped-call]

    @beartype
    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)  # type: ignore[has-type]
