from django.contrib import admin
from .models import KPI, KpiCard, ComponentPosition, KpiComponent
from .forms import KPIAdminForm, CardAdminForm

admin.site.index_template = "kpi/kpi_dashboards.html"


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    form = KPIAdminForm
    list_display = ("name", "model_field")
    list_filter = ("model_field",)
    search_fields = ("name",)

@admin.register(ComponentPosition)
class ComponentPositionAdmin(admin.ModelAdmin):
    list_display = ('component', 'x', 'y', 'w', 'h')
    list_filter = ('component',)
    search_fields = ('component__name',)


@admin.register(KpiCard)
class CardAdmin(admin.ModelAdmin):
    form = CardAdminForm
    list_display = [
        "svg_icon",
        "name",
        "kpi",
        "operation",
        "target_field",
        "condition",
        "target_value",
        "result",
        "published",
    ]
    list_filter = ["kpi", "operation", "condition", "published"]
    search_fields = ["name", "kpi__name", "description"]
    actions = [
        "publish_cards",
        "unpublish_cards",
        "reset_positions",
        "duplicate_cards",
    ]
    fieldsets = (
        (
            None,
            {"fields": ("kpi", "name", "description", "icon", "published")},
        ),
        ("Value Settings", {"fields": ("value_suffix", "operation")}),
        (
            "Target Settings",
            {
                "fields": (
                    "target_type",
                    "target_field",
                    "condition",
                    "target_value",
                )
            },
        ),
    )

    def result(self, instance: KpiCard):
        return instance.value

    def publish_cards(self, request, queryset):
        queryset.update(published=True)

    publish_cards.short_description = "Publish selected cards"

    def unpublish_cards(self, request, queryset):
        queryset.update(published=False)

    unpublish_cards.short_description = "Unpublish selected cards"

    def reset_positions(self, request, queryset):
        for card in queryset:
            position = card.position
            position.x = 0
            position.y = 0
            position.w = 2
            position.h = 1
            position.save()

    reset_positions.short_description = "Reset card positions"

    class Media:
        js = ("js/kpi_admin.js",)
