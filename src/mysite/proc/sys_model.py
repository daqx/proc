# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import Permission

class State(models.Model):
    code=models.CharField(max_length=20)
    name=models.CharField(max_length=50)
            
    class Meta:             
        app_label = "proc"
        
    def __unicode__(self):
        return self.name
    
class IpAddress(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='ipaddresses')
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey()
    
    ip=models.IPAddressField()
    
    def __unicode__(self):
        return self.ip
    class Meta:             
        app_label = "proc"
class Kopf(models.Model):
#Klasifikator organizatsionno pravovix form
    code        =models.CharField(max_length=5)
    name        =models.CharField(max_length=50)
    short_name  =models.CharField(max_length=5)        
    
    def __unicode__(self):
        return self.name
    class Meta:             
        app_label = "proc"

class Menu(models.Model):
#Menu dlya razgranicheniya prav v site
    code        =models.CharField(max_length=20)
    name        =models.CharField(max_length=50)
    order       =models.IntegerField()
    perms       =models.ForeignKey(Permission)
    url         =models.CharField(max_length=50,null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    class Meta:             
        app_label = "proc"
    