
import argparse as ap
import os
import re

import database as db
from pdfmanipulation import annotate_pdf

from annotations import Highlight, Note

if __name__ == "__main__":
    # Parse the command line arguments
    parser = ap.ArgumentParser()
    parser.add_argument( "db", help="The path to the mendeley sqlite database file", type=str )
    parser.add_argument( "dest", help="The destination directory to save the PDF files in", type=str )
    args = parser.parse_args()

    # Verify the directory exists
    if not os.path.exists( args.db ):
        print( "Error: Provided directory does not exist" )

    # Find the database file
    files = [f for f in os.listdir( args.db ) if re.match( r"\S*@www\.mendeley\.com\.sqlite$", f )]

    if len( files ) == 0:
        print( "Error: Could not find a database file" )

    print( "Using database file", args.db )

    # Open the database
    fullname = os.path.join( args.db, files[0] )
    dbfile = os.path.abspath( fullname )
    dbconnector = db.Database( dbfile )

    # Get the highlights and notes from the database
    highlights = dbconnector.get_highlights()
    notes = dbconnector.get_notes()

    annotate_pdf( args.dest, highlights, notes )
