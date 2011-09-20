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
from mysite.proc.views import grids



urlpatterns=patterns('',
    #url(r'^$', system.main),    
    url (r'^journal/(\d+)$', grids.journal_handler, name='jurnal_handler'), 
    url (r'^journal/cfg/$', grids.grid_config, name='grid_config'),
    
    url (r'^monitor/$', grids.grid_handler, name='grid_handler'), 
    url (r'^monitor/cfg/$', grids.grid_config, name='grid_config'),
    
    url (r'^pay/$', grids.pay_handler, name='pay_handler'),
    
    #(r'^login/$', login_view),
    #(r'^contact/$', contact),
    #(r'^contact_form/$', contact_form),
    
    
                     
)