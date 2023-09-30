from django.contrib import admin

# Register your models here.

from .models import *


class MyAdminView(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print("creado")
        super().save_model(request, obj, form, change)

admin.site.register(Univalluno,MyAdminView)
admin.site.register(ArticuloDeportivo)
admin.site.register(Prestamos)
admin.site.register(Multas)
