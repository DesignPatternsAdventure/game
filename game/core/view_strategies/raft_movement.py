from copy import deepcopy

from arcade.sprite import Sprite
from beartype import beartype

from ..constants import RAFT_COMPONENTS


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
def generate_missing_components_text(inventory: list[Sprite]) -> dict:
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
