from django.contrib import admin

from logistics.models import (
    Delevery,
    Product,
    Profile,
    UnitOrganization,
)


class UnitOrganizationAdmin(admin.ModelAdmin):
    fields = ("name", "slug")
    readonly_fields = ("slug",)


admin.site.register(UnitOrganization, UnitOrganizationAdmin)
admin.site.register(Product)
admin.site.register(Delevery)
admin.site.register(Profile)
