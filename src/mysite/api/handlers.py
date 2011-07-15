# -*- coding: utf-8 -*-

from piston.handler import BaseHandler
from mysite.proc.models import *
from mysite.proc.sys_class import *
from django.utils import simplejson
from mysite.api.utils import *

class AgentHandler(BaseHandler):
   allowed_methods = ('GET',)
   model= Agent
   
   def read( self, request ):
        return Agent.objects.all()
    

class CalcHandler( BaseHandler ):
    def read( self, request, expression ):
        return eval( expression )
    
class ListenHandler(BaseHandler):   
    # Все запросы будут обрабатыватся здесь
    def read( self, request, expression ):
        
        try:
            j_data = simplejson.loads(expression)               # Зачитаем в переменную объект сообщения (Message)
        
            if j_data["body"]!="":
                j_body = simplejson.loads(j_data["body"])       # Зачитаем объект тело сообшения
            else:
                j_body = "1234"

            print j_body
        
            ret = do_job(j_data["act"], j_body, j_data["login"])                 # Отправим тело сообщения на обработку

        except: #Exception as inst:
            #print type(inst)     # the exception instance
            #print inst.args      # arguments stored in .args
            #print inst
            ret = "-1"
        
        return ret
