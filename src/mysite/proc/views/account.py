# -*- coding: utf-8 -*-
'''
Created on 04.04.2011

@author: Admin
'''
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.shortcuts import *
from mysite.proc.models import *
from django.contrib import auth

def get_menu_list(user):
    i=0
    menu_list=[]
    for m in Menu.objects.all().order_by("order"):
        ps="proc.%s" % m.perms.codename
        if user.has_perm(ps):
            menu_list.append(m)
    return menu_list            

def login(request):
    if request.method=='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            
            request.session["is_admin"] = False
            
            try:
                d=user.agent
                request.session["user_type"]="agent"
            except Agent.DoesNotExist:
                pass    
                
            try:
                d=user.dealer
                request.session["user_type"]="dealer"
            except Dealer.DoesNotExist:
                pass
            
            #s=request.session["user_type"]
            
            if "user_type" not in request.session:
                request.session["user_type"]="admin"
                request.session["is_admin"] = True
            
            '''try:
                request.session["agent"]=Agent.objects.get(user=user)
            except Agent.DoesNotExist:
                return
                '''
            #Определим доступные меню
            request.session["menu_list"]=[]
            menu_list=request.session["menu_list"]
            menu_list=get_menu_list(user)                              #Menu.objects.all()
            #menu_list=Menu.objects.all()
            request.session["menu_list"]=menu_list
            
            # Redirect to a success page.
            #return HttpResponseRedirect("/account/loggedin/")
            return render(request,'main.html')
        else:
            # Show an error page
            return HttpResponseRedirect("/proc/accounts/invalid/")
    else:
        return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/proc/accounts/login/')
