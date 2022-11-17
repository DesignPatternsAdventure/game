"""Task 01: Select your player character.

> (S) **Single Responsibility**
>
> A class, function, method or module should have a single responsibility.
> If it has many responsibilities, it increases the possibility of bugs!



FYI: For this first lesson, we recommend you jump into the game and try making changes
to `task_s_select_character.py`, then return to this file to learn more about SRP!

"""

import arcade

from ...core.registration import Register, SpriteRegister
from ...core.views.rpg_sprites import CharacterSprite, PlayerSprite
from ...task03.task_l_crafting import PlayerInventory
from .task_s_select_character import SOURCE_NAME

"""

Now that you have selected your character and started to write code for the game,
lets provide a little more background on the Single Responsibility Principle (SRP)

In the task code, there was a class with one function 'pick_resource_path'. You may
have noticed that this made editing the resource path very straightforward. Regardless
of if the class implemented random selection or returned a hard coded string, the does
one thing.

As an alternative to how the task code could have been implemented, we could have
written everything in a single class like below:

"""


class OneClass:
    """Rewritten version of the above code without SRP."""

    def __init__(self) -> None:
        self.resource_path = ":characters:Female/Female 02-3.png"

    def make_sprite(self) -> arcade.Sprite:
        return PlayerSprite(self.resource_path, PlayerInventory())

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
        return PlayerSprite(self.resource_path, PlayerInventory())

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
        return PlayerSprite(self.resource_path, PlayerInventory())

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
will write.

As a rule of thumb, If you can describe a section of code as doing "<this> and <that>"
where you need to use "and" then that might be a good class or function to refactor
to better comply with the SRP.

However, there are trade offs to SRP. For example, code often contains both "functional
code *and* logging code." There are ways to separate these concerns, but the trade off
in complexity may not be worth the benefit. Software design has well defined principles,
but the application of them should be done selectively and with judgment that you accrue
over time.

If you would like to learn more about SRP, you can take a look at:

- https://en.wikipedia.org/wiki/Single-responsibility_principle
- https://phoenixnap.com/blog/solid-principles
- https://ezzeddinabdullah.com/post/solid-principles-srp-py/
- https://learnbatta.com/blog/solid-principles-oops-python/
- https://github.com/zedr/clean-code-python#single-responsibility-principle-srp

"""
