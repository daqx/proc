from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),
    (r'^$', include('mysite.proc.urls')),
    #(r'^blog/', include('mysite.blog.urls')),
    #(r'^ordercard/', include('mysite.ordercard.urls')),
    #(r'^kiosk/', include('mysite.kiosk.urls')),
    (r'^proc/', include('mysite.proc.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
)
