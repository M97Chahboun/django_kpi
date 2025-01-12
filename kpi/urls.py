from django.urls import path
from . import views

app_name = 'kpi'

urlpatterns = [
    path('kpi/get-model-fields/', views.get_model_fields, name='get_model_fields'),
    path('kpi/get-field-values/', views.get_field_values, name='get_field_values'),
]