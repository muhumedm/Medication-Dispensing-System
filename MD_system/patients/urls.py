from django.urls import path
from .views import (
    PatientListView,
    PatientCreateView,
    PatientUpdateView,
    PatientDeleteView,
)

urlpatterns = [
    path('', PatientListView.as_view(), name='patient_list'),
    path('add/', PatientCreateView.as_view(), name='patient_add'),
    path('<str:pk>/edit/', PatientUpdateView.as_view(), name='patient_edit'),
    path('<str:pk>/delete/', PatientDeleteView.as_view(), name='patient_delete'),
]

