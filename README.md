# Taller-django

***
## Integrantes: 
  * Alejandro Peñaranda Agudelo - 1941008
  * Alejandro Escobar Tafurt - 1941378
  * Diego Fernando Chaverra - 1940322
  * Juan Camilo Santa Gomez - 1943214


## Instalación
***
Pasos preliminares:
```
- Clonar el repositorio con el siguiente comando:

$ git clone https://github.com/santa51107HD/taller-django.git

- Instalar los requerimientos con el comando:

$ pip install -r requirements.txt
```
Comandos para la ejecución del Programa:
```
Entrar a la carpeta del proyecto

$ cd ../path/to/the/file   (path al directorio del proyecto)

Realizar las migraciones de la Base de Datos:

$ python manage.py makemigrations

Aplicar las migraciones de la Base de Datos:

$ python manage.py migrate

Arrancar el servidor local:

$ python manage.py runserver

Para editar y agregar registros a la base de datos se debe tener creado un superuser en Django,se puede crear con el
siguiente comando:

$ python manage.py createsuperuser
```
Urls para utilizar el Programa en el navegador:
```
http://127.0.0.1:8000/admin

En esta url se puede visualizar, editar y agregar nuevos registros de los modelos del programa.
```
```
http://127.0.0.1:8000/multa

Get

En esta url podemos generar las multas de todos los univallunos que tienen prestamos pendientes con una fecha de vencimiento
del prestamo menor o igual a el dia actual y que el prestamo no ha sido pagado.
```
```
http://127.0.0.1:8000/multa/pagar/

Post

En esta url podemos pagar la multa mediante un json con su id, ademas se verifica si todas las multas del univalluno han sido
pagadas para liberar al univalluno, el articulo deportivos y pagar el prestamo.

ejemplo json

{

"id_multa" : 1

}
```
```
http://127.0.0.1:8000/generate_reports_sports/

POST

Esta url genera un informe de la cantidad de artículos deportivos prestados por deporte

Ejemplo de JSON

{
fecha_inicial: 2023-09-29,
fecha_fin: 2023-10-01
}
```
```
http://127.0.0.1:8000/generate_reports_items/

POST

Esta url genera un informe de la cantidad de artículos deportivos prestados por día

Ejemplo de JSON

{
fecha_inicial: 2023-09-29,
fecha_fin: 2023-10-01
}
```
```
http://127.0.0.1:8000/generate_reports_fines/

POST

Esta url genera un informe del valor total de las multas generadas por día

Ejemplo de JSON

{
fecha_inicial: 2023-09-29,
fecha_fin: 2023-10-01
}
```
```
http://127.0.0.1:8000/reports

En esta url podemos generar reportes de cantidad artículos deportivos prestados por cada deporte, cantidad de artículos
deportivos prestados por cada día y sobre el valor de las multas generadas por día.
```
