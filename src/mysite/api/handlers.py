# -*- coding: utf-8 -*-

from piston.handler import BaseHandler
from mysite.proc.models import *

class AgentHandler(BaseHandler):
   allowed_methods = ('GET',)
   model= Agent
   
   def read( self, request, expression ):
        return eval( expression )
    

class CalcHandler( BaseHandler ):
    def read( self, request, expression ):
        return eval( expression )