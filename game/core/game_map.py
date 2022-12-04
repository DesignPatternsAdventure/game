"""Game Map."""

from collections import OrderedDict

import arcade
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
        self.tile_map = state.map_path
        self.load()  # type: ignore[no-untyped-call]

        self.sparkles = arcade.SpriteList()
        for item in self.map_layers.get("searchable", []):
            self.sparkles.append(
                AnimatedSprite(
                    game_clock, "sparkle", item.center_x, item.center_y, item, 0.8
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

        # Read in the tiled tile_map
        logger.debug(f"Loading tile_map: {self.tile_map}")
        my_map = load_tilemap(self.tile_map, scaling=1, layer_options=layer_options)

        self.scene = arcade.Scene.from_tilemap(my_map)

        # Get all the tiled sprite lists
        self.map_layers = my_map.sprite_lists  # type: ignore[assignment]

        # Define the size of the map, in tiles
        self.map_size = my_map.width, my_map.height

        # Set the background color
        self.background_color = my_map.background_color

        self.properties = my_map.properties

        # Any layer with '_blocking' in it, will be a wall
        self.scene.add_sprite_list("wall_list", use_spatial_hash=True)
        for layer, sprite_list in self.map_layers.items():
            if "_blocking" in layer or "coast" in layer:
                self.scene["wall_list"].extend(sprite_list)

    @beartype
    def move_on_water(self) -> None:
        self.scene["wall_list"].clear()
        for layer, sprite_list in self.map_layers.items():
            if "water" not in layer and "coast" not in layer:
                self.scene["wall_list"].extend(sprite_list)
