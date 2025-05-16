from django.urls import path
from . import views
from .views import patient_dose_chart_view

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('carer/', views.carer_dashboard, name='carer_dashboard'),
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('carer/doses/', views.carer_dose_history, name='carer_doses'),
    path('patient/doses/', views.patient_doses, name='patient_doses'),
    path('scheduled-doses/', views.scheduled_doses, name='scheduled_doses'),
    path('patient/chart/', patient_dose_chart_view, name='patient_chart'),
    path('confirm-dose/<int:dose_id>/', views.confirm_dose, name='confirm_dose'),
]
