from django.db import models
from django.contrib.auth.models import User


class Kid(models.Model):
    number = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    GENDERs = [
        ('MA', 'پسر'),
        ('FE', 'دختر'),
    ]
    gender = models.CharField(max_length=2, choices=GENDERs)

    STATUSs = [
        ('RE', 'درخواست تحویل'),
        ('SE', 'فرستاده شده'),
        ('DE', 'تحویل داده شده'),
    ]
    status = models.CharField(max_length=2, choices=STATUSs)

    PARENTs = [
        ('MO', 'مادر'),
        ('FA', 'پدر'),
    ]
    parent = models.CharField(max_length=2, choices=PARENTs)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
