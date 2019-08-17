from annotations import Highlight, Note

import _sqlite3 as sq
from urllib.parse import urlparse, unquote
from dateutil import parser as date


def parseurl( url ):
    try:
        # Try decoding UTF8
        return unquote( str( urlparse( url ).path ) ).decode( "utf8", "strict" )
    except:
        # String might already be UTF8
        return unquote( str( urlparse( url ).path ) )


def parsedate( dt ):
    return date.parse( dt )


class Database:
    def __init__( self, filename ):
        self.__filename = filename

        print( "Loading database from", filename )

        self.__db = sq.connect( filename )

    def get_highlights( self ):

        query = """SELECT Files.localUrl, FileHighlightRects.page,
                                    FileHighlightRects.x1, FileHighlightRects.y1,
                                    FileHighlightRects.x2, FileHighlightRects.y2,
                                    FileHighlights.createdTime, FileHighlights.color
                            FROM Files
                            LEFT JOIN FileHighlights
                                ON FileHighlights.fileHash=Files.hash
                            LEFT JOIN FileHighlightRects
                                ON FileHighlightRects.highlightId=FileHighlights.id
                            WHERE (FileHighlightRects.page IS NOT NULL)"""

        ret = self.__db.execute( query )

        highlights = {}
        for entry in ret:
            fname = parseurl( entry[0] )    # The filename
            page = entry[1] - 1             # The page number
            dt = parsedate( entry[6] )      # The creation date

            high = Highlight( fname,        # The filename
                              page,         # The page number
                              dt,           # The creation date
                              entry[7] )    # The color

            high.x = [entry[2], entry[4]]   # The x coordinates
            high.y = [entry[3], entry[5]]   # The Y coordinates

            # The highlights are stored in a file/page dictionary
            if fname in highlights:
                if page in highlights[fname]:
                    highlights[fname][page].append( high )
                else:
                    highlights[fname][page] = [high]
            else:
                highlights[fname] = { page: [high] }

        return highlights

    def get_notes( self ):
        query = """SELECT Files.localUrl, FileNotes.page,
                                    FileNotes.x, FileNotes.y,
                                    FileNotes.author, FileNotes.note,
                                    FileNotes.modifiedTime, FileNotes.color
                            FROM Files
                            LEFT JOIN FileNotes
                                ON FileNotes.fileHash=Files.hash
                            WHERE FileNotes.page IS NOT NULL"""

        ret = self.__db.execute( query )

        notes = {}
        for entry in ret:
            fname = parseurl( entry[0] )    # The filename
            page = entry[1] - 1             # The page number
            dt = parsedate( entry[6] )      # The creation date

            note = Note( fname,             # The filename
                         page,              # The page number
                         dt,                # The creation date
                         entry[7] )         # The color

            note.x = entry[2]               # The x-position of the note's corner
            note.y = entry[3]               # The y-position of the note's corner
            note.author = entry[4]          # The author of the note
            note.content = entry[5]         # The content of the note

            # The notes are stored in a file/page dictionary
            if fname in notes:
                if page in notes[fname]:
                    notes[fname][page].append( note )
                else:
                    notes[fname][page] = [note]
            else:
                notes[fname] = {page: [note]}

        return notes
