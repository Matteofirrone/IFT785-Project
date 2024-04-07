from api.models import SensorAlert, Caregiver
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.generic_caregiver import \
    GenericCaregiverHandler
from ift785_project import settings


class CaregiverOneHandler(GenericCaregiverHandler):
    """
    A handler that sends notifications to level 1 caregivers.

    This handler retrieves the level 1 caregivers associated with an elderly person
    and sends notifications to them when a sensor alert is triggered.
    """

    WAIT_TIME = settings.CAREGIVER_ONE_WAIT_TIME

    def get_caregivers(self, request: SensorAlert):
        """
        Retrieves the level 1 caregivers associated with an elderly person.

        :param request: The sensor alert to handle.
        :return: A list of level 1 caregivers.
        """
        return Caregiver.objects.filter(elderly=request.home.elderly, level__level=1)
