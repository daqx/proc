# -*- coding: utf-8 -*-
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.shortcuts import render_to_response
from mysite.proc.service_model import *
from mysite.proc.views.forms import *


def service_type(request):
    s_list = ServiceType.objects.all()   
    return render_to_response('service_type.html', {'s_list': s_list})

def service_type_form(request,id_):
    if request.method=='POST':
        a = ServiceType.objects.get(pk=id_)

        form=ServiceTypeForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/service_type/')
        else:
            return render_to_response('servicetype_form.html', {'form': form},context_instance=RequestContext(request))
    else:        
        s = ServiceType.objects.get(id=id_)
        form=ServiceTypeForm(instance=s)
        del_url="%s/delete" % id_
        
        return render_to_response('servicetype_form.html', {'form': form,'del_url': del_url},context_instance=RequestContext(request))

def service_type_delete(request,id_):
        s = ServiceType.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/service_type')

def service_type_form_add(request,id_=0):
    if request.method=='POST':        

        form=ServiceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/service_type/')
        else:
            return render_to_response('servicetype_form.html', {'form': form},context_instance=RequestContext(request))
    else:
        '''Добавление нового объекта'''
        form=ServiceTypeForm()      
        return render_to_response('servicetype_form.html', {'form': form},context_instance=RequestContext(request))
    
    
''' ================================ OP_SERVICE ========================'''

def op_service(request):
    s_list = OpService.objects.all().order_by('type')
    form=OpServiceForm
    return render_to_response('op_service.html', {'s_list': s_list})

def op_service_form(request,id_):
    if request.method=='POST':
        a = OpService.objects.get(pk=id_)

        form=OpServiceForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/op_service/')
        else:
            return render_to_response('op_service_form.html', {'form': form},context_instance=RequestContext(request))
    else:        
        s = OpService.objects.get(id=id_)
        form=OpServiceForm(instance=s)
        del_url="%s/delete" % id_
        
        return render_to_response('op_service_form.html', {'form': form,'del_url': del_url},context_instance=RequestContext(request))

def op_service_delete(request,id_):
        s = OpService.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/op_service')
    
def op_service_form_add(request,id_=0):
    if request.method=='POST':
        form=OpServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/op_service/')
        else:
            return render_to_response('op_service_form.html', {'form': form},context_instance=RequestContext(request))
    else:
        '''Добавление нового объекта'''
        form=OpServiceForm()      
        return render_to_response('op_service_form.html', {'form': form},context_instance=RequestContext(request))

    ''' ================================ OP_SERVICE ========================'''

def op_service_group(request):
    s_list = OpServiceGroup.objects.all()
    form=OpServiceGroupForm
    return render_to_response('op_service_group.html', {'s_list': s_list})

def op_service_group_form(request,id_):
    if request.method=='POST':
        a = OpServiceGroup.objects.get(pk=id_)

        form=OpServiceGroupForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/op_service_group/')
        else:
            return render_to_response('op_service_group_form.html', {'form': form},context_instance=RequestContext(request))
    else:        
        s = OpServiceGroup.objects.get(id=id_)
        form=OpServiceGroupForm(instance=s)
        del_url="%s/delete" % id_
        
        return render_to_response('op_service_group_form.html', {'form': form,'del_url': del_url},context_instance=RequestContext(request))

def op_service_group_delete(request,id_):
        s = OpServiceGroup.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/op_service_group')
    
def op_service_group_form_add(request,id_=0):
    if request.method=='POST':
        form=OpServiceGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/op_service_group/')
        else:
            return render_to_response('op_service_group_form.html', {'form': form},context_instance=RequestContext(request))
    else:
        '''Добавление нового объекта'''
        form=OpServiceGroupForm()      
        return render_to_response('op_service_group_form.html', {'form': form},context_instance=RequestContext(request))
    