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
        
        j_data = simplejson.loads(expression)               # Зачитаем в переменную объект сообщения (Message)
        
        j_body = simplejson.loads(j_data["body"])           # Зачитаем объект тело сообшения
        print j_body
        
        ret = do_job(j_data["act"], j_body)                 # Отправим тело сообщения на обработку
        
        return ret
