# Generated by Django 4.1.3 on 2023-10-09 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambikaapp', '0015_product_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='overrelayimage',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]