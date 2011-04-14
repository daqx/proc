# -*- coding: utf-8 -*-
'''
Created on 17.03.2011

@author: Admin
'''
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.shortcuts import render_to_response
from mysite.proc.tarif_model import *
from mysite.proc.views.forms import *


''' ================================ TARIF_ARR ========================'''

def tarif_arr(request,tr):
    s_list = TarifArr.objects.filter(tarif=tr)
    add_url='%s/add' %tr
    tarif = Tarif.objects.get(pk=tr)
    return render_to_response('tarif_arr.html', {'s_list': s_list,'add_url': add_url,'tr':tr,'tarif':tarif})

def tarif_arr_form(request,tr,id_):
    if request.method=='POST':
        a = TarifArr.objects.get(pk=id_)

        form=TarifArrForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_arr/%s'%tr)
        else:
            return render_to_response('tarif_arr_form.html', {'form': form},context_instance=RequestContext(request))
    else:        
        s = TarifArr.objects.get(id=id_)
        form=TarifArrForm(instance=s)
        del_url="%s/delete" % id_
        
        return render_to_response('tarif_arr_form.html', {'form': form,'del_url': del_url,'tr':tr,'id':id_},context_instance=RequestContext(request))

def tarif_arr_delete(request,tr,id_):
        s = TarifArr.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/tarif_arr/%s'%tr)
    
def tarif_arr_form_add(request,tr,id_=0):
    if request.method=='POST':
        form=TarifArrForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_arr/%s'%tr)
        else:
            return render_to_response('tarif_arr_form.html', {'form': form},context_instance=RequestContext(request))
    else:
        a = Tarif.objects.get(pk=tr)
        form=TarifArrForm(initial={'tarif':a})
           
        return render_to_response('tarif_arr_form.html', {'form': form},context_instance=RequestContext(request))
    
''' ================================ TARIF ========================'''

def tarif(request):
    s_list = Tarif.objects.all()
    form=TarifForm
    return render_to_response('tarif.html', {'s_list': s_list})

def tarif_form(request,id_):
    if request.method=='POST':
        a = Tarif.objects.get(pk=id_)

        form=TarifForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif/')
        else:
            return render_to_response('tarif_form.html', {'form': form},context_instance=RequestContext(request))
    else:        
        s = Tarif.objects.get(id=id_)
        form=TarifForm(instance=s)
        del_url="%s/delete" % id_
        arr_url="/proc/tarif_arr/%s" % id_
        
        return render_to_response('tarif_form.html', {'form': form,'del_url': del_url,'arr_url': arr_url},context_instance=RequestContext(request))

def tarif_delete(request,id_):
        s = Tarif.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/tarif')
    
def tarif_form_add(request,id_=0):
    if request.method=='POST':
        form=TarifForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif/')
        else:
            return render_to_response('tarif_form.html', {'form': form},context_instance=RequestContext(request))
    else:
        
        form=TarifForm()      
        return render_to_response('tarif_form.html', {'form': form},context_instance=RequestContext(request))
    
    ''' ================================ TARIF GROUP ========================'''

def tarif_group(request):
    s_list = TarifGroup.objects.all()
    form=TarifGroupForm
    return render_to_response('tarif_group.html', {'s_list': s_list})

def tarif_group_form(request,id_):
    if request.method=='POST':
        a = TarifGroup.objects.get(pk=id_)

        form=TarifGroupForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_group/')
        else:
            return render_to_response('tarif_group_form.html', {'form': form},context_instance=RequestContext(request))
    else:        
        s = TarifGroup.objects.get(id=id_)
        form=TarifGroupForm(instance=s)
        del_url="%s/delete" % id_
       
        
        return render_to_response('tarif_group_form.html', {'form': form,'del_url': del_url},context_instance=RequestContext(request))

def tarif_group_delete(request,id_):
        s = TarifGroup.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/tarif_group')
    
def tarif_group_form_add(request,id_=0):
    if request.method=='POST':
        form=TarifGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_group/')
        else:
            return render_to_response('tarif_group_form.html', {'form': form},context_instance=RequestContext(request))
    else:
        
        form=TarifGroupForm()      
        return render_to_response('tarif_group_form.html', {'form': form},context_instance=RequestContext(request))
    
''' ================================ TARIF profile ========================'''

def tarif_profile(request):
    s_list = TarifProfile.objects.all()
    form=TarifProfileForm
    return render_to_response('tarif_profile.html', {'s_list': s_list})

def tarif_profile_form(request,id_):
    if request.method=='POST':
        a = TarifProfile.objects.get(pk=id_)

        form=TarifProfileForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_profile/')
        else:
            return render_to_response('tarif_profile_form.html', {'form': form},context_instance=RequestContext(request))
    else:        
        s = TarifProfile.objects.get(id=id_)
        form=TarifProfileForm(instance=s)
        del_url="%s/delete" % id_
        
        return render_to_response('tarif_profile_form.html', {'form': form,'del_url': del_url},context_instance=RequestContext(request))

def tarif_profile_delete(request,id_):
        s = TarifProfile.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/tarif_profile')
    
def tarif_profile_form_add(request,id_=0):
    if request.method=='POST':
        form=TarifProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_profile/')
        else:
            return render_to_response('tarif_profile_form.html', {'form': form},context_instance=RequestContext(request))
    else:
        
        form=TarifProfileForm()      
        return render_to_response('tarif_profile_form.html', {'form': form},context_instance=RequestContext(request))