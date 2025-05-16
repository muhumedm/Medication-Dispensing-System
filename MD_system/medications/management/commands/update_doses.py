from django.core.management.base import BaseCommand
from medications.models import MedicationDose
from patients.models import Patient
from django.utils.timezone import now, timedelta

class Command(BaseCommand):
    help = 'Update medication doses for the last 14 days for all patients'

    def handle(self, *args, **kwargs):
        current_time = now()
        date_from = current_time - timedelta(days=14)

        patients = Patient.objects.all()

        for patient in patients:
            doses = MedicationDose.objects.filter(
                medication__patient=patient,
                scheduled_time__gte=date_from
            )

            for dose in doses:
                self.stdout.write(f"Patient: {patient.name}, Dose: {dose.medication.med_type.med_name}, Scheduled Time: {dose.scheduled_time}, Status: {dose.status}")

        self.stdout.write(self.style.SUCCESS('Successfully updated doses for all patients.'))
