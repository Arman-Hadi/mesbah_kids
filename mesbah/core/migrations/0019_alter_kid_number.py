# Generated by Django 4.0.6 on 2022-08-06 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_kid_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kid',
            name='number',
            field=models.CharField(blank=True, default='000', max_length=50),
        ),
    ]
