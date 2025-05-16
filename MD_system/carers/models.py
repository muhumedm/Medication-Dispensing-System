from django.db import models
from patients.models import Patient

class Carer(models.Model):
    CarerID = models.AutoField(primary_key=True, db_column='CarerID')
    PatientID = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        db_column='PatientID',
        to_field='patient_id',
        null=True,
        blank=True
    )
    type_of_carer = models.CharField(max_length=50, db_column='TypeofCarer', null=True, blank=True)
    preferred_contact = models.CharField(max_length=50, db_column='PreferredContactMethod', null=True, blank=True)
    phone_number = models.CharField(max_length=20, db_column='PhoneNumber', null=True, blank=True)
    email = models.CharField(max_length=100, db_column='Email', null=True, blank=True)

    def __str__(self):
        return f"Carer {self.CarerID} for patient {self.PatientID}"
    
    class Meta:
        db_table = 'Carers'
        managed = False
