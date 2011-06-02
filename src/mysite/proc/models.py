# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User 
from mysite.proc.service_model import *
from mysite.proc.addres_model import *
from mysite.proc.sys_model import *
from mysite.proc.tarif_model import *
from datetime import datetime
from django.db import connection, transaction


AGENT_TYPE = (
        ('T', 'Terminal'),
        ('M', 'Mobile'),
        ('W', 'Web'),
    )

class Dealer(models.Model):
    account         =models.CharField(max_length=8,blank=True)
    addresses       = generic.GenericRelation( Addres, null=True, blank=True )        
    check_for_ip    =models.BooleanField(default=False)
    #date_create     =models.DateTimeField(auto_now_add=True)
    #date_last_visit =models.DateTimeField( null=True, blank=True)
    dealer          =models.ForeignKey('self',related_name='parent', null=True, blank=True)
    #email           =models.EmailField(blank=True)    
    inn             =models.CharField(max_length=12,blank=True)
    ipaddresses     = generic.GenericRelation( IpAddress, null=True, blank=True )
    kopf            =models.ForeignKey(Kopf)
    limit           =models.FloatField(blank=True)
    #login           =models.CharField(max_length=20,unique=True)
    #name            =models.CharField(max_length=50)
    overdraft       =models.FloatField(blank=True)
    #password        =models.CharField(max_length=100)
    tel             =models.CharField(max_length=20,blank=True)    
    state           =models.ForeignKey(State)
    summa           =models.FloatField(blank=True)
    user            =models.OneToOneField(User, blank=True)
    
    def __unicode__(self):
        return self.user.username
    
    def __str__(self):
        return self.user.username

class Agent(models.Model):
    addresses = generic.GenericRelation( Addres, null=True, blank=True )    
    check_for_ip    =models.BooleanField(default=False)    
    dealer          =models.ForeignKey(Dealer, null=True, blank= True)    
    name            =models.CharField(max_length=50)
    imei            =models.CharField(max_length=20,blank=True)
    ipaddresses     = generic.GenericRelation( IpAddress, null=True, blank=True )    
    opservices      =models.ManyToManyField(OpService, null=True, blank=True)
    opservice_group =models.ManyToManyField(OpServiceGroup)    
    tarif_profile_arr=models.ManyToManyField(TarifProfile)
    tel             =models.CharField(max_length=20,blank=True)
    type            =models.CharField(max_length=1,choices=AGENT_TYPE)
    state           =models.ForeignKey(State)
    user            =models.OneToOneField(User, blank=True)
    
    def __unicode__(self):
        return self.name

    def calc_commiss(self,op_serv,summa):
        try:
            #cursor = connection.cursor()
            
            query = 'select t.* from proc_agent_tarif_profile_arr ata, proc_tarifprofile tp, proc_tarifgroup tg,proc_tarifprofile_tarif_group tptg, proc_tarifgroup_tarif tgt, proc_tarif t,proc_opservice os where ata.agent_id=12 and tp.id=ata.tarifprofile_id and tptg.tarifprofile_id=tp.id and tptg.tarifgroup_id=tg.id and tgt.tarifgroup_id=tg.id and tgt.tarif_id=t.id and os.id=t.op_service_id and os.id=%s' % op_serv.id
            tr = Tarif.objects.raw(query)[0]
                                           
            return tr.calc_tarif(summa)
            
        except(IndexError, TarifProfile.DoesNotExist) :
            return 0
    
class Transaction(models.Model):
    agent           =models.ForeignKey(Agent)    
    date            =models.DateTimeField(auto_now_add=True)
    opservices      =models.ForeignKey(OpService)
    number_key      =models.CharField(max_length=100)
    summa           =models.FloatField()
    summa_commiss   =models.FloatField()
    summa_pay       =models.FloatField()    
    state           =models.ForeignKey(State)
    return_reason   =models.CharField(max_length=100)                           # Причина отказа и служ отметки    
    date_proc       =models.DateTimeField(null=True, blank=True)                # Дата обработки
    seans_number    =models.CharField(max_length=20,null=True, blank=True)      # Номер сеанса обработки
    processed       =models.NullBooleanField(null=True, blank=True)             # Признак успешной обработки
    blocked         =models.NullBooleanField(null=True, blank=True)             # Признак блокировки процессом
    try_count       =models.FloatField(null=True, blank=True)                   # Количество попыток
    file_name       =models.CharField(max_length=20,null=True, blank=True)
    user_proc       =models.OneToOneField(User,null=True, blank=True)
    
    def __unicode__(self):
        return '%s %s' % self.summa, self.agent 

    def add(self):        
        '''Добавление новой записи'''
        ag=self.agent
        com=ag.calc_commiss(self.opservices,self.summa)
        self.summa_commiss=com
        self.summa_pay=self.summa-self.summa_commiss
        ''' ���������� ��������� ��������'''
        #//TODO надо изменитть статус
        self.state=State.objects.all()[0]
        ''' Сохраним все данные '''
        super(Transaction, self).save()
        am=ArcMove(dealer=self.agent.dealer,dt=True,summa=self.summa_pay,transaction=self,saldo=0)
        am.save()

class ArcMove(models.Model):
    date            =models.DateTimeField(auto_now_add=True)
    dealer          =models.ForeignKey(Dealer)
    dt              =models.BooleanField()    
    saldo           =models.FloatField()
    summa           =models.FloatField()
    transaction     =models.ForeignKey(Transaction,null=True, blank=True)
    
    def __unicode__(self):
        return self.summa
    