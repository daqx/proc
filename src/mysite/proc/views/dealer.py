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
from mysite.proc.models import *
from mysite.proc.views.forms import *

''' ================================ DEALER ========================'''
def dealer(request):
    s_list = Dealer.objects.all()   
    return render(request,'dealer.html', {'s_list': s_list})

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

def dealer_delete(request,id_):
        s = Dealer.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/dealer')

def dealer_form_add(request,id_=0):
    if request.method=='POST':
        form=DealerForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            u=User.objects.create_user(form.cleaned_data["username"], '', form.cleaned_data["password"])
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

def agent_form(request,id_):
    if request.method=='POST':
        a = Agent.objects.get(pk=id_)

        form=AgentEditForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            a = form.save(commit = False)
            u=User.objects.get(pk=a.user.id)
            u.username=form.cleaned_data["username"]            
            u.first_name =form.cleaned_data["first_name"]
            u.last_name =form.cleaned_data["last_name"]
            u.save()
            a.save()
            return HttpResponseRedirect('/proc/agent/')
        else:
            return render(request,'agent_form.html', {'form': form})
    else:        
        s = Agent.objects.get(id=id_)
        form=AgentEditForm(instance=s,initial={'username' : s.user.username ,'first_name' : s.user.first_name ,'last_name' : s.user.last_name})
        del_url="%s/delete" % id_
                
        return render(request,'agent_form.html', {'form': form,'del_url': del_url})

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
            u=User.objects.create_user(form.cleaned_data["username"], '', form.cleaned_data["password"])
            u.save()
            d.user = u
            d.save()
            return HttpResponseRedirect('/proc/agent/')
        else:
            return render(request,'agent_form.html', {'form': form})
    else:
        
        form=AgentForm(initial={'password':'', 'username' : ''})      
        return render(request,'agent_form.html', {'form': form})
       