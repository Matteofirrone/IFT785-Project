from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.caregiver_one_handler import CaregiverOneHandler
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.caregiver_three_handler import CaregiverThreeHandler
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.caregiver_two_handler import CaregiverTwoHandler
from chain_of_responsibility.handlers.Caregivers.caregiver_zero_handler import CaregiverZeroHandler
from chain_of_responsibility.handlers.abstract_handler import Handler


class ApplicationInitializerMeta(type):
    """
    Metaclass for ApplicationInitializer class to ensure singleton behavior.

    Attributes:
        _instances: Dictionary to store singleton instances of ApplicationInitializer.
            Key: An instance of the metaclass itself.
            Value: Singleton instance of ApplicationInitializer.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Override the __call__ method to create or return an existing instance.

        Returns:
            ApplicationInitializer: An instance of ApplicationInitializer.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ApplicationInitializer(metaclass=ApplicationInitializerMeta):
    """
    Singleton class responsible for initializing the chain of responsibility.

    Attributes:
        _chain_of_responsibility: The head of the chain of responsibility.
    """

    def __init__(self):
        """
        Initializes an instance of ApplicationInitializer and sets up the chain of responsibility.
        """
        self._chain_of_responsibility: Handler | None = None
        self.initialize_chain_of_responsibility()

    def initialize_chain_of_responsibility(self):
        """
        Initializes the chain of responsibility by creating instances of different handler classes
        and linking them together.
        """
        self._chain_of_responsibility = CaregiverZeroHandler()
        caregiver_one = CaregiverOneHandler()
        caregiver_two = CaregiverTwoHandler()
        caregiver_three = CaregiverThreeHandler()
        self._chain_of_responsibility.set_next(caregiver_one).set_next(caregiver_two).set_next(caregiver_three)

    def get_chain_of_responsibility(self):
        """
        Returns the head of the chain of responsibility.

        Returns:
            Handler or None: The head of the chain of responsibility.
        """
        return self._chain_of_responsibility
