from django.utils.timezone import now, timedelta
from medications.models import Patient, MedicationDose

today = now()
end_date = today + timedelta(days=30)

print("\n📅 Upcoming Scheduled Doses (Next 30 Days):\n")

for patient in Patient.objects.all():
    doses = MedicationDose.objects.filter(
        medication__patient=patient,
        status='Scheduled',
        scheduled_time__range=(today, end_date)
    ).order_by('scheduled_time')

    if doses.exists():
        print(f"🧍 {patient.patient_id} ({patient.name}) → {doses.count()} dose(s):")
        for d in doses:
            med_name = d.medication.med_type.med_name
            print(f"   - {med_name} @ {d.scheduled_time}")
    else:
        print(f"⚠️ {patient.patient_id} ({patient.name}) → No scheduled doses.")
