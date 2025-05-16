# Standard libraries
import json
import io
import base64
from datetime import date, datetime, timedelta, timezone

# matplotlib setup (non-GUI mode)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Django modules
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.timezone import now, make_aware, localtime, is_naive
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models

# Project imports
from .models import Medication
from .forms import MedicationForm
from medications.models import MedicationDose
from medications.notifications.email_alerts import send_email_alert

class MedicationListView(ListView):
    model = Medication
    template_name = 'medications/medication_list.html'
    context_object_name = 'medications'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('username'):
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.session['role'] == 'Carer':
            return Medication.objects.all()
        return Medication.objects.filter(patient_id=self.request.session['patient_id'])


class MedicationDetailView(DetailView):
    model = Medication
    template_name = 'medications/medication_detail.html'
    context_object_name = 'medication'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('username'):
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class MedicationCreateView(CreateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'medications/medication_form.html'
    success_url = reverse_lazy('medication_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('username') or request.session.get('role') != 'Carer':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context


class MedicationUpdateView(UpdateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'medications/medication_form.html'
    success_url = reverse_lazy('medication_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('username') or request.session.get('role') != 'Carer':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context
    
    def form_valid(self, form):
        print(f"[DEBUG] Editing medication: {form.instance} ")
        medication = form.save()

        # Delete existing doses
        MedicationDose.objects.filter(
            medication=medication,
            scheduled_time__gt=datetime.now(),
            actual_time_taken__isnull=True
        ).delete()

        # Get dosage times from cleaned form data
        times = [t.strip() for t in form.cleaned_data['dosage_time'].split(",") if t.strip()]
        today = datetime.now().date()
        
        print(f"[DEBUG] Raw form.cleaned_data keys: {form.cleaned_data.keys()}")
        print(f"[DEBUG] dosage_time: {form.cleaned_data.get('dosage_time')}")

        for t in times:
            try:
                dt = datetime.strptime(f"{today} {t}", "%Y-%m-%d %H:%M")
                aware_dt = make_aware(dt)
                print(f"[DEBUG] Processing time '{t}' → aware datetime: {aware_dt}")

                existing = MedicationDose.objects.filter(
                    medication=medication,
                    scheduled_time=aware_dt
                ).exists()

                if not existing:
                    MedicationDose.objects.create(
                        medication=medication,
                        scheduled_time=aware_dt,
                        status="Scheduled"
                    )
                    print(f"[DEBUG] Created dose for {aware_dt}")
                else:
                    print(f"[DEBUG] Skipped duplicate for {aware_dt}")
            except Exception as e:
                print(f"[ERROR] Could not create dose for time '{t}': {e}")

        print(f"[DEBUG] Medication and doses updated successfully.")
        return super().form_valid(form)

class MedicationDeleteView(DeleteView):
    model = Medication
    template_name = 'medications/medication_confirm_delete.html'
    success_url = reverse_lazy('medication_list')

    def dispatch(self, request, *args, **kwargs):
      if not request.session.get('username') or request.session.get('role') != 'Carer':
        return redirect('login')
      return super().dispatch(request, *args, **kwargs)

class PatientMedicationListView(ListView):
    model = Medication
    template_name = 'medications/patient_medications.html'
    context_object_name = 'medications'
            
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('username'):
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Medication.objects.filter(patient_id=self.request.session['patient_id'])
        

def confirm_dose(request, dose_id):
    if not request.session.get('username'):
        return redirect('login')
        
    try:
        dose = MedicationDose.objects.get(pk=dose_id)
        current_time = now()

        # Make timezone-aware
        if is_naive(dose.scheduled_time):
            dose.scheduled_time = make_aware(dose.scheduled_time)
        
        # Debug times
        print(f"Local Scheduled Time: {localtime(dose.scheduled_time)}")
        print(f"Local Current Time: {localtime(current_time)}")

        # Confirmation window
        window_start = dose.scheduled_time - timedelta(hours=2)
        window_end = dose.scheduled_time + timedelta(hours=1)

        print(f"Window Start: {window_start}")
        print(f"Window End: {window_end}")

        if not (window_start <= current_time <= window_end):
            messages.error(request, "It's too early or too late to confirm this dose.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        # On-time or late
        if current_time <= dose.scheduled_time + timedelta(minutes=10):
            dose.status = 'Taken On Time'
        else:
            dose.status = 'Taken Late'

        dose.actual_time_taken = current_time
        dose.save()
        print(f"Saved status: {dose.status}, Confirmed at: {dose.actual_time_taken}")

        send_email_alert(dose)
        messages.success(request, f"Dose marked as '{dose.status}'.")

    except MedicationDose.DoesNotExist:
        messages.error(request, "Dose not found.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def dose_chart(request):
    # Fetch doses and aggregate by status
    doses = MedicationDose.objects.all()

    # Update statuses: Merge 'On Time' and 'Taken On Time'
    status_counts = doses.values('status').annotate(count=models.Count('dose_id'))

    # Merge "On Time" and "Taken On Time"
    merged_statuses = []
    merged_counts = []
    
    for status_item in status_counts:
        status = status_item['status']
        count = status_item['count']
        
        # Merge "On Time" and "Taken On Time" into a single category
        if status == "On Time" or status == "Taken On Time":
            status = "Taken On Time"
        
        if status not in merged_statuses:
            merged_statuses.append(status)
            merged_counts.append(count)
        else:
            index = merged_statuses.index(status)
            merged_counts[index] += count
    
    # Now `merged_statuses` contains the statuses we want to display
    statuses = merged_statuses
    counts = merged_counts

    # Define the colour map for the statuses
    colour_map = {
        'Missed': '#4A90E2',        # medium blue
        'Taken On Time': '#50E3C2', # aqua blue
        'Taken Late': '#007AFF',    # vivid blue
        'Scheduled': '#B2DFDB'      # light blue (matches navbar)
    }

    # Use the colour map for the chart
    colours = [colour_map.get(status, '#A0C4FF') for status in statuses]

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(statuses, counts, color=colours, edgecolor='black')
    plt.title('Medication Dose Statuses', fontsize=20)
    plt.xlabel('Status', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()

    # Save the plot to a buffer and convert to base64 for embedding
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'medications/dose_chart.html', {'graphic': graphic})

@csrf_exempt
def api_due_doses(request):
    """Returns doses scheduled within 2 hours before to 1 hour after now, if not taken yet."""
    if request.method == 'GET':
        now_utc = datetime.now(timezone.utc)
        start = now_utc - timedelta(hours=2)
        end = now_utc + timedelta(hours=1)

        doses = MedicationDose.objects.filter(
            scheduled_time__range=(start, end)
        ).exclude(status__in=['Taken On Time', 'Taken Late'])

        data = [{
            'id': dose.pk,
            'medication_name': dose.medication.med_type.med_name,
            'scheduled_time': dose.scheduled_time.isoformat(),
            'patient_id': dose.medication.patient.patient_id,
            'patient_name': dose.medication.patient.name,
        } for dose in doses]

        return JsonResponse(data, safe=False)

@csrf_exempt
def api_confirm_dose(request):
    """Updates a dose to 'Taken On Time' or 'Taken Late', and sends an email."""
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            dose_id = body.get('dose_id')

            dose = MedicationDose.objects.get(dose_id=dose_id)

            # Ensure both times are timezone-aware
            now_time = datetime.now(timezone.utc)
            scheduled_time = dose.scheduled_time

            if scheduled_time.tzinfo is not None:
                scheduled_time = scheduled_time.astimezone(timezone.utc)

            # Define allowed confirmation window
            window_start = scheduled_time - timedelta(hours=2)
            window_end = scheduled_time + timedelta(hours=1)

            if not (window_start <= now_time <= window_end):
                return JsonResponse({'success': False, 'error': 'Too early or too late to confirm this dose.'}, status=400)

            # Determine if it's on time or late
            if now_time <= scheduled_time + timedelta(minutes=10):
                dose.status = "Taken On Time"
            else:
                dose.status = "Taken Late"

            dose.actual_time_taken = now_time
            dose.save()

            send_email_alert(dose)

            return JsonResponse({'success': True, 'message': f'Dose {dose_id} confirmed as {dose.status}.'})

        except MedicationDose.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Dose not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
