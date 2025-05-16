from django.urls import path
from . import views
from .views import (
    MedicationListView,
    MedicationDetailView,
    MedicationCreateView,
    MedicationUpdateView,
    MedicationDeleteView,
    PatientMedicationListView,
    confirm_dose,
    api_due_doses,
    api_confirm_dose,
    dose_chart
)

urlpatterns = [
    path('', MedicationListView.as_view(), name='medication_list'),
    path('<int:pk>/', MedicationDetailView.as_view(), name='medication_detail'),
    path('add/', MedicationCreateView.as_view(), name='medication_create'),
    path('<int:pk>/edit/', MedicationUpdateView.as_view(), name='medication_update'),
    path('<int:pk>/delete/', MedicationDeleteView.as_view(), name='medication_delete'),
    path('mine/', PatientMedicationListView.as_view(), name='patient_medications'),
    path('dose/<int:dose_id>/confirm/', confirm_dose, name='confirm_dose'),

    # Raspberry Pi API
    path('api/due-doses/', api_due_doses, name='api_due_doses'),
    path('api/confirm-dose/', api_confirm_dose, name='api_confirm_dose'),

    # Chart
    path('dose-chart/', dose_chart, name='dose_chart'),
]
