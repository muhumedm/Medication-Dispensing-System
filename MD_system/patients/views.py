from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Patient
from .forms import PatientForm
import random
import string
from django.db import connection

class PatientListView(ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'

class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patient_list')

    def form_invalid(self, form):
        print("Form is invalid:", form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        print("Form is valid:", form.cleaned_data)
        return super().form_valid(form)

class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patient_list')

    def form_invalid(self, form):
        print("Form is invalid:", form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        print("Form is valid:", form.cleaned_data)
        return super().form_valid(form)

class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'patients/patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        patient_id = self.object.patient_id

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE PatientID = %s", [patient_id])

        print(f"Deleted MySQL login for PatientID: {patient_id}")
        return super().delete(request, *args, **kwargs)
