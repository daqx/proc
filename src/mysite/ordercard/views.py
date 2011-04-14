# Create your views here.
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from mysite.ordercard.models import Card
from django.core.context_processors import request
from django.shortcuts import render_to_response
from mysite.ordercard.forms import *
from django.core.mail import send_mail



def archive(request):
    posts=Card.objects.all()
    t=loader.get_template("archive.html")
    c=Context({'posts':posts})
    return HttpResponse(t.render(c))

def search_form(request):
    return render_to_response('search_form.html')

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        books = ""#Book.objects.filter(title__icontains=q)
        return render_to_response('search_results.html',
            {'books': books, 'query': q})
    else:
        return render_to_response('search_form.html', {'error': True})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render_to_response('contact_form.html', {'form': form},context_instance=RequestContext(request))


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data            
            return HttpResponseRedirect('/contact/thanks/')