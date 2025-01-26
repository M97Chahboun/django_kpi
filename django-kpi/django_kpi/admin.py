from django.contrib import admin
from .models import KPI, KpiCard, ComponentPosition
from .forms import KPIAdminForm, CardAdminForm

admin.site.index_template = "kpi/kpi_dashboards.html"

@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    form = KPIAdminForm
    list_display = ('name', 'model_field')
    list_filter = ('model_field',)
    search_fields = ('name',)

@admin.register(KpiCard)
class CardAdmin(admin.ModelAdmin):
    form = CardAdminForm
    list_display = ['svg_icon', 'name', 'kpi', 'operation', 'target_field', 'condition', 'target_value', 'result']
    list_filter = ['kpi', 'operation', 'condition']
    search_fields = ['name', 'kpi__name', 'description']
    fieldsets = (
        (None, {'fields': ('kpi', 'name', 'description', 'icon', 'position', 'published')}),
        ('Value Settings', {'fields': ('value_suffix', 'operation')}),
        ('Target Settings', {'fields': ('target_type', 'target_field', 'condition', 'target_value')}),
    )

    def result(self, instance: KpiCard):
        return instance.value
    
    class Media:
        js = (
            'js/kpi_admin.js',
        )

@admin.register(ComponentPosition)
class ComponentPositionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'x', 'y', 'w', 'h')
    search_fields = ('kpi_card__name',)