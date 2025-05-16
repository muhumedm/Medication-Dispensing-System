from medications.models import MedicationDose
from patients.models import Patient
from django.utils.timezone import now

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MD_system.settings')
django.setup()

print("Future Scheduled Doses per Patient:\n")

patients = Patient.objects.all()

data = []

for patient in patients:
    count = MedicationDose.objects.filter(
        medication__patient=patient,
        status='Scheduled',
        scheduled_time__gte=now()
    ).count()
    data.append((count, patient.patient_id, patient.name))

# Sort by count, highest first
for count, pid, name in sorted(data, reverse=True):
    if count > 0:
        print(f"{name} ({pid}) → {count} scheduled doses")
