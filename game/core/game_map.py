"""Game Map."""

from collections import OrderedDict

import arcade
from arcade.sprite import Sprite
from arcade.tilemap import load_tilemap
from beartype import beartype
from loguru import logger

from .game_clock import GameClock
from .game_state import GameState
from .views.animated_sprite import AnimatedSprite


class GameMap:
    """Model the Game's Tile Map."""

    @beartype
    def __init__(self, state: GameState, game_clock: GameClock) -> None:
        self.state = state
        self.game_clock = game_clock
        self.load()

        self.sparkles = arcade.SpriteList()
        for item in self.map_layers.get("searchable", []):
            self.sparkles.append(
                AnimatedSprite(
                    self.game_clock,
                    "sparkle",
                    item.center_x,
                    item.center_y,
                    item,
                    scale=0.8,
                )
            )

    @beartype
    def remove_sprite(self, removed_sprite: Sprite, searchable: bool) -> None:
        removed_sprite.properties["removed"] = True
        removed_sprite.remove_from_sprite_lists()
        if dropped_item := self.state.sync_removed_sprite(removed_sprite, searchable):
            self.sparkles.append(
                AnimatedSprite(
                    self.game_clock,
                    "sparkle",
                    dropped_item.center_x,
                    dropped_item.center_y,
                    dropped_item,
                    scale=0.8,
                )
            )

    @beartype
    def draw(self) -> None:
        self.scene.draw()
        self.sparkles.draw()  # type: ignore[no-untyped-call]

    @beartype
    def on_update(self) -> None:
        self.sparkles.on_update()

    @beartype
    def load(self) -> None:
        self.map_layers = OrderedDict()  # type: ignore[var-annotated]

        # List of blocking sprites
        layer_options = {
            "trees_blocking": {
                "use_spatial_hash": True,
            },
            "misc_blocking": {
                "use_spatial_hash": True,
            },
            "bridges": {
                "use_spatial_hash": True,
            },
            "water_blocking": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled tile_path
        tile_path = self.state.map_path
        logger.debug(f"Loading tile_path: {tile_path}")
        tile_map = load_tilemap(tile_path, scaling=1, layer_options=layer_options)

        self.scene = arcade.Scene.from_tilemap(tile_map)

        # Get all the tiled sprite lists
        self.map_layers = tile_map.sprite_lists  # type: ignore[assignment]

        # Define the size of the map, in tiles
        self.map_size = (tile_map.width, tile_map.height)

        # Set the background color
        self.background_color = tile_map.background_color

        self.properties = tile_map.properties

        self.scene.add_sprite_list("wall_list", use_spatial_hash=True)

        if self.state.inverse_movement:
            self.move_on_water()
        else:
            self.move_on_land()

    def move_on_land(self) -> None:
        """Any layer with '_blocking' will be a wall."""
        self.scene["wall_list"].clear()
        for layer, sprite_list in self.map_layers.items():
            if "_blocking" in layer or "coast" in layer:
                self.scene["wall_list"].extend(sprite_list)

    @beartype
    def move_on_water(self) -> None:
        """Any layer not with 'water' or 'coast' will be a wall."""
        self.scene["wall_list"].clear()
        for layer, sprite_list in self.map_layers.items():
            if "water" not in layer and "coast" not in layer:
                self.scene["wall_list"].extend(sprite_list)

    def closest_land_coordinates(self, sprite: Sprite) -> Sprite:
        """Get closest land coordinates when on water and trying to dock."""
        return arcade.get_closest_sprite(sprite, self.scene["wall_list"])
