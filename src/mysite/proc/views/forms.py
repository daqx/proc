# -*- coding: utf-8 -*-
from django import forms
from mysite.proc.service_model import *
from mysite.proc import addres_model
from mysite.proc.addres_model import Addres
from mysite.proc.tarif_model import *
from mysite.proc.models import *


class AddressForm(forms.ModelForm):    
    class Meta:
        model=Addres
        exclude=('content_type', 'object_id')

class AgentForm(forms.ModelForm):    
    username = forms.RegexField(label=("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = ("Обязательный. 30 символов или менньше. Только буквы, цифры и @/./+/-/_ ."),
        error_messages = {'invalid': ("Обязательный. 30 символов или менньше. Только буквы, цифры и @/./+/-/_ .")})
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    cashcode_id = forms.CharField(max_length=30, required=False)
    hdd_id= forms.CharField(max_length=30, required=False)
    class Meta:
        model=Agent
        exclude=('user','hardware')

class AgentEditForm(forms.ModelForm):    
    username = forms.RegexField(label=("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = ("Обязательный. 30 символов или менньше. Только буквы, цифры и @/./+/-/_ ."),
        error_messages = {'invalid': ("Обязательный. 30 символов или менньше. Только буквы, цифры и @/./+/-/_ .")})    
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    cashcode_id = forms.CharField(max_length=30, required=False)
    hdd_id= forms.CharField(max_length=30, required=False)
    class Meta:
        model=Agent
        exclude=('user','hardware')

class ServiceTypeForm(forms.ModelForm):   
    parent = forms.ModelChoiceField(queryset=ServiceType.objects.filter(parent=None)
                                    ,widget=forms.Select,required=False)
    class Meta:
        model=ServiceType
        #exclude=pare

class OpServiceForm(forms.ModelForm):   
    #type = forms.ModelChoiceField(queryset=OpService.objects.all() ,widget=forms.Select)
    class Meta:
        model=OpService
        
class OpServiceGroupForm(forms.ModelForm):    
    class Meta:
        model=OpServiceGroup
        
'''=====================TARIFS==========================='''
class TarifArrForm(forms.ModelForm):    
    class Meta:
        model=TarifArr
        
class TarifForm(forms.ModelForm):    
    class Meta:
        model=Tarif
        #exclude=('op_service',)

class TarifGroupForm(forms.ModelForm):    
    class Meta:
        model=TarifGroup

class TarifProfileForm(forms.ModelForm):    
    class Meta:
        model=TarifProfile

'''=====================DEALER==========================='''
class DealerForm(forms.ModelForm):    
    username = forms.RegexField(label=("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = ("Обязательный. 30 символов или менньше. Только буквы, цифры и @/./+/-/_ ."),
        error_messages = {'invalid': ("Это значение может содержать только буквы, цифры и @/./+/-/_ символы.")})
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model=Dealer
        exclude=('user')

class DealerEditForm(forms.ModelForm):    
    username = forms.RegexField(label=("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = ("Обязательный. 30 символов или менньше. Только буквы, цифры и @/./+/-/_ ."),
        error_messages = {'invalid': ("Это значение может содержать только буквы, цифры и @/./+/-/_ символы.")})
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model=Dealer
        exclude=('user')
        


        
class TransactionForm(forms.ModelForm):    
    
    class Meta:
        model=Transaction
        exclude=('agent','state','date_state','summa_commiss','summa_pay','blocked','return_reason','date_proc','seans_number','processed','blocked','try_count','file_name','user_proc')

class TransactionAdminForm(forms.ModelForm):    
    
    class Meta:
        model=Transaction
        exclude=('state','date_state','summa_commiss','summa_pay','blocked','return_reason','date_proc','seans_number','processed','blocked','try_count','file_name','user_proc')


class FillAcForm(forms.ModelForm):    
    class Meta:
        model=ArcMove
        exclude=('transaction','saldo','dt','date')
