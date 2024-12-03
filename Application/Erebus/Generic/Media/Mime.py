import magic

class Mime:

    def __init__(self, valid_mime_types = []):
        """You must provide a list of valid mime types. This
        list is used to check if a file mimetype is in this list.

        Args: 
            valid_mime_types (tuple): A list of valid mime types.
        """
        self._type = None
        self._magic = magic.open(magic.MAGIC_MIME)
        self._magic.load()
        self._valid_mime_types = valid_mime_types

    @property
    def valid_mime_types(self):
        """An accessor method for the list of valid
        mime types.

        Returns: 
            list: The valid mime types.
        """
        return self._valid_mime_types

    @property
    def type(self):
        """An accessor method for the mime type.

        Returns: 
            string: The mime type.
        """
        return self._type

    @type.setter
    def type(self, type):
        """A setter method for setting a file mime type.

        Args:
            type (string): The mime type.
        """
        self._type = type

    def is_valid(self, file_location):
        """A method for verifying if a file is in the list
        of allowed mime types.

        Args:
            file_location (string): The location of the file.
        """
        self.type = self._magic.file(file_location)

        return True if self.type in self.valid_mime_types else False