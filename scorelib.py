#!/usr/bin/env python3

"""
Scorelib - A score library management programm

Copyright (C) 2015 - 2016 Marcel Kapfer (mmk2410) <marcelmichaelkapfer@yahoo.co.nz>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
Scorelib v0.1.2
A program for managing your music score collection

Author:
Marcel Kapfer (mmk2410) <marcelmichaelkapfer@yahoo.co.nz>

License:
GPL v3

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
Scorelib  Copyright (C) 2015 - 2016  Marcel Kapfer (mmk2410)
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it under certain
conditions; type `show c' for details.

    """
    )

    while True:
        cmd = input(" > ")

        if cmd in ['usage', 'help', '?']:
            helptext()
        elif cmd == 'show w':
            print(
                    """
THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.
EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER
PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT WARRANTY OF ANY KIND, EITHER
EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE
QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE
DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
"""
            )
        elif cmd == 'show c':
            print(
            """
4. Conveying Verbatim Copies.

You may convey verbatim copies of the Program's source code as you receive it,
in any medium, provided that you conspicuously and appropriately publish on each
copy an appropriate copyright notice; keep intact all notices stating that this
License and any non-permissive terms added in accord with section 7 apply to the
code; keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

You may charge any price or no price for each copy that you convey, and you may
offer support or warranty protection for a fee.

5. Conveying Modified Source Versions.

You may convey a work based on the Program, or the modifications to produce it
from the Program, in the form of source code under the terms of section 4,
provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified it, and
    giving a relevant date.
    b) The work must carry prominent notices stating that it is released under
    this License and any conditions added under section 7. This requirement
    modifies the requirement in section 4 to “keep intact all notices”.
    c) You must license the entire work, as a whole, under this License to
    anyone who comes into possession of a copy. This License will therefore
    apply, along with any applicable section 7 additional terms, to the whole of
    the work, and all its parts, regardless of how they are packaged. This
    License gives no permission to license the work in any other way, but it
    does not invalidate such permission if you have separately received it.
    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your work need
    not make them do so.

A compilation of a covered work with other separate and independent works, which
are not by their nature extensions of the covered work, and which are not
combined with it such as to form a larger program, in or on a volume of a
storage or distribution medium, is called an “aggregate” if the compilation and
its resulting copyright are not used to limit the access or legal rights of the
compilation's users beyond what the individual works permit. Inclusion of a
covered work in an aggregate does not cause this License to apply to the other
parts of the aggregate.

6. Conveying Non-Source Forms.

You may convey a covered work in object code form under the terms of sections
4 and 5, provided that you also convey the machine-readable Corresponding
Source under the terms of this License, in one of these ways:

    a) Convey the object code in, or embodied in, a physical product (including
    a physical distribution medium), accompanied by the Corresponding Source
    fixed on a durable physical medium customarily used for software
    interchange.
    b) Convey the object code in, or embodied in, a physical product (including
    a physical distribution medium), accompanied by a written offer, valid for
    at least three years and valid for as long as you offer spare parts or
    customer support for that product model, to give anyone who possesses the
    object code either (1) a copy of the Corresponding Source for all the
    software in the product that is covered by this License, on a durable
    physical medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this conveying of
    source, or (2) access to copy the Corresponding Source from a network
    server at no charge.
    c) Convey individual copies of the object code with a copy of the written
    offer to provide the Corresponding Source. This alternative is allowed only
    occasionally and noncommercially, and only if you received the object code
    with such an offer, in accord with subsection 6b.
    d) Convey the object code by offering access from a designated place
    (gratis or for a charge), and offer equivalent access to the Corresponding
    Source in the same way through the same place at no further charge. You
    need not require recipients to copy the Corresponding Source along with the
    object code. If the place to copy the object code is a network server, the
    Corresponding Source may be on a different server (operated by you or a
    third party) that supports equivalent copying facilities, provided you
    maintain clear directions next to the object code saying where to find the
    Corresponding Source. Regardless of what server hosts the Corresponding
    Source, you remain obligated to ensure that it is available for as long as
    needed to satisfy these requirements.
    e) Convey the object code using peer-to-peer transmission, provided you
    inform other peers where the object code and Corresponding Source of the
    work are being offered to the general public at no charge under subsection
    6d.

A separable portion of the object code, whose source code is excluded from the
Corresponding Source as a System Library, need not be included in conveying the
object code work.

A “User Product” is either (1) a “consumer product”, which means any tangible
personal property which is normally used for personal, family, or household
purposes, or (2) anything designed or sold for incorporation into a dwelling.
In determining whether a product is a consumer product, doubtful cases shall be
resolved in favor of coverage. For a particular product received by a particular
user, “normally used” refers to a typical or common use of that class of
product, regardless of the status of the particular user or of the way in which
the particular user actually uses, or expects or is expected to use, the
product. A product is a consumer product regardless of whether the product has
substantial commercial, industrial or non-consumer uses, unless such uses
represent the only significant mode of use of the product.

“Installation Information” for a User Product means any methods, procedures,
authorization keys, or other information required to install and execute
modified versions of a covered work in that User Product from a modified version
of its Corresponding Source. The information must suffice to ensure that the
continued functioning of the modified object code is in no case prevented or
interfered with solely because modification has been made.

If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as part of a
transaction in which the right of possession and use of the User Product is
transferred to the recipient in perpetuity or for a fixed term (regardless of
how the transaction is characterized), the Corresponding Source conveyed under
this section must be accompanied by the Installation Information. But this
requirement does not apply if neither you nor any third party retains the
ability to install modified object code on the User Product (for example, the
work has been installed in ROM).

The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates for a
work that has been modified or installed by the recipient, or for the User
Product in which it has been modified or installed. Access to a network may be
denied when the modification itself materially and adversely affects the
operation of the network or violates the rules and protocols for communication
across the network.

Corresponding Source conveyed, and Installation Information provided, in accord
with this section must be in a format that is publicly documented (and with an
implementation available to the public in source code form), and must require no
special password or key for unpacking, reading or copying.
    """
            )
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
