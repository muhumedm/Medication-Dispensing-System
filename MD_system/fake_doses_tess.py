from medications.models import Patient, Medication, MedicationDose
from django.utils.timezone import now, make_aware
from datetime import datetime, timedelta
import random

tess = Patient.objects.get(name__icontains='Tess Dunn')
meds = Medication.objects.filter(patient=tess)

statuses = ["Taken On Time", "Taken Late", "Missed"]
now_time = now()

for day in range(1, 31):
    for med in meds:
        scheduled_time = now_time - timedelta(days=day)
        scheduled_time = scheduled_time.replace(hour=8, minute=0, second=0, microsecond=0)

        status = random.choice(statuses)

        actual_time_taken = None
        if status != "Missed":
            delay = timedelta(minutes=random.randint(0, 30)) if status == "Taken Late" else timedelta(minutes=0)
            actual_time_taken = scheduled_time + delay

        MedicationDose.objects.create(
            medication=med,
            scheduled_time=scheduled_time,
            status=status,
            actual_time_taken=actual_time_taken
        )

print("✅ Fake dose history added for Tess Dunn for the past 30 days.")
