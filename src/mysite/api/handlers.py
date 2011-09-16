# -*- coding: utf-8 -*-

from django.contrib import auth
from django.utils import simplejson
from piston.handler import BaseHandler
from mysite.proc.models import *
from mysite.proc.sys_class import *
from mysite.api.utils import *
from urllib import unquote_plus
import logging

# Get an instance of a logger
logger = logging.getLogger('proc')



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
        
        #expression = expression.replace('/','\\')
        #logger.info(expression)
        retval = {}
        #print expression
        #print "path - %s" % request.path
        #b = request.path.find('/api/listen/')
        #e = request.path.find('/api/listen/',20)
        
        #if e>0:        
        #    expression = request.path[12:e]
        #else:
        #    expression = request.path[12:]
        
        # декодируем экранированную строку
        expression = unicode(unquote_plus(str(expression)), 'utf-8')
        #print "expression - %s" % expression
        try:
            j_data = simplejson.loads(expression)               # Зачитаем в переменную объект сообщения (Message)
            
            user = auth.authenticate(username = j_data["login"], password = j_data["passw"])
            
            retval["act"] = j_data["act"]                       # Зачитаем act для ответа
                        
            if j_data["body"]!="":
                j_body = simplejson.loads(j_data["body"])       # Зачитаем объект тело сообшения
            else:
                j_body = "1234"
            
            
            if "hesh_id" in j_body:                             # Если есть hesh_id 
                retval["hesh_id"] = j_body["hesh_id"]           # То зачитаем его для ответа
            
            # Аутентификация пользователя
            if user is None or not user.is_active:
                retval["status"]  = "-2"
                return retval
            
            print j_body
        
            ret = do_job(j_data["act"], j_body, j_data["login"], retval)                 # Отправим тело сообщения на обработку

        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst
            print expression
            retval["status"]  = "-1"
        
        return retval
