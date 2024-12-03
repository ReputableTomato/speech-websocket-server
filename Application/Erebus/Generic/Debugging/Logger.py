import logging

class Logger:

    def __init__(self, name, log_location, log_format):
        """We initialise the logging instance in the constructor. 

        Args:
            name (string): The name of our logging instance.
            log_location (string): The location to write the logs to.
            log_format (string): The format to write the logs in. E.g.
            %(asctime)s - %(name)s - %(levelname)s - %(message)s
        """
        self._name = name
        self._log_location = log_location
        self._log_format = log_format

        self._log = logging.getLogger(self._name)
        self._log.setLevel(logging.DEBUG)

        self._file_handle = logging.FileHandler(self._log_location)
        self._file_handle.setLevel(logging.DEBUG)

        self._stream_handle = logging.StreamHandler()
        self._stream_handle.setLevel(logging.ERROR)

        self._log_formatter = logging.Formatter(log_format)
        self._file_handle.setFormatter(self._log_formatter)
        self._stream_handle.setFormatter(self._log_formatter)

        self._log.addHandler(self._file_handle)
        self._log.addHandler(self._stream_handle)

    @property
    def log(self):
        """An accessor method for our logging instance.

        Returns:
            log (Logging): The name of our logging instance.
            log_location: The location to write the logs to.
            log_format: The format to write the logs in.
        """
        return self._log
