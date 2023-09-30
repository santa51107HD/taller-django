from django.contrib import admin

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
        intancia = self.instance

        print(self.cleaned_data)

        if(self.instance.numeroDeDocumento != self.cleaned_data["numeroDeDocumento"]):
            pass
            print("si cambia")
            raise forms.ValidationError("No se puede modificar el campo numero de documento")
        if(self.instance.tipoDeDocumento != self.cleaned_data["tipoDeDocumento"]):
            pass 
            print("si cambia")
            raise forms.ValidationError("No se puede modificar el campo tipo de documento")
        
        super().clean()

class UnivallunoAdminView(admin.ModelAdmin):
    form = UnivallunoForm
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)



admin.site.register(Univalluno, UnivallunoAdminView)
admin.site.register(ArticuloDeportivo)
admin.site.register(Prestamos)
admin.site.register(Multas)
