"""Game Map."""

from collections import OrderedDict

import arcade
from arcade.tilemap import load_tilemap
from loguru import logger


class GameMap:
    """Model the Game's Tile Map."""

    def __init__(self, state):
        self.tile_map = state.map_path
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

        # Read in the tiled tile_map
        logger.debug(f"Loading tile_map: {self.tile_map}")
        my_map = load_tilemap(self.tile_map, scaling=1, layer_options=layer_options)

        self.scene = arcade.Scene.from_tilemap(my_map)

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
                except IndexError:
                    logger.debug(f"{layer} has no objects")

                self.scene["wall_list"].extend(sprite_list)
