from django.contrib import admin
from .models import Stock,Order, Procucts

# Register your models here.
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(Procucts)

"""
class EmployeeAdmin(admin.ModelAdmin):
    list_display=['id','eno','ename','esal','eadd']

admin.site.register(Employee,EmployeeAdmin)
"""

class ProcuctsAdmin(admin.ModelAdmin):
    list_display=['product_name','product_brand','product_model','product_description','product_rating','prduct_img_path']