# Generated by Django 5.0.6 on 2024-06-30 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0020_alter_reparacion_estado_reparacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arriendo',
            name='costo_arriendo',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='arriendo',
            name='costo_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='arriendo',
            name='deposito_garantia',
            field=models.IntegerField(default=100000),
        ),
    ]
