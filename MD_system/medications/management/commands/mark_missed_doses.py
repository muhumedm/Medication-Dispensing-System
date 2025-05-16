from django.core.management.base import BaseCommand
from django.utils import timezone
from medications.models import MedicationDose
from medications.notifications.email_alerts import send_missed_alert  

class Command(BaseCommand):
    help = "Mark missed doses that are overdue and unconfirmed"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        missed_doses = MedicationDose.objects.filter(
            scheduled_time__lt=now,
            status__in=[None, '', 'Scheduled']
        )

        count = 0
        for dose in missed_doses:
            dose.status = 'Missed'
            dose.save()
            send_missed_alert(dose)  # send email alert
            count += 1

        self.stdout.write(self.style.SUCCESS(f" Marked {count} dose(s) as Missed."))
