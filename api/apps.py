from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    # Add CaregiverLevels to DB
    def ready(self):
        @receiver(post_migrate)
        def populate_caregiver_levels(sender, **kwargs):
            if sender.name == 'api':
                from api.models import CaregiverLevel  # Importez CaregiverLevel ici pour éviter l'erreur d'accès anticipé à l'application
                CaregiverLevel.objects.get_or_create(level=0)
                CaregiverLevel.objects.get_or_create(level=1)
                CaregiverLevel.objects.get_or_create(level=2)
                CaregiverLevel.objects.get_or_create(level=3)
