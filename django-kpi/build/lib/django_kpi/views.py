# views.py
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET
from django.apps import apps
from .models import Card
@require_GET
@staff_member_required
def get_model_fields(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    model_name = request.GET.get('model')
    try:
        app_label, model_name = model_name.split('.')
        model = apps.get_model(app_label, model_name)
        
        fields = []
        for field in model._meta.fields:
            # TODO: Handle relationship fields
            if field.is_relation:
                continue
            fields.append({
                'name': field.name,
                'verbose_name': str(field.verbose_name).title(),
                'type': field.get_internal_type()
            })
        
        return JsonResponse({'fields': fields})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



@require_GET
@staff_member_required
def get_field_values(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    model_name = request.GET.get('model')
    field_name = request.GET.get('field')
    
    try:
        app_label, model_name = model_name.split('.')
        model = apps.get_model(app_label, model_name)
                
        # Get distinct values
        values = list(model.objects.values_list(field_name, flat=True).distinct())
        
        # Convert all values to strings for consistent display
        values = [str(v) for v in values if v is not None]
        
        return JsonResponse({
            'values': values
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def dashboard_callback(request, context):
    cards = Card.objects.all()
    context.update({"cards": cards})
    return context