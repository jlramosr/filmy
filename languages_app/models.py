#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

class Language(models.Model):
    code = models.CharField(max_length=10, default='es', primary_key=True)
    name = models.CharField(max_length=100)
    
    class Meta:
	ordering = ('name',)
		
    def __unicode__(self):
        return '%s' % (self.name,)
