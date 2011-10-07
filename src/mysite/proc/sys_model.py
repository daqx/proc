# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import Permission, User



class Status(models.Model):
    code=models.CharField(max_length=20)
    name=models.CharField(max_length=50)
            
    class Meta:             
        app_label = "proc"
        
    def __unicode__(self):
        return self.name
    
class State(models.Model):
    ''' Статусы документов по продуктам '''
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    product = models.CharField(max_length=50,null=True, blank=True)
            
    class Meta:             
        app_label = "proc"
        
    def __unicode__(self):
        return self.name

    
class IpAddress(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='ipaddresses')
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey()
    
    ip  =models.IPAddressField()
    
    def __unicode__(self):
        return self.ip
    
    class Meta:             
        app_label = "proc"
        
class Kopf(models.Model):
    ''' Klasifikator organizatsionno pravovix form '''
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
    
    
CLASS_SOST = (
        ('T', 'Terminal'),
        ('C', 'CashCode'),
        ('P', 'Printer'),
    )    
    
class SostAgent(models.Model):
#Spravochnik sostoyaniy agenta
    type        =models.CharField(max_length=1,choices=CLASS_SOST)
    code        =models.CharField(max_length=50)
    name        =models.CharField(max_length=50)    
    
    def __unicode__(self):
        return self.name
    class Meta:             
        app_label = "proc"

    
class JourSostAgent(models.Model):
    ''' Jurnal sostoyaniy terminalov '''
    agent       =models.ForeignKey("Agent")
    date        =models.DateTimeField()    
    cash_count  =models.IntegerField(null=True, blank=True)                                          # Количество купюр
    link        =models.BooleanField(default=True)                                                   # Состояние связи
    cash_code   =models.ForeignKey(SostAgent, related_name="cash_code" ,null=True, blank=True)       # Состояние купюроприёмника
    printer     =models.ForeignKey(SostAgent, related_name="printer", null=True, blank=True)         # Состояние термопринтера
    terminal    =models.ForeignKey(SostAgent, related_name="terminal", null=True, blank=True)        # Состояние терминала
    
    
    def __unicode__(self):
        return "%s" % self.date
    
    class Meta:             
        app_label = "proc"


class ActualState(models.Model):
    ''' В этом типе хранится самое последнее состояние агента
        используется для мониторинга состояния терминалов
    '''
    agent       =models.ForeignKey("Agent")
    date        =models.DateTimeField()    
    cash_count  =models.IntegerField(null=True, blank=True)                                          # Количество купюр
    link        =models.BooleanField(default=True)                                                   # Состояние связи
    cash_code   =models.ForeignKey(SostAgent, related_name="ac_cash_code" ,null=True, blank=True)    # Состояние купюроприёмника
    printer     =models.ForeignKey(SostAgent, related_name="ac_printer", null=True, blank=True)      # Состояние термопринтера
    terminal    =models.ForeignKey(SostAgent, related_name="ac_terminal", null=True, blank=True)     # Состояние терминала
    date_link0  =models.DateTimeField()
    
    def __unicode__(self):
        return "%s" % self.date
    
    class Meta:             
        app_label = "proc"
      
class Action(models.Model):
    ''' Справочник актов команд
    '''
    code        =models.CharField(max_length=10)
    name        =models.CharField(max_length=50)
    description =models.CharField(max_length=200, null=True, blank=True)
    
    
    def __unicode__(self):
        return self.name
    
    class Meta:             
        app_label = "proc"
      
class Command(models.Model):
    ''' Команды для управления терминалами
    '''
    act         =models.ForeignKey(Action)
    agent       =models.ForeignKey("Agent")
    date        =models.DateTimeField()
    date_send   =models.DateTimeField(null=True, blank=True)
    status      =models.ForeignKey(Status)
    description =models.CharField(max_length=200, null=True, blank=True)
     
    
    def __unicode__(self):
        return "%s %s" % (self.date, self.agent.name)
    
    class Meta:             
        app_label = "proc"
        
class NominalVal(models.Model):
    ''' 
    '''
    code        =models.CharField(max_length=10)
    number      =models.IntegerField()
    description =models.CharField(max_length=200, null=True, blank=True)
    
    def __unicode__(self):
        return '%s' % self.number
    
    
class Nominal(models.Model):
    ''' 
    '''
    transaction =models.ForeignKey("Transaction")
    value       =models.ForeignKey(NominalVal)
    count       =models.IntegerField()     
    
    def __unicode__(self):
        return "%s %s" % (self.value, self.count)
    
    class Meta:             
        app_label = "proc"


