from django.urls import path
from . import views

urlpatterns = [
    path('get-model-fields/', views.get_model_fields, name='get_model_fields'),
    path('get-field-values/', views.get_field_values, name='get_field_values'),
    path('update-card-position/', views.update_card_position, name='update_card_position'),
]