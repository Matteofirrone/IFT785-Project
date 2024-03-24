
from django.contrib import admin
from api.models import SensorAlert, Person, Caregiver, CaregiverLevel


class SensorAlertAdmin(admin.ModelAdmin):
    list_display = ('subject', 'start', 'location', 'state', 'measurable', 'home')


class PersonAdmin(admin.ModelAdmin):
    pass


class CaregiverAdmin(admin.ModelAdmin):
    pass


class CaregiverLevelAdmin(admin.ModelAdmin):
    pass


admin.site.register(SensorAlert, SensorAlertAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Caregiver, CaregiverAdmin)
admin.site.register(CaregiverLevel, CaregiverLevelAdmin)

