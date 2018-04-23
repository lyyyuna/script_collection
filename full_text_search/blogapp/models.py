# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100, default='lyy')
    content = models.TextField(default='This is a excellent blog.')

    def __str__(self):
        return self.name