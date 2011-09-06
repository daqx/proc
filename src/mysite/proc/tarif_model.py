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
    parent      =models.BooleanField(default=False)                          # Признак родительского тарифа
    prc         =models.BooleanField(default=True)
    summa       =models.FloatField(default=0)
    min         =models.FloatField(default=0)
    max         =models.FloatField(default=0)
    tarif       =models.ForeignKey("Tarif",  verbose_name="tarif", related_name="tarifs")
    beg_time    =models.TimeField(blank=True, null=True)
    end_time    =models.TimeField(blank=True, null=True)
        
    def __unicode__(self):
        return "%s | %s | %s |"%(self.summa,self.min,self.max)
    
    class Meta:
        app_label = "proc"


class TarifPlan(models.Model):
    code        =models.CharField(max_length=20)
    name        =models.CharField(max_length=50)    
    date_begin  =models.DateTimeField()
    date_end    =models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = "proc"
    


class Tarif(models.Model):
    code        =models.CharField(max_length=20)
    name        =models.CharField(max_length=50)
    op_service  =models.ForeignKey(OpService)
    prc         =models.BooleanField(default=True)
    summa       =models.FloatField(default=0)    
    summa_own   =models.FloatField(default=0)
    min         =models.FloatField(default=0)
    max         =models.FloatField(default=0)
    tarif_plan  =models.ForeignKey(TarifPlan)
    ru_text     =models.TextField( blank=True, null=True)
    tj_text     =models.TextField( blank=True, null=True)
    en_text     =models.TextField( blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    def calc_tarif(self,summa):
        s=0
        if self.prc==True:              #Расчет по процентам
            s=summa*self.summa/100
           
            # Если сумма переопределена, то следует прибавить и добавочную комиссию
            if self.summa_own is not None and self.summa_own>0:
                s = s + (summa * self.summa_own/100) 
           
            if s < self.min and self.min!=0:
                s=self.min               
            if s > self.max and self.max!=0:
                s=self.max               
        else:
            if self.summa!=0:           #Расчет по сумме
                s=self.summa                
                # Если сумма переопределена, то следует прибавить и добавочную комиссию
                if self.summa_own>0:
                    s = s + self.summa_own
            else:                       #Если сумма 0 тариф вычисляется по массиву сумм тарифа
                
                # 1.Сначала рассчитаем комисию по базовому (унаследованному) массиву
                try:                
                    ta = TarifArr.objects.filter( tarif=self, min__lte = summa, max__gt = summa, parent = True)[0]
                    
                    if ta.prc:
                        s = summa * ta.summa/100
                    else:
                        s = ta.summa
                except(IndexError, TarifArr.DoesNotExist) :
                    pass
                
                # 2.Теперь прибавим добавочную комисию (praent = False)
                try:                
                    ta = TarifArr.objects.filter( tarif=self, min__lte = summa, max__gt = summa, parent = False)[0]
                    
                    if ta.prc:
                        s = s + summa * ta.summa/100
                    else:
                        s = s + ta.summa
                except(IndexError, TarifArr.DoesNotExist) :
                    pass
        
        return s
        
    
    class Meta:
        app_label = "proc"
        


class TarifArrBase(models.Model):    
    prc         =models.BooleanField(default=True)
    summa       =models.FloatField(default=0)
    min         =models.FloatField(default=0)
    max         =models.FloatField(default=0)
    tarif       =models.ForeignKey("TarifBase",  verbose_name="tarifbase", related_name="tarifs")
    beg_time    =models.TimeField(blank=True, null=True)
    end_time    =models.TimeField(blank=True, null=True)
        
    def __unicode__(self):
        return "%s | %s | %s |"%(self.summa,self.min,self.max)
    
    class Meta:
        app_label = "proc"


class TarifPlanBase(models.Model):
    code        =models.CharField(max_length=20,unique=True)
    name        =models.CharField(max_length=50)    
    date_begin  =models.DateTimeField()
    date_end    =models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = "proc"

class TarifBase(models.Model):
    code        =models.CharField(max_length=20,unique=True)
    name        =models.CharField(max_length=50)
    op_service  =models.ForeignKey(OpService)
    prc         =models.BooleanField(default=True)
    summa       =models.FloatField(default=0)
    min         =models.FloatField(default=0)
    max         =models.FloatField(default=0)
    tarif_plan  =models.ForeignKey(TarifPlanBase)
    ru_text     =models.TextField( blank=True, null=True)
    tj_text     =models.TextField( blank=True, null=True)
    en_text     =models.TextField( blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    
    class Meta:
        app_label = "proc"


