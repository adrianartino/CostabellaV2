# Generated by Django 4.2.13 on 2025-02-07 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCostabella', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleados',
            name='tipo_usuario',
            field=models.CharField(max_length=2, null=True),
        ),
    ]
