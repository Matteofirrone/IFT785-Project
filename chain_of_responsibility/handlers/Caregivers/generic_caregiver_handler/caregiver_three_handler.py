from api.models import SensorAlert, Caregiver, CaregiverLevel
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.generic_caregiver import \
    GenericCaregiverHandler


class CaregiverThreeHandler(GenericCaregiverHandler):
    """
    A handler that sends notifications to level 3 caregivers.

    This handler retrieves the level 3 caregivers associated with an elderly person
    and sends notifications to them when a sensor alert is triggered.
    """

    def __init__(self, head_of_chain):
        """
        Initialize the CaregiverThreeHandler object.

        This method initializes the CaregiverThreeHandler object by calling the constructor of the parent class with
        the head_of_chain argument and setting the value of the WAIT_TIME attribute to the one present in database.

        :param head_of_chain: The first handler in the chain of responsibility.
        """
        super().__init__(head_of_chain)
        self.WAIT_TIME = CaregiverLevel.objects.get(level=3).wait_time

    def get_caregivers(self, request: SensorAlert):
        """
        Retrieves the level 3 caregivers associated with an elderly person.

        :param request: The sensor alert to handle.
        :return: A list of level 3 caregivers.
        """
        return Caregiver.objects.filter(elderly=request.home.elderly, level__level=3)
