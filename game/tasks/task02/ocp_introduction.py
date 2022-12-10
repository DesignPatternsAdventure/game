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

from beartype import beartype
from loguru import logger

"""

As a quick aside, '@beartype' is a runtime type checker!

When used as a decorator, it will check that each argument matches the indicated type

```py
@beartype
def run(arg_1: int, arg_2: str | None) -> str:
    print(f"Received {arg_1} & {arg_2}")
    return arg_2
```

Which when run with different arguments will succeed or fail in different ways:

```sh
> run(1, "yes")
Received 1 & yes
'yes'
>
> run("1", None)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<@beartype(__main__.run) at 0x10e55f880>", line 22, in run
beartype.roar.BeartypeCallHintParamViolation: @beartyped __main__.run() parameter arg_1='1' violates type hint <class 'int'>, as str '1' not instance of int.
>
> run(1, None)
Received 1 & None
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<@beartype(__main__.run) at 0x10e55f880>", line 59, in run
beartype.roar.BeartypeCallHintReturnViolation: @beartyped __main__.run() return "None" violates type hint <class 'str'>, as <class "builtins.NoneType"> "None" not instance of str.
```

With beartype, Python typing is much more bearable. Back to the introduction!

"""

"""

When writing code, extending by adding new code is much easier for maintenance when
compared to a design that requires modification.

In the below is an example, we are creating a class to manage the different sprites, but
to add new sprites to this hypothetical class, one would need to *modify* internal code
that should be **closed**

"""

USER_INVENTORY = ["Pickaxe", "Rope", "Wood"]


@beartype
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


@beartype
def build_raft_action(inventory: list[str]) -> list[str]:
    if "Wood" in inventory and "Rope" in inventory:
        logger.info("Building the raft!")
        return [item for item in inventory if item not in ("Wood", "Rope")]
    logger.warning("Building a raft isn't possible")
    return inventory


@beartype
def equip_action(inventory: list[str]) -> list[str]:
    for portable_item in ("Pickaxe",):
        if portable_item in inventory:
            logger.info(f"Equipping {portable_item}")
            return [item for item in inventory if item != portable_item]

    logger.error(f"No portable items in {inventory}")
    return inventory


@beartype
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


@beartype
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
