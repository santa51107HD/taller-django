from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.serializer import MultaSerializer
from rest_framework import status
from .models import Multas, Prestamos
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models import Sum
from datetime import datetime  
# import datetime
# Create your views here.

# todos los prestamos que su fecha de pago es menor o igual a hoy y no esten pagados


@api_view(['GET'])
def generarMulta(request):

    prestamos_vencidos = Prestamos.objects.filter(
        fecha_vencimiento_prestamos__lte=datetime.now()).filter(pagado=False)

    # si tenemos algun prestamo vencido se le genera una multa al univalluno
    if prestamos_vencidos:

        for prestamo in prestamos_vencidos:

            univalluno = prestamo.univalluno
            articulo = prestamo.articuloDeportivo
            valor = round(articulo.valor*0.15)
            print(valor)
            pagado = False
            
            fecha_pago = None
            id = len(Multas.objects.all()) + 1
            print(id)
            univalluno.disponible = False
            univalluno.save()
            articulo.disponible = False
            articulo.save()
            multa = Multas(id, univalluno.id, articulo.id, prestamo.id,
                           valor,pagado, fecha_pago)
            multa.save()

        return Response({"error": False, "mensaje": "Se han generado las multas"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": False, "mensaje": "No se generaron multas"}, status=status.HTTP_200_OK)

# metodo para pagar una multa


@api_view(['POST'])
def pagarMulta(request):

    multa_pagada = Multas.objects.get(pk=request.data["id_multa"])
    if multa_pagada.pagado == False:
        multa_pagada.pagado = True
        multa_pagada.fecha_pago = datetime.now()
        multa_pagada.save()
        univalluno = multa_pagada.univalluno
        multas = Multas.objects.filter(univalluno=univalluno)
        # revisar si el univalluno tiene alguna multa sin pagar
        for multa in multas:
            if multa.pagado == False:
                return Response({"error": False, "mensaje": "Se ha pagado la multa"}, status=status.HTTP_200_OK)
        # liberar a los articulos deportivos, al univalluno y paga el prestamo que pago sus multas
        multa_pagada.prestamo.pagado = True
        multa_pagada.prestamo.save()
        multa_pagada.articuloDeportivo.disponible = True
        multa_pagada.articuloDeportivo.save()
        univalluno.disponible = True
        univalluno.save()

        return Response({"error": False, "mensaje": "Se ha pagado la multa y se liberaron los articulos y el estudiante"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": False, "mensaje": "La multa ya esta pagada"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def generate_report_sports(request):
    fecha_inicio = request.data['fecha_inicio']
    fecha_fin = request.data['fecha_fin']

    if fecha_inicio and fecha_fin:
        prestamos_por_deporte = Prestamos.objects.filter(fecha_prestamo__date__range=(fecha_inicio, fecha_fin)).values(
            'articuloDeportivo__deporte').annotate(cantidad=Count('articuloDeportivo'))
        deportes = [registro['articuloDeportivo__deporte']
                    for registro in prestamos_por_deporte]
        cantidades = [registro['cantidad']
                      for registro in prestamos_por_deporte]
        resultado = {
            'actividad': deportes,
            'cantidades': cantidades,
        }
        return Response(resultado)

    return Response("Por favor, proporciona las fechas de inicio y fin.")


@api_view(['POST'])
def generate_report_items(request):
    fecha_inicio = request.data['fecha_inicio']
    fecha_fin = request.data['fecha_fin']
    print("ITEMS")
    if fecha_inicio and fecha_fin:
        prestamos_por_dia = Prestamos.objects.filter(fecha_prestamo__date__range=(fecha_inicio, fecha_fin)).annotate(
            dia_prestamo=TruncDate('fecha_prestamo')).values('dia_prestamo').annotate(cantidad=Count('id'))

        fechas = [registro['dia_prestamo'] for registro in prestamos_por_dia]
        cantidades = [registro['cantidad'] for registro in prestamos_por_dia]
        resultado = {
            'actividad': fechas,
            'cantidades': cantidades,
        }
        return Response(resultado)

    return Response("Por favor, proporciona las fechas de inicio y fin.")


@api_view(['POST'])
def generate_report_fines(request):
    fecha_inicio = request.data['fecha_inicio']
    fecha_fin = request.data['fecha_fin']
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

    if fecha_inicio and fecha_fin:
        multas_por_dia = Multas.objects.annotate(dia_multa=TruncDate(
            'fecha_creacion')).values('dia_multa').annotate(total_multas=Sum('valor'))
        dias_solicitados = []
        for multa in multas_por_dia:
            dia_multa = multa['dia_multa']
            if fecha_inicio <= dia_multa <= fecha_fin:
                dias_solicitados.append(multa)
        valores_multas = [registro['total_multas']
                          for registro in dias_solicitados]
        fechas = [registro['dia_multa'] for registro in dias_solicitados]
        resultado = {
            'actividad': fechas,
            'cantidades': valores_multas,
        }
        return Response(resultado)

    return Response("Por favor, proporciona las fechas de inicio y fin.")


def reports(request):
    return render(request, 'reports.html')
