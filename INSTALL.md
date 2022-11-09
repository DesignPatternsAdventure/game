# Advanced Installation

<!-- TODO: Cleanup instructions now that there is a full file! -->

### Python and Poetry

If you already have a compatible version of Python and poetry installed, you can get started right away and skip to "Game Play" below.

The recommended installation is with `asdf` on Linux, Mac, and Windows (through WSL). For Windows native, see the recommended solutions further below

#### Mac, Linux, and Windows Subsystem for Linux (WSL)

`asdf` is a general purpose version manager and we use it to ensure consistency between setups. To install `asdf`, follow the [installation guide](https://asdf-vm.com/guide/getting-started.html)

Once you have installed `asdf`, there are a few additional steps

```sh
asdf plugin-add python https://github.com/asdf-community/asdf-python.git
asdf plugin-add poetry https://github.com/asdf-community/asdf-poetry.git

# Make sure you are within the project directory and then run:
cd community-rpg
asdf install # This one usually takes a while

# Then install the project to check that setup worked
poetry install
```

#### Windows Native

1. There are multiple ways to install Python on Windows if you don't have it already. Our recommend approach is to install Chocolatey and run `choco install python` ([link](https://community.chocolatey.org/packages/python)). See the [guide for installing and configuring chocolatey here](https://chocolatey.org/install).
1. Next, install `poetry` following the [official poetry installation guide](https://python-poetry.org/docs/#installing-with-the-official-installer). We recommend using `pipx` ([pipx guide](https://pypa.github.io/pipx/installation/)), but installing method with powershell is the fastest way to get started.
1. To test that installation succeeded, run `poetry install` in the game directory before proceeding.
