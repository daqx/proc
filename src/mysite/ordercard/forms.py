'''
Created on 13.02.2011

@author: Admin
'''
from django import forms
from django.forms.widgets import Widget

class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required=False)
    message = forms.CharField(widget=forms.Textarea)

