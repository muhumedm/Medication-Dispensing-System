from django.contrib import admin

# Register your models here.

from .models import Medication, MedicationDose

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('medication_id', 'patient', 'med_type')  # removed condition_type

@admin.register(MedicationDose)
class MedicationDoseAdmin(admin.ModelAdmin):
    list_display = ('medication', 'scheduled_time', 'status')
    list_filter = ('status', 'scheduled_time')
    search_fields = ('medication__patient__name',)
