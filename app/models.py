# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User(models.Model):
    pass

class Contact(models.Model):
    Name = models.CharField(max_length = 50)
