# -*- coding: utf-8 -*-
'''
Created on 26.02.2011
создано
'''

from django.db import models
from django.contrib import admin
from mysite.proc.sys_model import *

# Create your models here.
class ServiceType(models.Model):
    code    =models.CharField(max_length=20, unique = True)
    name    =models.CharField(max_length=50)
    order   =models.IntegerField()
    parent  =models.ForeignKey('self', related_name='parent_type',null=True,blank=True)
        
    class Meta:
        #ordering=('parent','order',)        
        unique_together = [('parent','order')]
        app_label = "proc"
        
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return '/proc/service_type/%s/' % self.id    
    
    
class OpService(models.Model):
    state       =models.ForeignKey(Status,blank=False)
    name        =models.CharField(max_length=50)
    code        =models.CharField(max_length=20, unique = True)
    order       =models.IntegerField()
    type        =models.ForeignKey(ServiceType)
    need_check  =models.BooleanField(default=False)
    mask        =models.CharField(max_length=20)
    
    class Meta:
        ordering=('order',)
        app_label = "proc"
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return '/proc/services/%s/' % self.id

class OpServiceGroup(models.Model):
    '''Группа сервисов'''
    code        =models.CharField(max_length=20,unique=True)
    name        =models.CharField(max_length=50)
    opservice   =models.ManyToManyField(OpService)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = "proc"
    

