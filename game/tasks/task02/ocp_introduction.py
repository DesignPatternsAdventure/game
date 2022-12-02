"""Task 02: Inventory.

> (O) **Open-Close Principle**
>
> Open for extension, not modification.
> Adding new features should not require changing the base class

```sh
# FYI: if you want to test this code, run with:
python -m game.tasks.task02.ocp_introduction
```

"""

from collections.abc import Callable

from loguru import logger

"""

When writing code, extending by adding new code is much easier for maintenance when
compared to a design that requires modification.

In the below is an example, we are creating a class to manage the different sprites, but
to add new sprites to this hypothetical class, one would need to *modify* internal code
that should be **closed**

"""

USER_INVENTORY = ["Pickaxe", "Rope", "Wood"]


def use_item(action: str, inventory: list[str]) -> list[str]:  # noqa: R701
    if action == "Build Raft":
        if "Wood" in inventory and "Rope" in inventory:
            logger.info("Building the raft!")
            return [item for item in inventory if item not in ("Wood", "Rope")]
        logger.warning("Building a raft isn't possible")
    elif action == "Equip":
        for portable_item in ("Pickaxe",):
            if portable_item in inventory:
                logger.info(f"Equipping {portable_item}")
                return [item for item in inventory if item != portable_item]
        logger.error(f"No portable items in {inventory}")
    else:
        logger.error(f"Unknown action: {action}")
    return inventory


if __name__ == "__main__":
    logger.info("Running `use_item`")
    use_item("Build Raft", USER_INVENTORY)
    use_item("Equip", USER_INVENTORY)
    use_item("Throw", USER_INVENTORY)  # Not implemented!


"""

To improve the above code, we could refactor `use_item` so that new actions
could be implemented without requiring changes to the `use_item` function.

One way to accomplish this goal is to make each action a function that
encapsulates the code that is prone to change.

"""


def build_raft_action(inventory: list[str]) -> list[str]:
    if "Wood" in inventory and "Rope" in inventory:
        logger.info("Building the raft!")
        return [item for item in inventory if item not in ("Wood", "Rope")]
    logger.warning("Building a raft isn't possible")
    return inventory


def equip_action(inventory: list[str]) -> list[str]:
    for portable_item in ("Pickaxe",):
        if portable_item in inventory:
            logger.info(f"Equipping {portable_item}")
            return [item for item in inventory if item != portable_item]

    logger.error(f"No portable items in {inventory}")
    return inventory


def use_item_by_action(
    do_action: Callable[[list[str]], list[str]],
    inventory: list[str],
) -> list[str]:
    return do_action(inventory)


"""

Now, we have defined the actions as interchangeable functions so that
`use_item_by_action` is closed for modification, but open for extension

With this refactoring, we can implement the `throw_action`!

"""


def throw_action(inventory: list[str]) -> list[str]:
    if "Rope" in inventory:
        logger.info("Throwing a rope!")
        return [item for item in inventory if item != "Rope"]

    logger.error(f"No portable items in {inventory}")
    return inventory


if __name__ == "__main__":
    logger.info("Running OCP-compliant `use_item_by_action`!")
    use_item_by_action(build_raft_action, USER_INVENTORY)
    use_item_by_action(equip_action, USER_INVENTORY)
    use_item_by_action(throw_action, USER_INVENTORY)


"""

If you would like to learn more about the Open-Close Principle, you can take a look at:

- https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle
- https://phoenixnap.com/blog/solid-principles
- https://ezzeddinabdullah.com/post/solid-principles-ocp-py/
- https://www.reddit.com/r/Python/comments/rz0enw/how_to_write_clean_code_in_python_with_solid/
- https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design

"""
