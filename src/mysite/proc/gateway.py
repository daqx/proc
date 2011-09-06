# -*- coding: utf-8 -*-
'''
Created on 25.08.2011

@author: D_Unusov
'''
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from mysite.proc.service_model import *




class Gateway(models.Model):
    code        = models.CharField(max_length=20, unique=True)
    name        = models.CharField(max_length=50)
    opservice   = models.ForeignKey(OpService)
    ip          = models.IPAddressField(null=True, blank=True)
    port        = models.CharField(max_length=10, null=True, blank=True)
    note        = models.CharField(max_length=300, null=True, blank=True)
    login       = models.CharField(max_length=50, null=True, blank=True)
    password    = models.CharField(max_length=50, null=True, blank=True)
    wait_time   = models.IntegerField( null=True, blank=True)
    status      = models.ForeignKey(Status)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = "proc"