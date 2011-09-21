# -*- coding: utf-8 -*-
'''
Created on 13.04.2011

@author: Admin
'''
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.shortcuts import *
from django.forms.util import ErrorList
from mysite.proc.models import *
from mysite.proc.views.forms import *
from django.contrib.auth.decorators import permission_required

''' ================================ PAY ========================'''
@permission_required('proc.view_transaction')
def pay_list(request, id_ = 0, content = ""):
    s_list = Transaction.objects.all()
    return render( request,'pay.html', {'s_list': s_list,'content':content, 'id_':id_})

@permission_required('proc.change_transaction')
def pay_form(request, id_ = 0, content = "", aid_=0):
    if request.method=='POST':
        a = Transaction.objects.get(pk=aid_)

        if request.session["is_admin"]:
            form=TransactionAdminForm(request.POST, instance=a)
        else:
            form=TransactionForm(request.POST, instance=a)
        
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            a = form.save(commit = False)
            
            a.save()
            if id_ != 0:
                return HttpResponseRedirect('/proc/pay/%s/%s' % (id_, content))
            else:            
                return HttpResponseRedirect('/proc/pay/')
        else:
            return render( request,'pay_form.html', {'form': form})
    else:       

        s = Transaction.objects.get(id=aid_)
        
        if content == "agent":
            form=TransactionAdminForm()
            form.fields["agent"].queryset = Agent.objects.filter(id = id_)
        elif content == "dealer":
            form=TransactionAdminForm()
            form.fields["agent"].queryset = Agent.objects.filter(dealer = id_)
        elif request.session["is_admin"]:
            form=TransactionAdminForm(instance=s)        
        else:
            form=TransactionForm(instance=s)
            
        del_url="%s/delete" % aid_
                
        return render( request,'pay_form.html', {'form': form,'del_url': del_url})

@permission_required('proc.delete_transaction')
def pay_delete(request, id_ = 0, content = "", aid_=0):
        s = Transaction.objects.get(id=aid_)
        s.delete()
        if id_ != 0:
            return HttpResponseRedirect('/proc/pay/%s/%s' % (id_, content))
        else:            
            return HttpResponseRedirect('/proc/pay/')

@permission_required('proc.add_transaction')
def pay_form_add(request, id_ = 0, content = ""):
    if request.method=='POST':
        
        if request.session["is_admin"]:
            form=TransactionAdminForm(request.POST)
        else:
            form=TransactionForm(request.POST)
            
            
        if form.is_valid():
            d=form.save(commit=False)            
            user=request.user
            
            if not request.session["is_admin"]:                         # Если пользователь не АДМИН то
                agent=user.agent                                        # агент берется с юзера
                d.agent=agent
                                                                        # Иначе агент берется с формы
            ret = d.add()
            if ret == -1:
                form._errors["summa"]= ErrorList([u"Остаток диллера не позволяет оплатить эту сумму"])
                return render( request,'pay_form.html', {'form': form})
            
            if id_ != 0:
                return HttpResponseRedirect('/proc/pay/%s/%s' % (id_, content))
            else:            
                return HttpResponseRedirect('/proc/pay/')
        else:
            return render( request,'pay_form.html', {'form': form})
    else:        
        
        if content == "agent":
            form=TransactionAdminForm()
            form.fields["agent"].queryset = Agent.objects.filter(id = id_)
        elif content == "dealer":
            form=TransactionAdminForm()
            form.fields["agent"].queryset = Agent.objects.filter(dealer = id_)
        elif request.session["is_admin"]:
            form=TransactionAdminForm()
        elif request.session["user_type"]=="dealer":
            form=TransactionAdminForm()
        else:
            form=TransactionForm()
        
        #query="select o.* from proc_opservice o, proc_agent_opservices ao where o.id=ao.opservice_id and ao.agent_id = %s" % id_    
        #op = OpService.objects.raw(query)[0:]
            
        return render( request,'pay_form.html', {'form': form})          

''' ================================ FILL_AC ========================
пополнение счета диллера
'''
'''   
def fill_ac_list(request):
    s_list = Transaction.objects.all()
    return render( request,'pay.html', {'s_list': s_list})
'''    

@permission_required('proc.view_arcmove')
def fill_ac_list(request):
    s_list = ArcMove.objects.filter(transaction = None, dt = False).order_by('-date')
    return render( request,'fill_ac.html', {'s_list': s_list})

@permission_required('proc.add_arcmove')
def fill_ac_form_add(request,id_=0):
    if request.method=='POST':
        form=FillAcForm(request.POST)
        if form.is_valid():
            fa=form.save(commit=False)            
                        
            d=fa.dealer
                                                                        # Иначе агент берется с формы
            d.fill_ac(fa)
            return HttpResponseRedirect('/proc/fill_ac/')
        else:
            return render( request,'fill_ac_form.html', {'form': form})
    else:        
        form=FillAcForm()      
        return render( request,'fill_ac_form.html', {'form': form})          

