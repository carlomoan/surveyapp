from django.contrib import admin
from .models import *

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'firstname',
                    'middlename', 'lastname', 'mobile', 'user_roles']

    class Meta:
        model = User


admin.site.register(User, UserAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = ['postcode', 'name']

    class Meta:
        model = Region


admin.site.register(Region, RegionAdmin)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['region', 'postcode', 'name']

    class Meta:
        model = District


admin.site.register(District, DistrictAdmin)


class WardAdmin(admin.ModelAdmin):
    list_display = ['district', 'postcode', 'name']

    class Meta:
        model = Ward


admin.site.register(Ward, WardAdmin)
