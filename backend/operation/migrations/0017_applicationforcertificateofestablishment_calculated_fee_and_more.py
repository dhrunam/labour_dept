# Generated by Django 4.2.2 on 2024-05-29 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0016_alter_applicationprogresshistory_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationforcertificateofestablishment',
            name='calculated_fee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='applicationforcertificateofestablishment',
            name='is_fee_deposited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='applicationforcertificateofestablishment',
            name='token_number',
            field=models.CharField(default='', max_length=20),
        ),
    ]
