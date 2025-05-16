from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
import pytz

from .models import Medication, MedicationDose

@receiver(post_save, sender=Medication)
def create_doses_for_medication(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        times = [t.strip() for t in instance.dosage_time.split(',')]
        current_date = instance.medication_start_date
        end_date = instance.medication_end_date or instance.medication_start_date

        while current_date <= end_date:
            for t in times:
                hour, minute = map(int, t.split(':'))
                dt = datetime.combine(current_date, datetime.min.time()).replace(hour=hour, minute=minute)

                # Optional timezone
                tz = pytz.timezone('UTC')
                dt = tz.localize(dt)

                MedicationDose.objects.create(
                    medication=instance,
                    scheduled_time=dt,
                    status='On Time',
                )
            current_date += timedelta(days=1)

    except Exception as e:
        print(f"Error creating doses: {e}")

