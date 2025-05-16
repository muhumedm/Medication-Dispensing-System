from medications.models import Medication
import re

fixed = 0
unfixed = []

for med in Medication.objects.all():
    original = med.dosage_time.strip()
    times = [t.strip() for t in original.split(',')]
    new_times = []

    valid = True
    for t in times:
        if re.match(r'^\d{2}:\d{2}$', t):
            new_times.append(t)
        elif re.match(r'^\d{2}\.\d{2}$', t):
            corrected = t.replace('.', ':')
            new_times.append(corrected)
        else:
            valid = False
            break

    if valid and new_times != times:
        med.dosage_time = ", ".join(new_times)
        med.save()
        print(f"✅ Fixed {med.medication_id} → {original} → {med.dosage_time}")
        fixed += 1
    elif not valid:
        print(f"❌ Could not fix: {med.medication_id} → {original}")
        unfixed.append((med.medication_id, original))

print(f"\n✅ Auto-fixed: {fixed}")
print(f"❌ Still invalid: {len(unfixed)}")
