from django.db import models

class MedicationType(models.Model):
    med_type_id = models.AutoField(primary_key=True, db_column='MedTypeID')
    med_name = models.CharField(max_length=100, db_column='MedName')

    class Meta:
        db_table = 'MedicationTypes'
        managed = False

    def __str__(self):
        return self.med_name

