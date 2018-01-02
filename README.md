# Scorelib

Scorelib is a free CLI (command line interface) programm written in python and for linux only. The idea behind this tool is, to combine the lightning fast UX of a keyboard-only terminal usage and the fully digitalization of your music score library.

## Features

Scorelib is in an early state, so it doesn’t include special features. The following ones are already implemented:

 - Add new pieces
 - Edit pieces
 - Delete pieces (through the editing mode)
 - List all pieces
 - Search for a piece

## Installation

Python 3 and sqlite3 is required for using this program.

To install it clone the repository or download a release form the release page and run (after extracting it):

```
sudo make install
```

Your database is stored in `~/.scorelib/scorelib.db`

To remove scorelib run:

```
sudo make uninstall
```

## Usage

When you first use the program, you have to initialize it. To do so start the program and enter `init` as a command. This command creates the directory ~/.scorelib where Scorelib stores its data. After that Scorelib creates and initializes a SQlite database in that directory.

There are two different modes: the normal mode and the edit mode. When you start the program you start out in the normal mode with the prompt ` > ` and you can run the following commands:

| Command          |         Description        |
|------------------|:--------------------------:|
| help, usage, ?   | print the help text        |
| add, new, a      | add a new piece            |
| list, l          | list all pieces            |
| edit, e          | edit a piece               |
| search, s        | search for a piece         |
| init             | initialize the database    |
| kill             | destroy the database       |
| quit, exit, x, q | close Scorelib             |

If you switch to the editing mode your prompt will look like this: ` (edit) > ` and you can run these commands:

| Commands           |          Description                        |
|--------------------|:-------------------------------------------:|
| help, usage, ?     | Print the help text                         |
| done, q            | Done editing piece, back to normal mode     |
| print, p           | Print piece information                     |
| delete, d          | Delete this item and go back to normal mode |
| edit, change, c, e | Change the values of the item               |

## Contributing

The program is licensed under GPL v3 license. If you want to contribute just follow these steps:

 1. Fork it
 2. Create your feature branch (`git chechout -b my-new-feature`)
 3. Commit your changes (`git commit -am 'Add some feature'`)
 4. Push to the branch (`git push origin my-new-feature`)
 5. Create new pull request

You can also add yourself to the CONTRIBUTORS.md file.

## News

If there any news, I'll write about them on Twitter ([@mmk2410](https://twitter.com/mmk2410)) and on my blog at [mmk2410.org](https://mmk2410.org).
