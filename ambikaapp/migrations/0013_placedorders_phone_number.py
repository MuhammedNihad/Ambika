# Generated by Django 4.1.3 on 2023-09-29 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambikaapp', '0012_placedorders_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='placedorders',
            name='phone_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
