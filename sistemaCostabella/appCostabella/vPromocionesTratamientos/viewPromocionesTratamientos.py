
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

# Importacion de modelos
from appCostabella.models import (Empleados, 
                                  PaquetesPromocionTratamientos, Permisos, Sucursales,
                                  Tratamientos)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)


def agregarPaquetePromocionTratamiento(request):
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
        
        #Tratamientos
        consultaTratamientos = Tratamientos.objects.all()

        listaTratamientosSelectMultiple = []
        listaTratamientosSelectMultipleJS = []
        listaNombresTratamientosSelectMultiple = []

        for tratamiento in consultaTratamientos:
            nombreTratamiento = tratamiento.nombre_tratamiento

            longitudListaNombres = len(listaNombresTratamientosSelectMultiple)

            if longitudListaNombres == 0:
                listaNombresTratamientosSelectMultiple.append(nombreTratamiento)
                #Agregar todos los datos de ese tratamiento a una sola posicion.
                arregloCodigosTratamientosIguales = []
                arregloCostoaDeVentaIguales = []
                arregloSucursalesIguales = []
                arregloNombresSucursalesIguales = []
                arregloNombreTratamiento = []
                arregloDatosTratamiento = []

                consultaTratamientosIguales = Tratamientos.objects.filter(nombre_tratamiento = nombreTratamiento)
                for tratamientoIgual in consultaTratamientosIguales:
                    codigoTratamientoIgual = tratamientoIgual.codigo_tratamiento
                    costoVentaTratamientoIgual = tratamientoIgual.costo_venta_tratamiento
                    sucursalTratamientoIgual = tratamientoIgual.sucursal_id
                    nombresitoTratamiento = tratamientoIgual.nombre_tratamiento

                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalTratamientoIgual)
                    for datoSucursal in consultaSucursal:
                        nombreSucursalTratamientoIgual = datoSucursal.nombre
                    
                   
                    arregloCodigosTratamientosIguales.append(codigoTratamientoIgual)
                    arregloCostoaDeVentaIguales.append(costoVentaTratamientoIgual)
                    arregloSucursalesIguales.append(sucursalTratamientoIgual)
                    arregloNombresSucursalesIguales.append(nombreSucursalTratamientoIgual)
                    arregloNombreTratamiento.append(nombresitoTratamiento)

                    sumaCostosDeVenta = 0
                    contadorCostosDeVenta = 0
                    for costo in arregloCostoaDeVentaIguales:
                        costito = costo
                        contadorCostosDeVenta = contadorCostosDeVenta + 1
                        sumaCostosDeVenta = sumaCostosDeVenta + costito
                    promedioCostoVentaTratamiento = sumaCostosDeVenta/contadorCostosDeVenta
                
                arregloDatosTratamiento.append([arregloCodigosTratamientosIguales,nombreTratamiento,arregloCostoaDeVentaIguales,arregloSucursalesIguales,arregloNombresSucursalesIguales, promedioCostoVentaTratamiento])
                
                listaTratamientosSelectMultiple.append(arregloDatosTratamiento)
                listaTratamientosSelectMultipleJS.append(arregloDatosTratamiento)
            else:
                if nombreTratamiento in listaNombresTratamientosSelectMultiple:
                    yaEstaEnArreglo = True
                else:
                    listaNombresTratamientosSelectMultiple.append(nombreTratamiento)

                    #Agregar todos los datos de ese tratamiento a una sola posicion.
                    arregloCodigosTratamientosIguales = []
                    arregloCostoaDeVentaIguales = []
                    arregloSucursalesIguales = []
                    arregloNombresSucursalesIguales = []
                    arregloNombreTratamiento = []
                    arregloDatosTratamiento = []

                    consultaTratamientosIguales = Tratamientos.objects.filter(nombre_tratamiento = nombreTratamiento)
                    for tratamientoIgual in consultaTratamientosIguales:
                        codigoTratamientoIgual = tratamientoIgual.codigo_tratamiento
                        costoVentaTratamientoIgual = tratamientoIgual.costo_venta_tratamiento
                        sucursalTratamientoIgual = tratamientoIgual.sucursal_id
                        nombresitoTratamiento = tratamientoIgual.nombre_tratamiento

                        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalTratamientoIgual)
                        for datoSucursal in consultaSucursal:
                            nombreSucursalTratamientoIgual = datoSucursal.nombre
                        
                        arregloCodigosTratamientosIguales.append(codigoTratamientoIgual)
                        arregloCostoaDeVentaIguales.append(costoVentaTratamientoIgual)
                        arregloSucursalesIguales.append(sucursalTratamientoIgual)
                        arregloNombresSucursalesIguales.append(nombreSucursalTratamientoIgual)
                        arregloNombreTratamiento.append(nombresitoTratamiento)

                        sumaCostosDeVenta = 0
                        contadorCostosDeVenta = 0
                        for costo in arregloCostoaDeVentaIguales:
                            costito = costo
                            contadorCostosDeVenta = contadorCostosDeVenta + 1
                            sumaCostosDeVenta = sumaCostosDeVenta + costito
                        promedioCostoVentaTratamiento = sumaCostosDeVenta/contadorCostosDeVenta

                    arregloDatosTratamiento.append([arregloCodigosTratamientosIguales,nombreTratamiento,arregloCostoaDeVentaIguales,arregloSucursalesIguales,arregloNombresSucursalesIguales, promedioCostoVentaTratamiento])
                    listaTratamientosSelectMultiple.append(arregloDatosTratamiento)
                    listaTratamientosSelectMultipleJS.append(arregloDatosTratamiento)

        



        if "tratamientoNoSeleccionado" in request.session:
            tratamientoNoSeleccionado = request.session["tratamientoNoSeleccionado"]
            del request.session["tratamientoNoSeleccionado"]
            return render(request,"21 PaquetesTratamientos/agregarPaquetePromocionTratamiento.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                         "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos, 
                                                                         "listaTratamientosSelectMultiple":listaTratamientosSelectMultiple, "listaTratamientosSelectMultipleJS":listaTratamientosSelectMultipleJS,
                                                                         "tratamientoNoSeleccionado":tratamientoNoSeleccionado,"notificacionCita":notificacionCita})
        if "promocionAgregada" in request.session:
            promocionAgregada = request.session["promocionAgregada"]
            del request.session["promocionAgregada"]
            return render(request,"21 PaquetesTratamientos/agregarPaquetePromocionTratamiento.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                         "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos, 
                                                                         "listaTratamientosSelectMultiple":listaTratamientosSelectMultiple, "listaTratamientosSelectMultipleJS":listaTratamientosSelectMultipleJS,
                                                                         "promocionAgregada":promocionAgregada,"notificacionCita":notificacionCita})
        if "promocionNoAgregada" in request.session:
            promocionNoAgregada = request.session["promocionNoAgregada"]
            del request.session["promocionNoAgregada"]
            return render(request,"21 PaquetesTratamientos/agregarPaquetePromocionTratamiento.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                         "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos, 
                                                                         "listaTratamientosSelectMultiple":listaTratamientosSelectMultiple, "listaTratamientosSelectMultipleJS":listaTratamientosSelectMultipleJS,
                                                                         "promocionNoAgregada":promocionNoAgregada,"notificacionCita":notificacionCita})


        
        return render(request,"21 PaquetesTratamientos/agregarPaquetePromocionTratamiento.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                         "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos, 
                                                                         "listaTratamientosSelectMultiple":listaTratamientosSelectMultiple, "listaTratamientosSelectMultipleJS":listaTratamientosSelectMultipleJS, "notificacionCita":notificacionCita})
    
    
    else:
        return render(request,"1 Login/login.html")  

def guardarPromocionTratamiento(request):
    if "idSesion" in request.session:
     

        if request.method == "POST":
            #tomar el nombre del tratamiento seleccionado:
            tratamientoSeleccionado = request.POST["tratamientoSeleccionado"]

            if tratamientoSeleccionado == "Todas":
                request.session["tratamientoNoSeleccionado"] = "No se ha seleccionado ningún Tratamiento!"
                return redirect("/agregarPaquetePromocionTratamiento/")
            else:
                nombrePaquete = request.POST["nombrePaquete"]

                idsTratamientos = []
                consultaTratamiento = Tratamientos.objects.filter(nombre_tratamiento = tratamientoSeleccionado)
                
                for datoTratamiento in consultaTratamiento:
                    idTratamiento = datoTratamiento.id_tratamiento
                    idsTratamientos.append(idTratamiento)
                    

                
                sesionesPaquete = request.POST["sesionesPaquete"]

                if request.POST.get("switchDescuento", False): #Checkeado

                    descuento = request.POST["descuentoPromo"]
                    precioConDescuento = request.POST["precioConDescuento"]

                    for tratamiento in idsTratamientos:
                        intIdTratamiento = int(tratamiento)
                        #registro de promocion
                        registroPromocion = PaquetesPromocionTratamientos(tratamiento = Tratamientos.objects.get(id_tratamiento = intIdTratamiento),
                        nombre_paquete = nombrePaquete, numero_sesiones = sesionesPaquete, descuento = float(descuento) ,precio_por_paquete = precioConDescuento, promocion_activa = "A")
                        registroPromocion.save()

                    if registroPromocion:
                        request.session["promocionAgregada"] = "Se ha agregado la promoción "+nombrePaquete+"!"
                        return redirect("/agregarPaquetePromocionTratamiento/")
                    else:
                        request.session["promocionNoAgregada"] = "Error en la base de datos! Contacte a soporte."
                        return redirect("/agregarPaquetePromocionTratamiento/")
                elif request.POST.get("switchDescuento", True): #No checkeado
                    precioFijo = request.POST["precioFijo"]


                    for tratamiento in idsTratamientos:
                        intIdTratamiento = int(tratamiento)
                        #registro de promocion
                        registroPromocion = PaquetesPromocionTratamientos(tratamiento = Tratamientos.objects.get(id_tratamiento = intIdTratamiento),
                        nombre_paquete = nombrePaquete, numero_sesiones = sesionesPaquete, precio_por_paquete = precioFijo, promocion_activa = "A")
                        registroPromocion.save()

                
                    if registroPromocion:
                        request.session["promocionAgregada"] = "Se ha agregado la promoción "+nombrePaquete+"!"
                        return redirect("/agregarPaquetePromocionTratamiento/")
                    else:
                        request.session["promocionNoAgregada"] = "Error en la base de datos! Contacte a soporte."
                        return redirect("/agregarPaquetePromocionTratamiento/")



        



        
                
        
    
    
    else:
        return render(request,"1 Login/login.html")

def verPaquetesPromocionTratamientos(request):

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
            sucursalTratamientos = request.POST["sucursalTratamientos"] #Sucursal que seleccionó el usuario
           
            promocionesTratamientos = []
            promocionesTratamientosInactivos = []

            promocionesTratamientosModalEditar = []
            promocionesTratamientosInactivosModalEditar = []

            promocionesTratamientosModalBaja = []
            promocionesTratamientosInactivosModalAlta = []

            #Mostrar todas las sucursales
            if sucursalTratamientos == "todasLasSucursales":
                consultaPromociones = PaquetesPromocionTratamientos.objects.all()
                nombreSucursalView = "Todas las sucursales"

                for datoPromocion in consultaPromociones:
                    idPromocion = datoPromocion.id_paquete_tratamiento
                    numeroSesiones = datoPromocion.numero_sesiones
                    descuento = datoPromocion.descuento
                    if descuento == None:
                        boolDescuento = "Sin descuento"
                    else:
                        boolDescuento = "Con descuento"
                    precioPorPaquete = datoPromocion.precio_por_paquete
                    nombrePaquete = datoPromocion.nombre_paquete

                    #Datos del tratamiento
                    datosTratamientoPaquete = []
                    idTratamiento = datoPromocion.tratamiento_id
                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)

                    for datoTratamiento in consultaTratamiento:
                        idTratamiento = datoTratamiento.id_tratamiento
                        nombreTratamiento = datoTratamiento.nombre_tratamiento
                        codigoTratamiento = datoTratamiento.codigo_tratamiento

                        precioUnitarioTratamiento = datoTratamiento.costo_venta_tratamiento

                        sucursalTratamiento = datoTratamiento.sucursal_id

                        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalTratamiento)
                        for datoSucursal in consultaSucursal:
                            nombreSucursal = datoSucursal.nombre
                        
                        datosTratamientoPaquete.append([idTratamiento, codigoTratamiento, nombreTratamiento, precioUnitarioTratamiento])

                    promocionActiva = datoPromocion.promocion_activa
                    if promocionActiva == "A":
                        promocionesTratamientos.append([idPromocion,nombrePaquete,numeroSesiones,boolDescuento,descuento,precioPorPaquete,datosTratamientoPaquete, nombreSucursal])
                        promocionesTratamientosModalEditar.append([idPromocion,nombrePaquete,numeroSesiones,boolDescuento,descuento,precioPorPaquete,datosTratamientoPaquete, nombreSucursal])
                        promocionesTratamientosModalBaja.append([idPromocion,nombrePaquete,numeroSesiones,boolDescuento,descuento,precioPorPaquete,datosTratamientoPaquete, nombreSucursal])
                    else:
                        promocionesTratamientosInactivos.append([idPromocion,nombrePaquete,numeroSesiones,boolDescuento,descuento,precioPorPaquete,datosTratamientoPaquete, nombreSucursal])
                        promocionesTratamientosInactivosModalEditar.append([idPromocion,nombrePaquete,numeroSesiones,boolDescuento,descuento,precioPorPaquete,datosTratamientoPaquete, nombreSucursal])
                        promocionesTratamientosInactivosModalAlta.append([idPromocion,nombrePaquete,numeroSesiones,boolDescuento,descuento,precioPorPaquete,datosTratamientoPaquete, nombreSucursal])
            #Si selecciono solo una sucursal
            else:
                consultaPromociones = PaquetesPromocionTratamientos.objects.all()
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalTratamientos)
                intSucursal = int(sucursalTratamientos)
                for datoSucursal in consultaSucursal:
                    nombreSucursalView = datoSucursal.nombre
                for promo in consultaPromociones:
                    idTratamiento = promo.tratamiento_id


                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)
                    for datoTratamiento in consultaTratamiento:
                        idSucursal = datoTratamiento.sucursal_id

                        if intSucursal == idSucursal:
                            #Promo se agrega al array de promos 
                            numeroSesiones = promo.numero_sesiones
                            descuento = promo.descuento
                            if descuento == None:
                                boolDescuento = "Sin descuento"
                            else:
                                boolDescuento = "Con descuento"
                            precioPorPaquete = promo.precio_por_paquete
                            nombrePaquete = promo.nombre_paquete
                            idPromocion = promo.id_paquete_tratamiento

                            #Datos del tratamiento
                            datosTratamientoPaquete = []
                            idTratamiento = promo.tratamiento_id
                            consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)

                            for datoTratamiento in consultaTratamiento:
                                idTratamiento = datoTratamiento.id_tratamiento
                                nombreTratamiento = datoTratamiento.nombre_tratamiento
                                codigoTratamiento = datoTratamiento.codigo_tratamiento

                                precioUnitarioTratamiento = datoTratamiento.costo_venta_tratamiento

                                sucursalTratamiento = datoTratamiento.sucursal_id

                                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalTratamiento)
                                for datoSucursal in consultaSucursal:
                                    nombreSucursal = datoSucursal.nombre
                                
                                datosTratamientoPaquete.append([idTratamiento, codigoTratamiento, nombreTratamiento, precioUnitarioTratamiento])
                            promocionActiva = promo.promocion_activa
                            if promocionActiva == "A":
                                promocionesTratamientos.append([idPromocion,nombrePaquete,numeroSesiones,boolDescuento,descuento,precioPorPaquete,datosTratamientoPaquete, nombreSucursal])
                                promocionesTratamientosModalEditar.append([idPromocion,nombrePaquete,numeroSesiones,boolDescuento,descuento,precioPorPaquete,datosTratamientoPaquete, nombreSucursal])
                                promocionesTratamientosModalBaja.append([idPromocion,nombrePaquete,numeroSesiones,boolDescuento,descuento,precioPorPaquete,datosTratamientoPaquete, nombreSucursal])
                            else:
                                promocionesTratamientosInactivos.append([idPromocion,nombrePaquete,numeroSesiones,boolDescuento,descuento,precioPorPaquete,datosTratamientoPaquete, nombreSucursal])
                                promocionesTratamientosInactivosModalEditar.append([idPromocion,nombrePaquete,numeroSesiones,boolDescuento,descuento,precioPorPaquete,datosTratamientoPaquete, nombreSucursal])
                                promocionesTratamientosInactivosModalAlta.append([idPromocion,nombrePaquete,numeroSesiones,boolDescuento,descuento,precioPorPaquete,datosTratamientoPaquete, nombreSucursal])
            return render(request, "21 PaquetesTratamientos/verPromocionesTratamientos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "nombreSucursalView":nombreSucursalView, "promocionesTratamientos":promocionesTratamientos, "promocionesTratamientosInactivos":promocionesTratamientosInactivos,
                "promocionesTratamientosModalEditar":promocionesTratamientosModalEditar, "promocionesTratamientosInactivosModalEditar":promocionesTratamientosInactivosModalEditar,
                "promocionesTratamientosModalBaja":promocionesTratamientosModalBaja, "promocionesTratamientosInactivosModalAlta":promocionesTratamientosInactivosModalAlta, "notificacionCita":notificacionCita})
    
        else:           
            if tipoUsuario == "esAdmin":
                sucursales = Sucursales.objects.all()
                
                if "promocionEstatus" in request.session:
                    promocionEstatus = request.session["promocionEstatus"]
                    del request.session["promocionEstatus"]
                    return render(request, "21 PaquetesTratamientos/seleccionarSucursalPaqueteTratamiento.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "promocionEstatus":promocionEstatus, "notificacionCita":notificacionCita})

                if "promocionEstatusFallo" in request.session:
                    promocionEstatusFallo = request.session["promocionEstatusFallo"]
                    del request.session["promocionEstatusFallo"]
                    return render(request, "21 PaquetesTratamientos/seleccionarSucursalPaqueteTratamiento.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "promocionEstatusFallo":promocionEstatusFallo, "notificacionCita":notificacionCita})



                return render(request, "21 PaquetesTratamientos/seleccionarSucursalPaqueteTratamiento.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})
            else:
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    sucursalEmpleado = datoEmpleado.id_sucursal_id
                sucursales = Sucursales.objects.filter(id_sucursal = sucursalEmpleado)
                
                if "promocionEstatus" in request.session:
                    promocionEstatus = request.session["promocionEstatus"]
                    del request.session["promocionEstatus"]
                    return render(request, "21 PaquetesTratamientos/seleccionarSucursalPaqueteTratamiento.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "promocionEstatus":promocionEstatus, "notificacionCita":notificacionCita})

                if "promocionEstatusFallo" in request.session:
                    promocionEstatusFallo = request.session["promocionEstatusFallo"]
                    del request.session["promocionEstatusFallo"]
                    return render(request, "21 PaquetesTratamientos/seleccionarSucursalPaqueteTratamiento.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "promocionEstatusFallo":promocionEstatusFallo, "notificacionCita":notificacionCita})


                return render(request, "21 PaquetesTratamientos/seleccionarSucursalPaqueteTratamiento.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})

        
    else:
        return render(request,"1 Login/login.html")

def bajaPromocionTratamiento(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idPromocionBaja = request.POST["idPromocionBaja"]

            #Actualización.
            actualizacionPromocion = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idPromocionBaja).update(promocion_activa = "I")
            
            if actualizacionPromocion:
                consultaPromo = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idPromocionBaja)
                for dato in consultaPromo:
                    nombrePromo = dato.nombre_paquete
                    tratamiento = dato.tratamiento_id
                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = tratamiento)
                    for datoTratamiento in consultaTratamiento:
                        idSucursal = datoTratamiento.sucursal_id

                    consultaSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                request.session["promocionEstatus"] = "Se ha desactivado la promoción "+nombrePromo+" de la sucursal "+nombreSucursal+"!"
                return redirect("/verPaquetesPromocionTratamientos/")
            else:
                request.session["promocionEstatusFallo"] = "Error en la base de datos, contacte a soporte!"
                return redirect("/verPaquetesPromocionTratamientos/")

    


        
    else:
        return render(request,"1 Login/login.html")

def altaPromocionTratamiento(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idPromocionAlta = request.POST["idPromocionAlta"]

            #Actualización.
            actualizacionPromocion = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idPromocionAlta).update(promocion_activa = "A")
            
            if actualizacionPromocion:
                consultaPromo = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idPromocionAlta)
                for dato in consultaPromo:
                    nombrePromo = dato.nombre_paquete
                    tratamiento = dato.tratamiento_id
                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = tratamiento)
                    for datoTratamiento in consultaTratamiento:
                        idSucursal = datoTratamiento.sucursal_id

                    consultaSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                request.session["promocionEstatus"] = "Se ha activado la promoción "+nombrePromo+" de la sucursal "+nombreSucursal+"!"
                return redirect("/verPaquetesPromocionTratamientos/")
            else:
                request.session["promocionEstatusFallo"] = "Error en la base de datos, contacte a soporte!"
                return redirect("/verPaquetesPromocionTratamientos/")

    


        
    else:
        return render(request,"1 Login/login.html")
