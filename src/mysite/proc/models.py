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


class TarifPlanM2M(models.Model):    
    tarif_plan  =models.ForeignKey(TarifPlan)
    
    content_type = models.ForeignKey(ContentType, related_name='TarifPlanM2Ms')
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey()
    
    def __unicode__(self):
        return self.id


class Dealer(models.Model):
    account         =models.CharField('Счет',max_length=8,blank=True)
    addresses       = generic.GenericRelation( Addres, null=True, blank=True )        
    check_for_ip    =models.BooleanField('Проверять IP',default=False)    
    dealer          =models.ForeignKey('self',related_name='parent', null=True, blank=True, verbose_name='Диллер')        
    inn             =models.CharField('ИНН',max_length=12,blank=True)
    ipaddresses     = generic.GenericRelation( IpAddress, null=True, blank=True )
    kopf            =models.ForeignKey( Kopf,  verbose_name='Код ОПФ')
    limit           =models.FloatField('Лимит',null=True,blank=True)    
    overdraft       =models.FloatField('Овердрафт',null=True,blank=True) 
    tarif_plan_arr  =generic.GenericRelation(TarifPlanM2M, null=True, blank=True)   
    tel             =models.CharField('Телефон',max_length=20,blank=True)    
    state           =models.ForeignKey(Status, verbose_name='Статус')
    summa           =models.FloatField('Сумма',blank=True)
    user            =models.OneToOneField(User, blank=True, verbose_name='Пользователь')
    
    def __unicode__(self):
        return self.user.username
    
    def __str__(self):
        return self.user.username
    
    def fill_ac(self, arc):        
        '''Пополнение счета диллера'''
        arc.dt = False
        arc.saldo = self.get_saldo(datetime.now()) 
        arc.save()
        
        self.summa = arc.saldo
        super(Dealer, self).save()
    
    def get_saldo(self, cdate):
        try:
            arc= self.arcmove_set.order_by('-date')[0]
        except IndexError:
            return 0

        sum=0
        ''' Если нет каких записей то это означает что выписка пуста
            и возвратим 0
        '''
        if arc is None:
            return 0
        
        if arc.dt:
            return arc.saldo-arc.summa
        else:
            return arc.saldo+arc.summa
            
        

class Agent(models.Model):
    addresses       = generic.GenericRelation( Addres, null=True, blank=True )    
    check_for_ip    =models.BooleanField('Проверить IP',default=False)    
    dealer          =models.ForeignKey(Dealer, null=True, blank= True, verbose_name='Диллер')    
    name            =models.CharField('Наименование',max_length=50)
    imei            =models.CharField('IMEI',max_length=20,blank=True)
    ipaddresses     = generic.GenericRelation( IpAddress, null=True, blank=True )    
    opservices      =models.ManyToManyField(OpService, null=True, blank=True, verbose_name='Операторы услуг')
    opservice_group =models.ManyToManyField(OpServiceGroup, verbose_name='Группы операторов услуг')    
    tarif_plan_arr  =generic.GenericRelation(TarifPlanM2M, null=True, blank=True)
    tel             =models.CharField('Телефон',max_length=20,blank=True)
    type            =models.CharField('Тип',max_length=1,choices=AGENT_TYPE)
    state           =models.ForeignKey(Status, verbose_name='Статус')
    user            =models.OneToOneField(User, blank=True, verbose_name='Пользователь')
    key_hash        =models.CharField('Хеш ключа',max_length=40, blank=True, null=True)
    hardware        =models.CharField(max_length=150, blank=True, null=True)
    cashcode_capacity=models.IntegerField('Емкость купюроприемника',blank=True, null=True)
    
    def __unicode__(self):
        return self.name

    def calc_commiss(self,op_serv,summa):
        try:
            #cursor = connection.cursor()
            
            query = 'select t.* from proc_agent_tarif_profile_arr ata, proc_tarifprofile tp, proc_tarifgroup tg,proc_tarifprofile_tarif_group tptg, proc_tarifgroup_tarif tgt, proc_tarif t,proc_opservice os where ata.agent_id=12 and tp.id=ata.tarifprofile_id and tptg.tarifprofile_id=tp.id and tptg.tarifgroup_id=tg.id and tgt.tarifgroup_id=tg.id and tgt.tarif_id=t.id and os.id=t.op_service_id and os.id=%s' % op_serv.id
            tr = Tarif.objects.raw(query)[0]
                                           
            return tr.calc_tarif(summa)
            
        except(IndexError, TarifPlan.DoesNotExist) :
            return 0
    
class Transaction(models.Model):
    agent           =models.ForeignKey(Agent, verbose_name='Агент')    
    date            =models.DateTimeField(auto_now_add=True, verbose_name='Дата')  # Время появления платежа на сервере
    date_state      =models.DateTimeField()                                     # Дата последнего изменения статуса
    date_input      =models.DateTimeField(null=True, blank=True)                # Дата платежа на терминале
    encashment      =models.IntegerField(null=True, blank=True)                 # инкасация 
    opservices      =models.ForeignKey(OpService)
    number_key      =models.CharField(max_length=100, verbose_name='Номер')
    summa           =models.FloatField(verbose_name='Сумма')
    summa_commiss   =models.FloatField(verbose_name='Комиссия')
    summa_pay       =models.FloatField(verbose_name='Сумма платежа')    
    state           =models.ForeignKey(State)
    ticket          =models.IntegerField(null=True, blank=True)                 # номер чека
    return_reason   =models.CharField(max_length=100)                           # Причина отказа и служ отметки    
    seans_number    =models.CharField(max_length=20,null=True, blank=True)      # Номер сеанса обработки
    processed       =models.NullBooleanField(null=True, blank=True)             # Признак успешной обработки
    locked          =models.NullBooleanField(null=True, blank=True)             # Признак блокировки процессом
    try_count       =models.FloatField(null=True, blank=True)                   # Количество попыток
    file_name       =models.CharField(max_length=20,null=True, blank=True)
    user_proc       =models.OneToOneField(User,null=True, blank=True)
    hesh_id         =models.CharField(max_length=40,null=True, blank=True)
    
    def __unicode__(self):
        return '%s  %s  %s' % (self.agent.user.username, self.summa , self.date) 

    def add(self, api = False):        
        '''Добавление новой записи'''
        
        #  Если не используем API то вычисляем комиссию и сумму платежа
        if not api:
            ag=self.agent
            com=ag.calc_commiss(self.opservices,self.summa)
            self.summa_commiss=com
            self.summa_pay=self.summa-self.summa_commiss
        
        # статус
        self.state=State.objects.get(code="0")                            # Новый
        self.date_state = datetime.now()
        
        # Сохраним все данные
        super(Transaction, self).save()
        
        # Добавим запись в выписку
        am=ArcMove(dealer=self.agent.dealer,dt=True,summa=self.summa_pay,transaction=self,saldo=0)
        am.save()
        
        # Добавим новый статус в историю (HistoryState)
        h = HistoryState(trans=self, date=self.date, state=self.state)
        h.save()
        

    def delete(self):
        ''' Удаление транзакций '''
        for item in self.arcmove_set.all():                                 # удалим сначала выписку
            item.delete()
        super(Transaction, self).delete()                                   # потом и сам документ
        

class ArcMove(models.Model):
    date            =models.DateTimeField(auto_now_add=True)
    dealer          =models.ForeignKey(Dealer)
    dt              =models.BooleanField()    
    saldo           =models.FloatField()
    summa           =models.FloatField()
    transaction     =models.ForeignKey(Transaction,null=True, blank=True)
    
    def __unicode__(self):
        return '%s  %s  %s' % (self.dealer.user.username, self.summa , self.date)


class HistoryState(models.Model):
    ''' История изменения состояний транзакций
    '''    
    date        =models.DateTimeField()
    user        =models.OneToOneField(User, blank=True, null=True)    
    state       =models.ForeignKey(State)
    description =models.CharField(max_length=200,null=True, blank=True)
    trans       =models.ForeignKey(Transaction, related_name="trans")
    
    def __unicode__(self):
        return "%s %s" % (self.state.name, self.date)

class Encashment(models.Model):
    ''' Инкасация
    '''
    user        =models.OneToOneField(User, blank=True, null=True)
    date        =models.DateTimeField(auto_now_add=True)                            # Время появления инкасации на сервере
    date_encash =models.DateTimeField()                                             # Время инкасации    
    number      =models.IntegerField(null=True, blank=True)                         # Номер инкасации
    summa       =models.FloatField(blank=True)                                      # Сумма инкасации
    description =models.CharField(max_length=200,null=True, blank=True)
    agent       =models.ForeignKey(Agent)
    
    def __unicode__(self):
        return "%s" % self.date   
    

