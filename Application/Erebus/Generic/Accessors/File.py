import json
import os
import shutil
import yaml

class File:

    @staticmethod
    def get_current_directory(path = None):
        """A method method for obtaining the current script
        path.

        Args: 
            count: The amount of files.
        Returns: 
            string: The executing script root path.
        """
        if path:
            path = os.path.dirname(os.path.abspath(path))
        else:
            path = os.path.dirname(os.path.abspath(__file__))

        if not path.endswith("/"):
            return "{}/".format(path)

        return path

    @staticmethod
    def directory_file_count(*arguments):
        """A method to get the number of files in a directory.
        
        Args:
            directory (string): The directory to count from.

        Returns:
            int: The number of files in the directory.

        Raises:
            ImportError: If the supplied directory does not exist.
        """
        directory = File.format_file_arguments(arguments)

        if not os.path.isdir(directory):
            raise ImportError("""The supplied directory is either
                            not a directory or does not exist.""")

        file_count = 0

        for root, dirs, files in os.walk(directory):
            file_count += len(files)

        return file_count

    @staticmethod
    def get_files_in_directory(directory, file_type = None, custom_extension_list = None):
        """A method to get a list of files in a folder. A type of
        file can be specified to get files with a certain extension.
        
        Args:
            directory (string): The directory.
            type (string): The type of files to get.

        Returns:
            list: The files in the directory.

        Raises:
            ImportError: If the supplied directory does not exist.
            ValueError: If a valid type is not specified.
        """
        if not os.path.isdir(directory):
            raise ImportError("""The supplied directory is either
                            not a directory or does not exist.""")

        valid_extension_types = {
            "images": ["jpg", "jpeg", "jpe", "jif", "jfif", "jfi","png", "gif", "webp", "tiff", "tif", "bmp",".svg"],
            "videos": ["webm", "mkv", "flv", "gif", "ogg", "avi", "mov", "mp4", "m4p", "m4v", "mpeg", "mpe", "mpv",
            "m2v", "mpg", "mp2", "m4v", "f4v"]
        }

        if file_type and file_type not in valid_extension_types.keys():
            raise ValueError("You have not provided a valid type. Valid types consist of {}.".format(",".join(valid_extension_types.keys())))

        files = []
        verify_slash = lambda root: root if root.endswith("/") else root + "/"

        for root, dirs, file_list in os.walk(directory):
            for file_name in file_list:
                extension = os.path.splitext(file_name)[1].replace(".", "")

                if file_type:
                    if extension in valid_extension_types[file_type]:
                        files.append(verify_slash(root) + file_name)
                elif custom_extension_list:
                    if extension in custom_extension_list:
                       files.append(verify_slash(root) + file_name) 
                else:
                    files.append(verify_slash(root) + file_name)

        return files

    @staticmethod
    def read_file(*arguments, file_name = None, mode = "r"):
        """A to read data from a file.
        
        Args:
            file_name (string): The file to read from.
            mode (string): The mode that we're opening the file type
            with - For example r or r+.

        Returns:
            True if file write was successful.

        Raises:
            ImportError: If the file already exists or if an
            invalid mode is provided.
            OSError: If unable to write to the file.
        """
        if not file_name:
            file_name = ""

            for argument in arguments:
                file_name += argument

        if not os.path.isfile(file_name):
            raise OSError("'{}' does not exist.".format(file_name))

        handle = open(file_name, mode)
        file_content = handle.read()
        handle.close()

        return file_content

    @staticmethod
    def format_file_arguments(arguments):
        """A function to format the file arguments passed to
        a function.
        
        Args:
            arguments (tuple): The list of strings.

        Returns:
            True if file write was successful.
        """
        file_name = ""

        for argument in arguments:
            file_name += str(argument)

        return file_name

    @staticmethod
    def write_to_file(file_name, content, mode):
        """A method for writing to a file.
        
        Args:
            file_name (string): The file to be written to.
            content (string): The content to be written to the
            file.
            mode (string): The mode that we're opening the file type
            with. For example w or w+.

        Returns:
            True if file write was successful.

        Raises:
            ValueError: If the file already exists or if an
            invalid mode is provided.
            OSError: If unable to write to the file.
        """
        if not os.path.isfile(file_name):
            raise ValueError("The file name provided does not exist.")

        write_modes = ["w", "w+"]

        if mode not in write_modes:
            raise ValueError("You must provide a valid mode.")

        try:
            handle = open(file_name, mode)
            handle.write(content)
            handle.close()

            return True
        except OSError as error:
            raise OSError("Unable to write to file.")

    @staticmethod
    def exists(*arguments):
        """A method for verifying if a path exists.

        Args:
            arguments (string): The path arguments.

        Returns:
            bool: True if exists, false if not.
        """
        path = File.format_file_arguments(arguments)

        return os.path.exists(path)

    @staticmethod
    def create_directory(directory):
        """A method to create a directory.

        Args:
            directory (string): A directory to be created.

        Returns:
            True if the directory was created.
        
        Raises:
            FileExistsError: If the directory exists.
        """
        if os.path.isdir(directory):
            raise FileExistsError("This directory already exists.")

        os.mkdir(directory)

        return True

    @staticmethod
    def recursively_create_path(*arguments):
        """A method to create a file in a directory that doesn't
           exist.

        Args:
            arguments (string): The path arguments.

        Returns:
            True if the path was created.
        
        Raises:
            FileExistsError: If the directory exists.
        """
        path = File.format_file_arguments(arguments)

        if File.exists(path):
            raise FileExistsError("This directory already exists.")

        directory = os.path.dirname(os.path.abspath(path))
        file_name = os.path.basename(path)

        os.makedirs(directory)

        File.create_file(directory, "/", file_name)

        return True
    
    @staticmethod
    def delete_directory(*arguments):
        """A method to delete a directory.

        Args:
            directory (string): A directory to be deleted.

        Returns:
            True if the directory was deleted.
        
        Raises:
            OSError: If unable to delete the directory.
        """
        directory = File.format_file_arguments(arguments)

        try:
            os.removedirs(directory)

            return True
        except OSError as error:
            raise OSError(error)

    @staticmethod
    def create_file(*arguments):
        """A method to delete a directory.

        Args:
            directory (string): A directory to be deleted.

        Returns:
            True if the file was created.

        Raises:
            FileExistsError: If unable to delete the directory.
        """
        file_name = File.format_file_arguments(arguments)

        if os.path.isfile(file_name):
            raise FileExistsError("This file already exists.")

        handle = open(file_name, "w+")
        handle.close()

        return True

    @staticmethod
    def read_json_file(*arguments):
        """A method to read the contents of a JSON file
        and to decode it.

        Args:
            file_name (string): The file name to be read.

        Returns:
            The json data.

        Raises:
            ValueError: If unable to decode the JSON data.
        """
        file_name = File.format_file_arguments(arguments)

        data = File.read_file(
            file_name = file_name
        )

        try:
            return json.loads(data)
        except ValueError:
            raise ValueError("Could not decode JSON file.")

    @staticmethod
    def read_yaml_file(*arguments):
        """A method to read the contents of a yaml file
        and to decode it.

        Args:
            file_name (string): The file name to be read.

        Returns:
            The file data.

        Raises:
            ValueError: If unable to decode the yaml data.
        """
        file_name = File.format_file_arguments(arguments)

        data = File.read_file(
            file_name = file_name
        )

        try:
            return yaml.load(data, Loader = yaml.FullLoader)
        except ValueError:
            raise ValueError("Could not decode yaml file.")

    @staticmethod
    def recursively_empty_folder(*arguments):
        """A method for emptying a specified folder.

        Args:
            arguments (string): The folder strings.

        Returns:
            The json data.

        Raises:
            ValueError: If unable to decode the JSON data.
        """
        folder = File.format_file_arguments(arguments)

        if not File.exists(folder):
            raise FileExistsError("{} does not exist.".format(folder))

        for file_name in os.listdir(folder):
            file_name = os.path.join(folder, file_name)

            try:
                if os.path.isfile(file_name) or os.path.islink(file_name):
                    os.unlink(file_name)
                elif os.path.isdir(file_name):
                    shutil.rmtree(file_name)
            except OSError as error:
                raise OSError("Could not delete {} - {}".format(file_name, error))

    @staticmethod
    def basename(*arguments):
        """Returns the folder a file is in.

        Args:
            file_location (string): The location of the file.
        Returns: 
            string: Folder the file is in.
        """
        location = File.format_file_arguments(arguments)
        folder = os.path.dirname(os.path.realpath(location))

        if not folder.endswith("/"):
            folder = folder + "/"

        return folder

    @staticmethod
    def split_filename(*arguments):
        """Returns the folder a file is in.

        Args:
            file_location (string): The location of the file.
        Returns: 
            tuple: The extracted file from a path e.g. ('test', '.png').
        """
        file_location = File.format_file_arguments(arguments)

        return os.path.splitext(os.path.basename(file_location))
    
    @staticmethod
    def delete_file(*arguments):
        file_location = File.format_file_arguments(arguments)

        os.remove(file_location)

    @staticmethod
    def size(*arguments, return_type = None):
        """A method to get the size of a file. A type
        can be specified to receive a certain format
        e.g. gb for gigabytes.

        Args:
            arguments (string): The file path arguments.
            return_type (string): The format to be returned.
        Returns:
            int|float: The file size.
        """
        path = File.format_file_arguments(arguments)
        file_byte_count = os.path.getsize(path)

        if return_type == "mb":
            return file_byte_count / 1000000
        elif return_type == "gb":
            return file_byte_count / 1000000000
        elif return_type == "kb":
            return file_byte_count / 1000
        else:
            return file_byte_count