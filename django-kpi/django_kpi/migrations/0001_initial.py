# Generated by Django 4.1.2 on 2025-01-12 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="KPI",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Optional description of the KPI"
                    ),
                ),
                ("model_field", models.CharField(max_length=100, verbose_name="Model")),
            ],
            options={
                "verbose_name": "KPI",
                "verbose_name_plural": "KPIs",
            },
        ),
        migrations.CreateModel(
            name="Card",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(help_text="Name of the card", max_length=100),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Optional description of the card"
                    ),
                ),
                (
                    "icon",
                    models.CharField(help_text="Icon class or name", max_length=50),
                ),
                (
                    "value_suffix",
                    models.CharField(
                        blank=True,
                        help_text="Suffix to append to the value (e.g., %, $)",
                        max_length=50,
                    ),
                ),
                (
                    "operation",
                    models.CharField(
                        choices=[
                            ("count", "Count"),
                            ("count_distinct", "Count Distinct"),
                            ("sum", "Sum"),
                            ("avg", "Average"),
                            ("min", "Minimum"),
                            ("max", "Maximum"),
                        ],
                        default="count",
                        max_length=16,
                    ),
                ),
                (
                    "target_type",
                    models.CharField(
                        default="NUMBER",
                        help_text="Type of the target value",
                        max_length=20,
                    ),
                ),
                (
                    "target_field",
                    models.CharField(
                        blank=True,
                        help_text="Field to compare against target value",
                        max_length=100,
                    ),
                ),
                (
                    "condition",
                    models.CharField(
                        choices=[
                            (
                                "TEXT",
                                [
                                    ("EXACT", "Exactly matches"),
                                    ("CONTAINS", "Contains"),
                                    ("NOT_EXACT", "Does not exactly match"),
                                    ("NOT_CONTAINS", "Does not contain"),
                                ],
                            ),
                            (
                                "NUM",
                                [
                                    ("GT", "Greater Than"),
                                    ("LT", "Less Than"),
                                    ("EQ", "Equal"),
                                    ("GTE", "Greater Than or Equal"),
                                    ("LTE", "Less Than or Equal"),
                                    ("BETWEEN", "Between"),
                                ],
                            ),
                            ("NONE", "None"),
                        ],
                        default="EXACT",
                        max_length=20,
                    ),
                ),
                (
                    "target_value",
                    models.CharField(
                        blank=True,
                        help_text="Target value to achieve",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "kpi",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="card",
                        to="kpi.kpi",
                    ),
                ),
            ],
        ),
    ]
