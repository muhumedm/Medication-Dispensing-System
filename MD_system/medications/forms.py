from datetime import date
from django import forms
from .models import Medication

class MedicationForm(forms.ModelForm):
    medication_start_date = forms.DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'type': 'text',
            'placeholder': 'DD/MM/YYYY',
            'class': 'form-control'
        })
    )

    medication_end_date = forms.DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'text',
            'placeholder': 'DD/MM/YYYY',
            'class': 'form-control'
        })
    )

#    status = forms.ChoiceField(
 #       choices=[('Chronic', 'Chronic'), ('Non-Chronic', 'Non-Chronic')],
  #      label="Condition Type",
   #     widget=forms.Select(attrs={'class': 'form-control'})
   # )

    def clean_dosage_time(self):
        """Ensure dosage time is correctly formatted."""
        dosage_time = self.cleaned_data.get('dosage_time')
        if dosage_time:
            try:
                # Check if it contains valid times like '08:00' or '08:00, 22:00'
                time_strings = dosage_time.replace('.', ':').split(',')
                for time_str in time_strings:
                    time_str = time_str.strip()  # Strip any leading/trailing spaces
                    # Ensure the format is 'HH:MM'
                    hour, minute = map(int, time_str.split(':'))
                    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                        raise ValueError("Time must be between 00:00 and 23:59.")
                return dosage_time  # Return valid dosage_time if no errors
            except ValueError:
                raise forms.ValidationError("Invalid time format. Please use 'HH:MM' or 'HH:MM, HH:MM' format.")
        return dosage_time  # If no dosage_time, return the cleaned value

    class Meta:
        model = Medication
        exclude = ['status', 'colour', 'course_type', 'notification_sent']
