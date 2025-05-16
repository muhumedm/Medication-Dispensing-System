from django.db import models
from django.utils.timezone import make_aware, get_current_timezone, now
from datetime import datetime, timezone
from django.apps import apps

from patients.models import Patient
from medtypes.models import MedicationType

class Medication(models.Model):
    medication_id = models.AutoField(primary_key=True, db_column='MedicationID')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='PatientID')
    health_condition = models.CharField(max_length=255, db_column='HealthCondition')
    med_type = models.ForeignKey(MedicationType, on_delete=models.SET_NULL, null=True, db_column='MedTypeID')
    dosage_time = models.CharField(max_length=50, db_column='DosageTime')  # Supports "08:00, 22:00"
    status = models.CharField(max_length=100, db_column='Status')
    colour = models.CharField(max_length=20, db_column='Colour', null=True, blank=True)
    medication_start_date = models.DateField(db_column='MedicationStartDate')
    medication_end_date = models.DateField(db_column='MedicationEndDate', null=True, blank=True)
    course_type = models.CharField(max_length=50, db_column='CourseType')
    notification_sent = models.BooleanField(db_column='NotificationSent', default=False)

    class Meta:
        db_table = 'Medication'
        managed = False  # External MySQL DB

    def __str__(self):
        return f"{self.med_type} for {self.patient.name}"

    def get_dosage_datetimes(self):
        """Returns a list of datetimes parsed from dosage_time (supports multiple times like '08:00, 22:00')."""
        try:
            now_base = datetime.now(timezone.utc)  # Current time in UTC
            time_strings = self.dosage_time.replace('.', ':').split(',')  # Replace '.' with ':' and split by commas
            datetimes = []  # List to hold datetime objects
            london = timezone('Europe/London')        

            for time_str in time_strings:
                time_str = time_str.strip()  # Remove any surrounding whitespace
                if time_str and ':' in time_str:  # Ensure the time is in 'HH:MM' format
                    hour, minute = map(int, time_str.split(':'))  # Split into hour and minute
                    dt = make_aware(now_base.replace(hour=hour, minute=minute, second=0, microsecond=0), london)                    
                    datetimes.append(dt)  # Add the datetime to the list
                else:
                    print(f"[Invalid time format for dosage_time: '{time_str}']")  # Invalid time format
                    return [make_aware(now_base, london)]

            return datetimes  # Return the list of valid datetimes
        except Exception as e:
            print(f"[Error parsing times: {self.dosage_time}] – {e}")  # Error handling
            return [make_aware(datetime.now(), timezone('Europe/London'))] 

    def save(self, *args, **kwargs):

        if self.medication_end_date:
            self.course_type = "Non-Chronic"
        else:
            self.course_type = "Chronic"

        # Save the medication itself
        super().save(*args, **kwargs)

        # Use apps.get_model to dynamically fetch the MedicationDose model
        MedicationDose = apps.get_model('medications', 'MedicationDose')
        from django.utils.timezone import now

        # Check if dosage time changed
        dosage_changed = False
        if self.pk:
            old = Medication.objects.get(pk=self.pk)
            if old.dosage_time != self.dosage_time:
                dosage_changed = True
        else:
            dosage_changed = True

        # If dosage time has changed, delete old doses and create new ones
        if dosage_changed:
            MedicationDose.objects.filter(
                medication=self,
                scheduled_time__gt=now(),
                status='Scheduled'
            ).delete()

            # Create new doses
            for dt in self.get_dosage_datetimes():
                MedicationDose.objects.create(
                    medication=self,
                    scheduled_time=dt,
                    status='Scheduled'
                )


class MedicationDose(models.Model):
    dose_id = models.AutoField(primary_key=True)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('On Time', 'On Time'),
        ('Missed', 'Missed'),
        ('Taken', 'Taken'),
        ('Taken On Time', 'Taken On Time'),
        ('Taken Late', 'Taken Late'),
        ('Scheduled', 'Scheduled'),
    ], default='Scheduled')
    notification_sent = models.BooleanField(default=False)
    actual_time_taken = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'MedicationDose'
        managed = True

    def __str__(self):
        return f"{self.medication.med_type} for {self.medication.patient.name} at {self.scheduled_time} - {self.status}"

    def save(self, *args, **kwargs):
        if self.scheduled_time and self.scheduled_time.tzinfo is None:
            self.scheduled_time = make_aware(self.scheduled_time, get_current_timezone())

        if self.status not in ['Taken On Time', 'Taken Late']:
            self.status = "Scheduled"
            self.actual_time_taken = None

        super().save(*args, **kwargs)
