# Generated by Django 4.0.6 on 2022-08-05 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_kid_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kid',
            name='caretaker_home_number',
            field=models.CharField(blank=True, default='ندارد', max_length=100),
        ),
        migrations.AlterField(
            model_name='kid',
            name='caretaker_phone_number',
            field=models.CharField(blank=True, default='ندارد', max_length=100),
        ),
        migrations.AlterField(
            model_name='kid',
            name='emergancy_calls',
            field=models.CharField(blank=True, default='ندارد', max_length=100),
        ),
    ]
