from django.contrib import admin
from .models import Trader,Trade,MetaTraderAccount
# Register your models here.
Data =[Trader,Trade,MetaTraderAccount]
admin.site.register(Data)

