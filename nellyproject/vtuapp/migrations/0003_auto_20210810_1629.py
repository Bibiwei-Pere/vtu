# Generated by Django 3.1 on 2021-08-10 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vtuapp', '0002_auto_20210810_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='network',
            name='recharge_pin',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='corporate_data_vending_medium',
            field=models.CharField(choices=[('MSORG_DEVELOPED_WEBSITE', 'MSORG_DEVELOPED_WEBSITE'), ('SMEPLUG', 'SMEPLUG'), ('SMS', 'SMS'), ('UWS', 'UWS')], max_length=30),
        ),
    ]
