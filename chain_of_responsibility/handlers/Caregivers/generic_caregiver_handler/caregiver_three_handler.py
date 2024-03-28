from api.models import SensorAlert, Caregiver
from chain_of_responsibility.handlers.Caregivers.generic_caregiver_handler.generic_caregiver import \
    GenericCaregiverHandler


class CaregiverThreeHandler(GenericCaregiverHandler):

    def __init__(self):
        super().__init__()

    def get_caregivers(self, request: SensorAlert):
        return Caregiver.objects.filter(elderly=request.home.elderly, level__level=3)
