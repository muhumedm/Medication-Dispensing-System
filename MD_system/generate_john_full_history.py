from medications.models import Medication, MedicationDose
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

# Target John Doe
meds = Medication.objects.filter(patient__patient_id='P001', med_type__med_name='Omeprazole')
created = 0

# Define start and end dates
start_date = datetime.strptime("2025-04-04", "%Y-%m-%d").date()
end_date = datetime.now().date()

for med in meds:
    if med.dosage_time == "15:00":
        time_obj = datetime.strptime("15:00", "%H:%M").time()
        for d in range((end_date - start_date).days + 1):
            day = start_date + timedelta(days=d)
            sched_time = make_aware(datetime.combine(day, time_obj))

            if not MedicationDose.objects.filter(medication=med, scheduled_time=sched_time).exists():
                dose = MedicationDose(
                    medication=med,
                    scheduled_time=sched_time,
                    status="Taken On Time",
                    actual_time_taken=sched_time + timedelta(minutes=3)
                )
                dose.save()
                created += 1
                print(f" Created dose on {sched_time}")

print(f"\nDone! Created {created} past doses for John Doe (P001).")
