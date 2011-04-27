# -*- coding: utf-8 -*-
'''
Created on 04.04.2011

@author: Admin
'''
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.shortcuts import render_to_response
from mysite.proc.models import *
from django.contrib import auth

def login(request):
    if request.method=='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
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
            '''try:
                request.session["agent"]=Agent.objects.get(user=user)
            except Agent.DoesNotExist:
                return
                '''

            # Redirect to a success page.
            #return HttpResponseRedirect("/account/loggedin/")
            return render_to_response('main.html', context_instance=RequestContext(request))
        else:
            # Show an error page
            return HttpResponseRedirect("/proc/accounts/invalid/")
    else:
        return render_to_response('accounts/login.html', context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/proc/accounts/login/')
