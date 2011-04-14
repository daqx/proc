from django.conf.urls.defaults import *
from mysite.ordercard.views import *
from django.conf.project_template.urls import urlpatterns

urlpatterns=patterns('',
    url(r'^$',archive),

    (r'^search-form/$', search_form),
    (r'^search/$', search),
    (r'^contact/$', contact),
    (r'^contact_form/$', contact_form),
                     
)