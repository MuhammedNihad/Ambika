# Generated by Django 4.1.3 on 2023-09-29 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambikaapp', '0011_remove_placedorders_order_items_placedorders_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='placedorders',
            name='total_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]