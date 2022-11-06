"""Track the game clock time."""

from collections import OrderedDict

import arcade
from beartype import beartype
from game.core.registration import ArcadeSpriteType
from loguru import logger
from pydantic import BaseModel


class GameMap():
    """Track repeated keys."""

    def __init__(self):
        self.map = ":assets:map.json"
        self.load()

    def draw(self):
        self.scene.draw()
        for item in self.map_layers.get("searchable", []):
            # TODO make animated
            arcade.Sprite(
                filename=":assets:shiny-stars.png",
                center_x=item.center_x,
                center_y=item.center_y,
                scale=0.8,
            ).draw()

    def load(self):
        self.map_layers = OrderedDict()

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

        # Read in the tiled map
        logger.debug(f"Loading map: {self.map}")
        my_map = arcade.tilemap.load_tilemap(
            self.map, scaling=1, layer_options=layer_options
        )

        self.scene = arcade.Scene.from_tilemap(my_map)

        # Get all the tiled sprite lists
        # Get all the tiled sprite lists
        self.map_layers = my_map.sprite_lists

        # Define the size of the map, in tiles
        self.map_size = my_map.width, my_map.height

        # Set the background color
        self.background_color = my_map.background_color

        self.properties = my_map.properties

        # Any layer with '_blocking' in it, will be a wall
        self.scene.add_sprite_list("wall_list", use_spatial_hash=True)
        for layer, sprite_list in self.map_layers.items():
            if "_blocking" in layer:
                try:
                    self.scene.remove_sprite_list_by_object(sprite_list)
                except:
                    logger.debug(f"{layer} has no objects")

                self.scene["wall_list"].extend(sprite_list)
