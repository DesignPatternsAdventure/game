"""Generic Sprite State."""

from typing import Literal

from pydantic import BaseModel


class SpriteState(BaseModel):
    """Sprite Model."""

    # PLANNED: Consider extending: https://api.arcade.academy/en/stable/api/sprites.html#arcade.Sprite

    angle: float = 0
    center_x: int
    center_y: int
    hit_box_algorithm: Literal['None', 'Simple', 'Detailed'] = 'None'
    scale: float = 1.0
    sprite_resource: str
    step_size: int | None = 5
