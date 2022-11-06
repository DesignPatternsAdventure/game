from arcade import key
from freezegun import freeze_time

from game.core.game_view import GameView
from game.tasks import task01_player

from . import stub_test_task


@freeze_time('2000', auto_tick_seconds=15)  # Shift time for on_key_hold
def test_game_view(window):
    """Smoke test the GameView."""
    # Create GameView with tasks that will register handlers for every type
    view = GameView(code_modules=[task01_player, stub_test_task])
    window.show_view(view)
    view.on_draw()
    for event in ('on_key_press', 'on_key_release'):
        for card_key in (key.DOWN, key.D, key.W, key.LEFT):
            window.dispatch_event(event, card_key, 0)
        window.dispatch_event(event, key.R, key.MOD_COMMAND)
        window.dispatch_event('on_update', 0.123)
    window.dispatch_event('on_mouse_motion', 0, 0, 123.0, -123.0)
    window.dispatch_pending_events()

    window.hide_view()
