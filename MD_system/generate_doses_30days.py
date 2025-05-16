from medications.models import Medication, MedicationDose
from django.utils.timezone import make_aware, now
from datetime import datetime, timedelta

all_meds = Medication.objects.all()
created = 0

for med in all_meds:
    if med.dosage_time:
        try:
            times = [t.strip() for t in med.dosage_time.split(',')]
            for t in times:
                time_obj = datetime.strptime(t, "%H:%M").time()

                for i in range(30):  # today + next 29 days
                    date_obj = (now() + timedelta(days=i)).date()
                    sched_time = make_aware(datetime.combine(date_obj, time_obj))

                    if not MedicationDose.objects.filter(medication=med, scheduled_time=sched_time).exists():
                        MedicationDose.objects.create(
                            medication=med,
                            scheduled_time=sched_time,
                            status='Scheduled'
                        )
                        created += 1
        except ValueError:
            print(f" Invalid time format: {med.dosage_time} for med {med.medication_id}")

print(f"Created {created} new Scheduled MedicationDose entries.")
