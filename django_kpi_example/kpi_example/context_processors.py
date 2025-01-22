from django_kpi.models import KpiCard

def get_kpis(request):
    context = {
        'cards': KpiCard.objects.all(),
    }
    return context