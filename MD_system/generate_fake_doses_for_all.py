from medications.models import Patient, Medication, MedicationDose
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

excluded_ids = ['A001', 'a004']  # Abir Mohamed + muna

statuses = ['Missed', 'Taken On Time', 'Taken Late', 'Scheduled']
created = 0

# Start from 1st April 2025
start_date = datetime(2025, 4, 1)

for patient in Patient.objects.exclude(patient_id__in=excluded_ids):
    meds = Medication.objects.filter(patient=patient)

    for med in meds:
        if not med.dosage_time:
            continue
        
        times = [t.strip() for t in med.dosage_time.split(',')]
        
        for i in range(44):
            status = statuses[i % 4]
            date = start_date + timedelta(days=i)
            
            for t in times:
                try:
                    time_obj = datetime.strptime(t, "%H:%M").time()
                    sched_time = make_aware(datetime.combine(date.date(), time_obj))
                    
                    if MedicationDose.objects.filter(medication=med, scheduled_time=sched_time).exists():
                        continue

                    dose = MedicationDose(
                        medication=med,
                        scheduled_time=sched_time,
                        status=status
                    )

                    if status in ['Taken On Time', 'Taken Late']:
                        delay = 2 if status == 'Taken On Time' else 20
                        dose.actual_time_taken = sched_time + timedelta(minutes=delay)

                    dose.save()
                    created += 1
                    print(f"✅ {patient.patient_id} - {med.med_type.med_name} @ {sched_time} → {status}")
                except ValueError:
                    print(f"❌ Invalid time: {t} for {med.medication_id}")

print(f"\n🎉 Done! Created {created} historical doses.")
