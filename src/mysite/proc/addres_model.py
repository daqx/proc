'''
Created on 01.03.2011

@author: Admin
'''
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

ADDRES_TYPE = (
        ('F', 'Fact'),
        ('R', 'Registration'),        
    )

class Country(models.Model):
    num_code=models.CharField(max_length=3)
    str_code=models.CharField(max_length=3)
    name=models.CharField(max_length=50)
    full_name=models.CharField(max_length=100)
    inter_name=models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = "proc"
    
class Region(models.Model):       
    name=models.CharField(max_length=50)
    city=models.ForeignKey('Town',related_name='center', blank=True,null=True)
    country=models.ForeignKey(Country)
    
    def __unicode__(self):
        return self.name
   

    class Meta:
        app_label = "proc"
    
class Town(models.Model):       
    name     = models.CharField(max_length=50)
    type_name= models.CharField(max_length=10)
    region   = models.ForeignKey(Region)
        
    def __unicode__(self):
        return self.name
    
        
    class Meta:
        app_label = "proc"
        
class Addres(models.Model):       
    content_type = models.ForeignKey(ContentType, related_name='addresses')
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey()
    
    
    address = models.CharField(max_length=150)
    town    = models.ForeignKey(Town)
    type    = models.CharField(max_length=1,choices=ADDRES_TYPE)
    
    
    
    def __unicode__(self):
        return '%s, %s'%(self.town,self.address)
    class Meta:
        app_label = "proc"
        