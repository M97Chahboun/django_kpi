from django.db import models
from django.apps import apps
from django.utils.html import format_html
from .utils import KPIQueryHelper
from django_icon_picker.field import IconField
class KPI(models.Model):
    """
    Main KPI model with comparison conditions
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, help_text="Optional description of the KPI")
    model_field = models.CharField(
        max_length=100,
        verbose_name="Model"
    )

    def __str__(self):
        return self.model_field
    
    
    def get_queryset(self, condition, target_field, target_value):
        """Get the queryset based on the condition and target"""
        app, model_name = self.model_field.split(".")
        queryset = apps.get_model(app, model_name).objects
        helper = KPIQueryHelper()
        return helper.apply_condition(queryset, condition, target_field, target_value)
    

    class Meta:
        verbose_name = "KPI"
        verbose_name_plural = "KPIs"


class Card(models.Model):
    """
    Card visualization for KPI with one-to-one relationship
    """
    TEXT_CONDITION_CHOICES = [
        ('EXACT', 'Exactly matches'),
        ('CONTAINS', 'Contains'),
        ('NOT_EXACT', 'Does not exactly match'),
        ('NOT_CONTAINS', 'Does not contain'),
    ]
    NUM_CONDITION_CHOICES = [
        ('GT', 'Greater Than'),
        ('LT', 'Less Than'),
        ('EQ', 'Equal'),
        ('GTE', 'Greater Than or Equal'),
        ('LTE', 'Less Than or Equal'),
        ('BETWEEN', 'Between'),
    ]
    CONDITION_CHOICES = [
        ('TEXT', TEXT_CONDITION_CHOICES),
        ('NUM', NUM_CONDITION_CHOICES),
        ('NONE', 'None'),
    ]
    OPERATION_CHOICES = [
        ('count', 'Count'),
        ('count_distinct', 'Count Distinct'),
        ('sum', 'Sum'),
        ('avg', 'Average'),
        ('min', 'Minimum'),
        ('max', 'Maximum'),
    ]
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='card')
    name = models.CharField(max_length=100, help_text="Name of the card")
    description = models.TextField(blank=True, help_text="Optional description of the card")
    icon = IconField(max_length=50, help_text="Icon class or name")
    value_suffix = models.CharField(max_length=50, blank=True, help_text="Suffix to append to the value (e.g., %, $)")
    operation = models.CharField(max_length=16, choices=OPERATION_CHOICES, default='count')
    target_type = models.CharField(
        max_length=20,
        default='NUMBER',
        help_text="Type of the target value"
    )
    target_field = models.CharField(
        max_length=100,
        blank=True,
        help_text="Field to compare against target value"
    )
    condition = models.CharField(
        max_length=20, 
        choices=CONDITION_CHOICES,
        default='EXACT'
    )
    target_value = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Target value to achieve"
    )

    def svg_icon(self):
        return format_html(
            '<img src="{}" height="30" width="30"/>'.format(
                f"/{self.icon}"
                if self.icon.endswith(".svg")
                else f"https://api.iconify.design/{self.icon}.svg"
            )
        )

    @property
    def value(self):
        queryset = self.kpi.get_queryset(self.condition, self.target_field, self.target_value)

        if self.operation == 'count':
            return queryset.count()
        elif self.operation == 'count_distinct':
            return queryset.values(self.target_field).distinct().count()  
        elif self.operation == 'sum':
            return queryset.aggregate(models.Sum(self.target_field)).get(f'{self.target_field}__sum', 0) or 0
        elif self.operation == 'average':
            return queryset.aggregate(models.Avg(self.target_field)).get(f'{self.target_field}__avg', 0) or 0
        elif self.operation == 'min':
            return queryset.aggregate(models.Min(self.target_field)).get(f'{self.target_field}__min', 0) or 0
        elif self.operation == 'max':
            return queryset.aggregate(models.Max(self.target_field)).get(f'{self.target_field}__max', 0) or 0


    def __str__(self):
        return f"Card for {self.kpi.name}"


# class Table(models.Model):
#     """
#     Table visualization for KPI
#     """
#     kpi = models.OneToOneField(KPI, on_delete=models.CASCADE, related_name='table')
#     fields = models.JSONField(help_text="List of fields to display in table")
#     sort_by = models.CharField(max_length=100)
#     page_size = models.IntegerField(default=10)
#     is_paginated = models.BooleanField(default=True)

#     def __str__(self):
#         return f"Table for {self.kpi.name}"


# class Tile(models.Model):
#     """
#     Tile visualization for KPI
#     """
#     kpi = models.OneToOneField(KPI, on_delete=models.CASCADE, related_name='tile')
#     fields = models.JSONField(help_text="List of fields to display in tile")
#     layout = models.CharField(max_length=50, default='grid')
#     columns = models.IntegerField(default=3)

#     def __str__(self):
#         return f"Tile for {self.kpi.name}"


# class Chart(models.Model):
#     """
#     Chart visualization for KPI
#     """
#     CHART_TYPES = [
#         ('line', 'Line Chart'),
#         ('bar', 'Bar Chart'),
#         ('pie', 'Pie Chart'),
#         ('doughnut', 'Doughnut Chart'),
#         ('area', 'Area Chart'),
#     ]

#     kpi = models.OneToOneField(KPI, on_delete=models.CASCADE, related_name='chart')
#     chart_type = models.CharField(max_length=20, choices=CHART_TYPES)
#     field = models.CharField(max_length=100)
#     time_range = models.CharField(max_length=50, default='last_30_days')
#     show_legend = models.BooleanField(default=True)

#     def __str__(self):
#         return f"Chart for {self.kpi.name}"


# class Progress(models.Model):
#     """
#     Progress visualization for KPI
#     """
#     kpi = models.OneToOneField(KPI, on_delete=models.CASCADE, related_name='progress')
#     fields = models.JSONField(help_text="List of fields to track progress")
#     target_value = models.FloatField()
#     min_value = models.FloatField(default=0)
#     max_value = models.FloatField(default=100)
#     display_percentage = models.BooleanField(default=True)
#     color_scheme = models.CharField(max_length=50, default='default')

#     def __str__(self):
#         return f"Progress for {self.kpi.name}"