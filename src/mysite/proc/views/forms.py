# -*- coding: utf-8 -*-
from django import forms
from mysite.proc.service_model import *
from mysite.proc import addres_model
from mysite.proc.addres_model import Addres
from mysite.proc.tarif_model import *
from mysite.proc.models import *


'''***********************************************************************************'''
# I used this instead of lambda expression after scope problems
def _get_cleaner(form, field):
    def clean_field():
         return getattr(form.instance, field, None)
    return clean_field

class ROFormMixin(forms.BaseForm):
    def __init__(self, *args, **kwargs):
        super(ROFormMixin, self).__init__(*args, **kwargs)
        if hasattr(self, "read_only"):
            if self.instance and self.instance.pk:
                for field in self.read_only:
                    self.fields[field].widget.attrs['readonly'] = True
                    setattr(self, "clean_" + field, _get_cleaner(self, field))


'''***********************************************************************************'''
class AddressForm(forms.ModelForm):
    
    required_css_class = 'required'    
    class Meta:
        model=Addres
        exclude=('content_type', 'object_id')

class AgentForm(forms.ModelForm):    
    username = forms.RegexField(label=("Имя пользователя"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = ("Обязательный. 30 символов или менньше. Только буквы, цифры и @/./+/-/_ ."),
        error_messages = {'invalid': ("Обязательный. 30 символов или менньше. Только буквы, цифры и @/./+/-/_ .")})
    password = forms.CharField(label=("Пароль"), widget=forms.PasswordInput)
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия',max_length=30)
    cashcode_id = forms.CharField(label='№ купюроприемника', max_length=30, required=False)
    hdd_id= forms.CharField(label='№ жесткого диска', max_length=30, required=False)
    
    required_css_class = 'required'
    class Meta:
        model=Agent
        exclude=('user','hardware')
        fields =('name', 'type','state','username','password','first_name','last_name','dealer','opservices','opservice_group','check_for_ip','imei',
                 'tel','key_hash','cashcode_capacity','cashcode_id','hdd_id')

class AgentEditForm(forms.ModelForm):    
    username = forms.RegexField(label=("Имя пользователя"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = ("Обязательный. 30 символов или менньше. Только буквы, цифры и @/./+/-/_ ."),
        error_messages = {'invalid': ("Обязательный. 30 символов или менньше. Только буквы, цифры и @/./+/-/_ .")})    
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия',max_length=30)
    #opservices = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),required=True)

    cashcode_id = forms.CharField(label='№ купюроприемника', max_length=30, required=False)
    hdd_id= forms.CharField(label='№ жесткого диска', max_length=30, required=False)
    
    required_css_class = 'required'
    class Meta:
        model=Agent
        exclude=('user','hardware')
        fields =('name', 'type','state','username','first_name','last_name','dealer','opservices','opservice_group'
                 ,'check_for_ip','imei','tel','key_hash','cashcode_capacity','cashcode_id','hdd_id')

'''=====================DEALER==========================='''
class DealerForm(forms.ModelForm):    
    username = forms.RegexField(label=("Имя пользователя"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = ("Обязательный. 30 символов или менньше. Только буквы, цифры и @/./+/-/_ ."),
        error_messages = {'invalid': ("Это значение может содержать только буквы, цифры и @/./+/-/_ символы.")})
    password = forms.CharField(label=("Пароль"), widget=forms.PasswordInput)
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия',max_length=30)
    
    required_css_class = 'required'
    
    class Meta:
        model=Dealer
        exclude=('user','summa')
        fields =('kopf','state','username','password','first_name','last_name','dealer','inn','check_for_ip','limit','overdraft','account','tel')
        
class DealerEditForm(forms.ModelForm):    
    username = forms.RegexField(label=("Имя пользователя"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = ("Обязательный. 30 символов или менньше. Только буквы, цифры и @/./+/-/_ ."),
        error_messages = {'invalid': ("Это значение может содержать только буквы, цифры и @/./+/-/_ символы.")})    
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия',max_length=30)
    
    required_css_class = 'required'
    
    class Meta:
        model=Dealer
        exclude=('user', 'summa')
        fields =('kopf','state','username','first_name','last_name','dealer','inn','check_for_ip','limit','overdraft','account','tel')
        
class IpAddressForm(forms.ModelForm):
    
    required_css_class = 'required'
    class Meta:
        model=IpAddress
        exclude=('content_type', 'object_id')


class ServiceTypeForm(forms.ModelForm):   
    parent = forms.ModelChoiceField(queryset=ServiceType.objects.filter(parent=None)
                                    ,widget=forms.CheckboxSelectMultiple,required=False)
    
    required_css_class = 'required'
    class Meta:
        model=ServiceType
        #exclude=pare

class OpServiceForm(forms.ModelForm):   
    #type = forms.ModelChoiceField(queryset=OpService.objects.all() ,widget=forms.Select)
    required_css_class = 'required'
    class Meta:
        model=OpService
        
class OpServiceGroupForm(forms.ModelForm):
    
    required_css_class = 'required'    
    class Meta:
        model=OpServiceGroup
        
'''=====================TARIFS==========================='''
class TarifArrForm(forms.ModelForm):
    
    required_css_class = 'required'    
    class Meta:
        model=TarifArr
        exclude =('parent','tarif')
        
class TarifForm(forms.ModelForm):   
    
    #def clean(self):
    #   cleaned_data = self.cleaned_data
    #   domain = cleaned_data.get("domain")
    #   extension = cleaned_data.get("extension")
        #return cleaned_data
    required_css_class = 'required'
    class Meta:
        model=Tarif
        exclude=('op_service','summa','prc','min','max','tarif_plan')

class TarifPlanForm(forms.ModelForm):
    
    required_css_class = 'required'    
    class Meta:
        model=TarifPlan

class TarifArrBaseForm(forms.ModelForm):
    
    required_css_class = 'required'    
    class Meta:
        model=TarifArrBase
        
class TarifBaseForm(forms.ModelForm):
    
    required_css_class = 'required'    
    class Meta:
        model=TarifBase
        #exclude=('op_service',)

class TarifPlanBaseForm(forms.ModelForm):
    
    required_css_class = 'required'    
    class Meta:
        model=TarifPlanBase




        
class TransactionForm(forms.ModelForm):    
    
    required_css_class = 'required'
    class Meta:
        model=Transaction
        exclude=('agent','state','date_state','summa_commiss','summa_pay','blocked','return_reason','date_proc','seans_number','processed','blocked','try_count','file_name','user_proc')

class TransactionAdminForm(forms.ModelForm):    
    
    required_css_class = 'required'
    class Meta:
        model=Transaction
        exclude=('state','date_state','summa_commiss','summa_pay','blocked','return_reason','date_proc','seans_number','processed','blocked','try_count','file_name','user_proc')


class FillAcForm(forms.ModelForm):
    
    required_css_class = 'required'    
    class Meta:
        model=ArcMove
        exclude=('transaction','saldo','dt','date')
