# Generated by Django 4.2.2 on 2024-04-06 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
        ('operation', '0007_applicationforcertificateofestablishment_office_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationforcertificateofestablishment',
            name='office_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='application_for_est', to='master.district'),
        ),
    ]
