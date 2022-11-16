"""Constant values for the game."""

from pathlib import Path

import arcade.key

# TODO: Merge constants with SETTINGS when necessary to override

SCREEN_WIDTH = 1280  # FYI: Set to zero to scale based on display size
SCREEN_HEIGHT = 720  # FYI: Set to zero to scale based on display size
TILE_SCALING = 1.0
SPRITE_SIZE = 32

# How fast does the player move
MOVEMENT_SPEED = 3

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
HORIZONTAL_MARGIN = 650
VERTICAL_MARGIN = 300

# What map, and what position we start at
MAP = Path("game/assets/maps/map.json")
MAP_SIZE = 4000
STARTING_X = 3600
STARTING_Y = 600

# Key mappings
NUMERIC_KEY_MAPPING = {
    getattr(arcade.key, f"KEY_{idx}"): idx for idx in range(1, 10)
} | {arcade.key.KEY_0: 10}
KEYS_UP = {arcade.key.UP, arcade.key.W}
KEYS_DOWN = {arcade.key.DOWN, arcade.key.S}
KEYS_LEFT = {arcade.key.LEFT, arcade.key.A}
KEYS_RIGHT = {arcade.key.RIGHT, arcade.key.D}
INVENTORY = [arcade.key.I]
SEARCH = [arcade.key.E]

# How fast does the camera pan to the user
CAMERA_SPEED = 0.1

SAVE_FILE_DIR = MAP.parent
PLAYER_SAVE_FILE = SAVE_FILE_DIR / "player_save_file"
MAP_SAVE_FILE = SAVE_FILE_DIR / "map_save_file.json"

ITEM_CONFIG = {
    "Pickaxe": {
        "animation": {
            "frames": 80,
            "speed": 2,
            "shift_x": 0,
            "shift_y": 0.2,
            "reversible": True,
            "reverse_frame": 20,
        }
    }
}

RAFT_COMPONENTS = {"Rope": 1, "Wood": 2}
