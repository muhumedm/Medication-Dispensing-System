from medications.models import Medication, MedicationDose
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

abir_meds = Medication.objects.filter(patient__patient_id='A001')

time_status_map = {
    "08:00": "Taken On Time",
    "22:00": "Taken Late",
    "16:24": "Missed"
}

created = 0

for med in abir_meds:
    for t_str, status in time_status_map.items():
        time_obj = datetime.strptime(t_str, "%H:%M").time()

        for days_ago in range(1, 4):
            date_obj = (datetime.now() - timedelta(days=days_ago)).date()
            sched_time = make_aware(datetime.combine(date_obj, time_obj))

            if not MedicationDose.objects.filter(medication=med, scheduled_time=sched_time).exists():
                dose = MedicationDose(
                    medication=med,
                    scheduled_time=sched_time,
                    status=status
                )

                if status != "Missed":
                    mins = 2 if status == "Taken On Time" else 15
                    dose.actual_time_taken = sched_time + timedelta(minutes=mins)

                dose.save()
                created += 1
                print(f"✅ Created {status} dose for {med.med_type.med_name} on {sched_time}")

print(f"\n✅ Done! Created {created} new past doses.")
