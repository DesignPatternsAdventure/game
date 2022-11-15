"""Game state."""

import json
import pickle

import arcade

from .constants import MAP, MAP_SAVE_FILE, PLAYER_SAVE_FILE, STARTING_X, STARTING_Y


class GameState:
    """Class to manage game state."""

    def __init__(self):
        # Game state
        self.map_path = self.get_map_path()
        self.tile_map = self.get_map_data()
        self.searchable_index = self.get_layer_index("searchable")
        self.tree_index = self.get_layer_index("interactables_blocking")

        # Player state
        self.player_data = self.get_player_data()
        self.center_x = self.player_data["x"]
        self.center_y = self.player_data["y"]
        self.inventory = self.load_inventory(self.player_data["inventory"])
        self.item = self.load_item(self.player_data["item"])

    def get_map_path(self):
        if MAP_SAVE_FILE.is_file():
            return MAP_SAVE_FILE
        return MAP

    def get_map_data(self):
        if MAP_SAVE_FILE.is_file():
            with open(MAP_SAVE_FILE) as f:
                return json.load(f)
        with open(MAP) as f:
            return json.load(f)

    def get_layer_index(self, name):
        for idx, layer in enumerate(self.tile_map["layers"]):
            if layer["name"] == name:
                return idx
        return None

    def get_player_data(self):
        if PLAYER_SAVE_FILE.is_file():
            with open(PLAYER_SAVE_FILE, "rb") as f:
                return pickle.load(f)
        return {"x": STARTING_X, "y": STARTING_Y, "inventory": [], "item": None}

    def save_map_data(self):
        with open(MAP_SAVE_FILE, "w") as f:
            json.dump(self.tile_map, f)
        return

    def save_player_data(self, player):
        self.center_x = player.center_x
        self.center_y = player.center_y
        self.inventory = player.inventory
        self.item = player.item
        data = {
            "x": self.center_x,
            "y": self.center_y,
            "inventory": self.compress_inventory(self.inventory),
            "item": self.compress_item(self.item),
        }
        with open(PLAYER_SAVE_FILE, "wb") as f:
            pickle.dump(data, f)

    def remove_sprite_from_map(self, sprite, searchable=False):
        sprite_id = sprite.properties["id"]
        index = self.searchable_index if searchable else self.tree_index
        layer_copy = self.tile_map["layers"][index]

        obj_to_remove = None
        for obj in layer_copy["objects"]:
            for prop in obj["properties"]:
                if prop["name"] == "id" and prop["value"] == sprite_id:
                    obj_to_remove = obj
                    break
        if obj_to_remove:
            layer_copy["objects"].remove(obj_to_remove)
            self.tile_map["layers"][index] = layer_copy

        sprite.remove_from_sprite_lists()
        self.save_map_data()

    def compress_item(self, item):
        if not item:
            return None
        compressed_item = {
            "name": item.properties["name"],
            "count": item.properties["count"],
        }
        try:
            compressed_item.update({"filename": item.filename})
        except Exception:
            compressed_item.update(
                {"texture": item.texture.name, "image": item.texture.image}
            )
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
        if "filename" in item:
            sprite = arcade.Sprite(filename=item["filename"])
        else:
            texture = arcade.Texture(name=item["texture"], image=item["image"])
            sprite = arcade.Sprite(texture=texture)
        sprite.properties = {"name": item["name"], "count": item["count"]}
        if "equippable" in item:
            sprite.properties["equippable"] = True
        return sprite

    def load_inventory(self, inventory):
        loaded = []
        for item in inventory:
            sprite = self.load_item(item)
            loaded.append(sprite)
        return loaded

    def clear_state(self):
        MAP_SAVE_FILE.unlink(missing_ok=True)
        PLAYER_SAVE_FILE.unlink(missing_ok=True)
