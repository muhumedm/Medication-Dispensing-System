from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import localtime

def send_email_alert(dose):
    subject = f"Medication Taken: {dose.medication.med_type.med_name} by {dose.medication.patient.name}"
    message = f"""
Dear Carer,

This is to inform you that the following medication was confirmed as taken:

- Patient: {dose.medication.patient.name}
- Medication: {dose.medication.med_type.med_name}
- Status: {dose.status}
- Scheduled Time: {localtime(dose.scheduled_time).strftime('%Y-%m-%d %H:%M')}
- Time Taken: {localtime(dose.actual_time_taken).strftime('%Y-%m-%d %H:%M')}

Best regards,
Medication Reminder System
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['muhumed579@gmail.com'],
        fail_silently=False,
    )


def send_missed_alert(dose):
    subject = f"Missed Medication Alert: {dose.medication.med_type.med_name} for {dose.medication.patient.name}"
    message = f"""
Dear Carer,

This is to inform you that the following dose has been missed:

- Patient: {dose.medication.patient.name}
- Medication: {dose.medication.med_type.med_name}
- Scheduled Time: {localtime(dose.scheduled_time).strftime('%Y-%m-%d %H:%M')}

Please follow up with the patient as appropriate.

Best regards,
Medication Reminder System
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['muhumed579@gmail.com'],
        fail_silently=False,
    )
