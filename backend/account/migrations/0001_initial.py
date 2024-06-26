# Generated by Django 4.2.2 on 2024-04-06 02:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('master', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(default=None, max_length=10, unique=True)),
                ('otp', models.CharField(default=None, max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=128)),
                ('contact_number', models.CharField(default=None, max_length=10)),
                ('email', models.CharField(default=None, max_length=128)),
                ('gender', models.CharField(default=None, max_length=16, null=True)),
                ('document_type', models.CharField(default=None, max_length=128, null=True)),
                ('id_proof', models.FileField(blank=True, null=True, upload_to='id_proofs/2024')),
                ('bar_registration_number', models.CharField(default=None, max_length=30, null=True)),
                ('bar_certificate', models.FileField(blank=True, null=True, upload_to='bar_certificates/2024')),
                ('is_deleted', models.BooleanField(default=None)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='master.officedetails')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
