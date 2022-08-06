from django.db import models
from django.contrib.auth.models import User

from datetime import date


class Kid(models.Model):
    GENDERs = [
        ('MA', 'پسر'),
        ('FE', 'دختر'),
        ('NO', 'معلوم نیست'),
    ]
    STATUSs = [
        ('RE', 'درخواست تحویل'),
        ('DE', 'تحویل داده شده'),
        ('SE', 'فرستاده شده'),
        ('IN', 'داخل غرفه'),
        ('NO', 'نیامده'),
    ]
    GATEs = [
        ('MA', 'آقایان'),
        ('FE', 'خانمها'),
        ('NO', 'معلوم نیست'),
    ]

    class Meta:
        ordering = ['last_change', 'status', 'gender', 'gate_in', 'gate_out',
            'first_name', 'last_name', '-number',]

    porsline_id = models.CharField(max_length=50, blank=True, default='----')

    first_name = models.CharField(max_length=100, blank=True, default='ندارد')
    last_name = models.CharField(max_length=100, blank=True, default='ندارد')
    birth_date = models.CharField(max_length=12, default='1396/01/01', blank=True)
    gender = models.CharField(max_length=2, choices=GENDERs, blank=True, default='NO')
    wc = models.BooleanField(default=True, blank=True)

    caretaker = models.CharField(max_length=100, blank=True, default='ندارد')
    caretaker_name = models.CharField(max_length=100, blank=True, default='ندارد')
    caretaker_phone_number = models.CharField(max_length=100, blank=True, default='ندارد')
    emergancy_calls = models.CharField(max_length=100, blank=True, default='ندارد')
    caretaker_home_number = models.CharField(max_length=100, blank=True, default='ندارد')

    gate_in = models.CharField(max_length=2, choices=GATEs, blank=True, default='NO')
    gate_out = models.CharField(max_length=2, choices=GATEs, blank=True, default='NO')

    number = models.CharField(max_length=5, blank=True, default='000')
    status = models.CharField(max_length=2, choices=STATUSs, blank=True, default='NO')

    last_change = models.DateTimeField(null=True, default=None, blank=True)

    def __str__(self):
        return f'{self.number}. {self.first_name} {self.last_name}'
