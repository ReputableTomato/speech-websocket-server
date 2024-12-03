import pdf2image

from Generic.Media.Mime import Mime
from Generic.Media.Image import Image
from Generic.Accessors.File import File
from Generic.Debugging.Performance.Profile import *

class PDF:

    def __init__(self):
        self._path = None
        self._image = Image
        self._mime = Mime([
            "application/pdf"
        ])
        self._type = "jpeg"

    @property
    def mime(self):
        """An accessor method to return the mime validator
        object.

        Returns:
            mime (Mime): The mime instance.
        """
        return self._mime

    @property
    def path(self):
        """An accessor method to return the file path.

        Returns:
            path (string): The file path.
        """
        return self._path

    @property
    def type(self):
        """An accessor method to return the file path.

        Returns:
            path (string): The file path.
        """
        return self._type

    @path.setter
    def path(self, path):
        """A setter method to set the file path.

        Args:
            path (string): The file path.
        """
        self._path = path

    @property
    def image(self):
        """An accessor method to return the Image instance.

        Returns:
            image (Image): The image instance.
        """
        return self._image

    @classmethod
    def convert_pdf(self, path, size):
        """A method to convert a pdf to an image with specific
        dimensions. Only the first page is taken. 

        Args:
            path (string): The file path.
            size (tuple): The image dimensions - (width, height).
        Returns:
            images (tuple): The images collected.
        """
        return pdf2image.convert_from_bytes(
            open(path, "rb").read(),
            single_file = True,
            fmt = "jpeg",
            size = size
        )

    def thumbnail(self, pdf_location, width, height, output_directory):
        """A method to convert a pdf to a thumbnail. 

        Args:
            pdf_location (string): The pdf file location.
            width (int): The width to set the image to.
            height (int): The height to set the image to.
            output_directory: The directory to output the thumbnail to.
        Returns:
            images (tuple): The images collected.
        """
        dimensions = (width, height)

        try:
            images = self.convert_pdf(pdf_location, dimensions)
        except:
            raise ImportError("Could not import {}.".format(pdf_location))

        file_name = File.split_filename(pdf_location)
        output_location = "{}{}_thumb{}".format(
            output_directory,
            file_name[0],
            ".jpg"
        )

        # If we have an imge, we will save it.
        if len(images) > 0:
            images[0].save(output_location)
        else:
            raise ValueError("The PDF you have provided does not have any pages.")