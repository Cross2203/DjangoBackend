# Generated by Django 5.0.6 on 2024-06-10 19:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_alter_examenfisico_consulta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consulta',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='consulta',
            name='signos_vitales',
        ),
        migrations.RemoveField(
            model_name='examenfisico',
            name='consulta',
        ),
        migrations.RemoveField(
            model_name='historialmedico',
            name='examen_fisico',
        ),
        migrations.RemoveField(
            model_name='historialmedico',
            name='organos_sistemas',
        ),
        migrations.RemoveField(
            model_name='revisionorganossistemas',
            name='consulta',
        ),
        migrations.RemoveField(
            model_name='tratamiento',
            name='nombre',
        ),
        migrations.AddField(
            model_name='examenfisico',
            name='historial_medico',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='records.historialmedico'),
        ),
        migrations.AddField(
            model_name='historialmedico',
            name='signos_vitales',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='records.signosvitales'),
        ),
        migrations.AddField(
            model_name='revisionorganossistemas',
            name='historial_medico',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='records.historialmedico'),
        ),
    ]
