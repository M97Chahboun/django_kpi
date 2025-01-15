# Suggested code may be subject to a license. Learn more: ~LicenseLog:4141344616.
from django import forms

from .utils import get_available_models
from .models import KPI, Card
# from core.widgets import IconPicker
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

class KPIAdminForm(forms.ModelForm):
    """
    Custom form for KPIAdmin
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set choices dynamically in form initialization
        self.fields['model_field'] = forms.ChoiceField(
            choices=[('', '--- Select Model ---')] + get_available_models(),
            required=True,
            widget=forms.Select
        )

    class Meta:
        model = KPI
        fields = '__all__'

class CardAdminForm(forms.ModelForm):
    """
    Custom form for CardAdmin
    """
    # icon = forms.CharField(widget=IconPicker())
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['target_type'].widget = forms.HiddenInput()
        self.fields['target_field'] = forms.CharField(
            required=True,
            widget=forms.Select(choices=[(self.instance.target_field, self.instance.target_field)],),
        )
        self.fields['target_value'] = forms.CharField(
            required=False,
            widget=forms.Select(choices=[(self.instance.target_value, self.instance.target_value)],),
        )
        self.fields["icon"].widget.attrs["model"] = self._meta.model.__name__
        if self.instance and self.instance.pk:
            object_id = self.instance.pk
            self.fields["icon"].widget.attrs["objectid"] = object_id
        else:
            last_item_id = (
                Card.objects.last().id if Card.objects.exists() else 1
            )
            next_id = last_item_id + 1
            self.fields["icon"].widget.attrs["objectid"] = next_id

    def clean(self):
        cleaned_data = super().clean()
        target_type = cleaned_data.get('target_type')
        target_value = cleaned_data.get('target_value')
        operation = cleaned_data.get('operation')
        condition = cleaned_data.get('condition')

        # Validate that target_value is present if condition is not NONE
        if condition != "NONE" and not target_value:
            raise ValidationError(_("Target value is required when a condition is selected."))

        # Validate operation against target_type
        if target_type and operation:
            is_numeric_field = issubclass(getattr(models, target_type), (models.IntegerField, models.FloatField, models.DecimalField))
            if not is_numeric_field and operation in ['sum', 'avg', 'max', 'min']:
                raise ValidationError(_(
                    f"Invalid operation '{operation}' for field type '{target_type}'. "
                    f"Choose 'count' or 'count_distinct' for non-numeric fields."
                ))
            
        # Validate condition against target_type 
        if target_type and condition.lower() in ['gt', 'gte', 'lt', 'lte', 'eq', 'between']:
            is_numeric_or_datetime_field = issubclass(
                getattr(models, target_type), 
                (models.IntegerField, models.FloatField, models.DecimalField, models.DateTimeField)
            )
            if not is_numeric_or_datetime_field:
                raise ValidationError(_(f"Comparison operations are not supported for '{target_type}' fields."))

        return cleaned_data
        

    class Meta:
        model = Card
        fields = '__all__'