from django.shortcuts import render

from django.shortcuts import render
from django_kpi.models import Card

def kpi_dashboards(request):
    context = {
        'cards': Card.objects.all(),
    }
    return render(request, 'kpi/kpi_dashboards.html', context)