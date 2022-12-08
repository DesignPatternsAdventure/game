"""End Game Menu."""

import arcade
from arcade.gui import UIAnchorWidget, UIBoxLayout, UIFlatButton, UIManager, UITextArea
from beartype import beartype


class EndGameMenu(arcade.View):
    """Class to manage the End Game Menu."""

    # TODO: Refactor to share code with the 'PauseMenu'

    def __init__(self, game_view) -> None:  # type: ignore[no-untyped-def]
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.game_view = game_view
        self.manager = UIManager()
        self.manager.enable()  # type: ignore[no-untyped-call]
        self.v_box = UIBoxLayout()

        ui_title = UITextArea(
            text="Congrats, you won!!!", width=500, height=100, font_size=36
        )
        self.v_box.add(ui_title)
        ui_text = UITextArea(text="Thank you for playing!", height=40, font_size=18)
        self.v_box.add(ui_text.with_space_around(bottom=40))

        resume_button = UIFlatButton(text="Resume Game", width=200)
        self.v_box.add(resume_button.with_space_around(bottom=20))
        resume_button.on_click = self.on_click_resume  # type: ignore[assignment]

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

    def on_click_quit(self, event):  # type: ignore[no-untyped-def]
        arcade.exit()  # type: ignore[no-untyped-call]

    @beartype
    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)  # type: ignore[has-type]
