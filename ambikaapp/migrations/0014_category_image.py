# Generated by Django 4.1.3 on 2023-10-02 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambikaapp', '0013_placedorders_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='categoryimage/'),
        ),
    ]
