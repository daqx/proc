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
from mysite.route import *

##выбрать нужные данные и отправить провайдеру
st_accept=State.objects.get(code='2000')  #статус на отправку
st_annul = State.objects.get(code = '16000')
while True:
    try :
        rt = Route.objects.get(code = 'pardokht')
        if rt.status.code == 'WORKING':
            tr=Transaction.objects.filter(Q(state=st_accept)|Q(state=st_annul), route="pardokht")[:3] #лимит по 3
            for i in tr: #цыкл только по тем транзакциям у которых статус =0
                if i.state==st_accept:
                    pardokht_pay(i)
                elif i.state==st_annul:
                    pardokht_pay(i)
            time.sleep(3)
            print ('Informations are select from transactions pardokht')
    except Exception as inst:
        print 'Error while runnig pardokht'
        print inst