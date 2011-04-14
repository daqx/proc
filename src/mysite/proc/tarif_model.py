'''
Created on 01.03.2011

@author: Admin
'''
from django.db import models
from django.contrib import admin
from mysite.proc.service_model import *


ADDRES_TYPE = (
        ('F', 'Fact'),
        ('R', 'Registration'),        
    )

class TarifArr(models.Model):    
    
    prc         =models.BooleanField(default=True)
    summa       =models.FloatField(default=0)
    min         =models.FloatField(default=0)
    max         =models.FloatField(default=0)
    tarif       =models.ForeignKey("Tarif",  verbose_name="tarif", related_name="tarifs")
    
    def __unicode__(self):
        return "%s | %s | %s |"%(self.summa,self.min,self.max)
    
    class Meta:
        app_label = "proc"


class Tarif(models.Model):
    code        =models.CharField(max_length=20,unique=True)
    name        =models.CharField(max_length=50)
    op_service  =models.ForeignKey(OpService)
    prc         =models.BooleanField(default=True)
    summa       =models.FloatField(default=0)
    min         =models.FloatField(default=0)
    max         =models.FloatField(default=0)
    
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = "proc"
        
class TarifGroup(models.Model):
    code        =models.CharField(max_length=20,unique=True)
    name        =models.CharField(max_length=50)
    tarif       =models.ManyToManyField(Tarif)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = "proc"
    
class TarifProfile(models.Model):
    code        =models.CharField(max_length=20,unique=True)
    name        =models.CharField(max_length=50)
    tarif_group =models.ManyToManyField(TarifGroup)
    date_begin  =models.DateTimeField()
    date_end    =models.DateTimeField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = "proc"
    