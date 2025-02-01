
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

import json
#Libreria Random
import random

# Importacion de modelos
from appCostabella.models import (Empleados, Permisos,
                                  ProductosGasto, Sucursales,
                                  Tratamientos, 
                                  TratamientosProductosGasto)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)


def agregarTratamiento(request):
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

        #Permisos
        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)
        
        #Sucursales
        sucursales = Sucursales.objects.all()
        
        #Consulta del código siguiente de tratamiento.
        consultaTratamientos = Tratamientos.objects.all()
        
        #Codigo Tratamiento
        if consultaTratamientos:
            ultimoCodigoTratamiento = ""
            for tratamiento in consultaTratamientos:
                ultimoCodigoTratamiento = tratamiento.codigo_tratamiento
            arrayUltimoCodigoTratamiento = ultimoCodigoTratamiento.split("-")
            indice = arrayUltimoCodigoTratamiento[1]
            nuevoIndice = int(indice)+1
            codigoTratamiento = arrayUltimoCodigoTratamiento[0]+"-"+str(nuevoIndice)
        else:
            codigoTratamiento = "TRAT-1000"
                
                
        #Botón Agregar Tratamiento
        if request.method == "POST":
            
            codigoTratamiento = request.POST["codigoTratamiento"]
            tipoTratamiento = request.POST["tipoTratamiento"]
            nombreTratamiento = request.POST["nombreTratamiento"]
            descripcionTratamiento = request.POST["descripcionTratamiento"]
            costoTratamiento = request.POST["costoTratamiento"]
            tiempoMinimo = request.POST["tiempoMinimo"]
            tiempoMaximo = request.POST["tiempoMaximo"]
            complementos = request.POST["complementos"]
            sesionesRecomendadas = request.POST["sesionesRecomendadas"]
            periodoRecomendado = request.POST["periodoRecomendado"]
            listaSucursales = request.POST.getlist('sucursales')
            
            if descripcionTratamiento == "":
                descripcionTratamiento = "Sin descripción"
            
            if complementos == "":
                complementos = "Sin complementos"
            
            if "Todas" in listaSucursales:
                #Esta en todas las sucursales
                sucursales = Sucursales.objects.all()
                contadorSucursales = 0
                for sucursal in sucursales:
                    idSucursal = sucursal.id_sucursal
                    contadorSucursales = contadorSucursales + 1

                    if contadorSucursales == 1:
                        codigoTratamientoNuevo = codigoTratamiento
                    else:
                        codigoEnPartes = codigoTratamiento.split("-")
                        parteIndice = codigoEnPartes[1]
                        parteIndiceNueva = int(parteIndice) + (contadorSucursales-1)
                        codigoTratamientoNuevo = codigoEnPartes[0] +"-"+str(parteIndiceNueva) 


                    registroTratamiento = Tratamientos(codigo_tratamiento = codigoTratamientoNuevo,
                                                        tipo_tratamiento = tipoTratamiento,
                                                        nombre_tratamiento = nombreTratamiento,
                                                        descripcion_tratamiento = descripcionTratamiento,
                                                        costo_venta_tratamiento = costoTratamiento,
                                                        tiempo_minimo = tiempoMinimo,
                                                        tiempo_maximo = tiempoMaximo,
                                                        complementos_tratamiento = complementos,
                                                        sesiones_rec_tratamiento = sesionesRecomendadas,
                                                        periodo_rec_tratamiento = periodoRecomendado,
                                                        sucursal = Sucursales.objects.get(id_sucursal = idSucursal))
                    registroTratamiento.save()
            else:
                contadorSucursales = 0
                for sucursal in listaSucursales:
                    idSucursal = int(sucursal)
                    contadorSucursales = contadorSucursales+1
                    
                    if contadorSucursales == 1:
                        codigoTratamientoNuevo = codigoTratamiento
                    else:
                        codigoEnPartes = codigoTratamiento.split("-")
                        parteIndice = codigoEnPartes[1]
                        parteIndiceNueva = int(parteIndice) + (contadorSucursales-1)
                        codigoTratamientoNuevo = codigoEnPartes[0] +"-"+str(parteIndiceNueva)
                    
                    registroTratamiento = Tratamientos(codigo_tratamiento = codigoTratamiento,
                                                        tipo_tratamiento = tipoTratamiento,
                                                        nombre_tratamiento = nombreTratamiento,
                                                        descripcion_tratamiento = descripcionTratamiento,
                                                        costo_venta_tratamiento = costoTratamiento,
                                                        tiempo_minimo = tiempoMinimo,
                                                        tiempo_maximo = tiempoMaximo,
                                                        complementos_tratamiento = complementos,
                                                        sesiones_rec_tratamiento = sesionesRecomendadas,
                                                        periodo_rec_tratamiento = periodoRecomendado,
                                                        sucursal = Sucursales.objects.get(id_sucursal = idSucursal))
                    registroTratamiento.save()
            if registroTratamiento:
                request.session["tratamientoAgregado"] = "El tratamiento fue agregado satisfactoriamente"
                return redirect("/agregarTratamiento/")
            else:
                request.session["tratamientoNoAgregado"] = "Error en la base de datos, intente más tarde."
                return redirect("/agregarTratamiento/")
        
        if "tratamientoAgregado" in request.session:
            tratamientoAgregado = request.session["tratamientoAgregado"]
            del request.session["tratamientoAgregado"]
            return render(request,"20 Tratamientos/agregarTratamiento.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                         "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos, "sucursales":sucursales,
                                                                         "codigoTratamiento":codigoTratamiento, "tratamientoAgregado":tratamientoAgregado, "notificacionCita":notificacionCita})
        
        if "tratamientoNoAgregado" in request.session:
            tratamientoNoAgregado = request.session["tratamientoNoAgregado"]
            del request.session["tratamientoNoAgregado"]
            return render(request,"20 Tratamientos/agregarTratamiento.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                         "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos, "sucursales":sucursales,
                                                                         "codigoTratamiento":codigoTratamiento, "tratamientoNoAgregado":tratamientoNoAgregado, "notificacionCita":notificacionCita})
        
        
        return render(request,"20 Tratamientos/agregarTratamiento.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                         "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos, "sucursales":sucursales,
                                                                         "codigoTratamiento":codigoTratamiento, "notificacionCita":notificacionCita})
    
    
    else:
        return render(request,"1 Login/login.html")  
    
def verTratamientos(request):

    if "idSesion" in request.session:

       # Variables de sesión
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']
        idPerfil = idEmpleado
        idConfig = idEmpleado
        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]
        #notificacionRentas
        notificacionRenta = notificacionRentas(request)
        #notificacionCitas
        notificacionCita = notificacionCitas(request)
        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)
        
        if request.method == "POST":
            sucursalTratamientos = request.POST["sucursalTratamientos"]
            tratamientosCorporales = []
            tratamientosCorporalesModal = []

            tratamientosFaciales = []
            tratamientosFacialesModal = []

            tratamientosCorporalesModalProductos = []
            tratamientosFacialesModalProductos = []
            #Mostrar todas las sucursales
            if sucursalTratamientos == "todasLasSucursales":
                consultaTratamientos = Tratamientos.objects.all()
                nombreSucursalView = "Todas las sucursales"
                
            else:
                consultaTratamientos = Tratamientos.objects.filter(sucursal_id__id_sucursal = sucursalTratamientos)
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalTratamientos)
                for datoSucursal in consultaSucursal:
                    nombreSucursalView = datoSucursal.nombre

            paqueteDeProductosTratamiento = []
            for tratamiento in consultaTratamientos:
                idTratamiento = tratamiento.id_tratamiento
                codigoTratamiento = tratamiento.codigo_tratamiento
                tipoTratamiento = tratamiento.tipo_tratamiento
                nombreTratamiento = tratamiento.nombre_tratamiento
                descripcionTratamiento = tratamiento.descripcion_tratamiento
                costoVentaTratamiento = tratamiento.costo_venta_tratamiento
                tiempoMinimoTratamiento = tratamiento.tiempo_minimo
                tiempoMaximoTratamiento = tratamiento.tiempo_maximo
                complementosTratamiento = tratamiento.complementos_tratamiento
                sesionesRecomendadasTratamiento = tratamiento.sesiones_rec_tratamiento
                periodoRecomendadoTratamiento = tratamiento.periodo_rec_tratamiento
                sucursal = tratamiento.sucursal_id

                datosSucursal = Sucursales.objects.filter(id_sucursal = sucursal)

                infoSucursalTratamiento = []
                arrayColores = ["primary","success","danger","warning","info"]
                for sucursal in datosSucursal:
                    idSucursal = sucursal.id_sucursal
                    nombreSucursal = sucursal.nombre
                    if sucursalTratamientos == "todasLasSucursales":
                        colorRandom = random.choice(arrayColores)
                    else:
                        colorRandom = "warning"
                infoSucursalTratamiento.append([idSucursal,nombreSucursal,colorRandom])

                #Consulta para saber si tiene un paquete de productos ya asignado
                tratamientoYaTienePaquete = False
                paquetesTratamientos = TratamientosProductosGasto.objects.all()
                productosTratamiento = []
                for productoUtilizado in paquetesTratamientos:
                    tratamientoUtilizado = productoUtilizado.tratamiento_id
                    
                    if tratamientoUtilizado == idTratamiento:
                        tratamientoYaTienePaquete = True
                        
                        #Ya tiene productos asignados... Sacar todos los productos y mandarlos a un arreglo de ese servicio.
                        idProductoGastoUtilizado = productoUtilizado.producto_gasto_id
                        cantidadUtilizada = productoUtilizado.cantidad
                        datosProducto = ProductosGasto.objects.filter(id_producto = idProductoGastoUtilizado)
                        for dato in datosProducto:
                            codigo = dato.codigo_producto
                            idProducto = dato.id_producto
                            sku = dato.sku_producto
                            nombre = dato.nombre_producto
                            cantidad_existencias = dato.cantidad
                            
                        productosTratamiento.append([idProducto,codigo,sku,nombre,cantidadUtilizada,cantidad_existencias])
                    
                if tratamientoYaTienePaquete:
                    paqueteDeProductosTratamiento.append(productosTratamiento)
                

                #asdfasdfasdf
                
                if tipoTratamiento == "Corporal":
                    tratamientosCorporales.append([idTratamiento,codigoTratamiento,
                    nombreTratamiento,descripcionTratamiento,costoVentaTratamiento,
                    tiempoMinimoTratamiento,tiempoMaximoTratamiento,complementosTratamiento,
                    sesionesRecomendadasTratamiento,periodoRecomendadoTratamiento,infoSucursalTratamiento, tratamientoYaTienePaquete, paqueteDeProductosTratamiento])


                    tratamientosCorporalesModal.append([idTratamiento,codigoTratamiento,
                    nombreTratamiento,descripcionTratamiento,costoVentaTratamiento,
                    tiempoMinimoTratamiento,tiempoMaximoTratamiento,complementosTratamiento,
                    sesionesRecomendadasTratamiento,periodoRecomendadoTratamiento,infoSucursalTratamiento, tratamientoYaTienePaquete, paqueteDeProductosTratamiento])

                    tratamientosCorporalesModalProductos.append([idTratamiento,codigoTratamiento,
                    nombreTratamiento,descripcionTratamiento,costoVentaTratamiento,
                    tiempoMinimoTratamiento,tiempoMaximoTratamiento,complementosTratamiento,
                    sesionesRecomendadasTratamiento,periodoRecomendadoTratamiento,infoSucursalTratamiento, tratamientoYaTienePaquete, paqueteDeProductosTratamiento])
                else:
                    tratamientosFaciales.append([idTratamiento,codigoTratamiento,
                    nombreTratamiento,descripcionTratamiento,costoVentaTratamiento,
                    tiempoMinimoTratamiento,tiempoMaximoTratamiento,complementosTratamiento,
                    sesionesRecomendadasTratamiento,periodoRecomendadoTratamiento,infoSucursalTratamiento, tratamientoYaTienePaquete, paqueteDeProductosTratamiento])


                    tratamientosFacialesModal.append([idTratamiento,codigoTratamiento,
                    nombreTratamiento,descripcionTratamiento,costoVentaTratamiento,
                    tiempoMinimoTratamiento,tiempoMaximoTratamiento,complementosTratamiento,
                    sesionesRecomendadasTratamiento,periodoRecomendadoTratamiento,infoSucursalTratamiento, tratamientoYaTienePaquete, paqueteDeProductosTratamiento])

                    tratamientosFacialesModalProductos.append([idTratamiento,codigoTratamiento,
                    nombreTratamiento,descripcionTratamiento,costoVentaTratamiento,
                    tiempoMinimoTratamiento,tiempoMaximoTratamiento,complementosTratamiento,
                    sesionesRecomendadasTratamiento,periodoRecomendadoTratamiento,infoSucursalTratamiento, tratamientoYaTienePaquete, paqueteDeProductosTratamiento])

            return render(request, "20 Tratamientos/verTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "tratamientosCorporales":tratamientosCorporales,
                "tratamientosCorporalesModal":tratamientosCorporalesModal,"tratamientosFaciales":tratamientosFaciales,"tratamientosFacialesModal":tratamientosFacialesModal,"nombreSucursalView":nombreSucursalView,
                "tratamientosCorporalesModalProductos":tratamientosCorporalesModalProductos,"tratamientosFacialesModalProductos":tratamientosFacialesModalProductos, "notificacionCita":notificacionCita})
    
        else:           
            if tipoUsuario == "esAdmin":
                sucursales = Sucursales.objects.all()
                
                if "tratamientoActualizado" in request.session:
                    tratamientoActualizado = request.session["tratamientoActualizado"]
                    del request.session["tratamientoActualizado"]
                    return render(request, "20 Tratamientos/seleccionarSucursalTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales, "tratamientoActualizado":tratamientoActualizado,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})

                if "tratamientoNoActualizado" in request.session:
                    tratamientoNoActualizado = request.session["tratamientoNoActualizado"]
                    del request.session["tratamientoNoActualizado"]
                    return render(request, "20 Tratamientos/seleccionarSucursalTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tratamientoNoActualizado":tratamientoNoActualizado,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})

                if "registroPaqueteProductos" in request.session:
                    registroPaqueteProductos = request.session["registroPaqueteProductos"]
                    del request.session["registroPaqueteProductos"]
                    return render(request, "20 Tratamientos/seleccionarSucursalTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"registroPaqueteProductos":registroPaqueteProductos,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})

                if "noRegistroPaqueteProductos" in request.session:
                    noRegistroPaqueteProductos = request.session["noRegistroPaqueteProductos"]
                    del request.session["noRegistroPaqueteProductos"]
                    return render(request, "20 Tratamientos/seleccionarSucursalTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"noRegistroPaqueteProductos":noRegistroPaqueteProductos,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})

                if "paqueteProductoTratamientoActualizado" in request.session:
                    paqueteProductoTratamientoActualizado = request.session["paqueteProductoTratamientoActualizado"]
                    del request.session["paqueteProductoTratamientoActualizado"]
                    return render(request, "20 Tratamientos/seleccionarSucursalTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"paqueteProductoTratamientoActualizado":paqueteProductoTratamientoActualizado,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})


                return render(request, "20 Tratamientos/seleccionarSucursalTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})
            else:
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    sucursalEmpleado = datoEmpleado.id_sucursal_id
                sucursales = Sucursales.objects.filter(id_sucursal = sucursalEmpleado)
                
                if "tratamientoActualizado" in request.session:
                    tratamientoActualizado = request.session["tratamientoActualizado"]
                    del request.session["tratamientoActualizado"]
                    return render(request, "20 Tratamientos/seleccionarSucursalTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales, "tratamientoActualizado":tratamientoActualizado,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})

                if "tratamientoNoActualizado" in request.session:
                    tratamientoNoActualizado = request.session["tratamientoNoActualizado"]
                    del request.session["tratamientoNoActualizado"]
                    return render(request, "20 Tratamientos/seleccionarSucursalTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales, "tratamientoNoActualizado":tratamientoNoActualizado,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})

                if "registroPaqueteProductos" in request.session:
                    registroPaqueteProductos = request.session["registroPaqueteProductos"]
                    del request.session["registroPaqueteProductos"]
                    return render(request, "20 Tratamientos/seleccionarSucursalTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales, "registroPaqueteProductos":registroPaqueteProductos,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})

                if "noRegistroPaqueteProductos" in request.session:
                    noRegistroPaqueteProductos = request.session["noRegistroPaqueteProductos"]
                    del request.session["noRegistroPaqueteProductos"]
                    return render(request, "20 Tratamientos/seleccionarSucursalTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales, "noRegistroPaqueteProductos":noRegistroPaqueteProductos,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})

                if "paqueteProductoTratamientoActualizado" in request.session:
                    paqueteProductoTratamientoActualizado = request.session["paqueteProductoTratamientoActualizado"]
                    del request.session["paqueteProductoTratamientoActualizado"]
                    return render(request, "20 Tratamientos/seleccionarSucursalTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales, "paqueteProductoTratamientoActualizado":paqueteProductoTratamientoActualizado,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})

                return render(request, "20 Tratamientos/seleccionarSucursalTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})

        
    else:
        return render(request,"1 Login/login.html")

def actualizarTratamientosCorporales(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idTratamientoCorporalEditar = request.POST['idTratamientoCorporalEditar']
            precioVentaEditar = request.POST['precioActualizado']
            minimoEditar = request.POST['minimoActualizado']
            maximoEditar = request.POST['maximoActualizado']
           

            consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamientoCorporalEditar)
            for datoTratamiento in consultaTratamiento:
                nombreTratamiento = datoTratamiento.nombre_tratamiento

            #Actualización.
            edicionTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamientoCorporalEditar).update(costo_venta_tratamiento = precioVentaEditar,
            tiempo_minimo = minimoEditar, tiempo_maximo = maximoEditar)

            if edicionTratamiento:
                request.session["tratamientoActualizado"] = "El tratamiento "+nombreTratamiento+" ha sido actualizado satisfactoriamente!"

                return redirect ("/verTratamientos/")
            else:
                request.session["tratamientoNoActualizado"] = "El tratamiento "+nombreTratamiento+" no ha podido actualizarse, contacte a soporte técnico!"

                return redirect ("/verTratamientos/")

def crearPaqueteTratamientos(request):

    
    if "idSesion" in request.session:

       # Variables de sesión
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']
        idPerfil = idEmpleado
        idConfig = idEmpleado
       

        

        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]
        
           #notificacionRentas
        notificacionRenta = notificacionRentas(request)

        #notificacionCitas
        notificacionCita = notificacionCitas(request)
        
         #permisosEmpleado
        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)

        
        if request.method == "POST":
            
            idTratamiento= request.POST['idTratamientoPaquete'] 
            intTratamiento = int(idTratamiento)
            intTratamiento = Tratamientos.objects.filter(id_tratamiento = intTratamiento)
            infoTratamiento = []
         
            for dato in intTratamiento:
                codigo = dato.codigo_tratamiento
                nombre = dato.nombre_tratamiento
                descripcion = dato.descripcion_tratamiento
                if dato.complementos_tratamiento == None:
                    complementos = "Ninguno"
                else:
                    complementos = dato.complementos_tratamiento
                tiempo_min = dato.tiempo_minimo
                tiempo_max = dato.tiempo_maximo
                precio = dato.costo_venta_tratamiento
                sesionesRecomendadas = int(dato.sesiones_rec_tratamiento)
                periodoRecomendado = dato.periodo_rec_tratamiento
                tipoTratamiento = dato.tipo_tratamiento
                
                idSucursal = dato.sucursal_id
                
                datosSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
                for suc in datosSucursal:
                    nombreSucursal = suc.nombre
            
                infoTratamiento.append([codigo,nombre,descripcion,complementos,tiempo_min,tiempo_max,precio,sesionesRecomendadas,periodoRecomendado,nombreSucursal, tipoTratamiento])
            data = [i.json() for i in ProductosGasto.objects.filter(sucursal_id__id_sucursal = idSucursal)]
            
            
            #----------------
            productos_totales = ProductosGasto.objects.filter(sucursal_id__id_sucursal = idSucursal)
            productos_ids = []
                
            for prod in productos_totales:
                productos_ids.append(prod.id_producto)
            
            productosTratamientos = TratamientosProductosGasto.objects.filter(tratamiento_id = idTratamiento)
            productosTratamiento = []
            for producto in productosTratamientos:
                ids_producto_gasto = producto.producto_gasto_id
            
                for dato in productos_ids:
                    if dato  == ids_producto_gasto:
                        productos_ids.remove(dato)
                
                  
                  
            datos_productos_no_paquete = []
                
            for id in productos_ids:
                datos = ProductosGasto.objects.filter(id_producto = id)
                for dato in datos:
                    id_producto = dato.id_producto
                    codigo_producto = dato.codigo_producto
                    sku = dato.sku_producto
                    nombreProd = dato.nombre_producto
                    existencias = dato.cantidad
                    descripcionP = dato.descripcion
                    imagen = dato.imagen_producto
                    fecha_alta = dato.fecha_alta
                    
                datos_productos_no_paquete.append([id_producto,codigo_producto,sku,nombreProd,existencias,descripcionP,imagen,fecha_alta])   
            
            
            
            
        
            productosVenta = ProductosGasto.objects.filter(sucursal_id__id_sucursal = idSucursal)
            productosVentaJavaScript = ProductosGasto.objects.filter(sucursal_id__id_sucursal = idSucursal)
            
        
            return render(request, "20 Tratamientos/crearPaqueteTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,
                                                                                       "infoTratamiento":infoTratamiento,"idTratamiento":idTratamiento,"productosVenta":productosVenta,"productosVentaJson":json.dumps(data),"productosVentaJavaScript":productosVentaJavaScript,
                                                                                       "datos_productos_no_paquete":datos_productos_no_paquete,"notificacionRenta":notificacionRenta})
            
            
         

       

            
            
        return render(request, "20 Tratamientos/crearPaqueteTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"notificacionRenta":notificacionRenta
                                                                                   
                                                                                 
                                                                                   
        })
    
    else:
        return render(request,"1 Login/login.html")

def guardarPaqueteTratamiento(request):

    
    if "idSesion" in request.session:
     

      
        
        if request.method == "POST":
            
            idTratamiento = request.POST['idTratamiento']
            productosSolicitados = request.POST['cantidadesProductosVenta']
            listaProductosSolicitados = productosSolicitados.split(",")
  
            listaCantidadesSolicitadas = []
           
            for idProducto in listaProductosSolicitados:
               
                nameCantidadProducto = "cantidadUsar" + str(idProducto)
                cantidadSolicitadaMandada = request.POST[nameCantidadProducto]
                listaCantidadesSolicitadas.append(cantidadSolicitadaMandada)
            
            lista = zip(listaProductosSolicitados,listaCantidadesSolicitadas)
            
            for producto, cantidad in lista:
                idProductoBD = producto
                cantidadProductoBD = cantidad
                
                registroProducto = TratamientosProductosGasto(tratamiento = Tratamientos.objects.get(id_tratamiento = idTratamiento),producto_gasto=ProductosGasto.objects.get(id_producto =idProductoBD),cantidad=cantidadProductoBD)
                
                registroProducto.save()
                
            if registroProducto:
                
                consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)
                for datoTratamiento in consultaTratamiento:
                    nombreTratamiento = datoTratamiento.nombre_tratamiento
                request.session['registroPaqueteProductos'] = "El paquete de productos del tratamiento "+nombreTratamiento+" sido gregado satisfactoriamente!"
                return redirect('/verTratamientos/')
                
                
            else:
                request.session['noRegistroPaqueteProductos'] = "Error en la base de datos, intentelo más tarde.."
                return redirect('/verTratamientos/')

            
            
            
            
            
            
            
    
    
    else:
        return render(request,"1 Login/login.html")

def verProductosPaqueteTratamientoEditar(request):

    if "idSesion" in request.session:
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

         #permisosEmpleado
        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)
        
        if request.method == "POST":
            
            idTratamientoEditar = request.POST['idTratamientoProductoEditar']
            consultaDatosTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamientoEditar)
            consultaDeProductos = TratamientosProductosGasto.objects.filter(tratamiento_id__id_tratamiento = idTratamientoEditar)
            
            productosElegidos = []
            
            for producto in consultaDeProductos:
                idProducto = producto.producto_gasto_id
                cantidadUtilizadaDeProducto = producto.cantidad
                
                consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                for dato in consultaProducto:
                    codigoProducto = dato.codigo_producto
                    nombreProducto = dato.nombre_producto
                    imagenProducto = dato.imagen_producto
                    skuProducto = dato.sku_producto
                    
                productosElegidos.append([idProducto,cantidadUtilizadaDeProducto,
                                          codigoProducto,
                                          nombreProducto,
                                          imagenProducto,
                                          skuProducto])
                
                
            #Sucursal de tratamiento
            for datoTratamiento in consultaDatosTratamiento:
                sucursal = datoTratamiento.sucursal_id
                
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
             
            #Lista de productos a elegir para agregar más al servicio.
            todosLosProductosGasto = ProductosGasto.objects.filter(sucursal_id__id_sucursal = sucursal)
            arrayProductosGastoNoEnTratamiento = []
            
            
            consultaProductosUtilizados = TratamientosProductosGasto.objects.filter(tratamiento_id__id_tratamiento = idTratamientoEditar)
            idsProductosYaUtilizados = []
            
            for productoTrat in consultaProductosUtilizados:
                idProducto = productoTrat.producto_gasto_id
                idsProductosYaUtilizados.append(idProducto)
                
            for producto in todosLosProductosGasto:
                idProducto = producto.id_producto
                productoYaEstaEnTratamiento = False
                for productoEnTratamiento in idsProductosYaUtilizados:
                    idProductoEnTratamiento = productoEnTratamiento
                    
                    if idProducto == idProductoEnTratamiento:
                        productoYaEstaEnTratamiento = True
                
                if productoYaEstaEnTratamiento == False:
                    consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                    for dato in consultaProducto:
                        codigoProducto = dato.codigo_producto
                        skuProducto = dato.sku_producto
                        nombreProducto = dato.nombre_producto
                        existenciasProducto = dato.cantidad
                        descripcionProducto = dato.descripcion
                        imagenProducto = dato.imagen_producto
                        fechaAgregadoProducto = dato.fecha_alta
                    
                    arrayProductosGastoNoEnTratamiento.append([idProducto,codigoProducto, skuProducto, nombreProducto,
                                                     existenciasProducto, descripcionProducto, imagenProducto, fechaAgregadoProducto])
                    
                    
            
            
            #Lista de productos en formato JSON.
            data = [i.json() for i in ProductosGasto.objects.filter(sucursal_id__id_sucursal = sucursal)]
            
        
        
            return render(request, "20 Tratamientos/actualizarPaqueteTratamiento.html", {"consultaPermisos":consultaPermisos,"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"notificacionRenta":notificacionRenta, "consultaDatosTratamiento":consultaDatosTratamiento, "productosElegidos":productosElegidos, "nombreSucursal":nombreSucursal, "arrayProductosGastoNoEnTratamiento":arrayProductosGastoNoEnTratamiento, "productosVentaJson":json.dumps(data),
                                                                                   "todosLosProductosGasto":todosLosProductosGasto, "notificacionCita":notificacionCita})
            

            
        return render(request, "20 Tratamientos/actualizarPaqueteTratamiento.html", {"consultaPermisos":consultaPermisos,"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"notificacionRenta":notificacionRenta, "consultaDatosTratamiento":consultaDatosTratamiento, "productosElegidos":productosElegidos, "nombreSucursal":nombreSucursal, "notificacionCita":notificacionCita,})
    
    else:
        return render(request,"1 Login/login.html")



def actualizarPaqueteTratamiento(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idTratamientoEditar = request.POST['idTratamientoEditar']
            
            paqueteActualizado = False
            paqueteBorrado = False
            #Nombre de tratamiento
            consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamientoEditar)
            for datoTratamiento in consultaTratamiento:
                nombreTratamiento = datoTratamiento.nombre_tratamiento
            
            nameInputEliminar = "eliminarProducto"
            nameInputCantidad = "cantidadProducto"
            
            consultaProductosTratamiento = TratamientosProductosGasto.objects.filter(tratamiento_id__id_tratamiento = idTratamientoEditar)
            
            for producto in consultaProductosTratamiento:
                idProductoUtilizado = producto.producto_gasto_id
                
                nameInputPorProductoEliminar = nameInputEliminar+str(idProductoUtilizado)
                nameInputCantidadProductoEditar = nameInputCantidad+str(idProductoUtilizado)
                
                
            
                if request.POST.get(nameInputPorProductoEliminar, False): #Checkeado Eliminar producto
                    borrado = TratamientosProductosGasto.objects.get(producto_gasto_id = idProductoUtilizado, tratamiento_id__id_tratamiento = idTratamientoEditar)
                    borrado.delete()
                    paqueteBorrado = True
                    
                elif request.POST.get(nameInputPorProductoEliminar, True): #No checkeado, actualizar producto
                    cantidadProductoActualizar = request.POST[nameInputCantidadProductoEditar]
                    actualizacionProductoPaquete = TratamientosProductosGasto.objects.filter(producto_gasto_id = idProductoUtilizado).update(cantidad = cantidadProductoActualizar)
                    paqueteActualizado = True
                
            #Agregar más productos.
            
            
            masProductos = request.POST['masProductos']
            if masProductos == "noMasProductos":
                
                if paqueteActualizado or paqueteBorrado: 
                    request.session['paqueteProductoTratamientoActualizado'] = "El paquete de productos del tratamiento "+nombreTratamiento+" ha sido actualizado correctamente!"
                    return redirect('/verTratamientos/')
            elif masProductos == "masProductos":
                productosAgregar = request.POST['idsProductosGastoTratamiento']
                listaProductosAgregar = productosAgregar.split(",")
                
                listaCantidadesSolicitadas = []
                
                for idProducto in listaProductosAgregar:
                    nameCantidadProducto = "cantidadUsar"+str(idProducto)
                    cantidadSolicitadaMandada = request.POST[nameCantidadProducto]
                    listaCantidadesSolicitadas.append(cantidadSolicitadaMandada)
                lista = zip(listaProductosAgregar,listaCantidadesSolicitadas)
                
                
                for producto, cantidad in lista:
                    idProductoBD = producto
                    cantidadProductoBD = cantidad
                    
                    registroProducto = TratamientosProductosGasto(tratamiento = Tratamientos.objects.get(id_tratamiento=idTratamientoEditar),producto_gasto=ProductosGasto.objects.get(id_producto =idProductoBD),cantidad=cantidadProductoBD)
                    registroProducto.save()
                
                if actualizacionProductoPaquete or borrado or registroProducto: 
                    request.session['paqueteProductoTratamientoActualizado'] = "El paquete de productos del tratamiento "+nombreTratamiento+" ha sido actualizado correctamente!"
                    return redirect('/verTratamientos/')

