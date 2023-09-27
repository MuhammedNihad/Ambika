# Generated by Django 4.1.3 on 2023-09-27 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambikaapp', '0005_orderitem_size_alter_size_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('conclusion', models.TextField()),
            ],
        ),
    ]