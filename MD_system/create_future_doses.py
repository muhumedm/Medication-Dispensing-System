from medications.models import Patient, Medication, MedicationDose
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

patients = Patient.objects.all()
days_ahead = 30  # Number of days to plan ahead

for patient in patients:
    meds = Medication.objects.filter(patient=patient)

    for med in meds:
        times = [t.strip() for t in med.dosage_time.split(",") if t.strip()]

        for day in range(1, days_ahead + 1):  # Start from 1 = tomorrow
            target_date = datetime.now().date() + timedelta(days=day)

            for t in times:
                try:
                    dt = datetime.strptime(f"{target_date} {t}", "%Y-%m-%d %H:%M")
                    aware_dt = make_aware(dt)

                    # Avoid creating duplicates
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
                        print(f"✅ Created dose for {patient.name} on {aware_dt}")
                except Exception as e:
                    print(f"❌ Error creating dose for {patient.name} at {t}: {e}")
