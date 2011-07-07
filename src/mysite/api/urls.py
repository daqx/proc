# Create your views here.
from django.conf.urls.defaults import *
from piston.resource import Resource
from mysite.api.handlers import AgentHandler, CalcHandler, ListenHandler

agent_handler = Resource(AgentHandler)

class CsrfExemptResource( Resource ):
    def __init__( self, handler, authentication = None ):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

calc_resource = CsrfExemptResource( CalcHandler )
listen_resource = Resource( ListenHandler )

urlpatterns = patterns('',
   url(r'^agent/(?P<post_slug>[^/]+)/', agent_handler),
   url(r'^agent/', agent_handler),
   url( r'^calc/(?P<expression>.*)$', calc_resource ),
   url( r'^listen/(?P<expression>.*)$', listen_resource ),
)