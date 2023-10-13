# Generated by Django 4.1.3 on 2023-10-10 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambikaapp', '0016_product_overrelayimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='occasions',
            field=models.CharField(blank=True, choices=[('Casual Wear', 'Casual Wear'), ('Comfort Wear', 'Comfort Wear'), ('Street Wear', 'Street Wear'), ('Club Wear', 'Club Wear'), ('Beach Wear', 'Beach Wear'), ('Party Wear', 'Party Wear'), ('Holiday Wear', 'Holiday Wear'), ('Weekend Wear', 'Weekend Wear'), ('College Wear', 'College Wear'), ('Office Wear', 'Office Wear')], max_length=20, null=True),
        ),
    ]
