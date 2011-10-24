# -*- coding: utf-8 -*-
'''
Created on 20.10.2011

@author: D_Unusov
'''
from django.core.context_processors import request
from django.http import HttpResponse, HttpResponseRedirect
from mysite.proc.sys_model import *
from mysite.proc.models import *

import xlwt


def pay_export( request):
    
    wb = xlwt.Workbook(encoding="UTF-8")
    ws = wb.add_sheet('pay')
    
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=payments.xls'
    
    try:                    
        begdate = datetime.strptime(request.POST.get('date_begin'),'%d.%m.%Y')
        enddate = datetime.strptime(request.POST.get('date_end'),'%d.%m.%Y')
    except ValueError:
        wb.save(response)
        return response
    
    borders = xlwt.Borders() # Create Borders
    borders.left    = xlwt.Borders.THIN
    borders.right   = xlwt.Borders.THIN
    borders.top     = xlwt.Borders.THIN
    borders.bottom  = xlwt.Borders.THIN
    
    style = xlwt.XFStyle() # Create Style
    style.borders = borders # Add Borders to Style
    
    ws.write(0, 3, u'Отчет по оплате услуг с %s по %s' % (request.POST.get('date_begin'),request.POST.get('date_end')), style)
    
    ws.write(3, 0, u'№ чека' , style)
    ws.write(3, 1, u'Время'  , style)
    ws.write(3, 2, u'Агент'  , style)
    ws.write(3, 3, u'Диллер' , style)
    ws.write(3, 4, u'Оператор' , style)
    ws.write(3, 5, u'Номер'  , style)
    ws.write(3, 6, u'Сумма'  , style)
    ws.write(3, 7, u'К оплате', style)
    ws.write(3, 8, u'Статус' , style)
    ws.write(3, 9, u'Маршрут', style)
    
    pix = 263
    ws.col(0).width = 20*pix
    ws.col(1).width = 20*pix
    ws.col(2).width = 20*pix
    ws.col(3).width = 20*pix
    ws.col(4).width = 20*pix
    ws.col(5).width = 20*pix
    ws.col(6).width = 10*pix
    ws.col(7).width = 10*pix
    ws.col(8).width = 20*pix
    ws.col(9).width = 15*pix
    
    qt = Transaction.objects.filter(date__gte=begdate,date__lte=enddate).order_by("date").values('id', 'date','agent__id','agent__user__username', 'agent__dealer__user__username','summa','summa_pay', 'state__name', 'ticket', 'route','number_key','opservices__name')
    
    i = 4
    
    for t in qt:
        ws.write(   i,  0, t["ticket"])
        ws.write(   i,  1, datetime.strftime(   t["date"],  "%Y.%m.%d %H:%M:%S"))
        ws.write(   i,  2, t["agent__user__username"])
        ws.write(   i,  3, t["agent__dealer__user__username"])
        ws.write(   i,  4, t["opservices__name"])
        ws.write(   i,  5, t["number_key"])
        ws.write(   i,  6, t["summa"])
        ws.write(   i,  7, t["summa_pay"])
        ws.write(   i,  8, t["state__name"])
        ws.write(   i,  9, t["route"])
        
        i = i + 1
        

    wb.save(response)
    return response