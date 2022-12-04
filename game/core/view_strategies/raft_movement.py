from copy import deepcopy

from arcade.sprite import Sprite
from beartype import beartype

from ..constants import RAFT_COMPONENTS, RAFT_STARTING_X, RAFT_STARTING_Y


@beartype
def check_missing_components(inventory: list[Sprite]) -> bool:
    components = deepcopy(RAFT_COMPONENTS)
    for item in inventory:
        name = item.properties["name"]
        count = item.properties["count"]
        if name in components:
            components[name] = max(components[name] - count, 0)
    num_missing_components = sum(components.values())
    return bool(num_missing_components)


@beartype
def generate_missing_components_text(inventory: list[Sprite]) -> dict:  # type: ignore[type-arg]
    expected = [f"{count} {component}" for component, count in RAFT_COMPONENTS.items()]
    actual = []
    for item in inventory:
        name = item.properties["name"]
        if name in RAFT_COMPONENTS:
            actual.append(f'{item.properties["count"]} {name}')
    conj = " and "
    return {
        "message": "Building a raft was unsuccessful",
        "notes": f"Raft requires {conj.join(expected)}. You have {conj.join(actual)}.",
    }


@beartype
def initial_board_raft(player_sprite, game_map) -> None:
    game_map.move_on_water()  # type: ignore[no-untyped-call]
    player_sprite.update_player_position(RAFT_STARTING_X, RAFT_STARTING_Y)
    if player_sprite.item:
        player_sprite.player_inventory.unequip_item()
    for item_name in RAFT_COMPONENTS:
        for _ in range(RAFT_COMPONENTS[item_name]):
            player_sprite.player_inventory.discard_item(item_name)


@beartype
def board_raft(player_sprite, game_map, raft) -> None:
    game_map.move_on_water()  # type: ignore[no-untyped-call]
    player_sprite.update_player_position(raft.center_x, raft.center_y)
    if player_sprite.item:
        player_sprite.player_inventory.unequip_item()


@beartype
def dock_raft(player_sprite, game_map, target) -> None:
    game_map.move_on_land()  # type: ignore[no-untyped-call]
    player_sprite.update_player_position(target.center_x, target.center_y)
