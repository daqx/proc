# -*- coding: utf-8 -*-
'''
Created on 09.04.2011

@author: Admin
'''

from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

def to_main(request):
    # Redirect to a success page.
    return HttpResponseRedirect("main/")



def main(request):
    return render_to_response('main.html', context_instance=RequestContext(request))
