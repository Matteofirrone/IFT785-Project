
from django.contrib import admin
from api.models import Person, Caregiver, CaregiverLevel, Home


class CaregiverLevelFilter(admin.SimpleListFilter):
    title = 'Caregiver Level'
    parameter_name = 'caregiver_level'

    def lookups(self, request, model_admin):
        return CaregiverLevel.objects.all().values_list('level', 'level')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(level__level=self.value())


class PersonAdmin(admin.ModelAdmin):
    pass


class CaregiverLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'wait_time')


class CaregiverAdmin(admin.ModelAdmin):
    list_display = ('elderly', 'caregiver', 'level')
    list_filter = (CaregiverLevelFilter,)
    search_fields = ['elderly__first_name', 'elderly__last_name']


class HomeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Home, HomeAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Caregiver, CaregiverAdmin)
admin.site.register(CaregiverLevel, CaregiverLevelAdmin)

