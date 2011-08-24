# -*- coding: utf-8 -*-
'''
Created on 16.03.2011

@author: Admin
'''
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.shortcuts import *
from mysite.proc.service_model import *
from mysite.proc.addres_model import *
from mysite.proc.views.forms import *

'''    А Д Р Е С А    '''
def address(request, id_, content):
    
    c = get_object_or_404(ContentType,app_label='proc', model=content)  # Проверим есть ли такой content
    s_list = Addres.objects.filter(content_type = c, object_id = id_)    
    return render( request,'address.html', {'s_list': s_list,'content':content, 'id_':id_})

def address_form(request,id_, content, aid_):
    if request.method=='POST':
        a = Addres.objects.get(pk=aid_)

        form=AddressForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            url_='/proc/address/%s/%s' % (id_, content)
            return HttpResponseRedirect(url_)
        else:
            return render( request,'address_form.html', {'form': form})
    else:        
        s = Addres.objects.get(id=aid_)
        form=AddressForm(instance=s)
        del_url="%s/delete" % aid_
        
        return render( request,'address_form.html', {'form': form,'del_url': del_url})

def address_delete(request,id_, content, aid_):
        s = Addres.objects.get(id=aid_)
        s.delete()
        url_='/proc/address/%s/%s' % (id_, content)
        return HttpResponseRedirect(url_)

def address_form_add(request, id_, content):
    if request.method=='POST':
        form=AddressForm(request.POST)
        c = get_object_or_404(ContentType,app_label='proc', model=content)  # Проверим есть ли такой content
        if form.is_valid():
            a=form.save(commit = False)
            a.content_type = c
            a.object_id = id_
            a.save()
            url_='/proc/address/%s/%s' % (id_, content)
            return HttpResponseRedirect(url_)
        else:
            return render( request,'address_form.html', {'form': form})
    else:
        '''Добавление нового объекта'''
        form=AddressForm()      
        return render( request,'address_form.html', {'form': form})


'''   I P   А Д Р Е С А    '''
   
def ipaddress(request, id_, content):
    
    c = get_object_or_404(ContentType,app_label='proc', model=content)  # Проверим есть ли такой content
    s_list = IpAddress.objects.filter(content_type = c, object_id = id_)    
    return render( request,'ipaddress.html', {'s_list': s_list,'content':content, 'id_':id_})

def ipaddress_form(request,id_, content, aid_):
    if request.method=='POST':
        a = IpAddress.objects.get(pk=aid_)

        form=IpAddressForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            url_='/proc/ipaddress/%s/%s' % (id_, content)
            return HttpResponseRedirect(url_)
        else:
            return render( request,'ipaddress_form.html', {'form': form})
    else:        
        s = IpAddress.objects.get(id=aid_)
        form=IpAddressForm(instance=s)
        del_url="%s/delete" % aid_
        
        return render( request,'ipaddress_form.html', {'form': form,'del_url': del_url})

def ipaddress_delete(request,id_, content, aid_):
        s = IpAddress.objects.get(id=aid_)
        s.delete()
        url_='/proc/ipaddress/%s/%s' % (id_, content)
        return HttpResponseRedirect(url_)

def ipaddress_form_add(request, id_, content):
    if request.method=='POST':
        form=IpAddressForm(request.POST)
        c = get_object_or_404(ContentType,app_label='proc', model=content)  # Проверим есть ли такой content
        if form.is_valid():
            a=form.save(commit = False)
            a.content_type = c
            a.object_id = id_
            a.save()
            url_='/proc/ipaddress/%s/%s' % (id_, content)
            return HttpResponseRedirect(url_)
        else:
            return render( request,'ipaddress_form.html', {'form': form})
    else:
        '''Добавление нового объекта'''
        form=IpAddressForm()      
        return render( request,'ipaddress_form.html', {'form': form})
