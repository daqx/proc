from django.db import models
from django.contrib import admin

#from django.core.management.validation import max_length

# Create your models here.
class OrderCard(models.Model):
    fio=models.CharField(max_length=50)
    tel=models.CharField(max_length=20)
    card=models.ForeignKey("Card")
    count=models.IntegerField()
    email=models.EmailField()
    file=models.FileField(upload_to='Daler',blank=True)
    text=models.TextField()
    
class Card(models.Model):
    code=models.CharField(max_length=4)
    name=models.CharField(max_length=20)
    file=models.FileField(upload_to='Daler',blank=True)
    
    def __unucode__(self):
        return self.name


class OrderCardAdmin(admin.ModelAdmin):
    list_display=('fio','tel','count')
    
class CardAdmin(admin.ModelAdmin):
    list_display=('code','name')
    

admin.site.register(OrderCard,OrderCardAdmin)
admin.site.register(Card,CardAdmin)
#admin.site.register(BlogPost)