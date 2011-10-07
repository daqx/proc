# -*- coding: utf-8 -*-
import sys;
import time;
import pycurl

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

class Response(object):
    """ utility class to collect the response """
    def __init__(self):
        self.chunks = []
    def callback(self, chunk):
        self.chunks.append(chunk)
    def content(self):
        return ''.join(self.chunks)
    
#отправка всех данных и проверка ошибок
def babilon_send_data(trans, url, gatew):
    req_id = rrn = st = ''  #переменные которые возвращаются, если пустые, то нет ответа от сервера
    #произвести запись в справочник лог данные url
    ins_log(trans, url, True)
    #
    wait_time = gatew.wait_time
    cert = 'C:/cert/CA.cer'
    key = 'C:/cert/key.pem'
    url=str(url)
    #открытие соединения
    try:
        res = Response()
        curl = pycurl.Curl()
        curl.setopt(curl.WRITEFUNCTION, res.callback)
        curl.setopt(curl.SSL_VERIFYHOST, 0)
        curl.setopt(curl.SSL_VERIFYPEER, 0)
        curl.setopt(curl.CAINFO, cert)
        curl.setopt(curl.SSLCERT, key)
        curl.setopt(curl.URL, url)
        curl.perform()
        page=res.content()   #ответ сервера провайдера
        ins_log(trans, page, False) #вставка в лог
        
        i=string.find(page,'<response')
        b=string.find(page,'>', i)
        page=page[:i+9]+page[b:] 
           
        xml_read = xml.fromstring(page)
        lst = xml_read.getiterator('response') 
        if len(lst)==1:     #в полученном xml должно быть "response"
            for item in lst:
                req_id = item.find("req_id").text    #идентификатор присвоенный запросу
                rrn = item.find("rrn").text          #идентификатор платежа
                st = item.find("status").text
                
    except Exception as inst:
        print 'Error while send data or check reply of MEGAFON'
        print inst
    return req_id, rrn, st   
        
def babilon_err_desc(st):
    if st=='OK':            #Операция завершена успешно.
        err_desc = '5000' 
    elif st == 'ERROR' or st=='ERR_SUMM' or  st=='ERR_CURRENCY':     #Ошибка обработки операции или неверный формат сообщения.
        err_desc = '1009' 
    elif st=='ERR_PHONE':   #Ошибка в номере абонента (например, абонент не найден).
        err_desc = '8000' 
    elif st=='ERR_NODB':    #Нет соединения с БД.
        err_desc = '1017'                   
    elif st=='ERR_FORBIDEN':#На контракт абонента запрещен прием данного вида платежей.
        err_desc = '8001'                
    elif st=='ERR_REPEAT':  #Платеж с таким номером уже принят.
        err_desc = '1018'                 
    elif st=='ERR_DATE':    #Ошибка в дате платежа: платеж либо слишком старый, либо будущей датой.
        err_desc = '1005' 
    elif st=='ERR_PAYMENT': #Платеж не найден.
        err_desc='4011'                
    else:
        err_desc = '4004'                #не опознанная ошибка    аааааааааа    

    return err_desc
        
#функция для отправки в megafon
def babilonm_pay (trans, gatew):
    #st_new=State.objects.get(code='0')  #статус на отправку
    trans.try_count = nvl(trans.try_count,0) + 1
    a = trans.state.code
    
    if a == '0' or a == '1023':
        #новый статус надо отправить запрос на уществование абонента
        #и обновить статус в табл
        
        #изменяем статус на "В обработке"
        trans.set_state("3000")
        trans.save()
        
        msisdn = trans.number_key       #номер абонента
        ip = gatew.ip                    #ip провайдера
        ps_id = gatew.password
        pt = gatew.login
        port = gatew.port
        
        msisdn = msisdn.replace('(','')
        msisdn = msisdn.replace(')','')
        msisdn = msisdn.replace(' ','')
        msisdn = msisdn.replace('-','')
       
        #отправляем платеж с суммой     
        reciept_num = trans.id     #уникальный номер платежа
        amount = trans.summa_pay   #сумма платежа
        
        #проверям дату отправки на провайдер, если существует то отправляем её, а если нет, тек дату время
        dt_ = trans.date_out
        if dt_ == None:
            dt_ = datetime.now()      
            trans.date_out = dt_
        
        dt = dt_.strftime('%Y%m%d')  #дата для отправки 
        tm = dt_.strftime('%H%M%S')  #время для отправки 
        
        url = "https://%s:%s/xmlinterface.asmx/Payment?ps_id=%s&rrn=%s"%(ip, port, ps_id, reciept_num)
        url += "&pt=%s&date=%s&time=%s&phone=%s&amount=%s&currency=TJS"%(pt, dt, tm, msisdn, amount)
        req_id, rrn, st  = babilon_send_data(trans, url, gatew) #отправляем провайдеру    
        
        if req_id != '' and st != '':  #если имеются параметры
            
            #обновляем статусы в таблице transaction
            if st=='ERR_REPEAT':  #платеж существует. Закрываем транзакцию
                trans.set_state("5000")
                trans.pay
            elif st == "OK":         #платеж принят
                trans.set_state("5000")
                trans.pay
            else:    
                err_desc = babilon_err_desc(st)
                trans.set_state(err_desc)
        else:
            #ответ от сервера не получен обновляем статус обратно 0
            trans.set_state(code='0')
            
        trans.save()
        

#выбрать нужные данные и отправить провайдеру
#Во всех транзакциях при выборке сотрировка идет сначала по статусу 0 потом 1023
st_new=State.objects.get(code='0')  #статус на отправку
st_no_money = State.objects.get(code='1023')
babilon98 = OpService.objects.get(code='babilon-m98')
babilon918 = OpService.objects.get(code='babilon-m918')
while True:
    try :
        gatew = Gateway.objects.get(code = 'babilon-m')
        st_gatew = gatew.status.code 
        if gatew.status.code == 'WORKING':
            st_route = gatew.route.code 
            #Если st_route = self, то маршрутизация не задана. Выбираем нужный маршрут и вызываем его 
            if st_route == 'self':
                tr=Transaction.objects.filter(Q(try_count__isnull=True)|Q(try_count__lte=10), Q(state = st_new)|Q(state = st_no_money), Q(opservices = babilon98)|Q(opservices = babilon918)).order_by("state")[:3] #лимит по 3
                for i in tr: #цыкл только по тем транзакциям у которых статус = 0 или 1023
                    d = i.agent.dealer
                    saldo = d.get_saldo(datetime.now())
                    
                    if d.overdraft == None:
                        d.overdraft = 0
                        
                    if d.limit == None:
                        d.limit = 0
                    if saldo + d.overdraft - d.limit >= i.summa_pay:     #проверяем баланс диллера
                        babilonm_pay(i, gatew)
                    else:
                        i.set_state('1023') #не достаточно средств
            elif st_route == 'pardokht':
                if gatew.route.status.code == 'WORKING':
                    tr=Transaction.objects.filter(Q(try_count__isnull=True)|Q(try_count__lte=10), Q(state = st_new)|Q(state = st_no_money), Q(opservices = babilon98)|Q(opservices = babilon918)).order_by("state")[:3] #лимит по 3
                    for i in tr: #цыкл только по тем транзакциям у которых статус =0 или 1023
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
        print ('Informations are select from transactions babilon-m')
    except Exception as inst:
        print 'Error while runnig log_msg'
        print inst
#выбрать нужные данные и отправить провайдеру
#try :
#    while True:
#        st_new=State.objects.get(code='0')  #статус на отправку
#        tr=Transaction.objects.filter(Q(try_count__isnull=True)|Q(try_count__lte=10), state = st_new)[:3] #лимит по 3
#        for i in tr: #цыкл только по тем транзакциям у которых статус =0
#            d = i.agent.dealer
#            saldo = d.get_saldo(datetime.now())
#            
#            if d.overdraft == None:
#                d.overdraft = 0
#                
#            if d.limit == None:
#                d.limit = 0
#                
#            if saldo + d.overdraft - d.limit >= i.summa_pay:     #проверяем баланс диллера
#                op_ser = i.opservices #ссылка на провайдера
#                gatew = Gateway.objects.get(opservice=op_ser)
#                if gatew.status.code == 'WORKING':
#                    if gatew.code == 'MEGAFON':
#                        #if i.number_key == '(90) 100-01-81':
#                        megafon_pay(i, gatew)
#        time.sleep(3)
#        print ('Informations are select from transactions')
#except Exception as inst:
#        print 'Error while runnig log_msg'
#        print inst
                    

#    if service.state=='true':
#        
#    
#    num=i.number_key
#    ser_ip=service.ip
#    ser_login=service.login
#    ser_password=service.password
    #api на сервере использовать для теста
    #найти urllib2 с https://

    
#    
#resp=urllib2.urlopen('http://192.168.7.219/api/calc/1+1')
#>>> page=resp.read()
#>>> print page

#    def inflect(name, case=2):
#    import urllib
#    from xml.etree import ElementTree
#    url = 'http://export.yandex.ru/inflect.xml?'
#    url += urllib.urlencode([('name', name.encode('utf-8'))])
#    response = urllib.urlopen(url)
#    tree = ElementTree.parse(response)
#    cases = tree.findall('inflection')
#    if len(cases) > 1:
#        return cases[case+1].text
#    return name


#def get_lat_long(location):
#  """a function that converts the location address to it's longitude and latitude"""
#  key=settings.GOOGLE_MAPS_API_KEY
#  output = 'csv'
#  location=urllib.quote_plus(location.encode('utf-8'))
#  request = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output, key) #wyslanie zapytania do google maps
#  data=urllib.urlopen(request).read()
#  dlist=data.split(',')
#  if dlist[0]=='200': 
#    return dlist[2],dlist[3] 
#  else:
#    return 0,0
#
#class Location(models.Model):
#  """a simple model for defining a company location and automatic calculation of longitude and latitude"""
#
#  address = models.CharField(blank=False, max_length=150,verbose_name='Adres'")
#  longitude = models.FloatField()
#  latitude = models.FloatField()
#
#
#  def save(self, **kwargs):       
#      self.latitude, self.longitude = get_lat_long(self.address)
#      super(Location, self).save(**kwargs)    
#    

#Есть урл который генерит мне PDF файл навиндовой машине.
#Мне со своей Бубунты надо подключатся к этой винде и дергать ссылку которая генерит файл. Для того чтоб генерация ссылки произошла надо авторизоватся на винде.
#Пробую авторизоватся так:
#
#import urllib2
#from ntlm import HTTPNtlmAuthHandler
#
#user = 'admin'
#password = "admin"
#url = "http://10.0.9.99:8080/ReportServer/Pages/ReportViewer.aspx?%2ftest_pdf&rs:Format=PDF&rs:Command=Render"
#
#passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
#passman.add_password(None, url, user, password)
#
#auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)
#
#
#opener = urllib2.build_opener(auth_NTLM)
#urllib2.install_opener(opener)
#
#
#response = urllib2.urlopen(url)
#print(response.read())