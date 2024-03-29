# Generated by Django 4.2.7 on 2024-02-09 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0003_report_latitude_report_longitude"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="latitude",
            field=models.DecimalField(
                blank=True, decimal_places=16, max_digits=22, null=True
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="longitude",
            field=models.DecimalField(
                blank=True, decimal_places=16, max_digits=22, null=True
            ),
        ),
    ]
