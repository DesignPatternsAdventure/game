"""Game state."""

import pickle
from pathlib import Path

import arcade
import json

from .constants import MAP, MAP_SAVE_FILE, PLAYER_SAVE_FILE, SAVE_FILE_DIR, STARTING_X, STARTING_Y


class GameState:
    """
    Class to manage game state.
    """

    def __init__(self):
        Path(SAVE_FILE_DIR).mkdir(exist_ok=True)

        # Game state
        self.map_path = self.get_map_path()
        self.map = self.get_map_data()

        # Player state
        self.player_data = self.get_player_data()
        self.center_x = self.player_data["x"]
        self.center_y = self.player_data["y"]
        self.inventory = self.load_inventory(self.player_data["inventory"])
        self.item = self.load_item(self.player_data["item"])

    def get_map_path(self):
        # TODO in progress
        # path = Path(MAP_SAVE_FILE)
        # if path.is_file():
        #     return path
        # print("can't find map")
        return MAP

    def get_map_data(self):
        path = Path(MAP_SAVE_FILE)
        if path.is_file():
            with open(MAP_SAVE_FILE) as f:
                return json.load(f)
        with open(MAP) as f:
            return json.load(f)

    def get_player_data(self):
        path = Path(PLAYER_SAVE_FILE)
        if path.is_file():
            with open(PLAYER_SAVE_FILE, 'rb') as f:
                return pickle.load(f)
        return {
            'x': STARTING_X,
            'y': STARTING_Y,
            'inventory': [],
            'item': None
        }

    def save_map_data(self):
        with open(MAP_SAVE_FILE, 'w') as f:
            json.dump(self.map, f)
        return

    def save_player_data(self, player):
        self.center_x = player.center_x
        self.center_y = player.center_y
        self.inventory = player.inventory
        self.item = player.item
        data = {
            'x': self.center_x,
            'y': self.center_y,
            'inventory': self.compress_inventory(self.inventory),
            'item': self.compress_item(self.item)
        }
        with open(PLAYER_SAVE_FILE, 'wb') as f:
            pickle.dump(data, f)

    def remove_sprite_from_map(self, sprite):
        # TODO make this robust
        sprite.remove_from_sprite_lists()
        self.map['layers'][4]['objects'] = []
        self.save_map_data()

    def compress_item(self, item):
        if not item:
            return None
        compressed_item = {
            'item': item.properties['item'],
            'count': item.properties['count']
        }
        try:
            compressed_item.update({
                'filename': item.filename
            })
        except:
            compressed_item.update({
                'texture': item.texture.name,
                'image': item.texture.image
            })
        if "equippable" in item.properties:
            compressed_item["equippable"] = True
        return compressed_item

    def compress_inventory(self, inventory):
        compressed = []
        for item in inventory:
            compressed_item = self.compress_item(item)
            compressed.append(compressed_item)
        return compressed

    def load_item(self, item):
        if not item:
            return None
        sprite = None
        if 'filename' in item:
            sprite = arcade.Sprite(filename=item['filename'])
        else:
            texture = arcade.Texture(
                name=item['texture'], image=item['image'])
            sprite = arcade.Sprite(texture=texture)
        sprite.properties = {
            'item': item['item'],
            'count': item['count']
        }
        if "equippable" in item:
            sprite.properties["equippable"] = True
        return sprite

    def load_inventory(self, inventory):
        loaded = []
        for item in inventory:
            sprite = self.load_item(item)
            loaded.append(sprite)
        return loaded