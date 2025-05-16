from medications.models import MedicationDose
from django.db.models import Count

# Find duplicate dose entries based on medication + scheduled_time
dupes = MedicationDose.objects.values('medication_id', 'scheduled_time') \
    .annotate(dose_count=Count('dose_id')) \
    .filter(dose_count__gt=1)

deleted = 0

# Priority: On Time > Late > Missed > Scheduled
def status_priority(status):
    return {
        'Taken On Time': 0,
        'Taken Late': 1,
        'Missed': 2,
        'Scheduled': 3
    }.get(status, 99)

for dup in dupes:
    doses = list(
        MedicationDose.objects.filter(
            medication_id=dup['medication_id'],
            scheduled_time=dup['scheduled_time']
        )
    )

    doses.sort(key=lambda d: status_priority(d.status))
    to_keep = doses[0]
    to_delete = doses[1:]

    for d in to_delete:
        d.delete()
        deleted += 1

print(f"\n Deleted {deleted} duplicate dose entries")
