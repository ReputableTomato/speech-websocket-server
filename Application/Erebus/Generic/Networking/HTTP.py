from urllib.parse import urlparse

class HTTP:

    @staticmethod
    def is_valid_url(website_url):
        """A method to determine if a url is valid.

        Args:
            website_url (string): The url to be checked.
        """
        try:
            result = urlparse(website_url)

            return all([result.scheme, result.netloc])
        except:
            return False

    @staticmethod
    def domain_from_url(website_url):
        """A method to extract a domain from a url.

        Args:
            website_url (string): The url.
        """
        return urlparse(website_url).netloc