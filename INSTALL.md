# Advanced Python Installation

If you already have a compatible version of Python and poetry installed, you can run `poetry install` then `poetry shell` to start using the commands. If not, see the below instructions for your system

## "asdf" Install

**For MacOS, Linux, and Windows Subsystem for Linux (WSL)**

`asdf` is a general purpose version manager and we use it to ensure consistency between setups. To install `asdf`, follow the [installation guide](https://asdf-vm.com/guide/getting-started.html), which is typically `brew install asdf` for Mac or variations of `apt-get install asdf` for Linux.

Once you have installed `asdf`, there are a few additional steps:

```sh
asdf plugin-add python https://github.com/asdf-community/asdf-python.git
asdf plugin-add poetry https://github.com/asdf-community/asdf-poetry.git

# Make sure you are within the project directory
cd game

asdf install # This one usually takes a while
```

#### Windows Native

There are multiple ways to install Python on Windows. Our recommend approach is to install Chocolatey and run `choco install python` ([link](https://community.chocolatey.org/packages/python)). See the [guide for installing and configuring chocolatey here](https://chocolatey.org/install).

Next, install `poetry` following the [official poetry installation guide](https://python-poetry.org/docs/#installing-with-the-official-installer). We recommend the `powershell` method, which at the time of writing looks like:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

## Post-Install

Regardless of how you installed `poetry`, check that the installation succeeded by running the below code:

```sh
# Install the game dependencies with poetry
poetry install

# Then activate the package environment managed by poetry
poetry shell

# And start the game!
doit play
```
