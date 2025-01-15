# utils.py
from django.apps import apps
from django.db.utils import OperationalError
from django.core.exceptions import AppRegistryNotReady
from datetime import datetime

def get_available_models():
    """
    Get all available models in the project excluding some built-in models
    Returns a list of tuples (model_name, verbose_name)
    """
    try:
        excluded_apps = ['admin', 'contenttypes', 'sessions', 'kpi']
        choices = []
        
        for model in apps.get_models():
            app_label = model._meta.app_label
            if app_label not in excluded_apps:
                model_name = f"{app_label}.{model._meta.model_name}"
                verbose_name = model._meta.verbose_name.title()
                choices.append((model_name, f"{verbose_name}"))
        
        return sorted(choices)
    except (AppRegistryNotReady, OperationalError):
        return []

class KPIQueryHelper:
    # TODO: Handle excepts using field type
    """
    Helper class to handle KPI query conditions
    """
    def apply_condition(self, queryset, condition, target_field, target_value):
        if condition == 'EXACT':
            return queryset.filter(**{f"{target_field}": target_value})
        elif condition == 'CONTAINS':
            return queryset.filter(**{f"{target_field}__icontains": target_value})
        elif condition == 'NOT_EXACT':
            return queryset.exclude(**{f"{target_field}": target_value})
        elif condition == 'NOT_CONTAINS':
            return queryset.exclude(**{f"{target_field}__icontains": target_value})
        elif condition in ['GT', 'LT', 'GTE', 'LTE', 'EQUAL']:
            try:
                target_value = datetime.strptime(target_value, '%Y-%m-%d').date()
            except ValueError:
                pass
            if condition == 'EQUAL':
                return queryset.filter(**{f"{target_field}": target_value}) 
            else:
                lookup = {
                    'GT': 'gt',
                    'LT': 'lt',
                    'GTE': 'gte',
                    'LTE': 'lte',
                }[condition]
                return queryset.filter(**{f"{target_field}__{lookup}": target_value})
        elif condition == 'BETWEEN':
            from_value, to_value = target_value.split(' to ')
            try:
                from_value = datetime.strptime(from_value.strip(), '%Y-%m-%d').date()
                to_value = datetime.strptime(to_value.strip(), '%Y-%m-%d').date()
            except (ValueError, IndexError):
                pass
            return queryset.filter(**{f"{target_field}__range": (from_value, to_value)})

        return queryset