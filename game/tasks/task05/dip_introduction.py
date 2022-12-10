"""Task 05: The New Island.

The fifth task will be to apply the "D" of the S.O.L.I.D design principles to landing on the new island!

> (D) **Dependency Inversion Principle**
>
> Depend upon abstract interfaces and not concrete implementations

```sh
# FYI: if you want to test this code, run with:
python -m game.tasks.task05.dip_introduction
```

"""

import itertools

"""

Below we have a 'DiagonalCyclingSprite' where 'render_non_player_sprite' must
provide a list of steps based on the implementation of 'itertools.cycle' which
restarts from the beginning rather going back in reverse.

"""

NUM_STEPS = 10  # We can set this to any value for testing


class DiagonalCyclingSprite:

    center = [0, 0]
    cycle = itertools.cycle([])

    def configure_cycle(self, cycle: list[int]) -> None:
        self.center = [0, 0]
        self.cycle = itertools.cycle(cycle)

    def step(self) -> None:
        step = next(self.cycle)
        self.center[0] += step
        self.center[1] += step
        print(f"Sprite is now at: {self.center}")


def render_non_player_cycling_sprite() -> None:
    sprite = DiagonalCyclingSprite()
    sprite.configure_cycle([1, 2, 3, -3, -2, -1])
    for _ in range(NUM_STEPS):
        sprite.step()


if __name__ == "__main__":
    print("Part 1: DiagonalCyclingSprite")
    render_non_player_cycling_sprite()
    print("\n")

"""

When we refactor, we want to invert the dependency on the specific implementation of
'itertools.cycle', which can be done by adding an attribute: 'walk_back_to_start'

This is an improvement in the implementation because the domain logic in
'render_non_player_sprite' doesn't need to know that they have to add '[-3, -2, -1]'
to have the sprite return to the initial position

"""


class DiagonalSprite(DiagonalCyclingSprite):
    def configure_cycle(  # pylint: disable=W0221
        self,
        cycle: list[int],
        walk_back_to_start: bool,
    ) -> None:
        self.center = [0, 0]
        if walk_back_to_start:
            cycle += [_c * -1 for _c in cycle[::-1]]
        self.cycle = itertools.cycle(cycle)
        print(f"Configured cycle: {cycle}")


def render_non_player_sprite() -> None:
    sprite = DiagonalSprite()
    sprite.configure_cycle([1, 2, 3], walk_back_to_start=True)
    for _ in range(NUM_STEPS):
        sprite.step()


if __name__ == "__main__":
    print("Part 2: DiagonalSprite")
    render_non_player_sprite()
    print("\n")

"""

However, we could further improve this code by using a special type of Dependency Inversion,
Dependency Injection. This is the case where the object is provided and the class does
not initialize what it depends on.

"""


def render_non_player_injected_sprite(sprite) -> None:
    for _ in range(NUM_STEPS):
        sprite.step()


if __name__ == "__main__":
    print("Part 3: Injected Sprite")
    _sprite = DiagonalSprite()
    _sprite.configure_cycle([1, 2, 3], walk_back_to_start=True)
    render_non_player_injected_sprite(_sprite)
    print("\n")


"""

With these changes for Dependency Inversion and then for Dependency Injection (DI), the
code is much easier to extend and we can support any type of behavior.

Like the other SOLID principles, the Principles work together. DI would not be possible
without the Liskov Substitution Principle for the interface to be consistent.

"""

"""

If you would like to learn more about the Dependency Inversion Principle, you can take a look at:

- https://en.wikipedia.org/wiki/Dependency_inversion_principle
- https://martinfowler.com/articles/dipInTheWild.html#YouMeanDependencyInversionRight
- https://phoenixnap.com/blog/solid-principles
- https://ezzeddinabdullah.com/post/solid-principles-dip-py-copy/
- https://drive.google.com/file/d/0BwhCYaYDn8EgMjdlMWIzNGUtZTQ0NC00ZjQ5LTkwYzQtZjRhMDRlNTQ3ZGMz/view?resourcekey=0-jRJy8Mi4CltX8KX84BqLFQ

"""
