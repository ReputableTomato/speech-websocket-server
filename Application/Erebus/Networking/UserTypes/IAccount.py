from abc import ABC, abstractmethod

class IAccount(ABC):

    @abstractmethod
    def get() -> dict:
        """ A method to get an account from the database """

    @abstractmethod
    def remove() -> bool:
        """ A method remove the account """

    @abstractmethod
    def update() -> bool:
        """ A method update the account """

    @abstractmethod
    def exists() -> bool:
        """ A method to see if an account exists """

    @property
    @abstractmethod
    def id() -> int:
        """ id property """

    @id.setter
    @abstractmethod
    def id() -> None:
        """ id setter """

    @property
    @abstractmethod
    def ip_address() -> str:
        """ ip_address property """

    @ip_address.setter
    @abstractmethod
    def ip_address() -> None:
        """ ip_address setter """

    @property
    @abstractmethod
    def database():
        """ database property """