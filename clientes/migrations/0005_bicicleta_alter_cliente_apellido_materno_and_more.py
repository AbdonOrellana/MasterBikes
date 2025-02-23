# Generated by Django 5.0.6 on 2024-06-24 02:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0004_remove_cliente_fecha_nacimiento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bicicleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('MTB', 'Montaña'), ('RDB', 'Ruta'), ('CTY', 'Ciudad'), ('TRC', 'Triciclo')], max_length=3)),
                ('marca', models.CharField(max_length=100)),
                ('modelo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='cliente',
            name='apellido_materno',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.CreateModel(
            name='Arriendo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('forma_pago', models.CharField(max_length=50)),
                ('deposito_garantia', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(default='pendiente', max_length=20)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('bicicleta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientes.bicicleta')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialMantencion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_mantencion', models.DateTimeField(auto_now_add=True)),
                ('detalle', models.TextField()),
                ('bicicleta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.bicicleta')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reparacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_problema', models.TextField()),
                ('fecha_solicitud', models.DateTimeField(auto_now_add=True)),
                ('fecha_programada', models.DateTimeField()),
                ('estado', models.CharField(default='pendiente', max_length=20)),
                ('bicicleta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientes.bicicleta')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
