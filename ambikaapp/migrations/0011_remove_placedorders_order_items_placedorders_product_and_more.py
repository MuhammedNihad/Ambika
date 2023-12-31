# Generated by Django 4.1.3 on 2023-09-28 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ambikaapp', '0010_orderitem_deleted_alter_placedorders_order_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placedorders',
            name='order_items',
        ),
        migrations.AddField(
            model_name='placedorders',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ambikaapp.product'),
        ),
        migrations.AddField(
            model_name='placedorders',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='placedorders',
            name='size',
            field=models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], max_length=3, null=True),
        ),
    ]
