# Generated by Django 5.0.2 on 2024-05-14 20:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("location", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ubicaciones",
            name="seguridad_zona",
            field=models.CharField(
                choices=[("0", "segura"), ("1", "insegura"), ("2", "zona delictiva")],
                default="segura",
                max_length=50,
                verbose_name="Seguridad de la zona",
            ),
        ),
    ]