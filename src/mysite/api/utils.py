# -*- coding: utf-8 -*-

from piston.handler import BaseHandler
from mysite.proc.models import *
from mysite.proc.sys_class import *
#from django.utils import simplejson

def transfer( body_, login_):
    ''' Функция вставки нового платежа '''
    print body_
    tr = Transaction()                          # Инициируем новый объект Transaction
    
    try:
        ag = Agent.objects.filter(user__username = login_)[0]           # Достанем Агента
            
        tr.opservices = OpService.objects.get(id= body_["id_uslugi"])
        tr.number_key = body_["nomer"]
        tr.summa = body_["summa"]
        tr.summa_pay = body_["summa_zachis"]
        
        #TODO: Пока оставим это так
        tr.summa_commiss = tr.summa - tr.summa_pay 
        
        tr.agent = ag 
        
        tr.add(api = True)
    except(IndexError, Agent.DoesNotExist, OpService.DoesNotExist) :
        return "-1"
    
    return "0"                                  # Если все нормально прошло то возвращается 0



def get_opservices(login_):
    ''' Функция возвращает все доступные операторы услуг для заданного агента '''
    
    try:
        id = Agent.objects.filter(user__username = login_)[0].id        # Достанем id Агента
    except(IndexError, Agent.DoesNotExist) :
        return "-1"
    
    query="select o.* from proc_opservice o, proc_agent_opservices ao where o.id=ao.opservice_id and ao.agent_id= %s  union   select o.* from proc_opservice o, proc_agent_opservice_group aog, proc_opservicegroup_opservice ogo where  aog.opservicegroup_id=ogo.opservicegroup_id and aog.agent_id = %s" % (12, 12)
    
    op = OpService.objects.raw(query)[0:]

    return op
     

def get_optype(login_):
    ''' Функция возвращает все типы '''
    
    try:
        id = Agent.objects.filter(user__username = login_)[0].id        # Достанем id Агента
    except(IndexError, Agent.DoesNotExist) :
        return "-1"
           
    opt = ServiceType.objects.all()

    return opt




def do_job(act_, body_, login_):
    ''' Функция обработки команд '''        
    ret = "-1"
    if act_ == "0":                             # Новый платеж
        ret = transfer( body_, login_)
    if act_ == "5":                             # Запрос доступных операторов услуг
        ret = get_optype(login_);
    if act_ == "6":                             # Запрос доступных операторов услуг
        ret = get_opservices(login_);
    
    
    return ret
    