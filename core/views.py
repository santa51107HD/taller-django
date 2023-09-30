from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.serializer import MultaSerializer
from rest_framework import status
from .models import Multas, Prestamos
import datetime
# Create your views here.

#todos los prestamos que son menores o iguales a hoy y no esten pagados
@api_view(['GET'])
def generarMulta(request):

    
    prestamos_vencidos = Prestamos.objects.filter(fecha_vencimiento_prestamos__lte=datetime.date.today()).filter(pagado = False)


    if prestamos_vencidos:

        for prestamo in prestamos_vencidos:

            univalluno = prestamo.univalluno
            articulo = prestamo.articuloDeportivo
            valor = round(articulo.valor*0,15)
            pagado = False
            fecha_pago = None

            multa = Multas(univalluno,articulo,prestamo,valor,pagado,fecha_pago)
            multa.save()


        return Response({"error":False, "mensaje": "Se han generado las multas"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": False, "mensaje": "No se generaron multas"}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def generarMulta(request, pk):

    multa = Multas.objects.get(pk=pk)
    if multa.pagado == False:
        multa.pagado= True
        multa.save()
# estaba haciendo lo de pagar

    
    
        
