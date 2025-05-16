import django
import os
from datetime import datetime

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MD_system.settings")
django.setup()

from django.utils.timezone import make_aware, get_current_timezone
from medications.models import MedicationDose

tz = get_current_timezone()
updated = 0

# Loop through all doses and fix timezone if needed
for dose in MedicationDose.objects.all():
    sched = dose.scheduled_time

    if sched is not None:
        # If time is naive, make it aware using the current timezone
        if sched.tzinfo is None:
            dose.scheduled_time = make_aware(sched, tz)
            dose.save()
            updated += 1
        # If it's already aware but still needs converting to current timezone
        elif sched.tzinfo.utcoffset(sched) == datetime.utcnow().astimezone().utcoffset():
            dose.scheduled_time = sched.astimezone(tz)
            dose.save()
            updated += 1

print(f"Done. Updated {updated} MedicationDose entries.")
