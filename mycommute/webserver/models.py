from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from decimal import Decimal

# Create your models here.

class Commuter(models.Model):
    user = models.OneToOneField(User)
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50, blank=True)
    lastName = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER)
    prof_pic = models.ImageField(upload_to='commuter_profile_pics/%Y-%m-%d/', blank=True)
    dob = models.DateField()
    aadhaar_regex = RegexValidator(regex=r'^\d{12}$', message="Aadhaar Number must contain 12 Digits!")
    aadhaar = models.CharField(max_length=12, validators=[aadhaar_regex], blank=True)
    email = models.EmailField()
    wallet = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True)

    def __str__(self):
        return self.firstName

class Route(models.Model):
    name = models.CharField(max_length=50)
    bus = models.ForeignKey(Bus)

    def __str__(self):
        return self.name

class Bus(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    contact = models.CharField(max_length=15, validators=[phone_regex], blank=True)

    def __str__(self):
        return self.name

class Trip(models.Model):
    user = models.OneToOneField(User)
    bus = models.OneToOneField(Bus)
