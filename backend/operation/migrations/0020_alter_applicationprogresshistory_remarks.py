# Generated by Django 4.2.2 on 2024-10-09 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0019_applicationforcertificateofestablishment_trade_licence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationprogresshistory',
            name='remarks',
            field=models.CharField(blank=True, default='', max_length=1024, null=True),
        ),
    ]
