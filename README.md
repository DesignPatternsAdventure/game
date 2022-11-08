# Design Pattern Island Game

## Quick Start

### Python

<!-- FIXME: Replace with pyinstaller-based binary -->

### Graphviz

Make sure to [install graphviz from the official website](https://www.graphviz.org/download/)

For Mac users, this might be `brew install graphviz`, while Windows may need to download the latest `.exe` installer from the site or [use chocolatey](https://community.chocolatey.org/packages/graphviz)

## Game Play

> Make sure you go through the installation steps first!

### Quick Start

Let's launch the game UI and make the first code changes!

```sh
> poetry shell
(shell) doit play
````

This will open the game window where you can walk around using the keys `W`, `A`, `S`, and `D` and pick up items by pressing `E`.

Press an item's inventory number to equip it (tool) or consume it (food). If the item is a tool, left-click to activate it.

To quit the game, click the red "x" icon to close or use the keyboard shortcut `Ctrl C`.

> Note: you may have seen it above, but we will use the convention of `>` to indicate a normal shell prompt and `(shell)` to indicate when the command must be run after running `poetry shell` at least once. Alternatively, you could use `poetry run doit play`, but using `poetry shell` first is more convenient.

## Shortcuts

```sh
# Run all of the default tasks
(shell) doit --continue
(shell) doit list
# Tasks can also be run one-by-one
(shell) doit run format
(shell) doit run test
(shell) doit run check
(shell) doit run build_diagrams
# Or you can use a watcher utility that will re-run tests on changes
(shell) doit watch_changes

# When ready to start the next task, call:
# (FYI: This hasn't been implemented yet!)
(shell) doit next_task
```

## Assets

* [Pipoya Free RPG Tileset 32x32](https://pipoya.itch.io/pipoya-rpg-tileset-32x32)
* [Pipoya Free RPG Character Sprites 32x32](https://pipoya.itch.io/pipoya-free-rpg-character-sprites-32x32)
* [Kenney Input Prompts Pixel 16x16](https://kenney.nl/assets/input-prompts-pixel-16)
* [Gentle Cat Studios Pixel 16x16](https://gentlecatstudio.itch.io/rpg-items)
