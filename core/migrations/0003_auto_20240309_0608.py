# Generated by Django 3.2.24 on 2024-03-09 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20240306_1740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='avatar',
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
