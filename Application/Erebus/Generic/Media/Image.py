import os
import cv2

from Generic.Accessors.File import File
from Generic.Media.Mime import Mime
from Generic.Debugging.Performance.Profile import *

class Image:

    def __init__(self):
        self._mime = Mime([
            "image/apng",
            "image/bmp",
            "image/x-icon",
            "image/jpeg",
            "image/png",
            "image/svg+xml",
            "image/tiff",
            "image/webp"
        ])
        self.file_handle = File()

    @property
    def mime(self):
        """An accessor method for the mime instance.

        Returns: 
            instance (Mime): The mime instance.
        """
        return self._mime

    def thumbnail(self, image_location, width, height, output_directory = None):
        """A method for creating an image thumbnail. The height must
        be double the width in order to create a valid thumbnail. If
        no output location is provided, the thumbnail is written is
        written to the current directory that the image resides in.

        Any existing thumbnails in the output location will be overwritten.

        Args:
            image_location (string): The image location.
            width (int): The width of the thumbnail.
            output_directory (string): The location where the thumbnail will be output to.
        """
        if not self.mime.is_valid(image_location):
            raise ValueError("{} ({}) is not a supported mime type for generating an image thumbnail.".format(
                image_location,
                self.mime.type
            ))

        if not output_directory:
            output_directory = File.basename(image_location)

        file_name = File.split_filename(image_location)
        output_location = "{}{}_thumb{}".format(
            output_directory,
            file_name[0],
            file_name[1]
        )

        image = self.load(image_location)
        dimensions = (width, height)
        resized_image = self.resize(image, dimensions)

        self.write(output_location, resized_image)

    def load(self, image_location):
        """A method for loading an image from a specific location.

        Args:
            image_location (string): The image location.
        """
        return cv2.imread(image_location, cv2.IMREAD_UNCHANGED)

    @classmethod
    def write(self, location, image):
        """A method for writing an image to file.

        Args:
            location (string): The location where to write the image to.
            image (2 dimension array): The output from loading an image.
        """
        cv2.imwrite(location, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    @classmethod
    def resize(self, image, dimensions):
        """A method to resize an image which has been loaded by opencv.

        Args:
            image (2 dimension array): The output from loading an image.
            dimensions (tuple): A tuple containing the width and height 
            the image.
        """
        return cv2.resize(image, dimensions, interpolation = cv2.INTER_AREA)