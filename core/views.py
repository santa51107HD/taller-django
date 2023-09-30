from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.serializer import MultaSerializer
from rest_framework import status
from .models import Multas, Prestamos
import datetime
# Create your views here.

#todos los prestamos que su fecha de pago es menor o igual a hoy y no esten pagados
@api_view(['GET'])
def generarMulta(request):

    
    prestamos_vencidos = Prestamos.objects.filter(fecha_vencimiento_prestamos__lte=datetime.date.today()).filter(pagado = False)

    # si tenemos algun prestamo vencido se le genera una multa al univalluno
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
    
#metodo para pagar una multa
@api_view(['POST'])
def pagarMulta(request):

    multa_pagada = Multas.objects.get(pk=request.data["id_multa"])
    if multa_pagada.pagado == False:
        multa_pagada.pagado= True
        multa_pagada.fecha_pago = datetime.date.today()
        multa_pagada.save()
        univalluno = multa_pagada.univalluno
        multas = Multas.objects.filter(univalluno=univalluno)
        #revisar si el univalluno tiene alguna multa sin pagar
        for multa in multas:
            if multa.pagado == False:
                return Response({"error":False, "mensaje": "Se ha pagado la multa"}, status=status.HTTP_200_OK)
        #liberar a los articulos deportivos 
        for multa in multas:
            multa.articuloDeportivo.disponible= True
            multa.save()
        
        #liberar al univalluno que pago sus multas
        univalluno.disponible=True
        univalluno.save()    
        
        return Response({"error":False, "mensaje": "Se ha pagado la multa y se liberaron los articulos y el estudiante"}, status=status.HTTP_200_OK)
    else:
        return Response({"error":False, "mensaje": "La multa ya esta pagada"}, status=status.HTTP_200_OK)