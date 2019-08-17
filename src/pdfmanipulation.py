import os
import fitz as pdf


def annotate_pdf( destdir, highlights, notes ):
    # Join the keys to find all files that will be annotated
    high_keys = list( highlights.keys() )
    note_keys = list( notes.keys() )

    all_files = high_keys
    all_files.extend( k for k in note_keys if k not in all_files )

    for fname in all_files:
        file = os.path.split( fname )
        dest_file = os.path.join( destdir, file[1] )

        # Open the file
        print( "Opening file", fname, "for annotating" )
        pdffile = pdf.open( fname )

        # Iterate over every page
        for pgnum in range( 0, pdffile.pageCount-1 ):
            page = pdffile.loadPage( pgnum )

            # Fix any errors on the page
            try:
                page._cleanContents()
            except:
                print( "Error cleaning page", pgnum )

            # Add the highlights
            if fname in highlights:
                if pgnum in highlights[fname]:
                    add_highlights( page, highlights[fname][pgnum] )

            # Add the notes
            if fname in notes:
                if pgnum in notes[fname]:
                    add_notes( page, notes[fname][pgnum] )

        # Save the output file
        print( "Saving to file", dest_file )
        pdffile.save( dest_file )
        pdffile.close()


def add_highlights( page, highlights ):
    for high in highlights:
        # Create the location, note that the Mendeley coordinate system seems to have its Y axis inverted when
        # compared to the pdf library's axis. So the Y position should be flipped
        page_lr = page.rect

        ll = pdf.Point( high.x[0], page_lr.y1 - high.y[0] )
        ul = pdf.Point( high.x[0], page_lr.y1 - high.y[1] )
        ur = pdf.Point( high.x[1], page_lr.y1 - high.y[1] )
        lr = pdf.Point( high.x[1], page_lr.y1 - high.y[0] )
        points = pdf.Quad( ul, ur, ll, lr )

        # Create the highlight
        anot = page.addHighlightAnnot( points )

        # Update the color
        color = anot.colors
        color["fill_color"] = high.color
        color["stroke_color"] = high.color
        anot.setColors( color )

        anot.update()


def add_notes( page, notes ):
    for note in notes:
        # Create the location, note that the Mendeley coordinate system seems to have its Y axis inverted when
        # compared to the pdf library's axis. So the Y position should be flipped
        page_lr = page.rect
        corner = pdf.Point( note.x, page_lr.y1 - note.y )

        # Get the date
        if note.date == None:
            date = pdf.getPDFnow()
        else:
            try:
                date = note.date.strftime( "D:%Y%m%d%H%M%SZ00'00" )
            except:
                date = pdf.getPDFnow()

        # Make the note
        anot = page.addTextAnnot( corner, note.content )

        color = anot.colors
        color["fill_color"] = note.color
        color["stroke_color"] = note.color
        anot.setColors( color )

        anot.setOpacity( 1 )

        info = anot.info
        info["title"]        = note.author
        info["content"]      = note.content
        info["subject"]      = note.content.partition("\n")[0]
        info["creationDate"] = date
        anot.setInfo( info )

        anot.update()
