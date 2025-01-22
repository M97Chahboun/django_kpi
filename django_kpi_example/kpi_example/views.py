from django.shortcuts import render

from django.shortcuts import render
from django_kpi.models import KpiCard

def kpi_dashboards(request):
    context = {
        'cards': KpiCard.objects.all(),
    }
    return render(request, 'kpi/kpi_dashboards.html', context)