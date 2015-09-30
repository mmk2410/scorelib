# Scorelib

A program for managing your music score collection. It runs on Linux and is written for the holy command line.

## Installation

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

When you first use the program, you have to initialize it. To do so start the program and enter `init` as a command.

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

The program is licensed under MIT license. If you want to contribute just follow these steps:

 1. Fork it
 2. Create your feature branch (`git chechout -b my-new-feature`)
 3. Commit your changes (`git commit -am 'Add some feature'`)
 4. Push to the branch (`git push origin my-new-feature`)
 5. Create new pull request

You can also add yourself to the CONTRIBUTORS.md file. (Create it if it doesn't exist)

## Social

Twitter: [@mmk2410](https://twitter.com/mmk2410)

Google+: [+MarcelMichaelKapfer](https://plus.google.com/+MarcelMichaelKapfer)
