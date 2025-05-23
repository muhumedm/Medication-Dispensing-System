# Generated by Django 5.2 on 2025-04-17 15:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Medication",
            fields=[
                (
                    "medication_id",
                    models.AutoField(
                        db_column="MedicationID", primary_key=True, serialize=False
                    ),
                ),
                (
                    "health_condition",
                    models.CharField(db_column="HealthCondition", max_length=255),
                ),
                (
                    "dosage_time",
                    models.CharField(db_column="DosageTime", max_length=50),
                ),
                ("status", models.CharField(db_column="Status", max_length=100)),
                (
                    "colour",
                    models.CharField(
                        blank=True, db_column="Colour", max_length=20, null=True
                    ),
                ),
                (
                    "medication_start_date",
                    models.DateField(db_column="MedicationStartDate"),
                ),
                (
                    "medication_end_date",
                    models.DateField(
                        blank=True, db_column="MedicationEndDate", null=True
                    ),
                ),
                (
                    "course_type",
                    models.CharField(db_column="CourseType", max_length=50),
                ),
                (
                    "notification_sent",
                    models.BooleanField(db_column="NotificationSent", default=False),
                ),
            ],
            options={
                "db_table": "Medication",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MedicationDose",
            fields=[
                ("dose_id", models.AutoField(primary_key=True, serialize=False)),
                ("scheduled_time", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[("On Time", "On Time"), ("Missed", "Missed")],
                        max_length=20,
                    ),
                ),
                ("notification_sent", models.BooleanField(default=False)),
                (
                    "medication",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medications.medication",
                    ),
                ),
            ],
            options={
                "db_table": "MedicationDose",
                "managed": True,
            },
        ),
    ]
