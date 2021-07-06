from django.contrib import admin

from logistics.models import (
    Delevery,
    Product,
    Profile,
    UnitOrganization,
)

admin.site.register(UnitOrganization)
admin.site.register(Product)
admin.site.register(Delevery)
admin.site.register(Profile)
