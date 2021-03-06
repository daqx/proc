# Create your views here.
from django.contrib import auth
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import *
from mysite.proc.views.grids import *

def requires_login(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/proc/login_form/')
        return view(request, *args, **kwargs)
    return new_view

#Login form
def login_form(request):
    return render_to_response('login.html')


def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/proc/main/")
    else:
        # Show an error page
        return HttpResponseRedirect("/proc/invalid/")


def grid_handler(request):
    # handles pagination, sorting and searching
    grid = ExampleGrid()
    return HttpResponse(grid.get_json(request), mimetype="application/json")

def grid_config(request):
    # build a config suitable to pass to jqgrid constructor   
    grid = ExampleGrid()
    return HttpResponse(grid.get_config(), mimetype="application/json")
