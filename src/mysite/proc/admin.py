from django.contrib import admin
from mysite.proc.addres_model import * 
from mysite.proc.sys_model import *
from mysite.proc.models import *
from mysite.proc.tarif_model import *

class ActionAdmin(admin.ModelAdmin):
    list_display=('code','name')

class ActualStateAdmin(admin.ModelAdmin):
    list_display=('date','agent')

class AddresAdmin(admin.ModelAdmin):
    list_display=('address',)

class ArcMoveAdmin(admin.ModelAdmin):
    list_display=('date','dealer','dt','summa','saldo')

class AgentAdmin(admin.ModelAdmin):
    list_display=('user','state')
    #raw_id_fields = ('addres',)
    
class CommandAdmin(admin.ModelAdmin):
    list_display=('act','agent','date','status','date_send','description')    


class CountryAdmin(admin.ModelAdmin):
    list_display=('str_code','name')
    search_fields = ('str_code', 'name')
    
class DealerAdmin(admin.ModelAdmin):
    list_display=( 'user', 'account')
    #raw_id_fields = ('addres',)
    
    
class EncashmentAdmin(admin.ModelAdmin):
    list_display=('date','agent')

class GatewayAdmin(admin.ModelAdmin):
    list_display=('code','name','opservice', 'status', 'route')

class RouteAdmin(admin.ModelAdmin):
    list_display=('code','name','status')

class GatelogAdmin(admin.ModelAdmin):
    list_display=('transaction','transaction2','date', 'sending')


class HistoryStateAdmin(admin.ModelAdmin):
    list_display=('date','state',)
    
class JourSostAgentAdmin(admin.ModelAdmin):
    list_display=('date','agent')

class KopfAdmin(admin.ModelAdmin):
    list_display=('code','short_name','name')

class MenuAdmin(admin.ModelAdmin):
    list_display=('code','name','order','get_perms_name')
    
    def get_perms_name(self,obj):
        return "proc.%s"%(obj.perms.codename)
    get_perms_name.short_description="perm"
    
class NominalValAdmin(admin.ModelAdmin):
    list_display=('code','number')

class NominalAdmin(admin.ModelAdmin):
    list_display=('transaction','value','count')

class OpServiceAdmin(admin.ModelAdmin):
    list_display=('id','code','name','state','order','type','need_check','mask')
    raw_id_fields = ('type',)

class OpServiceGroupAdmin(admin.ModelAdmin):
    list_display=('code','name')



class RegionAdmin(admin.ModelAdmin):
    list_display=('country','name')
    
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display=('code','name','parent','order')
    search_fields = ('code', 'name')

class StatusAdmin(admin.ModelAdmin):
    list_display=('code','name')

class StateAdmin(admin.ModelAdmin):
    list_display=('code','name', 'product')

class SostAgentAdmin(admin.ModelAdmin):
    list_display=('name','code','type',)
    
class TarifArrAdmin(admin.ModelAdmin):
    list_display=('tarif','summa','min','max',"prc")
    
class TarifAdmin(admin.ModelAdmin):
    list_display=('name','code','op_service','summa','min','max',"prc")
    raw_id_fields = ('op_service',)

#class TarifGroupAdmin(admin.ModelAdmin):
#    list_display=('name','code')
    #raw_id_fields = ('tarif',)
    
class TarifPlanAdmin(admin.ModelAdmin):
    list_display=('name','code','date_begin','date_end')

class TarifArrBaseAdmin(admin.ModelAdmin):
    list_display=('tarif','summa','min','max',"prc")
    
class TarifBaseAdmin(admin.ModelAdmin):
    list_display=('name','code','op_service','summa','min','max',"prc")
    raw_id_fields = ('op_service',)

#class TarifGroupAdmin(admin.ModelAdmin):
#    list_display=('name','code')
    #raw_id_fields = ('tarif',)
    
class TarifPlanBaseAdmin(admin.ModelAdmin):
    list_display=('name','code','date_begin','date_end')

    
class TownAdmin(admin.ModelAdmin):
    list_display=('get_country','region','name')
    
    def get_country(self,obj):
        return "%s"%(obj.region.country)
    get_country.short_description="Country"
    
class TransactionAdmin(admin.ModelAdmin):
    list_display=('date','agent','summa', 'state')


    

    
admin.site.register(Action, ActionAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(ArcMove, ArcMoveAdmin)
admin.site.register(Addres, AddresAdmin)
admin.site.register(ActualState, ActualStateAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(Dealer, DealerAdmin)
admin.site.register(Encashment, EncashmentAdmin)
admin.site.register(Gateway, GatewayAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Gatelog, GatelogAdmin)
admin.site.register(JourSostAgent, JourSostAgentAdmin)
admin.site.register(Kopf, KopfAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(NominalVal, NominalValAdmin)
admin.site.register(Nominal, NominalAdmin)
admin.site.register(OpService, OpServiceAdmin)
admin.site.register(OpServiceGroup, OpServiceGroupAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(HistoryState, HistoryStateAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(SostAgent, SostAgentAdmin)
admin.site.register(Tarif, TarifAdmin)
admin.site.register(TarifArr, TarifArrAdmin)
#admin.site.register(TarifGroup, TarifGroupAdmin)
admin.site.register(TarifPlan, TarifPlanAdmin)
admin.site.register(TarifBase, TarifAdmin)
admin.site.register(TarifArrBase, TarifArrAdmin)
admin.site.register(TarifPlanBase, TarifPlanAdmin)
admin.site.register(Town, TownAdmin)
admin.site.register(Transaction, TransactionAdmin)
