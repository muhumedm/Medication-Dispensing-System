from django.core.management.base import BaseCommand
from medications.models import Medication, MedicationDose
from datetime import datetime, timedelta, datetime as dt
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Auto-generates MedicationDose entries for all active medications (handles multiple times per day)'

    def handle(self, *args, **kwargs):
        today = datetime.now().date()
        days_ahead = 30
        total_created = 0
        total_skipped = 0

        for med in Medication.objects.all():
            if not med.medication_start_date:
                continue

            # Skip if medication ends before today
            if med.medication_end_date and med.medication_end_date < today:
                continue

            # Split multiple times (e.g., "08:00 20:00")
            raw_times = med.dosage_time.strip().replace(',', ' ').split()
            time_objects = []

            for time_str in raw_times:
                try:
                    parsed_time = dt.strptime(time_str.strip(), "%H:%M").time()
                    time_objects.append(parsed_time)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f"Skipping time '{time_str}' for med {med.medication_id}: {e}"
                    ))

            if not time_objects:
                self.stdout.write(self.style.WARNING(
                    f"Skipping medication {med.medication_id}: No valid times found."
                ))
                continue

            for i in range(days_ahead):
                scheduled_date = today + timedelta(days=i)
                if med.medication_end_date and scheduled_date > med.medication_end_date:
                    continue
                if scheduled_date < med.medication_start_date:
                    continue

                for t in time_objects:
                    scheduled_datetime = make_aware(datetime.combine(scheduled_date, t))

                    # Avoid duplicates
                    exists = MedicationDose.objects.filter(
                        medication=med,
                        scheduled_time=scheduled_datetime
                    ).exists()

                    if not exists:
                        MedicationDose.objects.create(
                            medication=med,
                            scheduled_time=scheduled_datetime,
                            status='On Time',
                            notification_sent=False
                        )
                        total_created += 1
                    else:
                        total_skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"✓ Done. Created {total_created} doses. Skipped {total_skipped} existing ones."
        ))
