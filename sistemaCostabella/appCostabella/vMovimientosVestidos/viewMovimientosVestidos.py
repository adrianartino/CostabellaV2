
#Para ruta
import os
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

import json

#Para mandar telegram
import telepot

#Plugin impresora termica
from appCostabella import keysBotCostabella
# Importacion de modelos
from appCostabella.models import (Empleados, Permisos, ProductosRenta,
                                  ProductosVenta, Sucursales)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)

def agregarMovimiento(request):

    if "idSesion" in request.session:

        #Variables de sesión
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']
        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]
        
        #notificacionRentas
        notificacionRenta = notificacionRentas(request)

        #notificacionCitas
        notificacionCita = notificacionCitas(request)

        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)

        if request.method == "POST":
            idSucursalOrigen = request.POST["idSucursalOrigen"]
            idSucursalDestino = request.POST["idSucursalDestino"]

            if idSucursalOrigen == idSucursalDestino:
                sucursalesPrimera = Sucursales.objects.all()
                sucursalesSegunda = Sucursales.objects.all()
                sucursalesIguales = True
                mensajeSucursalesIguales = "Se han elegido las mismas sucursales!"
                return render(request,"23 Movimientos/seleccionarSucursalesParaMovimiento.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                                "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                                "sucursalesPrimera":sucursalesPrimera, "sucursalesSegunda":sucursalesSegunda, "sucursalesIguales":sucursalesIguales,
                                                                                "mensajeSucursalesIguales":mensajeSucursalesIguales})
            else:
                #No son iguales
                consultaVestidosRenta = ProductosRenta.objects.filter(sucursal_id__id_sucursal = idSucursalOrigen, estado_renta = "Sin rentar")
                consultaVestidosRenta2 = ProductosRenta.objects.filter(sucursal_id__id_sucursal = idSucursalOrigen, estado_renta = "Sin rentar")
                consultaSucursalOrigen = Sucursales.objects.filter(id_sucursal = idSucursalOrigen)
                for dato in consultaSucursalOrigen:
                    nombreSucursalOrigen = dato.nombre

                consultaSucursalDestino = Sucursales.objects.filter(id_sucursal = idSucursalDestino)
                for dato in consultaSucursalDestino:
                    nombreSucursalDestino = dato.nombre

                dataProductosRenta = [i.jsonRenta() for i in ProductosRenta.objects.filter(sucursal_id__id_sucursal = idSucursalOrigen) ]
                rutaMedias= os.path.join(BASE_DIR,'media')

                return render(request,"23 Movimientos/agregarMovimientoVestidos.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "idSucursalOrigen":idSucursalOrigen, "nombreSucursalOrigen":nombreSucursalOrigen, 
                                                                            "idSucursalDestino":idSucursalDestino, "nombreSucursalDestino":nombreSucursalDestino, "consultaVestidosRenta":consultaVestidosRenta, "consultaVestidosRenta2":consultaVestidosRenta2,
                                                                            "data":json.dumps(dataProductosRenta), "rutaMedias":rutaMedias})

        else:
            sucursalesPrimera = Sucursales.objects.all()
            sucursalesSegunda = Sucursales.objects.all()

            if "movimientoRealizado" in request.session:
                movimientoRealizado = request.session["movimientoRealizado"]
                del request.session["movimientoRealizado"]

                return render(request,"23 Movimientos/seleccionarSucursalesParaMovimiento.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "sucursalesPrimera":sucursalesPrimera, "sucursalesSegunda":sucursalesSegunda, "movimientoRealizado":movimientoRealizado})



            return render(request,"23 Movimientos/seleccionarSucursalesParaMovimiento.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "sucursalesPrimera":sucursalesPrimera, "sucursalesSegunda":sucursalesSegunda})



        
    else:
        return render(request,"1 Login/login.html")


def guardarMovimiento(request):

    if "idSesion" in request.session:

        idEmpleado = request.session['idSesion']
        
        idSucursalOrigen = request.POST["idSucursalOrigen"]
        idSucursalDestino = request.POST["idSucursalDestino"]
        consultaVestidosRenta = ProductosRenta.objects.filter(sucursal_id__id_sucursal = idSucursalOrigen, estado_renta = "Sin rentar")

        datosVestidosMovidos = []
        
        for vestido in consultaVestidosRenta:
            idVestido = vestido.id_producto
            nameCheckbox = "checkboxVestido"+str(idVestido)

            if request.POST.get(nameCheckbox,False): #Significa que si el checkbox esta chequeado
                moverVestido = True
                
                #Actualizar solo el dato de la sucursal
                consultaVestido = ProductosRenta.objects.filter(id_producto = idVestido).update(sucursal = Sucursales.objects.get(id_sucursal = idSucursalDestino))

                #Agregar sus datos al arreglo para posteriormente sacarlos y agregarlos a telegram.
                segundaConsultaVestido = ProductosRenta.objects.filter(id_producto = idVestido)
                for datoVestido in segundaConsultaVestido:
                    codigoVestido = datoVestido.codigo_producto
                    nombreVestido = datoVestido.nombre_producto

                datosVestidosMovidos.append([idVestido, codigoVestido, nombreVestido])

                #Consultar si hay un vestido con el mismo nombre en productos para venta
                consultaProductoVenta = ProductosVenta.objects.filter(nombre_producto = nombreVestido)
                if consultaProductoVenta:
                    actualizacionProducto = ProductosVenta.objects.filter(nombre_producto = nombreVestido).update(sucursal = Sucursales.objects.get(id_sucursal = idSucursalDestino) )
                
            elif request.POST.get(nameCheckbox,True): #Significa que si el checkbox no esta chequeado
                moverVestido = False
        request.session["movimientoRealizado"] = "El movimiento de vestidos se ha realizado satisfactoriamente!!"   



        #Mensaje telegram
        consultaSucursalOrigen = Sucursales.objects.filter(id_sucursal = idSucursalOrigen)
        for datoSucursalOrigen in consultaSucursalOrigen:
            nombreSucursalOrigen = datoSucursalOrigen.nombre

        consultaSucursalDestino = Sucursales.objects.filter(id_sucursal = idSucursalDestino)
        for datoSucursalDestino in consultaSucursalDestino:
            nombreSucursalDestino = datoSucursalDestino.nombre

        
        #Consulta nombre empleado
        consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
        for datoEmpleado in consultaEmpleado:
            nombreEmpleado = datoEmpleado.nombres


        mensajeVestidos = ""
        for vestidito in datosVestidosMovidos:
            idVestidito = str(vestidito[0])
            codigoVestidito = str(vestidito[1])
            nombreVestidito = str(vestidito[2])
            
            mensajeVestidos = mensajeVestidos + "\n \n"+"\U0001F457	Vestido #"+idVestidito+" - "+codigoVestidito+" "+nombreVestidito


        try:
            tokenTelegram = keysBotCostabella.tokenBotCostabellaRentas
            botCostabella = telepot.Bot(tokenTelegram)

            idGrupoTelegram = keysBotCostabella.idGrupo
            
            mensaje = "\U0001F519 MOVIMIENTO DE VESTIDOS \U0001F51C \n La empleada "+nombreEmpleado+" ha generado el movimiento de vestidos de la sucursal "+nombreSucursalOrigen+" a la sucursal "+nombreSucursalDestino + mensajeVestidos
            botCostabella.sendMessage(idGrupoTelegram,mensaje)
        except:
            print("An exception occurred")
        


        





        return redirect("/agregarMovimiento/")

        



        
    else:
        return render(request,"1 Login/login.html")

