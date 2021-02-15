from django.contrib import admin
from .models import *

# Register your models here.


class SurveyProjectAdmin(admin.ModelAdmin):
    list_display = ['proid', 'author', 'site_No', 'Region', 'District', 'Ward']

    class Meta:
        model = SurveyProject


admin.site.register(SurveyProject, SurveyProjectAdmin)



class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'unit_of_size', 'material']

    class Meta:
        model = Equipment


admin.site.register(Equipment, EquipmentAdmin)


class WellInfoAdmin(admin.ModelAdmin):
    list_display = ['site', 'contact1', 'contact2']

    class Meta:
        model = WellInfo


admin.site.register(WellInfo, WellInfoAdmin)


class StoreInfoAdmin(admin.ModelAdmin):
    list_display = ['item', 'amount', 'buy_time', 'uploader']

    class Meta:
        model = Store


admin.site.register(Store, StoreInfoAdmin)