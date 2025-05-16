import io
import base64
import bcrypt
import random
import string
import matplotlib.pyplot as plt

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now, timedelta, localtime
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from .models import User
from .forms import CustomLoginForm

from patients.models import Patient
from medications.models import Medication, MedicationDose, MedicationType

class HomePageView(TemplateView):
    template_name = "home.html"

def login_view(request):
    form = CustomLoginForm()
    if request.method == 'POST':
        uname = request.POST['username']
        pword = request.POST['password']
        try:
            user = User.objects.get(username=uname)

            # Plaintext password comparison (no bcrypt)
            if user.password == pword:
                request.session['username'] = user.username
                request.session['role'] = user.role
                request.session['patient_id'] = user.patient_id

                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)

                if user.role == 'Carer':
                    return redirect('carer_dashboard')
                else:
                    return redirect('patient_dashboard')
            else:
                messages.error(request, 'Incorrect password')
        except User.DoesNotExist:
            messages.error(request, 'User not found')

    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    return redirect('login')

def carer_dashboard(request):
    confirmed = MedicationDose.objects.filter(
        status__in=["Taken On Time", "Taken Late"]
    ).select_related("medication__patient", "medication__med_type").order_by("-actual_time_taken")[:20]

    # 5 confirmed per page
    paginator = Paginator(confirmed, 5)
    page = request.GET.get("page")
    recent_confirmed = paginator.get_page(page)

    return render(request, 'users/carer_dashboard.html', {
        'username': request.session.get('username'),
        'recent_confirmed': recent_confirmed,
    })

def patient_dashboard(request):
    if request.session.get('role') != 'Patient':
        return redirect('login')

    patient_id = request.session.get('patient_id')
    print("Logged in patient:", patient_id)

    meds = Medication.objects.filter(patient_id=patient_id)

    return render(request, 'users/patient_dashboard.html', {
        'medications': meds,
        'username': request.session.get('username'),
    })


def carer_dose_history(request):
    if request.session.get('role') != 'Carer':
        return redirect('login')

    current_time = now()
    past_30_days = current_time - timedelta(days=30)

    #  Auto-update old scheduled/blank/null doses to 'Missed'
    MedicationDose.objects.filter(
        scheduled_time__lt=current_time,
        status__in=[None, 'Scheduled', '']
    ).update(status='Missed')

    #  Start with all doses
    doses = MedicationDose.objects.select_related(
        'medication__patient',
        'medication__med_type'
    )

    #  Optional filters
    patient_id = request.GET.get('patient')
    medication_filter = request.GET.get('medication')
    status_filter = request.GET.get('status')

    if status_filter == 'Missed':
        doses = doses.filter(
            status='Missed',
            scheduled_time__range=(past_30_days, current_time)
        )
    elif status_filter:
        doses = doses.filter(status=status_filter)

    # Always exclude future doses (optional safety)
    doses = doses.exclude(scheduled_time__gt=current_time)

    if patient_id:
        doses = doses.filter(medication__patient__patient_id=patient_id)
    if medication_filter:
        doses = doses.filter(medication__med_type__med_type_id=medication_filter)

    # Sort by latest taken/missed first
    doses = doses.order_by('-scheduled_time')

    #  Paginate
    paginator = Paginator(doses, 10)
    page = request.GET.get('page')
    try:
        doses = paginator.page(page)
    except PageNotAnInteger:
        doses = paginator.page(1)
    except EmptyPage:
        doses = paginator.page(paginator.num_pages)

    #  Render final view
    return render(request, 'users/carer_doses.html', {
        'doses': doses,
        'username': request.session.get('username'),
        'all_patients': Patient.objects.all(),
        'all_meds': MedicationType.objects.all(),
        'page_obj': doses
    })


from datetime import date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def patient_doses(request):
    if request.session.get('role') != 'Patient':
        return redirect('login')
    
    pid = request.session.get('patient_id')
    selected_med = request.GET.get('medication')
    status_filter = request.GET.get('status')
    
    meds = Medication.objects.filter(patient_id=pid)
    med_ids = meds.values_list('medication_id', flat=True)
    
    doses = MedicationDose.objects.filter(
        medication__medication_id__in=med_ids
    ).exclude(status='Scheduled')
    
    if status_filter:
        doses = doses.filter(status=status_filter)
    
    if selected_med:
        doses = doses.filter(medication__medication_id=selected_med)
    
    doses = doses.order_by('-scheduled_time')
    
    # allows patient to confirm dosage only current day 
    for dose in doses:
        if dose.status == "Missed" and dose.scheduled_time.date() == date.today():
            dose.allow_confirm = True
        else:
            dose.allow_confirm = False

    paginator = Paginator(doses, 10)
    page = request.GET.get('page')
    try:
        doses = paginator.page(page)
    except PageNotAnInteger:
        doses = paginator.page(1)
    except EmptyPage:
        doses = paginator.page(paginator.num_pages)
    
    return render(request, 'users/patient_doses.html', {
        'doses': doses,
        'username': request.session.get('username'),
        'medications': meds,
        'page_obj': doses
    })

def scheduled_doses(request):
    if request.session.get('role') != 'Carer':
        return redirect('login')
        
    # Get all future scheduled doses
    doses = MedicationDose.objects.filter(
        scheduled_time__gte=now(),
        status__iexact='Scheduled'  # Case-insensitive
    ).select_related('medication__patient', 'medication__med_type') 

    # Filters
    patient_id = request.GET.get('patient')
    med_id = request.GET.get('medication')   

    if patient_id:
        doses = doses.filter(medication__patient__patient_id=patient_id)
    if med_id:
        doses = doses.filter(medication__med_type__med_type_id=med_id)

    # Order by upcoming dose time
    doses = doses.order_by('scheduled_time')
    
    # Pagination
    paginator = Paginator(doses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert scheduled_time to local time (BST/GMT) for display only
    for dose in page_obj:
        dose.scheduled_time = localtime(dose.scheduled_time)

    return render(request, 'users/scheduled_doses.html', {
        'username': request.session.get('username'),
        'doses': page_obj,
        'page_obj': page_obj,
        'all_patients': Patient.objects.all(),
        'all_meds': MedicationType.objects.all(),
        'now': localtime(now()),  # For display comparison
    })

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def patient_dose_chart(request):
    from matplotlib import pyplot as plt
    from django.db.models import Count

    patient_id = request.session.get('patient_id')
    doses = MedicationDose.objects.filter(medication__patient__patient_id=patient_id)

    # Count statuses
    status_counts = doses.values('status').annotate(count=Count('dose_id'))

    # Ensure all statuses appear
    merged = {'Missed': 0, 'Taken On Time': 0, 'Taken Late': 0, 'Scheduled': 0}
    for item in status_counts:
        status = item['status']
        count = item['count']
        if status in ['Taken On Time', 'On Time']:
            merged['Taken On Time'] += count
        elif status in merged:
            merged[status] += count
        else:
            merged[status] = count  # Just in case any other label slipped in

    statuses = list(merged.keys())
    counts = list(merged.values())

    # Colour map
    colour_map = {
        'Missed': '#4A90E2',
        'Taken On Time': '#50E3C2',
        'Taken Late': '#007AFF',
        'Scheduled': '#B2DFDB',
    }
    colours = [colour_map.get(status, '#999') for status in statuses]

    # Plot chart
    plt.figure(figsize=(10, 6))
    plt.bar(statuses, counts, color=colours, edgecolor='black')
    plt.title('My Medication Progress', fontsize=22)
    plt.xlabel('Status', fontsize=18)
    plt.ylabel('Count', fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()

    # Encode image to display in template
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    return graphic


def patient_dose_chart_view(request):
    if request.session.get('role') != 'Patient':
        return redirect('login')
    
    chart_image = patient_dose_chart(request)  # Make sure this function exists above
    
    return render(request, 'users/patient_chart.html', {
        'chart': chart_image,
        'username': request.session.get('username'),
    })


def confirm_dose(request, dose_id):
    if request.method == 'POST':
        dose = get_object_or_404(MedicationDose, dose_id=dose_id)

        now_time = now()
        delay_minutes = abs((now_time - dose.scheduled_time).total_seconds()) / 60

        if delay_minutes <= 10:
            dose.status = 'Taken On Time'
        else:
            dose.status = 'Taken Late'

        dose.actual_time_taken = now_time
        dose.save()

        messages.success(request, "Dose confirmed successfully.")
    
    return redirect(request.META.get('HTTP_REFERER', 'patient_doses'))
