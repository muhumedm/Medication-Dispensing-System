from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from medications.models import Patient, Medication, MedicationDose

class Command(BaseCommand):
    help = "Restore Tess Dunn's medication doses for the next 30 days"

    def handle(self, *args, **kwargs):
        try:
            tess = Patient.objects.get(name__icontains="Tess Dunn")
        except Patient.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tess Dunn not found."))
            return

        medications = Medication.objects.filter(patient=tess)
        today = datetime.now().date()

        for med in medications:
            times = [t.strip() for t in med.dosage_time.split(",") if t.strip()]

            for i in range(0, 30):
                med_date = today + timedelta(days=i)

                for time_str in times:
                    try:
                        dt = datetime.strptime(f"{med_date} {time_str}", "%Y-%m-%d %H:%M")
                        aware_dt = make_aware(dt)

                        exists = MedicationDose.objects.filter(
                            medication=med,
                            scheduled_time=aware_dt
                        ).exists()

                        if not exists:
                            MedicationDose.objects.create(
                                medication=med,
                                scheduled_time=aware_dt,
                                status="Scheduled"
                            )
                            self.stdout.write(self.style.SUCCESS(
                                f"Created dose for {med.med_type.med_name} at {aware_dt}"
                            ))
                        else:
                            self.stdout.write(
                                f"Skipped existing dose for {med.med_type.med_name} at {aware_dt}"
                            )

                    except Exception as e:
                        self.stdout.write(self.style.WARNING(
                            f"Error parsing time '{time_str}': {e}"
                        ))

        self.stdout.write(self.style.SUCCESS("Tess Dunn's doses restored."))
