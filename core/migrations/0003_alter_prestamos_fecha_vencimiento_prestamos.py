# Generated by Django 4.2.5 on 2023-09-30 14:28

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_prestamos_pagado_alter_multas_fecha_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamos',
            name='fecha_vencimiento_prestamos',
            field=models.DateTimeField(default=core.models.Prestamos.fecha_vencimiento),
        ),
    ]
