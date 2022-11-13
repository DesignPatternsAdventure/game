"""Pause menu."""

import arcade
from arcade.gui import UIAnchorWidget, UIBoxLayout, UIFlatButton, UIManager


class PauseMenu(arcade.View):
    """
    Class to manage pause menu.
    """

    def __init__(self, game_view):
        super().__init__()
        arcade.set_background_color(arcade.color.ALMOND)

        self.game_view = game_view
        self.manager = UIManager()
        self.manager.enable()
        self.v_box = UIBoxLayout()

        resume_button = UIFlatButton(text="Resume Game", width=200)
        self.v_box.add(resume_button.with_space_around(bottom=20))
        resume_button.on_click = self.on_click_resume

        new_game_button = UIFlatButton(text="New Game", width=200)
        self.v_box.add(new_game_button.with_space_around(bottom=20))
        new_game_button.on_click = self.on_click_new_game

        quit_button = UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))
        quit_button.on_click = self.on_click_quit

        self.manager.add(
            UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box)
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_click_resume(self, event):
        self.window.show_view(self.game_view)

    def on_click_new_game(self, event):
        self.game_view.state.clear_state()
        self.game_view.restart()

    def on_click_quit(self, event):
        arcade.exit()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
