# Generated by Django 4.2.2 on 2024-04-06 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerparentagedetails',
            name='application_certificate_establishment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employer_parentel_details', to='operation.applicationforcertificateofestablishment'),
        ),
    ]
