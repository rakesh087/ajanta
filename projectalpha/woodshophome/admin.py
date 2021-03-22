from django.contrib import admin
from .models import Stock,Order, Procucts

# Register your models here.
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(Procucts)