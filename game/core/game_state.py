"""Game state."""

import json
import pickle
from pathlib import Path
from uuid import uuid4

import arcade
from arcade.sprite import Sprite
from beartype import beartype
from loguru import logger

from .constants import DEFAULT_PLAYER_DATA, MAP, MAP_SAVE_FILE, PLAYER_SAVE_FILE
from .views.vehicle_sprite import VehicleSprite, VehicleType


class GameState:
    """Class to manage game state."""

    def __init__(self):  # type: ignore[no-untyped-def]
        # Game state
        self.map_path = self.get_map_path()
        self._tile_map = self.get_map_data()
        self._searchable_index = self.get_layer_index("searchable")
        self._tree_index = self.get_layer_index("interactables_blocking")

        # Player state
        try:
            self.player_data = self.get_player_data()
            self.set_player_data()
        except Exception:
            logger.exception(f"Failed to load player state, using default data...")
            self.player_data = DEFAULT_PLAYER_DATA
            self.set_player_data()

    @beartype
    def get_map_path(self) -> Path:
        if MAP_SAVE_FILE.is_file():
            return MAP_SAVE_FILE
        return MAP

    @beartype
    def get_map_data(self) -> dict:  # type: ignore[type-arg]
        if MAP_SAVE_FILE.is_file():
            with open(MAP_SAVE_FILE) as _f:
                return json.load(_f)  # type: ignore[no-any-return]
        with open(MAP) as _f:
            return json.load(_f)  # type: ignore[no-any-return]

    @beartype
    def get_layer_index(self, name) -> int | None:  # type: ignore[no-untyped-def]
        for idx, layer in enumerate(self._tile_map["layers"]):
            if layer["name"] == name:
                return idx
        return None

    @beartype
    def set_player_data(self) -> None:
        self.center_x = self.player_data["x"]
        self.center_y = self.player_data["y"]
        self.inventory = self.load_inventory(self.player_data["inventory"])
        self.item = self.load_item(self.player_data["item"])
        self.vehicle = None
        if self.player_data["vehicle_type"]:
            self.vehicle = self.load_vehicle(self.player_data)
            self.vehicle_x = self.player_data["vehicle_x"]
            self.vehicle_y = self.player_data["vehicle_y"]
            self.vehicle_docked = self.player_data["vehicle_docked"]
        # Move on land or move on water
        self.inverse_movement = (
            True if self.vehicle and not self.vehicle_docked else False
        )

    @beartype
    def get_player_data(self) -> dict:  # type: ignore[type-arg]
        if PLAYER_SAVE_FILE.is_file():
            with open(PLAYER_SAVE_FILE, "rb") as _f:
                return pickle.load(_f)  # type: ignore[no-any-return]
        else:
            return DEFAULT_PLAYER_DATA

    @beartype
    def save_map_data(self) -> None:
        with open(MAP_SAVE_FILE, "w") as _f:
            json.dump(self._tile_map, _f)

    @beartype
    def save_player_data(self, player, vehicle) -> None:  # type: ignore[no-untyped-def]
        self.center_x = player.center_x
        self.center_y = player.center_y
        self.item = player.item
        self.vehicle = vehicle
        self.vehicle_x = self.vehicle.center_x if self.vehicle else None
        self.vehicle_y = self.vehicle.center_y if self.vehicle else None
        self.vehicle_docked = self.vehicle.docked if self.vehicle else False
        data = {
            "x": self.center_x,
            "y": self.center_y,
            "inventory": self.compress_inventory(self.inventory),  # type: ignore[arg-type]
            "item": self.compress_item(self.item),
            "vehicle_type": self.vehicle.type if self.vehicle else None,
            "vehicle_x": self.vehicle_x,
            "vehicle_y": self.vehicle_y,
            "vehicle_docked": self.vehicle_docked,
        }
        with open(PLAYER_SAVE_FILE, "wb") as _f:
            pickle.dump(data, _f)

    @beartype
    def sync_removed_sprite(
        self, removed_sprite: Sprite, searchable: bool
    ) -> Sprite | None:
        sprite_id = removed_sprite.properties["id"]
        index = self._searchable_index if searchable else self._tree_index
        layer = self._tile_map["layers"][index]

        dropped_sprite = None

        if obj_to_remove := next(
            (
                obj
                for obj in layer["objects"]
                for prop in obj["properties"]
                if prop["name"] == "id" and prop["value"] == sprite_id
            ),
            None,
        ):
            self._tile_map["layers"][index]["objects"].remove(obj_to_remove)
            if item_drop := removed_sprite.properties.get("drop"):
                dropped_sprite = arcade.Sprite(f":assets:{item_drop}.png")
                dropped_sprite.properties = {"name": item_drop, "id": str(uuid4())}
                dropped_sprite.center_x = removed_sprite.center_x
                dropped_sprite.center_y = removed_sprite.center_y
                # Best guess at unique IDs
                new_gid = obj_to_remove["gid"] + 10_000
                new_obj = {
                    "id": obj_to_remove["id"] + 1_000,
                    "gid": new_gid,
                    "height": dropped_sprite.height,
                    "name": "",
                    "properties": [
                        {"name": key, "type": "string", "value": value}
                        for key, value in dropped_sprite.properties.items()
                    ],
                    "rotation": 0,
                    "visible": True,
                    "width": dropped_sprite.width,
                    "x": obj_to_remove["x"],
                    "y": obj_to_remove["y"],
                }
                new_index = self._searchable_index
                self._tile_map["layers"][new_index]["objects"].append(new_obj)
                self._tile_map["tilesets"].append(
                    {"firstgid": new_gid, "source": f"{item_drop}.json"}
                )

            self.save_map_data()
        return dropped_sprite

    @beartype
    def compress_item(self, item: Sprite | None) -> dict | None:  # type: ignore[type-arg]
        if not item:
            return None
        compressed_item = {
            "name": item.properties["name"],
            "count": item.properties["count"],
        }
        try:
            compressed_item["filename"] = item.filename
        except Exception:  # pylint: disable=broad-except
            compressed_item |= {
                "texture": item.texture.name,
                "image": item.texture.image,
            }
        if "equippable" in item.properties:
            compressed_item["equippable"] = True
        return compressed_item

    @beartype
    def compress_inventory(self, inventory: list[Sprite | None]) -> list[dict]:  # type: ignore[type-arg]
        return [self.compress_item(item) for item in inventory if item]  # type: ignore[misc]

    @beartype
    def load_item(self, item: dict | None) -> Sprite | None:  # type: ignore[type-arg]
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
    def load_inventory(self, inventory: list[dict | None]) -> list[Sprite]:  # type: ignore[type-arg]
        return [self.load_item(item) for item in inventory if item]  # type: ignore[misc]

    @beartype
    def load_vehicle(self, data: dict) -> VehicleSprite | None:
        if data["vehicle_type"] == VehicleType.RAFT:
            return VehicleSprite(  # type: ignore[assignment]
                ":assets:raft.png", data["vehicle_x"], data["vehicle_y"]
            )
        else:
            # potentially add vehicles in the future
            pass


@beartype
def remove_saved_data() -> None:
    """Reset the map state, which is also used in `doit reset_map`."""
    MAP_SAVE_FILE.unlink(missing_ok=True)
    PLAYER_SAVE_FILE.unlink(missing_ok=True)
