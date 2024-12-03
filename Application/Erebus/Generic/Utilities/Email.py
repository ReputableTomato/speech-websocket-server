from email.utils import parseaddr

class Email:

    @staticmethod
    def validate_email(email_address):
        parsed_address = parseaddr(email_address)

        if not parsed_address[1]:
            return False

        if "@" not in parsed_address[1]:
            return False

        return True