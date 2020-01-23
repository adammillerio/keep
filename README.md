# keep

keep is a simple tool for managing and editing Google Keep notes via a local text editor. This enables the ability to leverage Keep for note storage while using your preferred editing workflow.

keep is compatible with Mac, Windows, and Linux

**NOTE:** keep is currently at a VERY early stage in development, see the TODO and Limitations sections.

# Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  * [Sync](#sync)
  * [Note](#note)
- [Development](#development)
  * [Building](#building)
  * [Testing](#testing)
    + [mypy](#mypy)
  * [Limitations](#limitations)
  * [TODO](#todo)

# Installation

To install keep, you will need Python 3 and Pip.

On Windows, it is recommended that you use the [ActivePython](https://www.activestate.com/products/activepython/) distribution of Python 3, as it comes with Pip.

On MacOS, [Homebrew](https://brew.sh/) is recommended.

Once Python3 and Pip are installed, run the following command to install cratedigger:

`pip install keep-cli`

# Usage

keep is a command line tool, so it must be run from either cmd/PowerShell on Windows or Terminal on MacOS.

There are a few global command line options:

* `--verbose` - Enable verbose output
* `--config-dir` - Directory to load/store configuration and state from, defaults to `~/.config/keep`
* `--username` - Google Keep username
* `--password` - Google Keep password

The equivalent values can also be specified in either `~/.config/keep/config.yaml` or `KEEP_` prefixed environment variables.

For example, the Google Keep password could be stored as `password: yourpass` in `config.yaml` or by setting `KEEP_PASSWORD=yourpass`.

## Sync

The sync command will attempt to Sync with Google Keep, creating a local cache of notes if one does not already exist. This will be stored in `~/.config/keep/state.json`.

Example:

`keep sync`

## Note

The note command takes a given expression and searches Google Keep for a note that matches it, selecting the first one that is found. If no note is found, a new blank note will be created with the expression as the title.

This note is then written to a temporary file and then opened in the editor specified in your `$EDITOR` environment variable. If this is not set, it defaults to `vim`. Keep will then wait until the editor process is closed, and then sync back any changes to the note to Google Keep.

**Note:** Your configured editor MUST be ran in such a way that the command waits for the file to be closed. For example, if you use VS Code, set editor to `code -w` which will make the code command hang until the file is closed.

Example:

`keep note "Foobar"`

This will either search for and select the first note found matching "Foobar" or create a new note with "Foobar" as the title.

# Development

## Building

To install keep, clone this repository and run the following command:

```
pip install .
```

Optionally, it can be installed in development mode, which allows for iteration on the current repository without reinstalling:

```
pip3 install -e .
```

## Testing

### mypy

This repository has MyPy type hints for type enforcement.

To use these, first install mypy:

```
pip install mypy
```

Then, run the following command from the root of the repository:

```
mypy keep
```

## Limitations

This tool is currently very early stages, and as such, has the following limitations:

* Passwords have to be provided in plaintext
* Only notes are supported (not lists)
* There is no handling of multiple notes meeting a given search expression
* No support for labels, tags, media, and other metadata

These will hopefully be added in future versions.

## TODO

* Serialize Keep notes in a structured text-based format such as markdown, the ideal setup would be expressing notes similar to how Jekyll/OctoPress/Hugo express blog posts and pages, with the metadata and content in one text file
