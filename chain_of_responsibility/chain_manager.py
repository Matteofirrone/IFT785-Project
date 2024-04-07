from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.caregiver_one_handler import CaregiverOneHandler
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.caregiver_three_handler import CaregiverThreeHandler
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.caregiver_two_handler import CaregiverTwoHandler
from chain_of_responsibility.handlers.Caregivers.caregiver_zero_handler import CaregiverZeroHandler
from chain_of_responsibility.handlers.abstract_handler import Handler


class SingletonMeta(type):
    """
    Metaclass for ApplicationInitializer class to ensure singleton behavior.

    Attributes:
        _instances: Dictionary to store singleton instances of ApplicationInitializer.
            Key: An instance of the metaclass itself.
            Value: Singleton instance of the class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Override the __call__ method to create or return an existing instance.

        Returns:
            obj: An instance of the class.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ChainManager(metaclass=SingletonMeta):
    """
    Singleton class responsible for managing chains of responsibility.

    Attributes:
        _chains: List to store all chains of responsibility.
    """

    def __init__(self):
        """
        Initializes an instance of ChainManager.
        """
        self._chains = []

    def initialize_chain_of_responsibility(self) -> Handler:
        """
        Initializes a new chain of responsibility by creating instances of different handler classes
        and linking them together.

        Returns:
            Handler: The head of the new chain of responsibility.
        """
        chain_of_responsibility = CaregiverZeroHandler()
        caregiver_one = CaregiverOneHandler(chain_of_responsibility)
        caregiver_two = CaregiverTwoHandler(chain_of_responsibility)
        caregiver_three = CaregiverThreeHandler(chain_of_responsibility)
        chain_of_responsibility.set_next(caregiver_one).set_next(caregiver_two).set_next(caregiver_three)
        self._chains.append(chain_of_responsibility)
        return chain_of_responsibility

    def get_chain_of_responsibility(self) -> Handler:
        """
        Initializes and returns a new chain of responsibility.

        Returns:
            Handler: The head of the new chain of responsibility.
        """
        return self.initialize_chain_of_responsibility()

    def get_chains_of_responsibility(self):
        """
        Returns all chains of responsibility.

        Returns:
            List[Handler]: All chains of responsibility.
        """
        return self._chains

    def remove_chain(self, chain: Handler) -> None:
        """
        Removes a chain of responsibility from the list once it has completed its work.

        Args:
            chain (Handler): The chain of responsibility to be removed (HEAD).
        """
        if chain in self._chains:
            self._chains.remove(chain)
