# -*- coding: utf-8 -*-
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
    
    def calc_tarif(self,summa):
        s=0
        if self.prc==True:              #Расчет по процентам
           s=summa*self.summa/100
           if s < self.min and self.min!=0:
               s=self.min               
           if s > self.max and self.max!=0:
               s=self.max               
        else:
            if self.summa!=0:           #Расчет по сумме
                s=self.summa                
            else:                       #Если сумма 0 тариф вычисляется по массиву сумм тарифа                
                pass
                #TODO: Здесь необходимо реализовать расчет по массиву сумм
        
        return s
        
    
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
    