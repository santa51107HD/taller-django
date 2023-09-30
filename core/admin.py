from typing import Any
from django.contrib import admin
from django.forms import ModelForm
from django import forms
# Register your models here.

from .models import *


class UnivallunoForm(ModelForm):
    class Meta:
        fields = [
            "nombre",
            "apellidos",
            "tipoDeUnivalluna",
            "tipoDeDocumento",
            "numeroDeDocumento",
            "codigoDeEstudiante",
            "email",
            "is_active",
            "disponible",
        ]
        model= Univalluno

    def clean(self):
        print(self.cleaned_data)
        print(self.instance.id)

        if self.cleaned_data["tipoDeUnivalluna"] == "E":
            if len(self.cleaned_data["codigoDeEstudiante"]) == 0:
                raise forms.ValidationError("El campo codigo de estudiante es requerido para el registro de estudiantes")
        else:
            self.cleaned_data["codigoDeEstudiante"] = ''

        if self.instance.id != None:
            if(self.instance.numeroDeDocumento != self.cleaned_data["numeroDeDocumento"]):

                raise forms.ValidationError("No se puede modificar el campo numero de documento")
            if(self.instance.tipoDeDocumento != self.cleaned_data["tipoDeDocumento"]):

                raise forms.ValidationError("No se puede modificar el campo tipo de documento")
        
        super().clean()

class UnivallunoAdminView(admin.ModelAdmin):
    form = UnivallunoForm
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class PrestamosForm(ModelForm):
    class Meta:
        fields = [
            "univalluno",
            "articuloDeportivo",
            "fecha_vencimiento_prestamos",
            "pagado"
        ]

    def clean(self):
        print(self.cleaned_data)

        if self.cleaned_data["pagado"] == False:

            if self.cleaned_data["univalluno"].disponible == False:
                raise forms.ValidationError("Este univalluno no puede tener mas de un artiuclo deportivo en prestamo")
            else:
                if self.cleaned_data["articuloDeportivo"].disponible == False:
                    raise forms.ValidationError("Este articulo deportivo no se encuentra disponible para prestamo")
                else:
                    self.cleaned_data["articuloDeportivo"].disponible = False
                    self.cleaned_data["articuloDeportivo"].save()

                    self.cleaned_data["univalluno"].disponible = False
                    self.cleaned_data["univalluno"].save()
        
        elif self.cleaned_data["pagado"] == True:

            if self.cleaned_data["univalluno"].disponible == False:

                self.cleaned_data["univalluno"].disponible = True
                self.cleaned_data["univalluno"].save()

            if self.cleaned_data["articuloDeportivo"].disponible == False:

                self.cleaned_data["articuloDeportivo"].disponible = True
                self.cleaned_data["articuloDeportivo"].save()

        super().clean()

class PrestamosAdminView(admin.ModelAdmin):
    form = PrestamosForm
    def save_model(self, request, obj, form, change):
        print(obj.univalluno)
        print(obj.articuloDeportivo)
        print(obj.fecha_prestamo)
        print(obj.fecha_vencimiento_prestamos)
        print(obj.pagado)
        super().save_model(request, obj, form, change)


admin.site.register(Univalluno, UnivallunoAdminView)
admin.site.register(ArticuloDeportivo)
admin.site.register(Prestamos, PrestamosAdminView)
admin.site.register(Multas)
