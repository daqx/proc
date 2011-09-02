# -*- coding: utf-8 -*-
'''
Created on 21.03.2011

@author: Admin
'''
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.contrib.auth.decorators import permission_required
from django.shortcuts import *
from django.utils import simplejson
from mysite.proc.models import *
from mysite.proc.views.forms import *

''' ================================ DEALER ========================'''
@permission_required('proc.view_dealer')
def dealer(request):
    s_list = Dealer.objects.all()   
    return render(request,'dealer.html', {'s_list': s_list})

@permission_required('proc.change_dealer')
def dealer_form(request,id_):
    if request.method=='POST':
        a = Dealer.objects.get(pk=id_)

        form=DealerEditForm(request.POST, instance=a)
        if form.is_valid():
            a = form.save(commit = False)
            u=User.objects.get(pk=a.user.id)
            u.username =form.cleaned_data["username"]
            u.first_name =form.cleaned_data["first_name"]
            u.last_name =form.cleaned_data["last_name"]
            u.save()
            a.save()
            return HttpResponseRedirect('/proc/dealer/')
        else:
            return render(request,'dealer_form.html', {'form': form})
    else:        
        s = Dealer.objects.get(id=id_)
        form=DealerEditForm(instance=s,initial={'username' : s.user.username ,'first_name' : s.user.first_name ,'last_name' : s.user.last_name })
        
        del_url="%s/delete" % id_
        
        return render(request,'dealer_form.html', {'form': form,'del_url': del_url})

@permission_required('proc.delete_dealer')
def dealer_delete(request,id_):
        s = Dealer.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/dealer')

@permission_required('proc.add_dealer')
def dealer_form_add(request,id_=0):
    if request.method=='POST':
        form=DealerForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            u=User.objects.create_user(form.cleaned_data["username"], '', form.cleaned_data["password"])
            u.first_name = form.cleaned_data["first_name"]
            u.last_name = form.cleaned_data["last_name"]
            u.save()
            
            d.user = u
            d.save()
            return HttpResponseRedirect('/proc/dealer/')
        else:
            return render(request,'dealer_form.html', {'form': form})
    else:
        '''���������� ������ �������'''
        form=DealerForm(initial={'password':'', 'username' : ''})      
        return render(request,'dealer_form.html', {'form': form})
    
''' ================================ AGENT ========================'''

@permission_required('proc.view_agent')
def agent(request):
    s_list = Agent.objects.all()    
    return render(request,'agent.html', {'s_list': s_list})

@permission_required('proc.change_agent')
def agent_form(request,id_):
    if request.method=='POST':
        a = Agent.objects.get(pk=id_)
        
        hardware = ''
        
        form=AgentEditForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            a = form.save(commit = False)
            
            a.opservices = form.cleaned_data["opservices"]
            
            # Прочитаем номера HDD и Купюроприемника и запишем в JSON формате в переменную hardware
            if len(form.cleaned_data["hdd_id"])>0 :
                hardware = '"hdd_id": "%s"' % form.cleaned_data["hdd_id"]
            
            if len(form.cleaned_data["cashcode_id"])>0 :
                if len(hardware)>0:
                    hardware = '%s, "cashcode_id": "%s"' % (hardware, form.cleaned_data["cashcode_id"])
                else:
                    hardware = '"cashcode_id": "%s"' % form.cleaned_data["cashcode_id"]
            
            if len(hardware)>0:
                hardware = '{ %s }' % hardware
                a.hardware = hardware
            
            
            u=User.objects.get(pk=a.user.id)
            u.username=form.cleaned_data["username"]            
            u.first_name =form.cleaned_data["first_name"]
            u.last_name =form.cleaned_data["last_name"]            
            u.save()
            a.save()
            form.save_m2m()
            return HttpResponseRedirect('/proc/agent/')
        else:
            return render(request,'agent_form.html', {'form': form})
    else:        
        s = Agent.objects.get(id=id_)
        
        hdd_id = None
        cashcode_id = None
        hardware = {}
        
        if s.hardware != None:
            try:
                hardware = simplejson.loads(s.hardware)
            except Exception as inst:
                pass
                
            if "hdd_id" in hardware:
                hdd_id = hardware["hdd_id"]
                
            if "cashcode_id" in hardware:
                cashcode_id = hardware["cashcode_id"]
            
        form=AgentEditForm(instance=s,initial={'username' : s.user.username ,'first_name' : s.user.first_name ,'last_name' : s.user.last_name, 'hdd_id':hdd_id, "cashcode_id": cashcode_id})
        del_url="%s/delete" % id_
                
        return render(request,'agent_form.html', {'form': form,'del_url': del_url})

@permission_required('proc.delete_agent')
def agent_delete(request,id_):
        s = Agent.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/agent')

@permission_required('proc.add_agent')
def agent_form_add(request,id_=0):
    if request.method=='POST':
        form=AgentForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            
            hardware=''
            
            # Прочитаем номера HDD и Купюроприемника и запишем в JSON формате в переменную hardware
            if len(form.cleaned_data["hdd_id"])>0 :
                hardware = '"hdd_id" = "%s"' % form.cleaned_data["hdd_id"]
            
            if len(form.cleaned_data["cashcode_id"])>0 :
                if len(hardware)>0:
                    hardware = '%s, "cashcode_id"= "%s"' % (hardware, form.cleaned_data["cashcode_id"])
                else:
                    hardware = '"cashcode_id" = "%s"' % form.cleaned_data["cashcode_id"]
            
            if len(hardware)>0:
                hardware = '{ %s }' % hardware
                d.hardware = hardware
            
            u=User.objects.create_user(form.cleaned_data["username"], '', form.cleaned_data["password"])
            u.first_name = form.cleaned_data["first_name"]
            u.last_name = form.cleaned_data["last_name"]
            u.save()
            d.user = u
            d.save()
            form.save_m2m()
            return HttpResponseRedirect('/proc/agent/')
        else:
            return render(request,'agent_form.html', {'form': form})
    else:
        
        form=AgentForm(initial={'password':'', 'username' : ''})      
        return render(request,'agent_form.html', {'form': form})
    
    
    