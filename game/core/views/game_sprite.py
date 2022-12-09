"""Generic Base Class for Sprites."""

import arcade
from beartype import beartype

from ..constants import SPRITE_SIZE
from ..game_clock import GameClock
from ..models import EntityAttr, SpriteState
from ..models.sprite_state import Direction


class GameSprite(arcade.Sprite):
    """Generic Base Class for Sprites."""

    @beartype
    def __init__(self, attr: EntityAttr, state: SpriteState) -> None:
        super().__init__()
        self.change_x, self.change_y = 0, 0
        self.attr = attr
        self.state = state.load_state()
        self._textures = arcade.load_spritesheet(
            state.sprite_resource,
            sprite_width=SPRITE_SIZE,
            sprite_height=SPRITE_SIZE,
            columns=3,
            count=12,
        )
        self.texture = self._textures[self.state.cur_texture_index]
        self.sync_with_state()

    @beartype
    def sync_with_state(self) -> None:
        """Sync the Sprite with the state."""
        self.state.save_state()
        for attr in ("center_x", "center_y", "angle"):
            setattr(self, attr, getattr(self.state, attr))

        # Update the rotation if necessary
        point = [self.center_x, self.center_y]
        self.position = arcade.rotate_point(
            self.center_x, self.center_y, point[0], point[1], self.angle
        )

    @beartype
    def move(
        self,
        d_x: int | float,
        d_y: int | float,
        angle: float | None = None,
    ) -> None:
        """Update the sprite position and state."""
        self.state.center_x = int(self.state.center_x + d_x)
        self.state.center_y = int(self.state.center_y + d_y)
        self.state.angle = angle or self.state.angle
        self.sync_with_state()

    @beartype
    def on_update(self, game_clock: GameClock) -> None:
        """Calculate speed based on the keys pressed."""
        self.state.on_update(game_clock.delta_time)
        if not self.change_x and not self.change_y:
            return
        self.move(self.change_x, self.change_y)

        slope = self.change_y / (self.change_x + 0.0001)
        if abs(slope) < 0.8:
            self.state.direction = (
                Direction.RIGHT if self.change_x > 0 else Direction.LEFT
            )
        else:
            self.state.direction = Direction.UP if self.change_y > 0 else Direction.DOWN

        self.texture = self._textures[self.state.cur_texture_index]
