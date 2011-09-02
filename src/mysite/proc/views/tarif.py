# -*- coding: utf-8 -*-
'''
Created on 17.03.2011

@author: Admin
'''
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.shortcuts import *
from mysite.proc.tarif_model import *
from mysite.proc.views.forms import *
from django.contrib.auth.decorators import permission_required

''' ================================ TARIF_ARR ========================'''

@permission_required('proc.view_tarif')
def tarif_arr(request,tr):
    s_list = TarifArr.objects.filter(tarif=tr)
    add_url='%s/add' %tr
    tarif = Tarif.objects.get(pk=tr)
    return render( request,'tarif/tarif_arr.html', {'s_list': s_list,'add_url': add_url,'tr':tr,'tarif':tarif})

@permission_required('proc.change_tarif')
def tarif_arr_form(request,tr,id_):
    if request.method=='POST':
        a = TarifArr.objects.get(pk=id_)

        form=TarifArrForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_arr/%s'%tr)
        else:
            return render( request,'tarif/tarif_arr_form.html', {'form': form})
    else:        
        s = TarifArr.objects.get(id=id_)
        form=TarifArrForm(instance=s)
        del_url="%s/delete" % id_
        
        return render( request,'tarif/tarif_arr_form.html', {'form': form,'del_url': del_url,'tr':tr,'id':id_})

@permission_required('proc.delete_tarif')
def tarif_arr_delete(request,tr,id_):
        s = TarifArr.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/tarif_arr/%s'%tr)

@permission_required('proc.add_tarif')
def tarif_arr_form_add(request,tr,id_=0):
    if request.method=='POST':
        form=TarifArrForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_arr/%s'%tr)
        else:
            return render( request,'tarif/tarif_arr_form.html', {'form': form})
    else:
        a = Tarif.objects.get(pk=tr)
        form=TarifArrForm(initial={'tarif':a})
           
        return render( request,'tarif/tarif_arr_form.html', {'form': form})
    
''' ================================ TARIF ========================'''

@permission_required('proc.view_tarif')
def tarif(request, tp):
    s_list = Tarif.objects.filter(tarif_plan= tp)
    form=TarifForm
    add_url='%s/add' %tp
    return render( request,'tarif/tarif.html', {'s_list': s_list, 'add_url': add_url, 'tp' : tp})

@permission_required('proc.change_tarif')
def tarif_form(request, tp, id_):
    if request.method=='POST':
        a = Tarif.objects.get(pk=id_)

        form=TarifForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        valid = True
        if form.is_valid():
        #    if 'code' in form.errors or 'name' in form.errors or 'summa_own' in form.errors:
        #        valid = False  
            
        #if valid:
            form.save()
            return HttpResponseRedirect('/proc/tarif/%s' % tp)
        else:            
            return render( request,'tarif/tarif_form.html', {'form': form})
    else:        
        s = Tarif.objects.get(id=id_)
        form=TarifForm(instance=s)
        del_url="%s/delete" % id_
        arr_url="/proc/tarif_arr/%s" % id_
        
        return render( request,'tarif/tarif_form.html', {'form': form,'del_url': del_url,'arr_url': arr_url})

@permission_required('proc.delete_tarif')
def tarif_delete(request, tp, id_):
        s = Tarif.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/tarif/%s' % tp)
    
@permission_required('proc.add_tarif')
def tarif_form_add(request, tp, id_=0):
    if request.method=='POST':
        form=TarifForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif/%s' % tp)
        else:
            return render( request,'tarif/tarif_form.html', {'form': form})
    else:
        
        form=TarifForm()      
        return render( request,'tarif/tarif_form.html', {'form': form})
    
   
    
''' ================================ TARIF profile ========================'''

@permission_required('proc.view_tarif')
def tarif_plan(request):
    s_list = TarifPlan.objects.all()
    form=TarifPlanForm
    return render( request,'tarif/tarif_plan.html', {'s_list': s_list})

@permission_required('proc.change_tarif')
def tarif_plan_form(request,id_):
    if request.method=='POST':
        a = TarifPlan.objects.get(pk=id_)

        form=TarifPlanForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_plan/')
        else:
            return render( request,'tarif/tarif_plan_form.html', {'form': form})
    else:        
        s = TarifPlan.objects.get(id=id_)
        form=TarifPlanForm(instance=s)
        del_url="%s/delete" % id_
        arr_url="/proc/tarif/%s" % id_
        
        return render( request,'tarif/tarif_plan_form.html', {'form': form,'del_url': del_url, 'arr_url': arr_url})

@permission_required('proc.delete_tarif')
def tarif_plan_delete(request,id_):
        s = TarifPlan.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/tarif_plan')

@permission_required('proc.add_tarif')
def tarif_plan_form_add(request,id_=0):
    if request.method=='POST':
        form=TarifPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_plan/')
        else:
            return render( request,'tarif/tarif_plan_form.html', {'form': form})
    else:
        
        form=TarifPlanForm()      
        return render( request,'tarif/tarif_plan_form.html', {'form': form})


def gen_tarifarr_from_tarif(tr, tr_new):
    ''' копирование массива тарифа с базового тарифа
    '''
    tr_arr_list = TarifArrBase.objects.filter(tarif = tr)
    
    for ta in tr_arr_list:
        ta_new = TarifArr(parent=True, prc = ta.prc, summa = ta.summa, min=ta.min, max=ta.max, tarif=tr_new, beg_time=ta.beg_time,end_time=ta.end_time)
        ta_new.save()


def gen_tarif_from_tarifplan_base(tpb, tp):
    ''' копирование тарифов ТП с базового ТП
        tpb - базовый тарифный план
        tp  - новый тарифный план для которого необходимо сгенерировать тарифы базового ТП  
    '''
    tr_list = TarifBase.objects.filter(tarif_plan = tpb)
    # В цикле создадим все тарифы которые принадлежат базовому тарифу
    for tr in tr_list:        
        tr_new = Tarif(code=tr.code, name=tr.name, op_service = tr.op_service, prc = tr.prc, summa = tr.summa, min=tr.min, max=tr.max, tarif_plan=tp)
        tr_new.save()
        # Сгенерируем массив
        gen_tarifarr_from_tarif(tr, tr_new)
        
        
@permission_required('proc.add_tarif')
def tarif_plan_gen_from_base(request,id_=0):
    ''' генерация тарифного плана на основе базового тарифного плана '''
    
    if request.method=='POST':
        tp_id = request.POST.get("tarif_plan",'')
        
        form=TarifPlanForm(request.POST)
        
        if form.is_valid() and tp_id!='':
            tpb = get_object_or_404(TarifPlanBase, id =tp_id)
            tp=form.save()
            gen_tarif_from_tarifplan_base(tpb, tp)              # Сгенерируем тарифы
            return HttpResponseRedirect('/proc/tarif_plan/')
        else:
            return render( request,'tarif/tarif_plan_form.html', {'form': form})
    else:        
        s_list = TarifPlanBase.objects.all()
        form=TarifPlanForm()      
        return render( request,'tarif/tarif_plan_gen.html', {'s_list': s_list, 'form' : form})


@permission_required('proc.add_tarif')
def tarif_plan_gen(request,id_=0):
    ''' генерация тарифного плана на основе другогово тарифного плана '''
    if request.method=='POST':
        form=TarifPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_plan/')
        else:
            return render( request,'tarif/tarif_plan_form.html', {'form': form})
    else:        
        s_list = TarifPlan.objects.all()      
        return render( request,'tarif/tarif_plan_gen.html', {'s_list': s_list})


''' ================================ TARIF_ARR_BASE ========================'''

@permission_required('proc.view_tarifbase')
def tarif_arr_base(request,tr):
    s_list = TarifArrBase.objects.filter(tarif=tr)
    add_url='%s/add' %tr
    tarif = TarifBase.objects.get(pk=tr)
    return render( request,'tarif/tarif_arr_base.html', {'s_list': s_list,'add_url': add_url,'tr':tr,'tarif':tarif})

@permission_required('proc.change_tarifbase')
def tarif_arr_base_form(request,tr,id_):
    if request.method=='POST':
        a = TarifArrBase.objects.get(pk=id_)

        form=TarifArrBaseForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_arr_base/%s'%tr)
        else:
            return render( request,'tarif/tarif_arr_base_form.html', {'form': form})
    else:        
        s = TarifArrBase.objects.get(id=id_)
        form=TarifArrBaseForm(instance=s)
        del_url="%s/delete" % id_
        
        return render( request,'tarif/tarif_arr_base_form.html', {'form': form,'del_url': del_url,'tr':tr,'id':id_})

@permission_required('proc.delete_tarifbase')
def tarif_arr_base_delete(request,tr,id_):
        s = TarifArrBase.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/tarif_arr_base/%s'%tr)

@permission_required('proc.add_tarifbase')
def tarif_arr_base_form_add(request,tr,id_=0):
    if request.method=='POST':
        form=TarifArrBaseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_arr_base/%s'%tr)
        else:
            return render( request,'tarif/tarif_arr_base_form.html', {'form': form})
    else:
        a = TarifBase.objects.get(pk=tr)
        form=TarifArrBaseForm(initial={'tarif':a})
           
        return render( request,'tarif/tarif_arr_base_form.html', {'form': form})
    
''' ================================ TARIF ========================'''

@permission_required('proc.view_tarifbase')
def tarif_base(request,tp):
    s_list = TarifBase.objects.filter(tarif_plan= tp)
    add_url='%s/add' %tp
    form=TarifBaseForm
    return render( request,'tarif/tarif_base.html', {'s_list': s_list, 'add_url': add_url, 'tp' : tp})

@permission_required('proc.change_tarifbase')
def tarif_base_form(request, tp,id_):
    if request.method=='POST':
        a = TarifBase.objects.get(pk=id_)

        form=TarifBaseForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_base/%s' % tp)
        else:
            return render( request,'tarif/tarif_base_form.html', {'form': form})
    else:        
        s = TarifBase.objects.get(id=id_)
        form=TarifBaseForm(instance=s)
        del_url="%s/delete" % id_
        arr_url="/proc/tarif_arr_base/%s" % id_
        
        return render( request,'tarif/tarif_base_form.html', {'form': form,'del_url': del_url,'arr_url': arr_url})

@permission_required('proc.delete_tarif')
def tarif_base_delete(request, tp, id_):
        s = TarifBase.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/tarif_base/%s' % tp)
    
@permission_required('proc.add_tarifbase')
def tarif_base_form_add(request, tp,id_=0):
    if request.method=='POST':
        form=TarifBaseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_base/%s' % tp)
        else:
            return render( request,'tarif/tarif_base_form.html', {'form': form})
    else:
        
        form=TarifBaseForm()      
        return render( request,'tarif/tarif_base_form.html', {'form': form})
    
   
    
''' ================================ TARIF plan BASE ========================'''

@permission_required('proc.view_tarifbase')
def tarif_plan_base(request):
    s_list = TarifPlanBase.objects.all()
    form=TarifPlanBaseForm
    return render( request,'tarif/tarif_plan_base.html', {'s_list': s_list})

@permission_required('proc.change_tarifbase')
def tarif_plan_base_form(request,id_):
    if request.method=='POST':
        a = TarifPlanBase.objects.get(pk=id_)

        form=TarifPlanBaseForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_plan_base/')
        else:
            return render( request,'tarif/tarif_plan_base_form.html', {'form': form})
    else:        
        s = TarifPlanBase.objects.get(id=id_)
        form=TarifPlanBaseForm(instance=s)
        del_url="%s/delete" % id_
        arr_url="/proc/tarif_base/%s" % id_
        
        return render( request,'tarif/tarif_plan_base_form.html', {'form': form,'del_url': del_url, 'arr_url': arr_url})

@permission_required('proc.delete_tarifbase')
def tarif_plan_base_delete(request,id_):
        s = TarifPlanBase.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/tarif_plan_base')

@permission_required('proc.add_tarifbase')
def tarif_plan_base_form_add(request,id_=0):
    if request.method=='POST':
        form=TarifPlanBaseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/proc/tarif_plan_base/')
        else:
            return render( request,'tarif/tarif_plan_base_form.html', {'form': form})
    else:
        
        form=TarifPlanBaseForm()      
        return render( request,'tarif/tarif_plan_base_form.html', {'form': form})