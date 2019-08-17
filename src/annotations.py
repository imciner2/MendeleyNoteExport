
class Annotation:
    def __init__( self, filename, page, date, color ):
        self.__set_filename( filename )
        self.__set_page( page )
        self.__set_date( date )
        self.__set_color( color )

    def __get_filename( self ):
        return self.__filename

    def __set_filename( self, filename ):
        self.__filename = filename

    filename = property( __get_filename, __set_filename )

    def __get_page( self ):
        return self.__page

    def __set_page( self, page ):
        self.__page = page

    page = property( __get_page, __set_page )

    def __set_date( self, date ):
        self.__date = date

    def __get_date( self ):
        return self.__date

    date = property( __get_date, __set_date )

    def __set_color( self, color ):
        self.__color = tuple( int( color[i:i + 2], 16 ) / 255 for i in (1, 3, 5) )

    def __get_color( self ):
        return self.__color

    color = property( __get_color, __set_color )


class Highlight( Annotation ):
    def __init__( self, filename, page, date, color ):
        super().__init__( filename, page, date, color )

    def __set_x( self, x ):
        x.sort()
        self.__x = x

    def __get_x(self):
        return self.__x

    x = property( __get_x, __set_x )

    def __set_y( self, y ):
        y.sort()
        self.__y = y

    def __get_y( self ):
        return self.__y

    y = property( __get_y, __set_y )


class Note( Annotation ):
    def __init__( self, filename, page, date, color ):
        super().__init__( filename, page, date, color )

    def __set_author( self, author ):
        self.__author = author

    def __get_author( self ):
        return self.__author

    author = property( __get_author, __set_author )

    def __set_content( self, content ):
        self.__content = content

    def __get_content( self ):
        return self.__content

    content = property( __get_content, __set_content )

    def __set_x( self, x ):
        self.__x = x

    def __get_x( self ):
        return self.__x

    x = property( __get_x, __set_x )

    def __set_y( self, y ):
        self.__y = y

    def __get_y( self ):
        return self.__y

    y = property( __get_y, __set_y )