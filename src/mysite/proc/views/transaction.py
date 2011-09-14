# -*- coding: utf-8 -*-
'''
Created on 13.04.2011

@author: Admin
'''
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.shortcuts import *
from mysite.proc.models import *
from mysite.proc.views.forms import *
from django.contrib.auth.decorators import permission_required

''' ================================ PAY ========================'''
@permission_required('proc.view_transaction')
def pay_list(request):
    s_list = Transaction.objects.all()
    return render( request,'pay.html', {'s_list': s_list})

@permission_required('proc.change_transaction')
def pay_form(request,id_):
    if request.method=='POST':
        a = Transaction.objects.get(pk=id_)

        if request.session["is_admin"]:
            form=TransactionAdminForm(request.POST, instance=a)
        else:
            form=TransactionForm(request.POST, instance=a)
        
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            a = form.save(commit = False)
            
            a.save()
            return HttpResponseRedirect('/proc/pay/')
        else:
            return render( request,'pay_form.html', {'form': form})
    else:       

        s = Transaction.objects.get(id=id_)
        
        if request.session["is_admin"]:
            form=TransactionAdminForm(instance=s)
        else:
            form=TransactionForm(instance=s)
            
        del_url="%s/delete" % id_
                
        return render( request,'pay_form.html', {'form': form,'del_url': del_url})

@permission_required('proc.delete_transaction')
def pay_delete(request,id_):
        s = Transaction.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/pay')

@permission_required('proc.add_transaction')
def pay_form_add(request,id_=0):
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
            d.add()
            return HttpResponseRedirect('/proc/pay/')
        else:
            return render( request,'pay_form.html', {'form': form})
    else:        
        if request.session["is_admin"]:
            form=TransactionAdminForm()
        else:
            form=TransactionForm()
            
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
    s_list = ArcMove.objects.filter(transaction = None, dt = False)
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
            return HttpResponseRedirect('/proc/main/')
        else:
            return render( request,'fill_ac_form.html', {'form': form})
    else:        
        form=FillAcForm()      
        return render( request,'fill_ac_form.html', {'form': form})          

