# Generated by Django 4.0.6 on 2022-08-05 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_kid_caretaker_home_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kid',
            name='porsline_id',
            field=models.CharField(blank=True, default='----', max_length=50),
        ),
    ]