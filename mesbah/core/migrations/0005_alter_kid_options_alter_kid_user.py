# Generated by Django 4.0.6 on 2022-08-02 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_alter_kid_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kid',
            options={'ordering': ['number', 'name']},
        ),
        migrations.AlterField(
            model_name='kid',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]