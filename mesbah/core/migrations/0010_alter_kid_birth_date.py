# Generated by Django 4.0.6 on 2022-08-04 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_kid_caretaker_home_number_kid_wc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kid',
            name='birth_date',
            field=models.CharField(blank=True, default='1396/01/01', max_length=12),
        ),
    ]