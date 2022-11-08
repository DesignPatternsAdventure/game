"""Generic Base Class for Sprites."""

import arcade
from beartype import beartype

from ..models import EntityAttr, SpriteState


class GameSprite(arcade.Sprite):
    """Generic Base Class for Sprites."""

    @beartype
    def __init__(self, attr: EntityAttr, state: SpriteState) -> None:
        super().__init__(state.sprite_resource, state.scale)
        self.attr = attr
        self.state = state
        self.sync_with_state()

    @beartype
    def sync_with_state(self) -> None:
        """Sync the Sprite with the state."""
        for attr in ("center_x", "center_y", "angle"):
            setattr(self, attr, getattr(self.state, attr))

        # Update the rotation if necessary
        point = [self.center_x, self.center_y]
        self.position = arcade.rotate_point(
            self.center_x, self.center_y, point[0], point[1], self.angle
        )

    @beartype
    def move(
        self, d_x: int | float, d_y: int | float, angle: float | None = None
    ) -> None:
        """Update the sprite position and state."""
        self.state.center_x = int(self.state.center_x + d_x)
        self.state.center_y = int(self.state.center_y + d_y)
        self.state.angle = angle or self.state.angle
        self.sync_with_state()
