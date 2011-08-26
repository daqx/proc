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



tr=Transaction.objects.all()

for i in tr:
	print i
	time.sleep(2)


cursor = connection.cursor()

result = cursor.execute("select nextval('winner')")
row = cursor.fetchone()	