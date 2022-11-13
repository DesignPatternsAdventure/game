import copy

RAFT_COMPONENTS = {"Rope": 1, "Wood": 2}

# TODO make into a class


def check_missing_components(inventory):
    components = copy.deepcopy(RAFT_COMPONENTS)
    for item in inventory:
        name = item.properties["name"]
        count = item.properties["count"]
        if name in components:
            components[name] = max(components[name] - count, 0)
    num_missing_components = sum(components.values())
    return bool(num_missing_components)


def generate_missing_components_text(inventory):
    expected = []
    actual = []
    conj = " and "
    for component, count in RAFT_COMPONENTS.items():
        expected.append(f"{count} {component}")
    for item in inventory:
        name = item.properties["name"]
        if name in RAFT_COMPONENTS:
            actual.append(f"{item.properties['count']} {name}")
    return {
        "message": "You attemped to build a raft and was unsuccessful",
        "notes": f"Raft requires {conj.join(expected)}. You have {conj.join(actual)}.",
    }
