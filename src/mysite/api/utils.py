# -*- coding: utf-8 -*-

from piston.handler import BaseHandler
from mysite.proc.models import *
from mysite.proc.sys_class import *
#from django.utils import simplejson

def transfer(body_):
    ''' Функция вставки нового платежа '''
    print body_
    tr = Transaction()                      # Инициируем новый объект Transaction
    
    try:
        ag = Agent.objects.get(id=12)           # Тащим от себя агента
            
        tr.opservices = OpService.objects.get(id= body_["id_uslugi"])
        tr.number_key = body_["nomer"]
        tr.summa = body_["summa"]
        tr.summa_pay = body_["summa_zachis"]
        tr.agent = ag 
        
        tr.add(api = True)
    except(IndexError, Agent.DoesNotExist, OpService.DoesNotExist) :
        return "-1"
    
    return "0"                              # Если все нормально прошло то возвращается 0


def do_job(act_, body_):
    ''' Функция обработки команд '''        
    ret = "-1"
    if act_ == "0":                         # Новый платеж
        ret = transfer(body_)
    
    return ret
    
        
        
