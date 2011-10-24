from django.conf.urls.defaults import *
from django.conf.project_template.urls import urlpatterns
from django.conf import settings
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from mysite.proc.views import *
from mysite.proc.views import service
from mysite.proc.views import address
from mysite.proc.views import tarif
from mysite.proc.views import dealer
from mysite.proc.views import account
from mysite.proc.views import system
from mysite.proc.views import transaction
from mysite.proc.views import monitor
from mysite.proc.views import xls



urlpatterns=patterns('',
    
    url (r'^pay/$', xls.pay_export),
    #url (r'^pay/(?P<id_>\d+)/(?P<content>\w+)$', grids.pay_handler, name='pay_handler'),
    
    
    
    
                     
)