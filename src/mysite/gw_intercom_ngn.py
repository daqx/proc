# -*- coding: utf-8 -*-
import sys;
import time;

sys.path.append('D:/work/python/proc/src/')
from django.core import management;
import mysite.settings as settings;
management.setup_environ(settings)
from mysite.proc.models import *
from mysite.proc.sys_model import *
from mysite.proc.service_model import *
from mysite.proc.tarif_model  import *
from mysite.proc.gateway  import *
import urllib2;
import xml.etree.ElementTree as xml;
from datetime import datetime 
from django.db.models import Q
from mysite.proc.helpers import *
from mysite.route import *
#import datetime

#выбрать нужные данные и отправить провайдеру
st_new=State.objects.get(code='0')  #статус на отправку
st_no_money = State.objects.get(code='1023') #не достаточно средств на счете диллера
intercom_ngn = OpService.objects.get(code = 'intercom_ngn')
while True:
    try :
        gatew = Gateway.objects.get(code = 'intercom_ngn')
        st_gatew = gatew.status.code 
        if st_gatew == 'WORKING':
            st_route = gatew.route.code 
            #Если st_route != self, то маршрутизация задана. Выбираем нужный маршрут и вызываем его 
            if st_route == 'self':
                tr=Transaction.objects.filter(Q(try_count__isnull=True)|Q(try_count__lte=10), Q(state = st_new)|Q(state = st_no_money), opservices = intercom_ngn).order_by("state")[:3] #лимит по 3
                for i in tr: #цыкл только по тем транзакциям у которых статус =0
                    d = i.agent.dealer
                    saldo = d.get_saldo(datetime.now())
                    
                    if d.overdraft == None:
                        d.overdraft = 0
                        
                    if d.limit == None:
                        d.limit = 0
                    if saldo + d.overdraft - d.limit >= i.summa_pay:     #проверяем баланс диллера
                        pass
                    else:
                        i.set_state('1023') #не достаточно средств
            elif st_route == 'pardokht':
                if gatew.route.status.code == 'WORKING':
                    tr=Transaction.objects.filter(Q(try_count__isnull=True)|Q(try_count__lte=10), Q(state = st_new)|Q(state = st_no_money), opservices = intercom_ngn).order_by("state")[:3] #лимит по 3
                    for i in tr: #цыкл только по тем транзакциям у которых статус =0
                        d = i.agent.dealer
                        saldo = d.get_saldo(datetime.now())
                        
                        if d.overdraft == None:
                            d.overdraft = 0
                            
                        if d.limit == None:
                            d.limit = 0
                        if saldo + d.overdraft - d.limit >= i.summa_pay:     #проверяем баланс диллера
                            pardokht_pay(i)
                        else:
                            i.set_state('1023') #не достаточно средств
        time.sleep(3)
        print ('Informations are select from transactions intercom_ngn')
    except Exception as inst:
        print 'Error while runnig log_msg'
        print inst