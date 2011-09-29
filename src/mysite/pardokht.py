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
#import datetime

def ins_log(trans, data, sending):
    a=Gatelog()
    a.transaction = trans
    a.sending = sending
    a.date = datetime.now()
    a.text = data
    a.save()

#отправка всех данных и проверка ошибок
def  pardokht_send_data(trans, url, gatew):
    pay_id = reciept = status_code = dt  = ''  #переменные которые возвращаются, если пустые, то нет ответа от сервера
    #произвести запись в справочник лог данные url
    ins_log(trans, url, True)
    
    wait_time = gatew.wait_time
    #открытие соединения
    try:
        resp=urllib2.urlopen(url, None, wait_time)
        page=resp.read()    #ответ сервера провайдера
        ins_log(trans, page, False) #вставка в лог
            
        xml_read = xml.fromstring(page)
        lst = xml_read.getiterator('pay-response') 
        if len(lst)==1:     #в полученном xml должно быть "KKM_PG_GATE"
            for item in lst:
                status_code = item.find("status_code").text
                dt = item.find("time_stamp").text
                pay_id = item.find("pay_id")
                if pay_id != None:
                    pay_id = item.find("pay_id").text
                reciept = item.find("reciept")
                if reciept != None:
                    reciept = item.find("reciept").text
                   
    except Exception as inst:
        print 'Error while send data or check reply of pardokht'
        print inst
        
    return pay_id, reciept, status_code, dt    
        
def pardokht_err_desc(err_code_):
    
    try:
        err_code = int(err_code_);        
    except ValueError:
        err_code = 20820;
    
    if err_code in (-85,-84):
        err_desc = '1012'                #Ошибка аннулирования
    elif err_code >= -83 and err_code <= -51:
        err_desc = '1009'                 #Ошибка данных
    elif err_code >= -50 and err_code <= -48:
        err_desc = '1017'                #Ошибка сомонкома
    elif err_code == -46:   
        err_desc = '1010'                #Платеж зарегистрирован, но не проведен   
    elif err_code in (-41,-40):
        err_desc = '8000'                #Ошибка абонента
    elif err_code == -30:
        err_desc = '4008'                #Не достаточно средств             
    elif err_code >= -35 and err_code <= -2:
        err_desc = '1017'                #платеж не возможен, ошибки провайдера или данных
    elif err_code in (20,21):
        err_desc = '2000'                  #Транзакция создана
    elif err_code in (22,45):
        err_desc = '5000'                  #подтвержден
    elif err_code == 23:
        err_desc = '1013'                  #отменен
    elif err_code == 60:
        err_desc = '17000'                  #Пароль изменен
    elif err_code >= -112 and err_code <= -102:
        err_desc = '1001'                  #отклонен
    else:
        err_desc = '1000'                #не опознанная ошибка    аааааааааа    
    
    return err_desc

       
#функция для отправки в pardokht
def pardokht_pay (trans, gatew):
    #st_new=State.objects.get(code='0')  #статус на отправку
    trans.try_count = nvl(trans.try_count,0) + 1
    ip = gatew.ip                    #ip провайдера
    port = gatew.port
    login = gatew.login
    password = gatew.password
    
    if trans.state.code == '0':
        #новый статус надо отправить запрос на уществование абонента
        #и обновить статус в табл
        
        #изменяем статус на "В обработке"
        trans.set_state("3000")
        trans.save()
        
        msisdn = trans.number_key       #номер абонента
        
        #msisdn =  msisdn[1:3]+msisdn[5:]
        msisdn = msisdn.replace('(','')
        msisdn = msisdn.replace(')','')
        msisdn = msisdn.replace(' ','')
        msisdn = msisdn.replace('-','')
        #отправляем платеж с суммой     
        reciept_num = trans.id      #уникальный номер платежа
        amount = trans.summa_pay   #сумма платежа
        
        url = 'https://%s:%s/?USERNAME=%s&PASSWORD=%s&ACT=0&MSISDN=%s&'%(ip, port, login, password, msisdn)
        url += 'PAY_AMOUNT=%s&SOURCE_TYPE=1&TRADE_POINT=%s&CURRENCY_CODE=1&PAYMENT_NUMBER=%s'%(amount, login, reciept_num)
        
        pay_id, reciept, st, dt = pardokht_send_data(trans, url, gatew) #отправляем провайдеру    
        
        if st != '' and dt != '' and pay_id != '':  #если имеются параметры
            
            #обновляем статусы в таблице transaction
            if st == "20":         #транзакция создана
                trans.seans_number = pay_id
                trans.set_state("2000")
            else:    
                err_desc = pardokht_err_desc(st)
                trans.set_state(err_desc)
                
            trans.date_out = datetime.strptime(dt,'%d.%m.%Y %H:%M:%S')
            
            if st == "20":
                #подтверждаем платеж
                url = 'https://%s:%s/?USERNAME=%s&PASSWORD=%s&ACT=1&pay_id=%s'%(ip,port,login,password,pay_id)
                pay_id, reciept, st, dt = pardokht_send_data(trans, url, gatew) #отправляем провайдеру
                if st != '' and dt != '' and pay_id != '':  #если имеются параметры
                    if st == '22' or st == '45': #платеж успешно проведен
                        trans.set_state("5000")
                        trans.pay()
                    else:
                        err_desc = pardokht_err_desc(st)
                        trans.set_state(err_desc)
                    trans.date_out = datetime.strptime(dt,'%d.%m.%Y %H:%M:%S')    
        else:
            #ответ от сервера не получен обновляем статус обратно 0
            trans.set_state(code='0')
            
        trans.save()
    elif  trans.state.code == '2000':  #латеж уже отправлен подтверждаем его
        pay_id = trans.seans_number #номер платежа который надо проверить
        if pay_id == None:
            trans.set_state('0')
        else:
            url = 'https://%s:%s/?USERNAME=%s&PASSWORD=%s&ACT=1&pay_id=%s'%(ip,port,login,password,pay_id)
            pay_id, reciept, st, dt = pardokht_send_data(trans, url, gatew) #отправляем провайдеру
            if st != '' and dt != '' and pay_id != '':  #если имеются параметры
                if st == '22' or st == '45': #платеж успешно проведен
                    trans.set_state("5000")
                    trans.pay()
                else:
                    err_desc = pardokht_err_desc(st)
                    trans.set_state(err_desc)
                trans.date_out = datetime.strptime(dt,'%d.%m.%Y %H:%M:%S')
            else:
                #ответ от сервера не получен обновляем статус обратно 2000
                trans.set_state(code='2000')
        trans.save()

##выбрать нужные данные и отправить провайдеру
#while True:
#    try :
#        gatew = Gateway.objects.get(code = 'pardokht')
#        if gatew.status.code == 'WORKING':
#            st_new=State.objects.get(code='0')  #статус на отправку
#            tr=Transaction.objects.filter(Q(try_count__isnull=True)|Q(try_count__lte=10), Q(state = st_new)|Q(state__code = '2000') , opservices__code = 'pardokht')[:3] #лимит по 3
#            for i in tr: #цыкл только по тем транзакциям у которых статус =0
#                d = i.agent.dealer
#                saldo = d.get_saldo(datetime.now())
#                
#                if d.overdraft == None:
#                    d.overdraft = 0
#                    
#                if d.limit == None:
#                    d.limit = 0
#                if saldo + d.overdraft - d.limit >= i.summa_pay:     #проверяем баланс диллера
#                    pardokht_pay(i, gatew)
#            time.sleep(3)
#            print ('Informations are select from transactions')
#    except Exception as inst:
#        print 'Error while runnig log_msg'
#        print inst
#                    
