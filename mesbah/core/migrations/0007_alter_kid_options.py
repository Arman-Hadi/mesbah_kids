# Generated by Django 4.0.6 on 2022-08-03 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_kid_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kid',
            options={'ordering': ['id', '-number', 'name']},
        ),
    ]
