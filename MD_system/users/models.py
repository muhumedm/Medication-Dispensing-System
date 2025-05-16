from django.db import models

class User(models.Model):
    userid = models.AutoField(primary_key=True, db_column='UserID')
    username = models.CharField(max_length=100, db_column='Username')
    password = models.CharField(max_length=255, db_column='Password')
    role = models.CharField(max_length=10, db_column='Role')
    patient_id = models.CharField(max_length=10, db_column='PatientID', null=True)

    class Meta:
        db_table = 'Users'
        managed = False

    def __str__(self):
        return f"{self.username} ({self.role})"

