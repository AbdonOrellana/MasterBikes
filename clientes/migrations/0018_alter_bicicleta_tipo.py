# Generated by Django 5.0.6 on 2024-06-28 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0017_alter_reparacion_options_reparacion_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bicicleta',
            name='tipo',
            field=models.CharField(choices=[('Montaña', 'Montaña'), ('Ruta', 'Ruta'), ('Ciudad', 'Ciudad'), ('BMX', 'BMX')], max_length=15),
        ),
    ]
