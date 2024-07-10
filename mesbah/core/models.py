from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


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
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDERs, blank=True, default='NO')
    wc = models.BooleanField(default=True, blank=True)

    caretaker = models.CharField(max_length=100, blank=True, default='ندارد')
    caretaker_name = models.CharField(max_length=100, blank=True, default='ندارد')
    caretaker_phone_number = models.CharField(max_length=100, blank=True, default='ندارد')
    emergancy_calls = models.CharField(max_length=100, blank=True, default='ندارد')
    caretaker_home_number = models.CharField(max_length=100, blank=True, default='ندارد')

    gate_in = models.CharField(max_length=2, choices=GATEs, blank=True, default='NO')
    gate_out = models.CharField(max_length=2, choices=GATEs, blank=True, default='NO')

    number = models.CharField(max_length=50, blank=True, default='000')
    status = models.CharField(max_length=2, choices=STATUSs, blank=True, default='NO')

    last_change = models.DateTimeField(null=True, default=None, blank=True)

    def save(self, *args, **kwargs):
        self.age = self.calculate_age(nosave=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.number}. {self.first_name} {self.last_name}'

    def calculate_age(self, nosave=False):
        try:
            y = int(self.birth_date[0:4])
        except:
            return None

        if y < 1500:
            age = 1403 - y
        else:
            age = timezone.now().year - y
        if age < 0:
            return None

        if not nosave:
            self.age = age
            self.save()
        return age


class StatusChange(models.Model):
    kid = models.ForeignKey(Kid, on_delete=models.CASCADE)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        null=True, blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    previous_status = models.CharField(blank=True, default="", max_length=10)
    status = models.CharField(blank=True, default="", max_length=10)
