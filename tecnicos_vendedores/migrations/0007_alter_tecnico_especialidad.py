# Generated by Django 5.0.6 on 2024-07-01 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tecnicos_vendedores', '0006_alter_venta_total_alter_ventadetalle_subtotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tecnico',
            name='especialidad',
            field=models.CharField(choices=[('MTB', 'Montaña'), ('RDB', 'Ruta'), ('CTY', 'Ciudad'), ('BMX', 'BMX')], max_length=3),
        ),
    ]
