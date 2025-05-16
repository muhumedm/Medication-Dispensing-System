from django import forms
from .models import Patient
from datetime import date

class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'placeholder': 'DD/MM/YYYY',
            'type': 'text',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Patient
        fields = ['patient_id', 'name', 'date_of_birth', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'date_of_birth':
                field.widget.attrs.update({'class': 'form-control'})

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return date_of_birth
