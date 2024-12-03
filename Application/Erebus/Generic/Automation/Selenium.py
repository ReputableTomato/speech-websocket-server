from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Generic.Accessors.File import File
from Generic.Media.Image import Image
from Generic.Networking.HTTP import HTTP

class Selenium:

    def __init__(self, chrome_driver_location = "/usr/bin/chromedriver"):
        """
        Args: 
            chrome_driver_location (string): The location of the chrome driver.
        """
        self._options = Options()
        # This argument is required or this will not run as root.
        self._options.add_argument('--no-sandbox')
        # Headless is required so we can run via command line.
        self._options.headless = True
        # We set the default resolution so the thumbnail is large.
        self._options.add_argument('--window-size=1920,1080')
        self._driver = webdriver.Chrome(chrome_driver_location, chrome_options = self.options)
        self._image = Image()
    
    @property
    def image(self):
        """An accessor method for the image instance.

        Returns: 
            instance (Mime): The mime instance.
        """
        return self._image

    def load(self, url):
        """A method to load a url using the webdriver.

        Args:
            url (string): The website url.
        Returns: 
            chrome driver instance (Chrome): The chrome driver instance.
        """
        self.driver.get(url)

        return self.driver

    def screenshot(self, website_url, output_location):
        """Attempts to take a screenshot of the website provided.

        Args:
            website_url (string): The website url.
            output_location (string): The location to output the screenshot to.
        Returns: 
            bool: Returns true if saving the screenshot was succesful, otherwise false.
        """
        return self.load(website_url).save_screenshot(output_location)

    def thumbnail(self, website_url, width, height, output_directory):
        """A method for creating a thumbnail of a website.

        Args:
            website_url (string): The website url.
            width (int): The thumbnail width
            height (int): The thumbnail height.
            output_directory (string): The output location.
        """
        if not HTTP.is_valid_url(website_url):
            raise ValueError("{} is not a valid website URL.".format(website_url))

        if not output_directory:
            raise ValueError("You must provide an output directory for a website thumbnail.")

        # Selenium requires the output file to be a png.
        output_location = "{}{}.png".format(
            output_directory,
            HTTP.domain_from_url(website_url).replace(".", "_")
        )

        if not self.screenshot(website_url, output_location):
            raise IOError("Could not save screenshot to disk {}".format(output_location))

        self.image.thumbnail(output_location, width, height, output_directory)
        # We have to delete the original file provided by selenium.
        File.delete_file(output_location)

    @property
    def driver(self):
        """An accessor method for the chrome driver instance.

        Returns: 
            Chrome: The chrome instance.
        """
        return self._driver

    @property
    def options(self):
        """An accessor method for the chrome options instance.

        Returns: 
            Options: The chrome options instance.
        """
        return self._options

    def close(self):
        """A method to close the chrome driver when we're finished
        with it.
        """
        self.driver.close()