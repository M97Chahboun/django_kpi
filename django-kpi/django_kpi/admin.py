from django.contrib import admin
from .models import KPI, Card
from .forms import KPIAdminForm, CardAdminForm

@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    form = KPIAdminForm
    list_display = ('name', 'model_field')
    list_filter = ('model_field',)
    search_fields = ('name',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    form = CardAdminForm
    list_display = ['svg_icon', 'name', 'kpi', 'operation', 'target_field', 'condition', 'target_value', 'result']
    list_filter = ['kpi', 'operation', 'condition']
    search_fields = ['name', 'kpi__name', 'description']
    fieldsets = (
        (None, {'fields': ('kpi', 'name', 'description', 'icon')}),
        ('Value Settings', {'fields': ('value_suffix', 'operation')}),
        ('Target Settings', {'fields': ('target_type', 'target_field', 'condition', 'target_value')}),
    )

    def result(self, instance: Card):
        return instance.value
    
    class Media:
        js = (
            'js/kpi_admin.js',
        )