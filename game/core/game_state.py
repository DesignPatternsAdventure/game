"""Game state."""

import json
import pickle
from pathlib import Path

import arcade
from arcade.sprite import Sprite
from beartype import beartype

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
        # FIXME: Delegate saving/loading to the player_inventory..
        self.inventory = self.load_inventory(self.player_data["inventory"])
        self.item = self.load_item(self.player_data["item"])

    @beartype
    def get_map_path(self) -> Path:
        if MAP_SAVE_FILE.is_file():
            return MAP_SAVE_FILE
        return MAP

    @beartype
    def get_map_data(self) -> dict:
        if MAP_SAVE_FILE.is_file():
            with open(MAP_SAVE_FILE) as _f:
                return json.load(_f)
        with open(MAP) as _f:
            return json.load(_f)

    @beartype
    def get_layer_index(self, name) -> int | None:
        for idx, layer in enumerate(self.tile_map["layers"]):
            if layer["name"] == name:
                return idx
        return None

    @beartype
    def get_player_data(self) -> dict:
        if PLAYER_SAVE_FILE.is_file():
            with open(PLAYER_SAVE_FILE, "rb") as _f:
                return pickle.load(_f)
        return {"x": STARTING_X, "y": STARTING_Y, "inventory": [], "item": None}

    @beartype
    def save_map_data(self) -> None:
        with open(MAP_SAVE_FILE, "w") as _f:
            json.dump(self.tile_map, _f)

    @beartype
    def save_player_data(self, player) -> None:
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
        with open(PLAYER_SAVE_FILE, "wb") as _f:
            pickle.dump(data, _f)

    @beartype
    def remove_sprite_from_map(self, sprite, searchable: bool = False) -> None:
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

    @beartype
    def compress_item(self, item: Sprite | None) -> dict | None:
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

    @beartype
    def compress_inventory(self, inventory: list[Sprite | None]) -> list[dict]:
        return [self.compress_item(item) for item in inventory if item]

    @beartype
    def load_item(self, item: dict | None) -> Sprite | None:
        if not item:
            return None

        if "filename" in item:
            sprite = arcade.Sprite(filename=item["filename"])
        else:
            texture = arcade.Texture(name=item["texture"], image=item["image"])
            sprite = arcade.Sprite(texture=texture)
        sprite.properties = {"name": item["name"], "count": item["count"]}
        if "equippable" in item:
            sprite.properties["equippable"] = True
        return sprite

    @beartype
    def load_inventory(self, inventory: list[dict | None]) -> list[Sprite]:
        return [self.load_item(item) for item in inventory if item]


@beartype
def remove_saved_data() -> None:
    """Reset the map state, which is also used in `doit reset_map`."""
    MAP_SAVE_FILE.unlink(missing_ok=True)
    PLAYER_SAVE_FILE.unlink(missing_ok=True)
