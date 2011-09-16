# -*- coding: utf-8 -*-
import sys;
import time;

sys.path.append('D:/work/proc/src/')
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

#import datetime

def ins_log(trans, data, sending):
	a=Gatelog()
	a.transaction = trans
	a.sending = sending
	a.date = datetime.now()
	a.text = data
	a.save()

#отправка всех данных и проверка ошибок
def megafon_send_data(trans, url, gatew):
	err_code = dt_oper = reciept_num = ''  #переменные которые возвращаются, если пустые, то нет ответа от сервера
	#произвести запись в справочник лог данные url
	ins_log(trans, url, True)
	#
	login = gatew.login
	password = gatew.password
	wait_time = gatew.wait_time
	
	#подготовка к подключению
	pass_man=urllib2.HTTPPasswordMgrWithDefaultRealm()
	pass_man.add_password(None, url, login, password)
	auth_handler=urllib2.HTTPBasicAuthHandler(pass_man)
	opener=urllib2.build_opener(auth_handler)
	urllib2.install_opener(opener)
	
	#открытие соединения
	try:
		resp=urllib2.urlopen(url, None, wait_time)
		page=resp.read()    #ответ сервера провайдера
		ins_log(trans, page, False) #вставка в лог
			
		xml_read = xml.fromstring(page)
		lst = xml_read.getiterator('KKM_PG_GATE') 
		if len(lst)==1:     #в полученном xml должно быть "KKM_PG_GATE"
			for item in lst:
				dt_oper=item.find("OPERATION_DATE").text    #дата операции с сервера
				er=item.getiterator("ERROR")
				for error in er:
					err_code = error.attrib["SQLCODE"]		#код ошибки
					err_mes = error.attrib["SQLERRM"]		#собщ. ошибки
				
	except Exception as inst:
		print 'Error while send data or check reply of MEGAFON'
		print inst
	return err_code, dt_oper, reciept_num	
		
def megafon_err_desc(err_code_):
	
	try:
		err_code = abs(int(err_code_));		
	except ValueError:
		err_code = 20820;
	
	if err_code in (20800,20801):
		err_desc = '8000'				#Клиент не найден
	elif err_code in(20808, 20809):
		err_desc = '1011' 				#указанный номер чека уже существует    аааааааааа
	elif err_code == 20810:
		err_desc = '1016'				#Платеж не принимается     аааааааааа
	elif err_code in (20818, 20819):	#Отвергнут по техническим причинам
		err_desc =	'1002'
	elif err_code>=20820 and err_code<=20825:
		err_desc = '1017'				#ошибки сервера         аааааааааа		
	elif err_code>=20826 and err_code<=20871:
		err_desc = '1009'				#не правильные данные   Отвергнут, неверный запрос.
	elif err_code in (20875,20876,20894):
		err_desc = '0'  				#операция запрещена провайдером    аааааааааа
	elif err_code in (20877,20893) or err_code==20895:
		err_desc = '1000'  				#операция запрещена провайдером    аааааааааа
	else:
		err_desc = '1000'				#не опознанная ошибка    аааааааааа	
	
	return err_desc
		
#функция для отправки в megafon
def megafon_pay (trans, gatew):
	#st_new=State.objects.get(code='0')  #статус на отправку
	trans.try_count+=1
	
	if trans.state.code == '0':
		#новый статус надо отправить запрос на уществование абонента
		#и обновить статус в табл
		
		#изменяем статус на "В обработке"
		trans.set_state("3000")
		trans.save()
		
		msisdn = trans.number_key       #номер абонента
		ip = gatew.ip					#ip провайдера
		url = 'https://%s/ttm_kkm_int/kkm_pg_gate/KKM_PG_GATE.HTTP_ADD_PAYMENT?P_MSISDN=%s' %(ip, msisdn)
		err_code, dt_oper, reciept_num = megafon_send_data(trans, url, gatew)
		if err_code != '' and dt_oper != '':  		#если имеются параметры
			if err_code != '0':				
				err_desc = megafon_err_desc(err_code)	#получаем статус для обновление таблицы
				trans.set_state(err_desc)				#обновляем статусы в таблице transaction
			
		else:
			#ответ от сервера не получен обновляем статус обратно на 0
			trans.set_state("0")
			return
		
		trans.save()
		
		#если err_code не 0 то выходим из операции, так как произошла ошибка при проверке абонента
		if err_code != '0':
			return 0
		
		#отправляем платеж с суммой 	
		reciept_num = trans.id      #уникальный номер платежа
		amount = trans.summa_pay   #сумма платежа
		
		#проверям дату отправки на провайдер, если существует то отправляем её, а если нет, тек дату время
		dt = trans.date_out
		if dt == None:
			dt = datetime.now() 	 
			trans.date_out = dt
		
		dt = dt.strtime('%d%m%Y%H%M%S')  #дата время для отправки на провайдер
		
		url = 'https://%s/ttm_kkm_int/kkm_pg_gate/KKM_PG_GATE.HTTP_ADD_PAYMENT?P_MSISDN=%s&'%(ip, msisdn)
		url += 'P_RECEIPT_NUM=%s&P_PAY_AMOUNT=%s&'%(reciept_num, amount)
		url += 'P_RECEIPT_GLOBALLY_UNIQUE=1&P_DATE=%s'%dt 
		err_code, dt_oper, reciept_num = megafon_send_data(trans, url, gatew) #отправляем провайдеру	
		
		if err_code != '' and dt_oper != '':  #если имеются параметры
			
			#обновляем статусы в таблице transaction
			if err_code=='-20808':  #платеж существует. Закрываем транзакцию
				trans.set_state("5000")
				trans.pay
			elif err_code == "0": 		#платеж принят
				trans.set_state("0")
			else:	
				err_desc = megafon_err_desc(err_code)
				trans.set_state(err_desc)
		else:
			#ответ от сервера не получен обновляем статус обратно 0
			trans.set_state(code='0')
			
		trans.save()
		
		if err_code != '-20808': #платеж существует
			return 0
		
		#проверяем платеж на существование
		url = 'https://%s/ttm_kkm_int/kkm_pg_gate/KKM_PG_GATE.HTTP_ADD_PAYMENT?P_RECEIPT_NUM=%s'%(ip,reciept_num)
		url += '&P_RECEIPT_GLOBALLY_UNIQUE=1&P_DATE=%s'%dt
		err_code, dt_oper, reciept_num = megafon_send_data(trans, url, gatew) #отправляем провайдеру
		if err_code != '' and dt_oper != '':  #если имеются параметры
						
			#обновляем статусы в таблице transaction
			if err_code=='-20808':  #платеж существует. Закрываем транзакцию
				trans.stet_state("5000")
				trans.pay
			elif err_code=='0':   #платеж не существует устанавливаем статус на 0
				trans.set_state("0")			
			else:
				err_desc = megafon_err_desc(err_code)	#получаем статус ошибки
				trans.set_state(err_desc)	
		else:
			#ответ от сервера не получен обновляем статус обратно на 0
			trans.set_state("0")
		trans.save()

#выбрать нужные данные и отправить провайдеру

st_new=State.objects.get(code='0')  #статус на отправку
tr=Transaction.objects.filter(try_count__lte=10, state = st_new)[:3] #лимит по 3
for i in tr: #цыкл только по тем транзакциям у которых статус =0
	d = i.agent.dealer
	saldo = d.get_saldo(datetime.now())
	if saldo + d.overdraft - d.limit >= i.summa_pay:     #проверяем баланс диллера
		op_ser = i.opservices #ссылка на провайдера
		gatew = Gateway.objects.get(opservice=op_ser)
		if gatew.status.code == 'WORKING':
			if gatew.code == 'MEGAFON':
				if i.number_key == '901000181':
					megafon_pay(i, gatew)
			elif gatew.name == 'tcell':
				a=1

#	if service.state=='true':
#		
#	
#	num=i.number_key
#	ser_ip=service.ip
#	ser_login=service.login
#	ser_password=service.password
	#api на сервере использовать для теста
	#найти urllib2 с https://

	
#	
#resp=urllib2.urlopen('http://192.168.7.219/api/calc/1+1')
#>>> page=resp.read()
#>>> print page

#	def inflect(name, case=2):
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