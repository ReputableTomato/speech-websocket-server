import time
import datetime
import subprocess
import os
import cv2

from Generic.Accessors.File import File
from Generic.Media.Image import Image
from Generic.Media.Mime import Mime
from Generic.Debugging.Performance.Profile import *

class Video:

    def __init__(self):
        self._current_time = None
        self._video_location = None
        self._image = Image()
        self._mime = Mime([
            "image/gif",
            "video/mp4",
            "video/x-flv",
            "application/x-mpegURL",
            "video/MP2T",
            "video/3gpp",
            "video/quicktime",
            "video/x-msvideo",
            "video/x-ms-wmv"
        ])

    @property
    def mime(self):
        """An accessor method for the mime instance.

        Returns: 
            instance (Mime): The mime instance.
        """
        return self._mime

    @property
    def image(self):
        """An accessor method the instance of the Image class.

        Returns: 
            instance (Image): The image instance.
        """
        return self._image

    @property
    def video_location(self):
        """An accessor method the video video location.

        Returns: 
            string: The video location.
        """
        return self._video_location

    @video_location.setter
    def video_location(self, location):
        """A setter method for the video location.

        Args: 
            location: The location of the video.
        """
        self._video_location = location

    def thumbnail(self, video_location, width, height, output_directory = None, middle = False):
        """A method to generate a thumbnail from a video file. If no
        time is specified, the time will be the middle of the video.

        Args:
            video_location (string): The video location.
        """
        if not self.mime.is_valid(video_location):
            raise ValueError("{} ({}) is not a supported mime type for generating a video thumbnail.".format(
                video_location,
                self.mime.type
            ))

        if output_directory and not File.exists(output_directory):
            raise ValueError("{} output directory does not exist.".format(output_directory))

        self.video_location = video_location

        video_capture = cv2.VideoCapture(video_location)

        """
            If middle is true, we will try and get the middle
            frame of the video. If a gif is provided, the frame
            count is always a negative number, so we get the first
            frame.
        """
        if middle:
            # Obtain a list of the amount of frames
            frame_count = (int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT)))

            # If the image is a gif, we receive a negative integer.
            if frame_count < 0:
                frame_number = 1
            else:
                frame_number = int(frame_count / 2)

            # Set the current frame to frame number we have.
            video_capture.set(1, frame_number)

        resource, frame = video_capture.read()

        # Close the video now we have finished with it.
        video_capture.release()

        if not output_directory:
            output_directory = File.basename(video_location)

        file_name = File.split_filename(video_location)
        output_location = "{}{}_thumb{}".format(
            output_directory,
            file_name[0],
            ".png"
        )

        frame = self.image.resize(frame, (width, height))
        self.image.write(output_location, frame)