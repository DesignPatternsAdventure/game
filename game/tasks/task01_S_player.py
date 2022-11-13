"""Task 01: Player.

Welcome to Design Pattern Island! Your first task will be to personalize your character
by applying the "S" of the S.O.L.I.D design principles.

> (S) **Single Responsibility**
>
> A class, function, method or module should have a single responsibility.
> If it has many responsibilities, it increases the possibility of bugs!

"""

import random

import arcade
from loguru import logger

from ..core.registration import Register, SpriteRegister
from ..core.views.rpg_sprites import CharacterSprite, PlayerSprite

"""

Each task can be reloaded when you make code changes with either `Ctrl R` or `CMD R`!

Avoid making any changes to `SOURCE_NAME` or the function signature to `load_sprites`
because those are required for reload, but you can change the content of the
`load_sprites` function. On reload, the game will attempt to identify any errors and
recommended fixes, so you can often fix and reload without guitting!

"""

SOURCE_NAME = "task01_S_player"  # FYI: Required for code reload


class ResourcePicker:
    """Initial challenge."""

    @classmethod
    def pick_resource_path(cls) -> str:
        """Returns the string path to a sprite resource.

        Design Pattern Island is built using the Python arcade library. The library has
        a set of shorthand ways to refer to file paths to make them easier to load.

        All of the initial assets are placed in `game/assets`, which can be referenced
        with `:assets:`, but we provide additional shorthand for `:characters:` which
        evaluates to `game/assets/characters`. For reference, this file is currently in
        the `game/tasks` directory.

        For this first task, return the string `resource` that you want as your primary
        character. Note that for demonstration purposes, the character is chosen randomly
        from the list, but you only need to return a single hardcoded string.

        """
        resources = []
        for idx in range(18):  # There are more than just 18!
            resources.extend(
                [
                    f":characters:Female/Female {idx + 1:02}-1.png",
                    f":characters:Male/Male {idx + 1:02}-1.png",
                    f":characters:Animals/pipo-nekonin{idx + 1:03}.png",
                ]
            )
        resource = random.choice(resources)  # nosec B311
        logger.info(f"Selecting resource: '{resource}'")
        return resource

        # # Example solution:
        # return ':characters:Female/Female 02-3.png'


# FYI: Required for code reload
def load_sprites(sprite_register: SpriteRegister) -> None:
    """Create the special 'player sprite' who can be moved with WASD or the arrow keys."""
    resource = ResourcePicker.pick_resource_path()
    register = Register(sprite=PlayerSprite(resource), source=SOURCE_NAME)
    sprite_register.register_sprite(register)


"""

Now that you have selected your character and started to write code for the game,
lets provide a little more background on the Single Responsibility Principle (SRP)

In the above code, there was a class with one function 'pick_resource_path'. You may
have noticed that this made editing the resource path very straightforward. Regardless
of if the class implemented random selection or returned a hard coded string, the does
one thing.

As an alternative to how the above code could have been implemented, we could have
written everything in a single class like below:

"""


class OneClass:
    """Rewritten version of the above code without SRP."""

    def __init__(self) -> None:
        self.resource_path = ":characters:Female/Female 02-3.png"

    def make_sprite(self) -> arcade.Sprite:
        return PlayerSprite(self.resource_path)

    def register_sprite(self, sprite_register: SpriteRegister) -> None:
        register = Register(sprite=self.make_sprite, source=SOURCE_NAME)
        sprite_register.register_sprite(register)


"""

Now let's say that we decide we want to add the random selection or we want to change
which type of Sprite is created. We may then end up writing code like this:

"""


class OneClassWithExtraLogic:
    """Above code with logic to select the sprite type."""

    def __init__(self, is_player: bool = True) -> None:
        self.resource_path = ":characters:Female/Female 02-3.png"
        self.is_player = is_player

    def make_player_sprite(self) -> arcade.Sprite:
        return PlayerSprite(self.resource_path)

    def make_game_sprite(self) -> arcade.Sprite:
        return CharacterSprite(self.resource_path)

    def register_sprite(self, sprite_register: SpriteRegister) -> None:
        sprite = (
            self.make_player_sprite() if self.is_player else self.make_game_sprite()
        )
        register = Register(sprite=sprite, source=SOURCE_NAME)
        sprite_register.register_sprite(register)


# Note: leading underscore prevents shadowing the actual load_sprites function
def _load_sprites(sprite_register: SpriteRegister) -> None:
    """Example using the OneClassWithExtraLogic."""
    OneClassWithExtraLogic(is_player=True).register_sprite(sprite_register)


"""

Following SRP, this class could be rewritten to separate responsibilities between
selecting the sprite and registering.

"""


class JustSprite:
    """Just a Sprite."""

    def __init__(self) -> None:
        self.resource_path = ":characters:Female/Female 02-3.png"

    def make_player_sprite(self) -> arcade.Sprite:
        return PlayerSprite(self.resource_path)

    def make_game_sprite(self) -> arcade.Sprite:
        return CharacterSprite(self.resource_path)


class JustRegister:
    """Just a Register method."""

    def register_sprite(
        self, sprite: arcade.Sprite, sprite_register: SpriteRegister
    ) -> None:
        register = Register(sprite=sprite, source=SOURCE_NAME)
        sprite_register.register_sprite(register)


# Note: leading underscore prevents shadowing the actual load_sprites function
def __load_sprites(sprite_register: SpriteRegister) -> None:
    """Example using JustSprite and JustRegister."""
    sprite = JustSprite().make_player_sprite()
    JustRegister().register_sprite(sprite, sprite_register)


"""

The above examples were a little contrived to demonstrate the differences, but as you
proceed with the tasks, you'll have opportunities to consider the SRP in the code you
will write. If you can describe a section of code as doing "<this> and <that>" where
you need to use "and" then that might be a good class or function to refactor with SRP

There are trade offs to SRP. For example, code often contains both functional code and
logging. There are ways to separate these concerns, but the trade off in complexity may
not be worth the benefit. Software design has well defined principles, but they are not

If you would like to learn more about SRP, you can take a look at:

- https://en.wikipedia.org/wiki/Single-responsibility_principle
- https://phoenixnap.com/blog/solid-principles
- https://ezzeddinabdullah.com/post/solid-principles-srp-py/
- https://learnbatta.com/blog/solid-principles-oops-python/
- TODO: https://github.com/zedr/clean-code-python#single-responsibility-principle-srp

"""
