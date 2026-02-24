# Getting started

All you need to get started building Textual apps.

## Requirements

Textual requires Python 3.9 or later (if you have a choice, pick the most recent Python). Textual runs on Linux, macOS, Windows and probably any OS where Python also runs.

### Installation

#### Windows

The new Windows Terminal runs Textual apps beautifully.

### From PyPI

Since we are developing a textual app you should install textual developer tools:

```bash
pip install textual-dev
```

If you would like to enable syntax highlighting in the TextArea widget, you should specify the "syntax" extras when you install Textual:

```bash
pip install "textual[syntax]"
```

## Textual CLI

If you installed the developer tools you should have access to the textual command. There are a number of sub-commands available which will aid you in building Textual apps. Run the following for a list of the available commands:

```bash
textual --help
```

See devtools for more about the textual command.

## Demo

Once you have Textual installed, run the following to get an impression of what it can do (you cannot exit with textual's example file in VScode since ctrl+q is the exit keybind - which conflicts with native VScode keybinds - you must close your terminal instance instead):

```bash
python -m textual
```

## Examples

We have included some example Textual files in this repository for reference. You can find them inside /textual-reference.

## Further Reference

get started doc: https://textual.textualize.io/getting_started/#__tabbed_1_1
