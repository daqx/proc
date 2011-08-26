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
from django.db import connection
from django.utils import simplejson



def isNoneId(obj):
    ''' Возвращает ID объекта если он не пустой(None)
        иначе возвращает None
    '''
    if obj is not None:
        return obj.id
    else:
        return None


def get_tarif_arr(t):
    
    ar = TarifArr.objects.filter(tarif=t)
    
    data = simplejson.dumps([{"id": tr.id, "prc": tr.prc, "summa": tr.summa, "min": tr.min, "max": tr.max} for tr in ar])
    print data
    return data



login_= 'agent4_2'
    
try:
    id = Agent.objects.filter(user__username = login_)[0].id        # Достанем id Агента
except(IndexError, Agent.DoesNotExist) :
    pass
           
query="select o.* from proc_opservice o, proc_agent_opservices ao where o.id=ao.opservice_id and ao.agent_id= %s  union   select o.* from proc_opservice o, proc_agent_opservice_group aog, proc_opservicegroup_opservice ogo where  aog.opservicegroup_id=ogo.opservicegroup_id and aog.agent_id = %s" % (id, id)
    
# Выберем список доступных операторов
op = OpService.objects.raw(query)
ar=[]
    
# В цикле по операторам заполним массив ar[] тарифами этих операторов
for o in op:
    query = 'select t.* from proc_agent_tarif_profile_arr ata, proc_tarifprofile tp, proc_tarifgroup tg,proc_tarifprofile_tarif_group tptg, proc_tarifgroup_tarif tgt, proc_tarif t,proc_opservice os where ata.agent_id=12 and tp.id=ata.tarifprofile_id and tptg.tarifprofile_id=tp.id and tptg.tarifgroup_id=tg.id and tgt.tarifgroup_id=tg.id and tgt.tarif_id=t.id and os.id=t.op_service_id and os.id=%s' % o.id
    
    try:
        tr =Tarif.objects.raw(query)[0]
        ar.append(tr)
    except(IndexError) :
        pass
    

data = simplejson.dumps([{"id": tr.id, "name": tr.name, "op_service_id": tr.op_service.id, "prc": tr.prc,
                             "summa": tr.summa, "min": tr.min, "max": tr.max, "arr" : get_tarif_arr(tr)} for tr in ar])


print data




