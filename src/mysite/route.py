# -*- coding: utf-8 -*-
import sys;
import time;
import string;
import hashlib;

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

#import datetime

#отправка всех данных и проверка ошибок
def  pardokht_send_data(trans, url, xml_data, gatew):
    status_code = result_code = final_st = fatal_error = ''  #переменные которые возвращаются, если пустые, то нет ответа от сервера
    #произвести запись в справочник лог данные url
    ins_log(trans, url+xml_data, True)
    
    wait_time = gatew.wait_time
    #открытие соединения
    try:
        resp=urllib2.urlopen(url, xml_data, wait_time)
        page=resp.read()    #ответ сервера провайдера
        ins_log(trans, page, False) #вставка в лог
            
        xml_read = xml.fromstring(page)
        lst = xml_read.getiterator('payment') 
        if len(lst)==1:     #в полученном xml должно быть "KKM_PG_GATE"
            for item in lst:
                status_code = item.attrib["status"]
                result_code = item.attrib["result-code"]
                final_st    = item.attrib["final-status"]
                fatal_error = item.attrib["fatal-error"]
                                 
    except Exception as inst:
        print 'Error while send data or check reply of pardokht'
        print inst
        
    return status_code, result_code, final_st, fatal_error   
        
def pardokht_err_desc(err_code_):
    
    try:
        err_code = int(err_code_);        
    except ValueError:
        err_code = 20820;
    
    if err_code == 10:
        err_desc = '1014'                #Не обработана
    elif err_code >= 20 and err_code <= 50:
        err_desc = '2000'                #обрабатывается
    elif err_code in (51,60,61):
        err_desc = '5000'                #проведен
    elif err_code >= 120 and err_code <= 160:   
        err_desc = '1017'                #Ошибка на сервере
    else:
        err_desc = '4004'                #не опознанная ошибка      
    
    return err_desc

def get_service_id(code):
    ret = ''
    if code == 'babilon_ngn': #5
        ret = '871'
    elif code == 'tcell92': #tcell92   1
        ret = '4914'
    elif code == 'tcell93':#11
        ret='474' 
    elif code=='intercom_ngn':#6
        ret='1921'
    elif code=='megafon': #4
        ret = '424'
    elif code == 'ttl_ngn':#23
        ret = '684'
    elif code == 'beeline': #9
        ret = '438'       
    elif code =='babilon-m98' or code == 'babilon-m918': #7 or 8 
        ret = '416'
    elif code == 'tkmobile':#10
        ret = '455'         
           
    return ret 
#def get_service_id(code):
#    ret = ''
#    if code == 5: #babilon_ngn
#        ret = '871'
#    elif code == 1: #tcell92
#        ret = '4914'
#    elif code == 11:#tcell93
#        ret='474' 
#    elif code==6:#intercom_ngn
#        ret='1921'
#    elif code == 4: 
#        ret = '424'
#    elif code == 23:#ttl_ngn
#        ret = '684'
#    elif code == 9: 
#        ret = '438'       
#    elif code == 7 or code == 8: 
#        ret = '416'
#    elif code == 10:#tkmobile
#        ret = '455'         
           
 #   return ret 
 
 
#функция для отправки в pardokht
def pardokht_pay (trans):
    gatew = Route.objects.get(code = 'pardokht')
    trans.try_count = nvl(trans.try_count,0) + 1
    url = gatew.note
    terminal_id = gatew.port 
    login = gatew.login
    password = gatew.password
    password = hashlib.md5(password).hexdigest()
    reciept_num = trans.id      #уникальный номер платежа
    a = trans.state.code
    if a == '0' or a == '1023':
        #новый статус надо отправить запрос на уществование абонента
        #и обновить статус в табл
        
        #изменяем статус на "В обработке"
        trans.set_state("3000")
        trans.save()
        
        msisdn = trans.number_key       #номер абонента
        #достанем код с номера
#        a = string.index(msisdn,'(')
#        b = string.index(msisdn,')')
#        code = msisdn[1+a:b]
        a=trans.opservices.code
        service_id = get_service_id(a)
        
        #msisdn =  msisdn[1:3]+msisdn[5:]
        msisdn = msisdn.replace('(','')
        msisdn = msisdn.replace(')','')
        msisdn = msisdn.replace(' ','')
        msisdn = msisdn.replace('-','')
        #отправляем платеж с суммой     
        amount = trans.summa_pay   #сумма платежа
        
        xml_data = '''<?xml version="1.0" encoding="utf-8"?>
                        <request>
                            <protocol-version>4.00</protocol-version>
                            <request-type>10</request-type>
                            <terminal-id>%s</terminal-id>
                            <extra name="login">%s</extra>
                            <extra name="password-md5">%s</extra>
                            <extra name="client-software">XML v1.1</extra>
                            <extra name="user-agent">1.2.3456.7890</extra>
                            <extra name="operating-system">Windows XP (Build 2600)</extra>
                            <extra name="serial">ABC12345</extra>
                            <auth count="1" to-amount="%s">
                            <payment>
                                <transaction-number>%s</transaction-number>
                                <from>
                                    <amount>%s</amount>
                                </from>
                                <to>
                                    <amount>%s</amount>
                                    <service-id>%s</service-id>
                                    <account-number>%s</account-number>
                                </to>
                            </payment>
                            </auth>
                        </request>'''%(terminal_id,login, password, amount,reciept_num, amount,amount, service_id,msisdn)
        
        status_code, result_code, final_st, fatal_error  = pardokht_send_data(trans, url, xml_data, gatew) #отправляем провайдеру    
        
        if result_code != '' and status_code != '':  #если имеются параметры
            
            #обновляем статусы в таблице transaction
            if result_code == "0":         #транзакция создана
                trans.date_out = datetime.now()
                trans.set_state("5000")
                trans.pay()
            elif result_code == "90":         #транзакция создана
                trans.date_out = datetime.now()
                trans.set_state("2000")
            else:    
                err_desc = pardokht_err_desc(status_code)
                trans.set_state(err_desc)
            trans.route = 'pardokht'
        
            trans.save()    
                       
            
#            #проверяем статус платежа
#            if result_code == "90":   
#                xml_data = '''<?xml version="1.0" encoding="utf-8"?>
#                        <request>
#                            <protocol-version>4.00</protocol-version>
#                            <request-type>10</request-type>
#                            <terminal-id>%s</terminal-id>
#                            <extra name="login">%s</extra>
#                            <extra name="password-md5">%s</extra>
#                            <extra name="client-software">XML v1.1</extra>
#                            <extra name="user-agent">1.2.3456.7890</extra>
#                            <extra name="operating-system">Windows XP (Build 2600)</extra>
#                            <extra name="serial">ABC12345</extra>
#                            <status count="1">
#                                <payment>
#                                    <transaction-number>%s</transaction-number>
#                                </payment>
#                            </status>
#                        </request>'''%(terminal_id,login, password, reciept_num)
#                status_code, result_code, final_st, fatal_error  = pardokht_send_data(trans, url, xml_data, gatew) #отправляем провайдеру    
#       
#                if result_code != '' :  #если имеются параметры
#                
#                    if result_code == "0":         #платеж прошел
#                        trans.set_state("5000")
#                        trans.pay()
#                    elif result_code == "90":         #транзакция создана
#                        err_desc = pardokht_err_desc(status_code) 
#                        trans.set_state("2000")
#                    else:    
#                        err_desc = pardokht_err_desc(status_code) #берем код status_code_desc и пишем в базу
#                        trans.set_state(err_desc)
#                    trans.save()    
#        else:
#            #ответ от сервера не получен обновляем статус обратно 0
#            trans.set_state(code=a)
#            
#        trans.save()
        
    elif  a == '2000':  #латеж уже отправлен проверяем статус
       
        xml_data = '''<?xml version="1.0" encoding="utf-8"?>
                        <request>
                            <protocol-version>4.00</protocol-version>
                            <request-type>10</request-type>
                            <terminal-id>%s</terminal-id>
                            <extra name="login">%s</extra>
                            <extra name="password-md5">%s</extra>
                            <extra name="client-software">XML v1.1</extra>
                            <extra name="user-agent">1.2.3456.7890</extra>
                            <extra name="operating-system">Windows XP (Build 2600)</extra>
                            <extra name="serial">ABC12345</extra>
                            <status count="1">
                                <payment>
                                    <transaction-number>%s</transaction-number>
                                </payment>
                            </status>
                        </request>'''%(terminal_id,login, password, reciept_num)
        status_code, result_code, final_st, fatal_error  = pardokht_send_data(trans, url, xml_data, gatew) #отправляем провайдеру    
        
        if result_code != '' :  #если имеются параметры
            if result_code == "0":         #платеж прошел
                trans.set_state("5000")
                trans.pay()
            elif result_code == "90":         #транзакция создана
                err_desc = pardokht_err_desc(status_code) 
                trans.set_state("2000")
            else:    
                err_desc = pardokht_err_desc(status_code) #берем код status_code_desc и пишем в базу
                trans.set_state(err_desc)
        else:
            trans.set_state(a)
        trans.save()
     
        
def annulment_pardokht(trans):
    gatew = Route.objects.get(code = 'pardokht')
    #st_annul = State.objects.get(code = '16000')
    url = gatew.note
    terminal_id = gatew.port 
    login = gatew.login
    password = gatew.password
    password = hashlib.md5(password).hexdigest()
    #tr=Transaction.objects.filter(Q(try_count__isnull=True)|Q(try_count__lte=20), route="pardokht", state = st_annul)[:3] #лимит по 3
    #for trans in tr: 
    trans.try_count = nvl(trans.try_count,0) + 1
    a = trans.state.code
    
    if a == '16000': #статус Отзыв
        reciept_num = trans.id      #уникальный номер платежа
        a = trans.state.code
   
#        #проверям дату отправки на провайдер, если существует то отправляем её, а если нет, тек дату время
#        dt_ = trans.date_out
#        if dt_ == None:
#            dt_ = datetime.now()      
#            trans.date_out = dt_
#        
        xml_data = '''<?xml version="1.0" encoding="utf-8"?>
                    <request>
                        <protocol-version>4.00</protocol-version>
                        <request-type>84</request-type>
                        <terminal-id>%s</terminal-id>
                        <extra name="login">%s</extra>
                        <extra name="password-md5">%s</extra>
                        <extra name="client-software">XML v1.1</extra>
                        <revoke-payment-list>
                           <revoke-payment transaction-number="%s"/>
                        </revoke-payment-list >
                    </request>'''%(terminal_id,login, password, reciept_num)


        
        status_code, result_code, final_st, fatal_error = pardokht_send_data(trans, url,xml_data, gatew) #отправляем провайдеру    
        
#        if req_id != '' and st != '':  #если имеются параметры
#            if st == "OK":         #платеж отменен
#                trans.set_state("14000")
#                st_copy = copy_trans(trans) #если возвращает 0, то новая транзакция создана
#                if st_copy != 0:
#                    trans.set_state('16001')
#                else:
#                    #увеличить баланс диллера на сумму отмены
#                    a = dealer_pay(trans)   #Если a =0, то все нормально
#                    if a != 0:          
#                        trans.set_state('16002')  
#                
#            else:    
#                err_desc = pardokht_err_desc(st)
#                trans.set_state(err_desc)
#        else:
#            #ответ от сервера не получен обновляем статус обратно 0
#            trans.set_state(code=a)
            
        trans.save()
            
def ins_log(trans, data, sending):
    a=Gatelog()
    a.transaction = trans
    a.sending = sending
    a.date = datetime.now()
    a.text = data
    a.save()
    
def copy_trans(trans):
    try:
        tr = Transaction()                          # Инициируем новый объект Transaction
        tr.opservices = trans.opservices
        tr.number_key = trans.number_key
        tr.summa = trans.summa
        tr.summa_pay = trans.summa_pay
        tr.hesh_id = trans.hesh_id
        tr.encashment = trans.encashment
        tr.ticket = trans.ticket 
        tr.summa_commiss = trans.summa_commiss 
        tr.agent = trans.agent 
        tr.return_reason = str(trans.date_input)+', Sozdana ot otmeni'
        #tr.date_input = datetime.now()
        
        tr.add(api = True)
        nominal = Nominal.objects.filter(transaction=trans)
        for i in nominal:
            nam = Nominal()
            nam.value = i.value
            nam.count = i.count
            nam.transaction = tr
            nam.save()
        return 0
    except Exception as inst:
        return inst

def dealer_pay(trans):
    try:
        
        d=trans.agent.dealer
        summa = trans.summa_pay
        d.summa = d.summa + summa
        d.save() 
        
#        arc = ArcMove
#        arc.dt      = False
#        arc.date    = datetime.now()
#        arc.saldo   = d.get_saldo(arc.date) 
#       
#        arc.save()
#        
        return 0
    except Exception as inst:
        return inst
        

                    
