#!/usr/bin/env python3

"""
Scorelib - A score library management programm
Marcel Kapfer (mmk2410)
MIT License
Version 0.1.1
"""

import sqlite3
import readline
import getpass
import os

USER = getpass.getuser()
CONFIG = "/home/" + USER + "/.scorelib/"
DBPATH = CONFIG + "scorelib.db"

class Piece:
    """ A class for working with scores """

    def __init__(self, piece=None):
        if piece is None:
            raise NameError("No piece list given")
        if piece['id'] is None:
            raise NameError("No piece id given")
        self.pieceid = piece['id']
        self.name = piece['name']
        self.composer = piece['composer']
        self.opus = piece['opus']
        self.key = piece['key']
        self.book = piece['book']

    def get_list(self):
        """ Returns a list for sending to the database """
        piece = (self.name, self.composer, self.opus, self.key, self.book, self.pieceid)
        return piece

    def print_piece(self):
        """ prints the current piece """
        print(
            """
Name:       {}
Composer:   {}
Opus:       {}
Key:        {}
Book:       {}
            """.format(self.name, self.composer, self.opus, self.key, self.book))

    def delete(self):
        """
        Delete a item
        """
        con = None
        try:
            con = sqlite3.connect(DBPATH)
            cur = con.cursor()
            sqlcmd = "DELETE FROM Scores WHERE id = " + str(self.pieceid)
            cur.execute(sqlcmd)
            con.commit()
        except sqlite3.Error as err:
            print("Error: %s" % err.args[0])
        finally:
            if con:
                con.close()

    def change(self):
        """)
        Change a item
        """
        # Updating the values
        name = rlinput("Name: ", self.name)
        self.name = name or self.name
        self.composer = rlinput("Composer: ", self.composer)
        self.opus = rlinput("Opus: ", self.opus)
        self.key = rlinput("Key: ", self.key)
        self.book = rlinput("Book: ", self.book)
        # Pushing changes to the database
        con = sqlite3.connect(DBPATH)
        print(self.get_list)
        with con:
            cur = con.cursor()
            cur.execute("UPDATE Scores SET Name=?, Composer=?, Opus=?, Key=?, Book=? WHERE Id=?",\
                self.get_list())
            con.commit()


def rlinput(prompt, prefill=''):
    """ Function for advanced input (preset user input) """
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()

def initialize():
    """
    Initializing the database by creating a table
    """

    print("Initializing the database...")

    os.mkdir(CONFIG, 0o755)

    con = None

    try:
        con = sqlite3.connect(DBPATH)

        cur = con.cursor()

        cur.execute(
            "CREATE TABLE Scores( \
                    Id INTEGER PRIMARY KEY ASC NOT NULL, \
                    Name TEXT NOT NULL, \
                    Composer TEXT, \
                    Opus TEXT, \
                    Key TEXT, \
                    Book TEXT);"
        )

    except sqlite3.Error as err:
        print("Error: %s" % err.args[0])
        return 1

    finally:
        if con:
            con.close()

    return 0

def destroy():
    """
    Destroys the table.
    """
    print("Destroying all informations...")

    con = None

    try:
        con = sqlite3.connect(DBPATH)

        cur = con.cursor()

        cur.execute("DROP TABLE IF EXISTS Scores")

    except sqlite3.Error as err:
        print("Error: %s" % err.args[0])
        return 1

    finally:
        if con:
            con.close()

    return 0

def add():
    """ Add a entry to the database """
    while True:
        title = input("Title: ")
        if title:
            break
        else:
            print("You have to enter the name of the piece")
    piece = {"id": 0, "name":title}
    piece['composer'] = input("Composer: ")
    piece['opus'] = input("Opus: ")
    piece['key'] = input("Key: ")
    piece['book'] = input("Book: ")

    try:
        new_piece = Piece(piece)
    except NameError as err:
        print("Error: %s" % err.args[0])
        return -1

    new_piece.print_piece()

    con = None

    try:
        con = sqlite3.connect(DBPATH)

        cur = con.cursor()

        sqlcmd = "INSERT INTO Scores VALUES(NULL,'"\
                + piece['name'] + "','" \
                + piece['composer'] + "','" \
                + piece['opus'] + "','" \
                + piece['key'] + "','" \
                + piece['book'] + "')"

        cur.execute(sqlcmd)

        con.commit()

    except sqlite3.Error as err:
        print("Error: %s" % err.args[0])
        return 1

    finally:
        if con:
            con.close()

    return 0

def list_scores():
    """
    List all available scores
    """

    con = None

    try:

        con = sqlite3.connect(DBPATH)

        cur = con.cursor()

        cur.execute("SELECT * FROM Scores")

        print()

        while True:

            row = cur.fetchone()

            if row is None:
                break

            print(
                """
Piece number:   {}
Name:           {}
Composer:       {}
Opus:           {}
Key:            {}
Book:           {}
                """.format(row[0], row[1], row[2], row[3], row[4], row[5])
            )


    except sqlite3.Error as err:
        print("Error: %s" % err.args[0])
        return 1

    finally:
        if con:
            con.close()

    return 0

def edit_get_id():
    """ Get the piece id from the user"""
    pieceid = None
    while True:
        pieceid = input("Enter the piece number: ")
        if pieceid == 'quit':
            return 0
        elif pieceid and pieceid.isdigit():
            con = sqlite3.connect(DBPATH)
            piecerow = None
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Scores WHERE Id=" + str(pieceid))
                piecerow = cur.fetchone()
            if piecerow is None:
                print("No Piece with this number available.")
            else:
                break
        else:
            print("Input must be a valid number!")
        return piecerow


def edit():
    """Function for editing the pieces"""
    # Ask piece id from user
    piecerow = edit_get_id()

    # Getting the piece information
    piecedata = {"id": piecerow[0], "name": piecerow[1], "composer": piecerow[2],\
            "opus": piecerow[3], "key": piecerow[4], "book": piecerow[5]}
    piece = Piece(piecedata)
    print("Piece Information:")
    piece.print_piece()

    # edit prompt
    while True:
        edtcmd = input(" (edit) > ")
        if edtcmd in ['help', '?', 'usage']:
            helpedittext()
        elif edtcmd in ['done', 'q']:
            return 0
        elif edtcmd in ['print', 'p']:
            piece.print_piece()
        elif edtcmd in ['delete', 'd']:
            piece.delete()
            return 0
        elif edtcmd in ['edit', 'change', 'c', 'e']:
            piece.change()
        else:
            helpedittext(True)

def search():
    """ Search through the database """
    term = input("Search for: ")
    con = sqlite3.connect(DBPATH)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Scores")
        rows = cur.fetchall()
        for item in range(1, 6):
            if item == 1:
                print("By name\n")
            elif item == 2:
                print("By Composer\n")
            elif item == 3:
                print("By Opus\n")
            elif item == 4:
                print("By Key\n")
            elif item == 5:
                print("By Book\n")
            for row in rows:
                if term in row[item]:
                    piecedata = {"id": row[0], "name": row[1], "composer": row[2],\
                    "opus": row[3], "key": row[4], "book": row[5]}
                    piece = Piece(piecedata)
                    print("Piece number: %s" % str(row[0]))
                    piece.print_piece()


def helpedittext(doneshit=False):
    """ print the edit help text """
    if doneshit:
        print("The entered command ist not available.")
    print(
        """
Edit help text:

help, ?, usage              Print edit help
done, q                     Done editing piece; back to main menu
print, p                    Print piece information
delete, d                   Delete this item and go back to main menu
edit, change, c, e          Change the values of the item
        """
    )

def helptext(doneshit=False):
    """ print the help text """
    if doneshit:
        print("The entered command is not available.")
    print(
        """
Scorelib v0.1.1
A program for managing your music score collection

Author:
Marcel Kapfer (mmk2410) <marcelmichaelkapfer@yahoo.co.nz>

License:
MIT License

Help:

help, usage, ?              prints this text
add, new, a                 add a new piece
list, l                     list all pieces
edit, e                     edit a piece (piece number required)
search, s                   search for a piece
init                        initializes the database
kill                        destroys the database
quit, exit, x, q            close Scorelib

        """
    )


def main():
    """ Main """
    print(
        """
Welcome to Scorelib -  A program for managing your music score collection

If you use this program the first time you have to initialize the database \
        before you can use it.

Type 'help' to see a list of commands
    """
    )

    while True:
        cmd = input(" > ")

    if cmd in ['usage', 'help', '?']:
        helptext()
    elif cmd in ['quit', 'exit', 'x', 'q']:
        print("Good Bye!")
        exit(0)
    elif cmd == 'init':
        status = initialize()
        if status == 1:
            print("A database error occurred. Please try again.")
    elif cmd == 'kill':
        status = destroy()
        if status == 1:
            print("A database error occurred. Please try again.")
    elif cmd in ['add', 'new', 'a']:
        status = add()
        if status == 1:
            print("A database error occurred. Please try again.")
        elif status == -1:
            print("An input you made was not accepted.")
    elif cmd in ['list', 'l']:
        list_scores()
    elif cmd in ['edit', 'e']:
        edit()
    elif cmd in ['search', 's']:
        search()
    else:
        helptext(True)

if __name__ == "__main__":
    main()
