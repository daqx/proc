# -*- coding: utf-8 -*-

from piston.handler import BaseHandler
from mysite.proc.models import *
from mysite.proc.sys_class import *
from mysite.proc.sys_model import *
from django.utils import simplejson
from datetime import datetime;
import time;

def isNoneId(obj):
    ''' Возвращает ID объекта если он не пустой(None)
        иначе возвращает None
    '''
    if obj is not None:
        return obj.id
    else:
        return None

def date_to_timestamp(d):
    ''' Переводит datetime в timestamp    
    '''
    if d is None:
        return None
    else:
        return time.mktime(d.timetuple())

def get_tarif_arr(t):
    ''' Возвращает в виде JSON строки массив тарифа'''
    
    ar = TarifArr.objects.filter(tarif=t)           # выберем массив тарифа
    
    data = simplejson.dumps([{"id": tr.id, "prc": tr.prc, "summa": tr.summa, "min": tr.min, "max": tr.max, 
                              "parent": tr.parent, "beg_time": tr.beg_time, "end_time": tr.end_time} for tr in ar])
    
    return data

def add_nominal( body_, tr_, val_, nam_code_):
    ''' Функция добавляет количество номиналов в массив транзакций
    '''
    if val_ in body_:
            if body_[val_]>0:
                try:
                    nam = Nominal()
                    v = NominalVal.objects.get(code = nam_code_)
                    nam.count =body_[val_] 
                    nam.value = v
                    nam.transaction = tr_
                    nam.save()
                except(NominalVal.DoesNotExist) :
                    pass

def transfer( body_, login_, retval_):
    ''' Функция вставки нового платежа 
        ACT = 0
    '''    
    retval_["status"] = "0"
        

    tr = Transaction()                          # Инициируем новый объект Transaction
    
    
    try:
        ag = Agent.objects.filter(user__username = login_)[0]           # Достанем Агента
    
        # проверить есть ли перевод с таким же hesh_id от этого терминала
        try:
            trans = Transaction.objects.filter(agent=ag.id, hesh_id=body_["hesh_id"])
        except(Transaction.DoesNotExist):
            pass
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst
            retval_["status"] = "-1"
            return
            
        tr.opservices = OpService.objects.get(id= body_["id_uslugi"])
        tr.number_key = body_["nomer"]
        tr.summa = body_["summa"]
        tr.summa_pay = body_["summa_zachis"]
        tr.hesh_id = body_["hesh_id"]
        tr.encashment = body_["id_inkas"]
        #
        tr.ticket = body_["chekn"]
        
        # Дата платежа на терминале
        if "date_create" in body_:
            try:            
                tr.date_input = datetime.fromtimestamp(float(body_["date_create"])) 
            except ValueError:
                pass
    
    
        
        #TODO: Пока оставим это так
        tr.summa_commiss = tr.summa - tr.summa_pay 
        
        tr.agent = ag 
        
        tr.add(api = True)
        
        add_nominal( body_, tr, "val1", "1_SOMONI")
        add_nominal( body_, tr, "val3", "3_SOMONI")
        add_nominal( body_, tr, "val5", "5_SOMONI")
        add_nominal( body_, tr, "val10", "10_SOMONI")
        add_nominal( body_, tr, "val20", "20_SOMONI")
        add_nominal( body_, tr, "val50", "50_SOMONI")
        add_nominal( body_, tr, "val100", "100_SOMONI")
        add_nominal( body_, tr, "val200", "200_SOMONI")
        add_nominal( body_, tr, "val500", "500_SOMONI")
               
    except(IndexError, Agent.DoesNotExist, OpService.DoesNotExist) :
        retval_["status"] = "-1"


def reg_sost( body_, login_, retval_):
    ''' Регистрация состояния терминала
        ACT = 1
    '''
    
    retval_["status"] = "0"
    
    try:
        ag = Agent.objects.filter(user__username = login_)[0]           # Достанем Агента
    except(IndexError, Agent.DoesNotExist) :
        try:
            ag = Agent.objects.filter(key_hash = login_)[0]           # Достанем Агента по хешу ключа
        except(IndexError, Agent.DoesNotExist) :
            retval_["status"] = "-1"
            return 0
    
    js = JourSostAgent()
    actS = ActualState()
    
    try:
        actS = ActualState.objects.get(agent = ag)
    except( ActualState.DoesNotExist) :
        actS.agent = ag
    
    js.agent = ag
    
    if "id" in body_:                             # Если есть hesh_id 
        retval_["hesh_id"] = body_["id"]           # То зачитаем его для ответа
  
    
    if "date" in body_:
        if body_["date"]!="0":
            try:
                js.date = datetime.fromtimestamp(float(body_["date"])) #datetime.strptime(body_["date"],'YYYY-MM-DD HH:MI:ss')
            except ValueError:
                retval_["status"] = "-1"
                return 0
        else:
            js.date = datetime.now()        
    
    else:
        js.date = datetime.now()
    
    
    actS.date = js.date        
    
    if "cash_count" in body_:
        js.cash_count = body_["cash_count"]
        actS.cash_count = js.cash_count
        
    if "link" in body_:
        js.link = bool(int(body_["link"]))
        actS.link = js.link
        
    if "cash_code" in body_:
        sa = SostAgent.objects.filter(type = "C", code = body_["cash_code"])[0]
        js.cash_code = sa
        actS.cash_code = js.cash_code
        
    if "printer" in body_:
        sa = SostAgent.objects.filter(type = "P", code = body_["printer"])[0]      
        js.printer = sa
        actS.printer = js.printer
        
    if "terminal" in body_:
        sa = SostAgent.objects.filter(type = "T", code = body_["terminal"])[0]
        js.terminal = sa
        actS.terminal = js.terminal
    
    # сохраним новый статус агента в журнале состояний
    js.save()
    
    # Очистим статус этого агента в таблице для мониторинга
    #ActualState.objects.filter(agent=ag).delete()
    
    
    # И сохраним новый статус агента
    actS.save()


def get_time(retval_):
    ''' Возвращает текущую дату
        ACT = 2
    '''
    retval_["status"] = "0"
    dt = datetime.now()
    dt = dt.strftime('%Y-%m-%d %H:%M:%S.%f') 
    retval_["body"] = str(dt)


def get_optype(login_, retval_):
    ''' Функция возвращает все типы услуг
        ACT = 5
    '''
    
    retval_["status"] = "0"
    
    try:
        id = Agent.objects.filter(user__username = login_)[0].id        # Достанем id Агента
    except(IndexError, Agent.DoesNotExist) :
        retval_["status"]="-1"
        return "-1"
           
    opt = ServiceType.objects.all()
    data = simplejson.dumps([{"id": o.id,"code": o.code, "name": o.name, "parent": isNoneId(o.parent), "order": o.order} for o in opt])
    retval_["body"] = data
    return 0


def get_opservices(login_, retval_):
    ''' Функция возвращает все доступные операторы услуг для заданного агента 
        ACT = 6
    '''
    
    retval_["status"] = "0"
    
    try:
        id = Agent.objects.filter(user__username = login_)[0].id        # Достанем id Агента
    except(IndexError, Agent.DoesNotExist) :
        retval_["status"]="-1"
        return "-1"
    
    query="select o.* from proc_opservice o, proc_agent_opservices ao where o.id=ao.opservice_id and ao.agent_id = %s" % id
    
    op = OpService.objects.raw(query)[0:]
    data = simplejson.dumps([{"id": o.id,"code": o.code, "name": o.name, "need_check": o.need_check, "mask": o.mask, "state": o.state.id, "type": o.type.id, "order": o.order} for o in op])
    retval_["body"] = data
    return 0
     
def get_tarif_from_tarifplan(tp):
    ''' Возвращает в формате JSON тарифы для заданного тарифного плана tp
    '''
    data = simplejson.dumps([{"id": tr.id, "name": tr.name,"code": tr.code, "op_service_id": tr.op_service.id, "prc": tr.prc,
                             "summa": tr.summa,"summa_own": tr.summa_own, "min": tr.min, "max": tr.max,"ru_text": tr.ru_text,
                             "tj_text": tr.tj_text,"en_text": tr.en_text, "arr" : get_tarif_arr(tr)} for tr in Tarif.objects.filter(tarif_plan = tp)])
    return data

def get_tarif_all(login_, retval_):
    ''' Функция возвращает все тарифы для доступных операторов услуг, для заданного агента 
        ACT = 7
    '''
    
    retval_["status"] = "0"
    
    try:
        id = Agent.objects.filter(user__username = login_)[0].id        # Достанем id Агента
    except(IndexError, Agent.DoesNotExist) :
        retval_["status"]="-1"
        return "-1"
    
    
    obj_ct = get_object_or_404(ContentType,app_label='proc', model='agent')  # Проверим есть ли такой content
    tp_m2m = TarifPlanM2M.objects.filter(content_type = obj_ct, object_id = id)
    s_list = []
    
    curdate = datetime.now()                                # Текущее время
    s_list = []
    # Зачитаем в массив s_list актуальные тарифные планы
    # у которых дата окончания пустая или меньше текущей даты
    for t in tp_m2m:
        if t.tarif_plan.date_end is None or t.tarif_plan.date_end > curdate:
            s_list.append(t.tarif_plan)    
    
    data = simplejson.dumps([{"id": t.id, "name": t.name, "code": t.code, "date_begin": date_to_timestamp(t.date_begin),
                             "date_end": date_to_timestamp(t.date_end),"tarif":get_tarif_from_tarifplan(t)} for t in s_list])
       
    

    retval_["body"] = data
    return 0


def get_tarif( body_, login_, retval_):
    ''' Функция возвращает тарифы для оператора услуг, для заданного агента 
        
    '''
    
    retval_["status"] = "0"
    
    try:
        id = Agent.objects.filter(user__username = login_)[0].id        # Достанем id Агента
    except(IndexError, Agent.DoesNotExist) :
        retval_["status"]="-1"
        return "-1"
    
    query="select o.* from proc_opservice o, proc_agent_opservices ao where o.id=ao.opservice_id and ao.agent_id= %s  union   select o.* from proc_opservice o, proc_agent_opservice_group aog, proc_opservicegroup_opservice ogo where  aog.opservicegroup_id=ogo.opservicegroup_id and aog.agent_id = %s" % (id, id)
    
    # Выберем список доступных операторов
    op = OpService.objects.get(body_)
    ar=[]
    
    # В цикле по операторам заполним массив ar[] тарифами этих операторов
    for o in op:
        query = 'select t.* from proc_agent_tarif_profile_arr ata, proc_tarifprofile tp, proc_tarifgroup tg,proc_tarifprofile_tarif_group tptg, proc_tarifgroup_tarif tgt, proc_tarif t,proc_opservice os where ata.agent_id=%s and tp.id=ata.tarifprofile_id and tptg.tarifprofile_id=tp.id and tptg.tarifgroup_id=tg.id and tgt.tarifgroup_id=tg.id and tgt.tarif_id=t.id and os.id=t.op_service_id and os.id=%s' % ( id, o.id)
    
        try:
            tr =Tarif.objects.raw(query)[0]
            ar.append(tr)
        except(IndexError) :
            pass
    
    # сконвертируем выбранные тарифы в JSON строку
    data = simplejson.dumps([{"id": tr.id, "name": tr.name, "op_service_id": tr.op_service.id, "prc": tr.prc,
                             "summa": tr.summa, "min": tr.min, "max": tr.max, "arr" : get_tarif_arr(tr)} for tr in ar])
    retval_["body"] = data
    return 0

def get_encashment( body_, login_, retval_):
    ''' Инкассация
        ACT = 8
    ''' 
    retval_["status"] = "0"
    
    enc = Encashment()
    
    try:
        id = Agent.objects.filter(user__username = login_)[0]        # Достанем id Агента
        enc.agent = id
    except(IndexError, Agent.DoesNotExist) :
        retval_["status"]="-1"
        return "-1"
    
    
    
    if "inkass_id" in body_:                             # Номер инкасации 
        enc.number = body_["inkass_id"]                  # То зачитаем его
        retval_["hesh_id"] = enc.number 
        
    if "summa" in body_:                                # Сумма 
        enc.summa = body_["summa"]                     # То зачитаем его
    
    if "date_inkass" in body_:
        try:
            enc.date_encash = datetime.fromtimestamp(float(body_["date_inkass"])) #datetime.strptime(body_["date"],'YYYY-MM-DD HH:MI:ss')
        except ValueError:
            retval_["status"] = "-1"
            return "-1"    
    
    
    if "user" in body_:    
        try:
            us = User.objects.filter(username = body_["user"])[0]        # Достанем User -а
            enc.user = us
        except(IndexError, User.DoesNotExist) :
            retval_["status"] = "-1"
            return "-1" 
    try:
        enc.save()
    except Exception as inst:
        print type(inst) 
        retval_["status"] = "-1"
        return "-1" 
    return 0


def do_job(act_, body_, login_, retval_):
    ''' Функция обработки команд '''        
    
    retval_["status"] = "0"
    
    if act_ == "0":                                 # Новый платеж
        transfer( body_, login_, retval_)
    
    elif act_ == "1":                               # Для журналирования состояния
        reg_sost( body_, login_, retval_)
        ret = "0"        
    
    elif act_ == "2":                               # Запрос текущего времени
        ret = get_time(retval_);
    
    elif act_ == "5":                               # Запрос типов операторов услуг
        ret = get_optype(login_, retval_);
    
    elif act_ == "6":                               # Запрос доступных операторов услуг
        ret = get_opservices(login_, retval_);
    
    elif act_ == "7":                               # Запрос списка тарифов доступных операторов услуг
        ret = get_tarif_all(login_, retval_);
    
    elif act_ == "8":                               # Инкасация
        ret = get_encashment( body_, login_, retval_);
        
    
    