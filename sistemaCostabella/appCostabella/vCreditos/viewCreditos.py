
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

# Librerías de fecha
from datetime import date, datetime, time, timedelta

#Plugin impresora termica
from appCostabella import Conector
# Importacion de modelos
from appCostabella.models import (Clientes, ConfiguracionCredito, Creditos, Descuentos,
                                  Empleados, 
                                  MovimientosCaja, PagosCreditos,
                                  PaquetesPromocionTratamientos, Permisos, ProductosRenta,
                                  ProductosVenta, Servicios, Sucursales,
                                  Tratamientos, Ventas,)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)

def configuracionCredito(request):

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
        
        
        
        sucursales = []
        
        configuracionesTotales = ConfiguracionCredito.objects.all()
        for configuracion in configuracionesTotales:
            id_sucursal = configuracion.sucursal_id
            
            sucursal = Sucursales.objects.filter(id_sucursal = id_sucursal)
            for dato in sucursal:
                nombreSucursal = dato.nombre
            sucursales.append(nombreSucursal)
            
        lista = zip(configuracionesTotales, sucursales)
        
        if 'configuracionCreditoAgregada' in request.session:
            configuracionAgregada = request.session['configuracionCreditoAgregada']
            del request.session['configuracionCreditoAgregada']
            return render(request, "14 Creditos/configuracionCredito.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "lista":lista, "configuracionAgregada":configuracionAgregada, "notificacionCita":notificacionCita
            })
        
        if 'configuracionCreditoNoAgregado' in request.session:
            configuracionNoAgregado = request.session['configuracionCreditoNoAgregado']
            del request.session['configuracionCreditoNoAgregado']
            return render(request, "14 Creditos/configuracionCredito.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "lista":lista, "configuracionNoAgregado":configuracionNoAgregado, "notificacionCita":notificacionCita
            })

        if 'configuracionActivada' in request.session:
            configuracionActivada = request.session['configuracionActivada']
            del request.session['configuracionActivada']
            return render(request, "14 Creditos/configuracionCredito.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "lista":lista, "configuracionActivada":configuracionActivada, "notificacionCita":notificacionCita
            })
            
        return render(request, "14 Creditos/configuracionCredito.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "lista":lista, "notificacionCita":notificacionCita
        })
    
    else:
        return render(request,"1 Login/login.html")

def agregarConfiguracionCredito(request):

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
        

        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]
        
           #notificacionRentas
        notificacionRenta = notificacionRentas(request)

        #notificacionCitas
        notificacionCita = notificacionCitas(request)
        
         #permisosEmpleado
        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)

        # retornar sucrusales
        sucursales = Sucursales.objects.all()
        if request.method == "POST":
            limite_credito = request.POST['limiteCredito']  #Requerido
            
            fecha_config_credito = datetime.today().strftime('%Y-%m-%d') #Requerido
            sucursal =  request.POST['sucursal']  #Requerido
            #fechaAlta = datetime.now()
            
         
            

            registroConfiguracionCredito = ConfiguracionCredito(limite_credito = limite_credito,
                    fecha = fecha_config_credito, 
                    sucursal = Sucursales.objects.get(id_sucursal = sucursal), activo = "N")
               
       

            registroConfiguracionCredito.save()
            
            if registroConfiguracionCredito:
                    request.session['configuracionCreditoAgregada'] = "La configuracion de límite de crédito de $" + str(limite_credito) +  " por cliente ha sido gregado satisfactoriamente!"

                    return redirect('/configuracionCredito/')
                    
            else:
                    request.session['configuracionCreditoNoAgregado'] = "Error en la base de datos, intentelo más tarde!"

                    return redirect('/configuracionCredito/')

            
        return render(request, "14 Creditos/agregarConfiguracionCredito.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "notificacionRenta":notificacionRenta,"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "sucursales":sucursales, "notificacionCita":notificacionCita
        })
    
    else:
        return render(request,"1 Login/login.html")

def verCreditosClientes(request):

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
        
        #------ Creditos pendientes
        agregados = []
        sucursalesCreditos =[]
        clientesCreditos =[]
        fechasCreditosPendientes = []
        estatusPago =[]
        fechasPago = []
        productosPendientes = []
        serviciosCorporalesPendientes = []
        serviciosFacialesPendientes = []
        tratamientosPendientes = []
        paquetesPendientes = []
        
        contadorPendientes = 0
        totalCreditosPendientes= Creditos.objects.filter(estatus="Pendiente")
        if totalCreditosPendientes:
            for pendiente in totalCreditosPendientes:
                contadorPendientes = contadorPendientes+1
                id_persona_realizo = pendiente.empleado_vendedor_id
                id_sucursal  = pendiente.sucursal_id
                id_cliente =pendiente.cliente_id
                id_credito = pendiente.id_credito
                
                empleado = Empleados.objects.filter(id_empleado = id_persona_realizo)
                for dato in empleado:
                    nombre = dato.nombres
                    apellidoPat = dato.apellido_paterno
                    apellidoMat = dato.apellido_materno
                nombreCompleto = nombre + " " + apellidoPat + " " + apellidoMat
                agregados.append(nombreCompleto)
                
                sucursales = Sucursales.objects.filter(id_sucursal = id_sucursal)
                for sucursal in sucursales:
                    nombreSucursal = sucursal.nombre
                    sucursalesCreditos.append(nombreSucursal)
                    
                clientes = Clientes.objects.filter(id_cliente = id_cliente)
                for cliente in clientes:
                    idCliente = cliente.id_cliente
                    nombreCliente = cliente.nombre_cliente
                    apellidoP = cliente.apellidoPaterno_cliente
                    apellidoM = cliente.apellidoPaterno_cliente
                clienteCompleto= str(idCliente) + " - " + nombreCliente + " " + apellidoP + " " + apellidoM
                clientesCreditos.append(clienteCompleto)
                
                fechaAltaCredito = pendiente.fecha_venta_credito
                fechaPrimerPago = fechaAltaCredito + timedelta(days = 15)
                fechaSegundoPago =fechaAltaCredito + timedelta(days = 30)
                fechaTercerPago =fechaAltaCredito + timedelta(days = 45)
                fechaCuartoPago =fechaAltaCredito + timedelta(days = 60)
                
                fechasCreditosPendientes.append([fechaPrimerPago,fechaSegundoPago,fechaTercerPago,fechaCuartoPago])
                
                datosPagos = PagosCreditos.objects.filter(id_credito__id_credito = id_credito)
                for pago in datosPagos:
                    pago1 = pago.monto_pago1
                    
                    pago2 = pago.monto_pago2
                
                    pago3 = pago.monto_pago3
                    
                    pago4 = pago.monto_pago4
                    
                    
                    estatusPago1=""
                    estatusPago2=""
                    estatusPago3=""
                    estatusPago4=""
                    if pago1 == None:
                        estatusPago1 = "Pendiente"
                        fechaPago1 = "Sin fecha"
                    else:
                        fechaPago1 = pago.fecha_pago1
                        estatusPago1 = "Se pagaron $ "  + str(pago1) + "MXN el día "
                        
                        
                        
                    if pago2 == None:
                        estatusPago2 = "Pendiente"
                        fechaPago2 = "Sin fecha"
                    else:
                        fechaPago2 = pago.fecha_pago2
                        estatusPago2 = "Se pagaron $ "  + str(pago2) + "MXN el día "+str(fechaPago2)
                        
                        
                    if pago3 == None:
                        estatusPago3 = "Pendiente"
                        fechaPago3 = "Sin fecha"
                    else:
                        fechaPago3 = pago.fecha_pago3
                        estatusPago3 = "Se pagaron $ "  + str(pago3) + "MXN el día "+str(fechaPago3)
                        
                        
                        
                    if pago4 == None:
                        estatusPago4 = "Pendiente"
                        fechaPago4 = "Sin fecha"
                    else:
                        fechaPago4 = pago.fecha_pago4
                        estatusPago4 = "Se pagaron $ "  + str(pago4) + "MXN el día "+str(fechaPago4)
                        
                        
                    estatusPago.append([estatusPago1,estatusPago2,estatusPago3,estatusPago4])
                    fechasPago.append([fechaPago1,fechaPago2,fechaPago3,fechaPago4])
                    
                #SACAR LO QUE COMPRO EN LA VENTA o renta...
                
                venta = pendiente.venta_id
                consultaVenta = Ventas.objects.filter(id_venta = venta)
                for datoVenta in consultaVenta:
                    codigosProductos = datoVenta.ids_productos
                    cantidadesProductos = datoVenta.cantidades_productos
                    serviciosCorporales = datoVenta.ids_servicios_corporales
                    cantidadesSC = datoVenta.cantidades_servicios_corporales
                    serviciosFaciales = datoVenta.ids_servicios_faciales
                    cantidadesSF = datoVenta.cantidades_servicios_faciales
                    idTratamiento = datoVenta.id_tratamiento_vendido_id
                    idPaquete = datoVenta.id_paquete_promo_vendido_id
                
                hayProductos = False
                haySC = False
                haySF = False
                hayTratamiento = False
                hayPquete = False
                
                if codigosProductos == "":
                    hayProductos = False
                else:
                    hayProductos = True
                    arregloCodigosProductos = codigosProductos.split(",")
                    arregloCantidadesProductos = cantidadesProductos.split(",")
                    listaProductos = zip(arregloCodigosProductos, arregloCantidadesProductos)
                
                if serviciosCorporales == "":
                    haySC = False
                else:  
                    haySC = True
                    arregloidsSC = serviciosCorporales.split(",")
                    arregloCantidadesSC = cantidadesSC.split(",")
                    listaServiciosCorporales = zip(arregloidsSC,arregloCantidadesSC)
                
                if serviciosFaciales == "":
                    haySF = False
                else:
                    haySF = True
                    arregloidsSF = serviciosFaciales.split(",")
                    arregloCantidadesSF = cantidadesSF.split(",")
                    listaServiciosFaciales = zip(arregloidsSF, arregloCantidadesSF)
                
                if idTratamiento == None:
                    hayTratamiento = False
                else:
                    hayTratamiento = True
                
                if idPaquete == None:
                    hayPaquete = False
                else:
                    hayPaquete = True

            
                
                miniProductos = []
                if hayProductos:
                    for codigo, cantidadProducto in listaProductos:
                        codigoProducto = str(codigo)
                        strCantidadProducto = str(cantidadProducto)
                        if "PV" in codigoProducto:
                            consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
                        else:
                            consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigoProducto)
                        for datoProducto in consultaProducto:
                            nombreProducto = datoProducto.nombre_producto
                        miniProductos.append([codigoProducto,nombreProducto,strCantidadProducto])
            
                
                miniSC = []
                if haySC:
                    for idSC, cantidadSC in listaServiciosCorporales:
                        idServicio = int(idSC)
                        strCantidadServicio = str(cantidadSC)
                        consultarServicio = Servicios.objects.filter(id_servicio = idServicio)
                        for datoServicio in consultarServicio:
                            nombreServicio = datoServicio.nombre_servicio
                        miniSC.append([idServicio,nombreServicio,strCantidadServicio])
                    
                miniSF = []
                if haySF:
                    for idSF, cantidadSF in listaServiciosFaciales:
                        idServicio = int(idSF)
                        strCantidadServicio = str(cantidadSF)
                        consultarServicio = Servicios.objects.filter(id_servicio = idServicio)
                        for datoServicio in consultarServicio:
                            nombreServicio = datoServicio.nombre_servicio
                        miniSF.append([idServicio,nombreServicio,strCantidadServicio])
                
                miniTrata = []
                if hayTratamiento:
                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)
                    for datoTratamiento in consultaTratamiento:
                        codigoTratamiento = datoTratamiento.codigo_tratamiento
                        nombreTratamiento = datoTratamiento.nombre_tratamiento
                    miniTrata.append([codigoTratamiento, nombreTratamiento])

                miniPaquete = []
                if hayPaquete:
                    consultaPaquete = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idPaquete)
                    for datoPaquete in consultaPaquete:
                        nombre_paquete = datoPaquete.nombre_paquete
                        numero_sesiones = datoPaquete.numero_sesiones
                    miniPaquete.append([nombre_paquete,numero_sesiones])


                
                
                productosPendientes.append(miniProductos)
                serviciosCorporalesPendientes.append(miniSC)
                serviciosFacialesPendientes.append(miniSF)


                tratamientosPendientes.append(miniTrata)
                paquetesPendientes.append(miniPaquete)
                
            listaCreditosPendientes = zip(totalCreditosPendientes,clientesCreditos,agregados,sucursalesCreditos,fechasCreditosPendientes, estatusPago,fechasPago, productosPendientes, serviciosCorporalesPendientes, serviciosFacialesPendientes,
            tratamientosPendientes, paquetesPendientes)
        else:
            listaCreditosPendientes = None
        #------ Creditos finalizados
        
        agregadosFinalizados = []
        sucursalesCreditosFinalizados =[]
        clientesCreditosFinalizados =[]
        fechasDePago = []
        
        productosFinalizados = []
        serviciosCorporalesFinalizados = []
        serviciosFacialesFinalizados = []
        
        contadorFinalizado = 0
        totalCreditosFinalizados= Creditos.objects.filter(estatus="Finalizado")
        for finalizado in totalCreditosFinalizados:
            idCreditoFinalizado = finalizado.id_credito
            contadorFinalizado = contadorFinalizado + 1
            id_persona_realizo = finalizado.empleado_vendedor_id
            id_sucursal  = finalizado.sucursal_id
            id_cliente =finalizado.cliente_id
            
            empleado = Empleados.objects.filter(id_empleado = id_persona_realizo)
            for dato in empleado:
                nombre = dato.nombres
                apellidoPat = dato.apellido_paterno
                apellidoMat = dato.apellido_materno
            nombreCompleto = nombre + " " + apellidoPat + " " + apellidoMat
            agregadosFinalizados.append(nombreCompleto)
            
            sucursales = Sucursales.objects.filter(id_sucursal = id_sucursal)
            for sucursal in sucursales:
                nombreSucursal = sucursal.nombre
                sucursalesCreditosFinalizados.append(nombreSucursal)
                
            clientes = Clientes.objects.filter(id_cliente = id_cliente)
            for cliente in clientes:
                idCliente = cliente.id_cliente
                nombreCliente = cliente.nombre_cliente
                apellidoP = cliente.apellidoPaterno_cliente
                apellidoM = cliente.apellidoPaterno_cliente
            clienteCompleto= str(idCliente) + " - " + nombreCliente + " " + apellidoP + " " + apellidoM
            clientesCreditosFinalizados.append(clienteCompleto)
            
            #Fechas de cuando pago..
            consultaPagos = PagosCreditos.objects.filter(id_credito_id__id_credito = idCreditoFinalizado)
            paguitos = []
            for datosPago in consultaPagos:
                fechaPago1 = datosPago.fecha_pago1
                fechaPago2 = datosPago.fecha_pago2
                fechaPago3 = datosPago.fecha_pago3
                fechaPago4 = datosPago.fecha_pago4
                
                if fechaPago1 != None:#Si hay una fecha del pago
                    monto_pago1 = datosPago.monto_pago1
                    paguitos.append(["Pago 1",fechaPago1,monto_pago1])
                if fechaPago2 != None:#Si hay una fecha del pago
                    monto_pago2 = datosPago.monto_pago2
                    paguitos.append(["Pago 2",fechaPago2,monto_pago2])
                if fechaPago3 != None:#Si hay una fecha del pago
                    monto_pago3 = datosPago.monto_pago3
                    paguitos.append(["Pago 3",fechaPago3,monto_pago3])
                if fechaPago4 != None:#Si hay una fecha del pago
                    monto_pago4 = datosPago.monto_pago4
                    paguitos.append(["Pago 4",fechaPago4,monto_pago4])
            fechasDePago.append(paguitos)    
                
            #SACAR LO QUE COMPRO EN LA VENTA...
            
            venta = finalizado.venta_id
            consultaVenta = Ventas.objects.filter(id_venta = venta)
            for datoVenta in consultaVenta:
                codigosProductos = datoVenta.ids_productos
                cantidadesProductos = datoVenta.cantidades_productos
                serviciosCorporales = datoVenta.ids_servicios_corporales
                cantidadesSC = datoVenta.cantidades_servicios_corporales
                serviciosFaciales = datoVenta.ids_servicios_faciales
                cantidadesSF = datoVenta.cantidades_servicios_faciales
            
            hayProductos = False
            haySC = False
            haySF = False
            
            if codigosProductos == "":
                hayProductos = False
            else:
                hayProductos = True
                arregloCodigosProductos = codigosProductos.split(",")
                arregloCantidadesProductos = cantidadesProductos.split(",")
                listaProductos = zip(arregloCodigosProductos, arregloCantidadesProductos)
            
            if serviciosCorporales == "":
                haySC = False
            else:  
                haySC = True
                arregloidsSC = serviciosCorporales.split(",")
                arregloCantidadesSC = cantidadesSC.split(",")
                listaServiciosCorporales = zip(arregloidsSC,arregloCantidadesSC)
            
            if serviciosFaciales == "":
                haySF = False
            else:
                haySF = True
                arregloidsSF = serviciosFaciales.split(",")
                arregloCantidadesSF = cantidadesSF.split(",")
                listaServiciosFaciales = zip(arregloidsSF, arregloCantidadesSF)
           
            
            miniProductos = []
            if hayProductos:
                for codigo, cantidadProducto in listaProductos:
                    codigoProducto = str(codigo)
                    strCantidadProducto = str(cantidadProducto)
                    if "PV" in codigoProducto:
                        consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
                    else:
                        consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigoProducto)
                    for datoProducto in consultaProducto:
                        nombreProducto = datoProducto.nombre_producto
                    miniProductos.append([codigoProducto,nombreProducto,strCantidadProducto])
        
            
            miniSC = []
            if haySC:
                for idSC, cantidadSC in listaServiciosCorporales:
                    idServicio = int(idSC)
                    strCantidadServicio = str(cantidadSC)
                    consultarServicio = Servicios.objects.filter(id_servicio = idServicio)
                    for datoServicio in consultarServicio:
                        nombreServicio = datoServicio.nombre_servicio
                    miniSC.append([idServicio,nombreServicio,strCantidadServicio])
                
            miniSF = []
            if haySF:
                for idSF, cantidadSF in listaServiciosFaciales:
                    idServicio = int(idSF)
                    strCantidadServicio = str(cantidadSF)
                    consultarServicio = Servicios.objects.filter(id_servicio = idServicio)
                    for datoServicio in consultarServicio:
                        nombreServicio = datoServicio.nombre_servicio
                    miniSF.append([idServicio,nombreServicio,strCantidadServicio])
            
            
            
            productosFinalizados.append(miniProductos)
            serviciosCorporalesFinalizados.append(miniSC)
            serviciosFacialesFinalizados.append(miniSF)
            
        listaCreditosFinalizados = zip(totalCreditosFinalizados,clientesCreditosFinalizados,agregadosFinalizados,sucursalesCreditosFinalizados, fechasDePago, productosFinalizados, serviciosCorporalesFinalizados, serviciosFacialesFinalizados)
        
        #Balance de credito de costabella
        todasLasSucursales = Sucursales.objects.all()
        balanceSucursales = []
        montoPagadoTodasLasSucursales = 0
        montoPendienteTodasLasSucursales = 0
        montoTotalTodasLasSucursales = 0
        for sucursal in todasLasSucursales:
            idSucursal = sucursal.id_sucursal
            nombreSucursal = sucursal.nombre
            consultaCreditosDeSucursal = Creditos.objects.filter(sucursal_id__id_sucursal = idSucursal, estatus="Pendiente")
            montoPagado = 0
            montoPendiente = 0
            montoTotal = 0
            for credito in consultaCreditosDeSucursal:
                montoPagadoCredito = credito.monto_pagado
                montoPendienteCredito = credito.monto_restante
                montoTotalCredito = credito.monto_pagar

                montoPagado = montoPagado + montoPagadoCredito
                montoPendiente = montoPendiente + montoPendienteCredito
                montoTotal = montoTotal + montoTotalCredito
            
            #Agregar a array
            balanceSucursales.append([idSucursal, nombreSucursal,montoPagado, montoPendiente, montoTotal])

            montoPagadoTodasLasSucursales = montoPagadoTodasLasSucursales + montoPagado
            montoPendienteTodasLasSucursales = montoPendienteTodasLasSucursales + montoPendiente
            montoTotalTodasLasSucursales = montoTotalTodasLasSucursales + montoTotal




            
            
        if "pago1Agregado" in request.session:
            pago1Agregado = True
            mensaje = request.session['pago1Agregado']
            del request.session['pago1Agregado']
            return render(request, "14 Creditos/verCreditosClientes.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaCreditosPendientes":listaCreditosPendientes,
                                                                        "listaCreditosFinalizados":listaCreditosFinalizados, "pago1Agregado":pago1Agregado, "mensaje":mensaje, "contadorPendientes":contadorPendientes, "contadorFinalizado":contadorFinalizado, "notificacionCita":notificacionCita,
                                                                        "balanceSucursales":balanceSucursales, "montoPagadoTodasLasSucursales":montoPagadoTodasLasSucursales, "montoPendienteTodasLasSucursales":montoPendienteTodasLasSucursales, "montoTotalTodasLasSucursales":montoTotalTodasLasSucursales
            })
        
        if "pago1NoAgregado" in request.session:
            pago1NoAgregado = True
            mensaje = request.session['pago1Agregado']
            del request.session['pago1Agregado']
            return render(request, "14 Creditos/verCreditosClientes.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaCreditosPendientes":listaCreditosPendientes,
                                                                        "listaCreditosFinalizados":listaCreditosFinalizados, "pago1NoAgregado":pago1NoAgregado, "mensaje":mensaje, "contadorPendientes":contadorPendientes, "contadorFinalizado":contadorFinalizado, "notificacionCita":notificacionCita,
                                                                        "balanceSucursales":balanceSucursales, "montoPagadoTodasLasSucursales":montoPagadoTodasLasSucursales, "montoPendienteTodasLasSucursales":montoPendienteTodasLasSucursales, "montoTotalTodasLasSucursales":montoTotalTodasLasSucursales
            })
            
        if "pago2Agregado" in request.session:
            pago2Agregado = True
            mensaje = request.session['pago2Agregado']
            del request.session['pago2Agregado']
            return render(request, "14 Creditos/verCreditosClientes.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaCreditosPendientes":listaCreditosPendientes,
                                                                        "listaCreditosFinalizados":listaCreditosFinalizados, "pago2Agregado":pago2Agregado, "mensaje":mensaje, "contadorPendientes":contadorPendientes, "contadorFinalizado":contadorFinalizado, "notificacionCita":notificacionCita,
                                                                        "balanceSucursales":balanceSucursales, "montoPagadoTodasLasSucursales":montoPagadoTodasLasSucursales, "montoPendienteTodasLasSucursales":montoPendienteTodasLasSucursales, "montoTotalTodasLasSucursales":montoTotalTodasLasSucursales
            })
        
        if "pago2NoAgregado" in request.session:
            pago2NoAgregado = True
            mensaje = request.session['pago2NoAgregado']
            del request.session['pago2NoAgregado']
            return render(request, "14 Creditos/verCreditosClientes.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaCreditosPendientes":listaCreditosPendientes,
                                                                        "listaCreditosFinalizados":listaCreditosFinalizados, "pago2NoAgregado":pago2NoAgregado, "mensaje":mensaje, "contadorPendientes":contadorPendientes, "contadorFinalizado":contadorFinalizado, "notificacionCita":notificacionCita,
                                                                        "balanceSucursales":balanceSucursales, "montoPagadoTodasLasSucursales":montoPagadoTodasLasSucursales, "montoPendienteTodasLasSucursales":montoPendienteTodasLasSucursales, "montoTotalTodasLasSucursales":montoTotalTodasLasSucursales
            })
            
        if "pago3Agregado" in request.session:
            pago3Agregado = True
            mensaje = request.session['pago3Agregado']
            del request.session['pago3Agregado']
            return render(request, "14 Creditos/verCreditosClientes.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaCreditosPendientes":listaCreditosPendientes,
                                                                        "listaCreditosFinalizados":listaCreditosFinalizados, "pago3Agregado":pago3Agregado, "mensaje":mensaje, "contadorPendientes":contadorPendientes, "contadorFinalizado":contadorFinalizado, "notificacionCita":notificacionCita,
                                                                        "balanceSucursales":balanceSucursales, "montoPagadoTodasLasSucursales":montoPagadoTodasLasSucursales, "montoPendienteTodasLasSucursales":montoPendienteTodasLasSucursales, "montoTotalTodasLasSucursales":montoTotalTodasLasSucursales
            })
        
        if "pago3NoAgregado" in request.session:
            pago3NoAgregado = True
            mensaje = request.session['pago3NoAgregado']
            del request.session['pago3NoAgregado']
            return render(request, "14 Creditos/verCreditosClientes.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaCreditosPendientes":listaCreditosPendientes,
                                                                        "listaCreditosFinalizados":listaCreditosFinalizados, "pago3NoAgregado":pago3NoAgregado, "mensaje":mensaje, "contadorPendientes":contadorPendientes, "contadorFinalizado":contadorFinalizado, "notificacionCita":notificacionCita,
                                                                        "balanceSucursales":balanceSucursales, "montoPagadoTodasLasSucursales":montoPagadoTodasLasSucursales, "montoPendienteTodasLasSucursales":montoPendienteTodasLasSucursales, "montoTotalTodasLasSucursales":montoTotalTodasLasSucursales
            })
            
        if "pago4Agregado" in request.session:
            pago4Agregado = True
            mensaje = request.session['pago4Agregado']
            del request.session['pago4Agregado']
            return render(request, "14 Creditos/verCreditosClientes.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaCreditosPendientes":listaCreditosPendientes,
                                                                        "listaCreditosFinalizados":listaCreditosFinalizados, "pago4Agregado":pago4Agregado, "mensaje":mensaje, "contadorPendientes":contadorPendientes, "contadorFinalizado":contadorFinalizado, "notificacionCita":notificacionCita,
                                                                        "balanceSucursales":balanceSucursales, "montoPagadoTodasLasSucursales":montoPagadoTodasLasSucursales, "montoPendienteTodasLasSucursales":montoPendienteTodasLasSucursales, "montoTotalTodasLasSucursales":montoTotalTodasLasSucursales
            })
        
        if "pago4NoAgregado" in request.session:
            pago4NoAgregado = True
            mensaje = request.session['pago4NoAgregado']
            del request.session['pago4NoAgregado']
            return render(request, "14 Creditos/verCreditosClientes.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaCreditosPendientes":listaCreditosPendientes,
                                                                        "listaCreditosFinalizados":listaCreditosFinalizados, "pago4NoAgregado":pago4NoAgregado, "mensaje":mensaje, "contadorPendientes":contadorPendientes, "contadorFinalizado":contadorFinalizado, "notificacionCita":notificacionCita,
                                                                        "balanceSucursales":balanceSucursales, "montoPagadoTodasLasSucursales":montoPagadoTodasLasSucursales, "montoPendienteTodasLasSucursales":montoPendienteTodasLasSucursales, "montoTotalTodasLasSucursales":montoTotalTodasLasSucursales
            })
            
        

        return render(request, "14 Creditos/verCreditosClientes.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaCreditosPendientes":listaCreditosPendientes,
                                                                        "listaCreditosFinalizados":listaCreditosFinalizados, "contadorPendientes":contadorPendientes, "contadorFinalizado":contadorFinalizado, "notificacionCita":notificacionCita,
                                                                        "balanceSucursales":balanceSucursales, "montoPagadoTodasLasSucursales":montoPagadoTodasLasSucursales, "montoPendienteTodasLasSucursales":montoPendienteTodasLasSucursales, "montoTotalTodasLasSucursales":montoTotalTodasLasSucursales
        })
        
        
        
    
    else:
        return render(request,"1 Login/login.html")
    
def activarConfiguracionCredito(request):

    if "idSesion" in request.session:

       if request.method == "POST":
            idConfiguracionCreditoAActivar = request.POST['idConfiguracionCredito']

            consultaConfiguracion = ConfiguracionCredito.objects.filter(id_configuracion_credito = idConfiguracionCreditoAActivar)


            for dato in consultaConfiguracion:
                idSucursal = dato.sucursal_id

                configuracionesSucursal = ConfiguracionCredito.objects.filter(sucursal_id__id_sucursal = idSucursal)

                configuracionActivaEnSucursal = False #Variable para saber si ya hay o si aun no hay una configuracion Activa..

                for configuracion in configuracionesSucursal:
                    if configuracion.activo == "S":
                        configuracionActivaEnSucursal = True

                if configuracionActivaEnSucursal == False: #Si no hay ninguna configuracion activa actualmente en esa sucursal..
                    actualizacionConfiguracionCredito = ConfiguracionCredito.objects.filter(id_configuracion_credito = idConfiguracionCreditoAActivar).update(activo = "S")
                elif configuracionActivaEnSucursal == True:
                    for config in configuracionesSucursal:
                        idConfig = config.id_configuracion_credito
                        ponerComoInactivoConfiguracion = ConfiguracionCredito.objects.filter(id_configuracion_credito = idConfig).update(activo = "N")
                    actualizacionConfiguracionCredito = ConfiguracionCredito.objects.filter(id_configuracion_credito = idConfiguracionCreditoAActivar).update(activo = "S")

            if actualizacionConfiguracionCredito:
                request.session['configuracionActivada'] = "La configuración de limite ha sido activada satisfactoriamente!"
                return redirect('/configuracionCredito/')
    else:
        return render(request,"1 Login/login.html")

def pagosCreditosClientes(request):

    if "idSesion" in request.session:

       # Variables de sesión
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']
        idPerfil = idEmpleado
        idConfig = idEmpleado
       

        
     
      
        clientesCreditos =[]
        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]
        
           #notificacionRentas
        notificacionRenta = notificacionRentas(request)

        #notificacionCitas
        notificacionCita = notificacionCitas(request)
        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)
        
        
        creditos =[]
        montosRestantes = []
        pagosQuincenales = []
        montosTotales = []
        sumasPagados = []
        
        totalYaPagado = []
        totalTotal = []
        
       
        
        totalCreditosPendientes= Creditos.objects.filter(estatus="Pendiente",concepto_credito ="Venta")
        contadorCreditosPendientes = 0
        for pendiente in totalCreditosPendientes:
            contadorCreditosPendientes = contadorCreditosPendientes +1
            idCreditoPendiente = pendiente.id_credito
            
            montoPagado = pendiente.monto_pagado
            montoTotal = pendiente.monto_pagar
         
            id_cliente =pendiente.cliente_id
            
            monto_pagar_total = pendiente.monto_pagar
       
                
            clientes = Clientes.objects.filter(id_cliente = id_cliente)
            for cliente in clientes:
                idCliente = cliente.id_cliente
                nombreCliente = cliente.nombre_cliente
                apellidoP = cliente.apellidoPaterno_cliente
                apellidoM = cliente.apellidoPaterno_cliente
            clienteCompleto= str(idCliente) + " - " + nombreCliente + " " + apellidoP + " " + apellidoM
            clientesCreditos.append(clienteCompleto)
            
            pagosCreditos = PagosCreditos.objects.filter(id_credito_id__id_credito = idCreditoPendiente)
            for x in pagosCreditos:
                idPago = x.id_historialCredito                           #0
                idC = x.id_credito_id                                    
                fechaPago1 = x.fecha_pago1
                tipoPago1 = x.tipo_pago1
                tipoTarjetaPago1 =x.tipo_tarjeta1
                referenciaPago1 =x.referencia_pago_tarjeta1
                clavePago1 =x.clave_rastreo_pago_transferencia1
                montoPago1 = x.monto_pago1
                
                fechaPago2 = x.fecha_pago2
                tipoPago2 = x.tipo_pago2
                tipoTarjetaPago2 =x.tipo_tarjeta2
                referenciaPago2 =x.referencia_pago_tarjeta2
                clavePago2 =x.clave_rastreo_pago_transferencia2
                montoPago2 = x.monto_pago2
                
                fechaPago3 = x.fecha_pago3
                tipoPago3 = x.tipo_pago3
                tipoTarjetaPago3 =x.tipo_tarjeta3
                referenciaPago3 =x.referencia_pago_tarjeta3
                clavePago3 =x.clave_rastreo_pago_transferencia3
                montoPago3 = x.monto_pago3
                
                fechaPago4 = x.fecha_pago4
                tipoPago4 = x.tipo_pago4
                tipoTarjetaPago4 =x.tipo_tarjeta4
                referenciaPago4 =x.referencia_pago_tarjeta4
                clavePago4 =x.clave_rastreo_pago_transferencia4
                montoPago4 = x.monto_pago4
                
                if montoPago1 == None and montoPago2 == None and montoPago3 == None and montoPago4 == None:
                    sumaPagados = 0
                    restante = monto_pagar_total
                    
                
                elif montoPago1 and montoPago2 == None and montoPago3 == None and montoPago4 == None:
                    sumaPagados = montoPago1
                    restante = monto_pagar_total - montoPago1
                    
                    
                elif montoPago1 and montoPago2  and montoPago3 == None and montoPago4 == None:
                    sumaPagados = montoPago1 + montoPago2
                    restante = monto_pagar_total - sumaPagados
                elif montoPago1 and montoPago2  and montoPago3  and montoPago4 == None:
                    sumaPagados = montoPago1 + montoPago2 + montoPago3
                    restante = monto_pagar_total - sumaPagados
                elif montoPago1 and montoPago2  and montoPago3  and montoPago4:
                    sumaPagados = montoPago1 + montoPago2 + montoPago3 + montoPago4
                    restante = monto_pagar_total - sumaPagados
                    
                #los pagos son a 4 quincenas
                pago_por_quincena = monto_pagar_total / 4
                
                    
            sumasPagados.append(sumaPagados)
            montosTotales.append(monto_pagar_total)
            pagosQuincenales.append(pago_por_quincena)
            montosRestantes.append(restante)
            totalYaPagado.append(montoPagado)
            totalTotal.append(montoTotal)
            creditos.append([idPago,idC,fechaPago1,tipoPago1,tipoTarjetaPago1,referenciaPago1,clavePago1,montoPago1,fechaPago2,tipoPago2,tipoTarjetaPago2,referenciaPago2,clavePago2,montoPago2,
                             fechaPago3,tipoPago3,tipoTarjetaPago3, referenciaPago3,clavePago3,montoPago3,fechaPago4,tipoPago4,tipoTarjetaPago4,referenciaPago4,clavePago4,montoPago4])
            
        
            
            
            
            
            
        listaCreditosPago1 = zip(creditos,clientesCreditos, pagosQuincenales,montosRestantes,montosTotales,sumasPagados, totalYaPagado,totalTotal)
        
        listaCreditosPago1Modal = zip(creditos,clientesCreditos, pagosQuincenales,montosRestantes,montosTotales,sumasPagados, totalYaPagado,totalTotal)
        listaCreditosPago2Modal = zip(creditos,clientesCreditos,pagosQuincenales, montosRestantes,montosTotales,sumasPagados,totalYaPagado,totalTotal)
        listaCreditosPago3Modal = zip(creditos,clientesCreditos,pagosQuincenales, montosRestantes,montosTotales,sumasPagados,totalYaPagado,totalTotal)
        listaCreditosPago4Modal = zip(creditos,clientesCreditos,pagosQuincenales, montosRestantes,montosTotales,sumasPagados,totalYaPagado,totalTotal)
        
        
        listaCreditosPago1JS = zip(creditos,clientesCreditos,pagosQuincenales, montosRestantes,montosTotales,sumasPagados)
        listaCreditosPago2JS = zip(creditos,clientesCreditos,pagosQuincenales, montosRestantes,montosTotales,sumasPagados)
        listaCreditosPago3JS = zip(creditos,clientesCreditos,pagosQuincenales, montosRestantes,montosTotales,sumasPagados)
        listaCreditosPago4JS = zip(creditos,clientesCreditos,pagosQuincenales, montosRestantes,montosTotales,sumasPagados)
        
      
        
        
            
            
            
        
            
        return render(request, "14 Creditos/pagosCreditos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaCreditosPago1":listaCreditosPago1,
                                                                        "creditos":creditos,"listaCreditosPago1Modal":listaCreditosPago1Modal,"listaCreditosPago2Modal":listaCreditosPago2Modal,
                                                                        "listaCreditosPago3Modal":listaCreditosPago3Modal,"listaCreditosPago4Modal":listaCreditosPago4Modal,"listaCreditosPago1JS":listaCreditosPago1JS,
                                                                        "listaCreditosPago2JS":listaCreditosPago2JS,"listaCreditosPago3JS":listaCreditosPago3JS,"listaCreditosPago4JS":listaCreditosPago4JS, "contadorCreditosPendientes":contadorCreditosPendientes, "notificacionCita":notificacionCita
                                                                        
        })
    
    else:
        return render(request,"1 Login/login.html")   


def guardarPago1(request):
    if "idSesion" in request.session:
        # Variables de sesión
        idEmpleado = request.session['idSesion']
        if request.method == "POST":
            
            

            idCreditoAPagar = request.POST['idCredito']
            idPagoCredito = request.POST['idPagoCredito']
            cantidadPago1 = request.POST['cantidadPago1']

            fechaPago1 = datetime.now()
            horaVenta= datetime.now().time()
             
            formaPago = request.POST['tipoPago'] #Efectivo,  tarjeta o transferencia
            
            datosCredito = Creditos.objects.filter(id_credito = idCreditoAPagar)
            for dato in datosCredito:
                montoTotalCredito = dato.monto_pagar
                montoPagado = dato.monto_pagado
                sucursal = dato.sucursal_id
                montoRestante = dato.monto_restante
                idVentaCredito = dato.venta_id
                
                
           
            floatCantidadPago1 = float(cantidadPago1)
            floatRestante = float(montoRestante)
                
                
           
                
            if floatCantidadPago1 == floatRestante:
                restante = 0
                estado = "Finalizado"
           
                
            
            else:
                restante = montoTotalCredito - float(cantidadPago1)
                estado = "Pendiente"
                
                   
                 
                    
            esConEfectivo = False
            esConTarjeta = False
            esConTransferencia = False

            if formaPago == "Efectivo":
                esConEfectivo = True
            elif formaPago == "Tarjeta":
                esConTarjeta = True
                tipo_tarjeta = request.POST['tipoTarjeta']    
                referencia_tarjeta = request.POST['referenciaTarjeta'] 
                        
            elif formaPago == "Transferencia":
                esConTransferencia = True
                clave_transferencia = request.POST['claveRastreoTransferencia'] 

                    


            if esConEfectivo:
                        
                registrarPago1 = PagosCreditos.objects.filter(id_historialCredito = idPagoCredito).update(fecha_pago1 = fechaPago1,tipo_pago1 ="Efectivo",monto_pago1 =cantidadPago1) 
                
                if registrarPago1:
                    
                    
                    actualizarEstadoCredito = Creditos.objects.filter(id_credito = idCreditoAPagar).update(monto_pagado = cantidadPago1,monto_restante =restante,estatus =estado) 
                    if actualizarEstadoCredito:
                         
                        tipoMovimiento ="IN"
                        montoMovimiento = float(cantidadPago1)
                        descripcionMovimiento ="Movimiento por abono de crédito " + str(idCreditoAPagar) 
                        fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                        horaMovimiento = datetime.now().time()
                        ingresarCantidadEfectivoAcaja =MovimientosCaja(fecha =fechaMovimiento,hora = horaMovimiento,tipo=tipoMovimiento,monto =montoMovimiento, descripcion=descripcionMovimiento,sucursal =  Sucursales.objects.get(id_sucursal = sucursal),
                                                                            realizado_por = Empleados.objects.get(id_empleado = idEmpleado))
                        ingresarCantidadEfectivoAcaja.save()

                        #IMPRESION DE TICKEEETSSSS

                        #Fecha
                        hoy = datetime.now()
                        hoyFormato = hoy.strftime('%Y/%m/%d')

                        #Consulta de venta
                        consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                        for datoVenta in consultaVenta:
                            empleadoVendedor = datoVenta.empleado_vendedor_id
                            sucursal = datoVenta.sucursal_id
                            cliente = datoVenta.cliente_id
                        #Empleado vendedor
                        consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                        for datoVendedor in consultaEmpleadoVendedor:
                            nombreEmpleado = datoVendedor.nombres
                            apellidoPatEmpleado = datoVendedor.apellido_paterno

                        nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                        #Datos sucurssal
                        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                        for datoSucursal in consultaSucursal:
                            nombreSucursal = datoSucursal.nombre
                            telefonoSucursal = datoSucursal.telefono
                            direccionSucursal = datoSucursal.direccion

                        
                        
                        
                        #Hora bien
                        horaVenta = horaVenta.strftime("%H:%M:%S")

                        # Esto es para obtener las impresoras. No es obligatorio hacerlo siempre que se quiera imprimir
                        impresoras = Conector.ConectorV3.obtenerImpresoras()
                        print(f"Las impresoras son: {impresoras}")
                        
                        contadorTickets = 0
                        for x in range(2):
                            contadorTickets = contadorTickets + 1

                            
                            c = Conector.ConectorV3()
                            c.Iniciar()
                            c.Corte(1)
                            
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            # Recuerda que la imagen debe existir y debe ser legible para el plugin. Si no, comenta las líneas
                            c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EstablecerEnfatizado(True)
                            c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("TEL: "+telefonoSucursal+"\n")
                            c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")

                            c.EstablecerEnfatizado(True)
                            c.EscribirTexto("================================================\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EscribirTexto("PAGO DE VENTA #"+str(idVentaCredito)+"\n")
                            c.EscribirTexto("CRÉDITO #"+str(idCreditoAPagar)+"\n")
                            c.EstablecerEnfatizado(False)
                            c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("\n")
                            c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                            c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                            c.EscribirTexto("\n")

                            #Listado de productos 
                            #Productos vendidos en ese credito

                            consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                            for datoVenta in consultaVenta:
                                codigosProductosVenta = datoVenta.ids_productos
                                cantidadesProductosVenta = datoVenta.cantidades_productos
                                idsServiciosCorporales = datoVenta.ids_servicios_corporales
                                cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                                idsServiciosFaciales = datoVenta.ids_servicios_faciales
                                cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                                descuento = datoVenta.descuento
                                costoTotalAPagar = datoVenta.monto_pagar
                                cliente = datoVenta.cliente_id

                            if cliente == None:
                                nombreClienteTicket = "Momentaneo"
                                idCienteTicket="Sin id"
                            else:
                                consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                                for datoCliente in consultaCliente:
                                    idCienteTicket = datoCliente.id_cliente
                                    nombreCliente = datoCliente.nombre_cliente
                                    apellidoCliente = datoCliente.apellidoPaterno_cliente
                                nombreClienteTicket = nombreCliente + " "+apellidoCliente
                                
                                

                            listaCodigosProductos = codigosProductosVenta.split(",")
                            listaCantidadesProductos = cantidadesProductosVenta.split(",")
                            listaIdsServiciosCorporales = idsServiciosCorporales.split(",")
                            listaCantidadesServiciosCorporales = cantidadServiciosCorporales.split(",")
                            listaIdsServiciosFaciales = idsServiciosFaciales.split(",")
                            listaCantidadesServiciosFaciales = cantidadServiciosFaciales.split(",")
                            
                            longitudProductos = len(listaCodigosProductos)
                            longitudServiciosCorporales = len(listaIdsServiciosCorporales)
                            longitudServiciosFaciales = len(listaIdsServiciosFaciales)


                            listaProductos = zip(listaCodigosProductos,listaCantidadesProductos)
                            listaServiciosCorporales = zip(listaIdsServiciosCorporales, listaCantidadesServiciosCorporales)
                            listaServiciosFaciales = zip(listaIdsServiciosFaciales, listaCantidadesServiciosFaciales)

                            if longitudProductos >= 1:
                                for codigo, cantidad in listaProductos:
                                    if codigo != "":
                                        strCodigo = str(codigo)
                                        strCantidad = str(cantidad)
                                        consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                                        for datoProductoVenta in consultaProductoVenta:
                                            nombreProducto = datoProductoVenta.nombre_producto
                                            costoIndividualProducto = datoProductoVenta.costo_venta

                                        floatCantidad = float(cantidad)
                                        costototalProducto = costoIndividualProducto * floatCantidad
                                        costototalProductoDosDecimales = round(costototalProducto, 2)
                                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                        longitudCostoTotal = int(longitudCostoTotal)

                                        
                                        caracteresProducto = len(nombreProducto)

                                        if longitudCostoTotal == 2:
                                            espacio = 38
                                        if longitudCostoTotal == 2:
                                            espacio = 37
                                        elif longitudCostoTotal == 3:
                                            espacio = 36
                                        elif longitudCostoTotal == 4:
                                            espacio = 35
                                        elif longitudCostoTotal == 5:
                                            espacio = 34
                                        elif longitudCostoTotal == 6:
                                            espacio = 33
                                        numeroEspacios = espacio - int(caracteresProducto)
                                        
                                        espaciosTicket = ""
                                        for x in range(numeroEspacios):
                                            espacioMini = " "
                                            espaciosTicket = espaciosTicket + espacioMini
                                        c.EscribirTexto(strCantidad+" x "+nombreProducto+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                            
                            if longitudServiciosCorporales >=1:
                                for idd, cantidad in listaServiciosCorporales:
                                    if idd != "":
                                        idServicio = int(idd)
                                        strCantidad = str(cantidad)
                                        consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                        for datoServicio in consultaServicio:
                                            nombreServicio = datoServicio.nombre_servicio
                                            costoServicio = datoServicio.precio_venta

                                        floatCantidad = float(cantidad)
                                        costototalProducto = costoServicio * floatCantidad
                                        costototalProductoDosDecimales = round(costototalProducto, 2)
                                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                        longitudCostoTotal = int(longitudCostoTotal)

                                        
                                        caracteresProducto = len(nombreServicio)

                                        if longitudCostoTotal == 2:
                                            espacio = 38
                                        if longitudCostoTotal == 2:
                                            espacio = 37
                                        elif longitudCostoTotal == 3:
                                            espacio = 36
                                        elif longitudCostoTotal == 4:
                                            espacio = 35
                                        elif longitudCostoTotal == 5:
                                            espacio = 34
                                        elif longitudCostoTotal == 6:
                                            espacio = 33
                                        numeroEspacios = espacio - int(caracteresProducto)
                                        
                                        espaciosTicket = ""
                                        for x in range(numeroEspacios):
                                            espacioMini = " "
                                            espaciosTicket = espaciosTicket + espacioMini
                                        c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")

                            if longitudServiciosFaciales >=1:
                                for idd, cantidad in listaServiciosFaciales:
                                    if idd != "":
                                        idServicio = int(idd)
                                        strCantidad = str(cantidad)
                                        consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                        for datoServicio in consultaServicio:
                                            nombreServicio = datoServicio.nombre_servicio
                                            costoServicio = datoServicio.precio_venta

                                        floatCantidad = float(cantidad)
                                        costototalProducto = costoServicio * floatCantidad
                                        costototalProductoDosDecimales = round(costototalProducto, 2)
                                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                        longitudCostoTotal = int(longitudCostoTotal)

                                        
                                        caracteresProducto = len(nombreServicio)

                                        if longitudCostoTotal == 2:
                                            espacio = 38
                                        if longitudCostoTotal == 2:
                                            espacio = 37
                                        elif longitudCostoTotal == 3:
                                            espacio = 36
                                        elif longitudCostoTotal == 4:
                                            espacio = 35
                                        elif longitudCostoTotal == 5:
                                            espacio = 34
                                        elif longitudCostoTotal == 6:
                                            espacio = 33
                                        numeroEspacios = espacio - int(caracteresProducto)
                                        
                                        espaciosTicket = ""
                                        for x in range(numeroEspacios):
                                            espacioMini = " "
                                            espaciosTicket = espaciosTicket + espacioMini
                                        c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                            
                            

                            c.EscribirTexto("\n")
                            c.EscribirTexto("\n")

                            if descuento == None:
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                                costoTotalPagarCredito = costoTotalAPagar
                                c.EscribirTexto("ABONADO: $"+str(cantidadPago1)+"\n")
                                c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                            else:
                                intDescuento = int(descuento)
                                consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                                for datoDescuento in consultaDescuentos:
                                    nombreDescuento = datoDescuento.nombre_descuento
                                    porcentajeDescuento = datoDescuento.porcentaje

                                porcentajePagado = 100 - porcentajeDescuento #85
                                totalSinDescuento1 = 100 * costoTotalAPagar
                                totalSinDescuento2 = totalSinDescuento1/porcentajePagado
                                totalSinDescuento2 = round(totalSinDescuento2)

                                primerMulti = porcentajeDescuento * float(totalSinDescuento2)
                                primerDivision = primerMulti/100
                                resultadoDescuento = round(primerDivision)
                                
                                costoTotalAPagarConDescuento = totalSinDescuento2 - resultadoDescuento

                                c.EstablecerTamañoFuente(1, 1)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("Subtotal:  $"+str(totalSinDescuento2)+"\n")
                                c.EscribirTexto("Descuento:  $"+str(resultadoDescuento)+"\n")
                                c.EstablecerTamañoFuente(2, 2)
                                c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConDescuento)+"\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("Descuento aplicado: -"+str(porcentajeDescuento)+"%- "+str(nombreDescuento)+"\n")
                                c.EscribirTexto("ABONADO: $"+str(cantidadPago1)+"\n")
                                c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                                costoTotalPagarCredito = costoTotalAPagarConDescuento

                            c.EscribirTexto("\n")
                            c.EstablecerEnfatizado(True)
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                            c.EscribirTexto("\n")
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("\n")
                            c.EstablecerEnfatizado(True)
                            c.EscribirTexto("Pago en efectivo.\n")
                            c.EscribirTexto("Pago a crédito 4 quincenas.\n")
                            c.EscribirTexto("Primer pago recibido.\n")
                            c.EstablecerEnfatizado(False)
                            if restante == 0:
                                c.EscribirTexto("PAGO LIQUIDADO\n")
                            else:
                                restantePorPagar = float(restante)/3
                                restantePorPagar = round(restantePorPagar,2)
                                c.EscribirTexto("Abonos restantes de: $"+str(restantePorPagar)+" MXN.\n")
                                ahora = datetime.now()
                                fechaSegundoPago = ahora + timedelta(days=15)
                                fechaSegundoPago = fechaSegundoPago.strftime('%Y-%m-%d')
                                c.EscribirTexto("Segundo pago el día: "+str(fechaSegundoPago)+".\n")
                            
                        
                            c.EscribirTexto("\n")
                            c.EstablecerEnfatizado(True)
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                            if nombreClienteTicket == "Momentaneo":
                                c.EstablecerEnfatizado(False)
                                c.EscribirTexto("Cliente momentaneo.\n")
                            else:
                                c.EstablecerEnfatizado(False)
                                c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                            c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerEnfatizado(True)
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            if contadorTickets == 1:
                                c.EscribirTexto("\n")
                                c.EscribirTexto("COPIA TIENDA.\n")
                                c.EscribirTexto("\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("________________________________________________\n")
                                c.EscribirTexto("Firma de cliente.\n")
                            else:
                                c.EscribirTexto("\n")
                                c.EscribirTexto("COPIA CLIENTE.\n")
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            

                            c.Feed(1)
                            c.Corte(1)
                            #c.abrirCajon()
                            c.Pulso(48, 60, 120)
                            print("Imprimiendo...")
                            # Recuerda cambiar por el nombre de tu impresora
                            respuesta = c.imprimirEn("POS80 Printer")
                            if respuesta == True:
                                print("Impresión correcta")
                            else:
                                print(f"Error. El mensaje es: {respuesta}")

                

            if esConTarjeta:
                    
                        
                registrarPago1 = PagosCreditos.objects.filter(id_historialCredito = idPagoCredito).update(fecha_pago1 = fechaPago1,tipo_pago1 ="Tarjeta",tipo_tarjeta1=tipo_tarjeta,referencia_pago_tarjeta1=referencia_tarjeta,monto_pago1 =cantidadPago1) 
                
                if registrarPago1:
                    
                    
                    actualizarEstadoCredito = Creditos.objects.filter(id_credito = idCreditoAPagar).update(monto_pagado = cantidadPago1,monto_restante =restante,estatus =estado) 

                    #IMPRESION DE TICKEEETSSSS

                    #Fecha
                    hoy = datetime.now()
                    hoyFormato = hoy.strftime('%Y/%m/%d')

                    #Consulta de venta
                    consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                    for datoVenta in consultaVenta:
                        empleadoVendedor = datoVenta.empleado_vendedor_id
                        sucursal = datoVenta.sucursal_id
                        cliente = datoVenta.cliente_id
                    #Empleado vendedor
                    consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                    for datoVendedor in consultaEmpleadoVendedor:
                        nombreEmpleado = datoVendedor.nombres
                        apellidoPatEmpleado = datoVendedor.apellido_paterno

                    nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                    #Datos sucurssal
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        telefonoSucursal = datoSucursal.telefono
                        direccionSucursal = datoSucursal.direccion

                    
                    
                    
                    #Hora bien
                    horaVenta = horaVenta.strftime("%H:%M:%S")

                    # Esto es para obtener las impresoras. No es obligatorio hacerlo siempre que se quiera imprimir
                    impresoras = Conector.ConectorV3.obtenerImpresoras()
                    print(f"Las impresoras son: {impresoras}")
                    
                    contadorTickets = 0
                    for x in range(2):
                        contadorTickets = contadorTickets + 1

                        
                        c = Conector.ConectorV3()
                        c.Iniciar()
                        c.Corte(1)
                        
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        # Recuerda que la imagen debe existir y debe ser legible para el plugin. Si no, comenta las líneas
                        c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("TEL: "+telefonoSucursal+"\n")
                        c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")

                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("================================================\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EscribirTexto("PAGO DE VENTA #"+str(idVentaCredito)+"\n")
                        c.EscribirTexto("CRÉDITO #"+str(idCreditoAPagar)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        #Productos vendidos en ese credito

                        consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                        for datoVenta in consultaVenta:
                            codigosProductosVenta = datoVenta.ids_productos
                            cantidadesProductosVenta = datoVenta.cantidades_productos
                            idsServiciosCorporales = datoVenta.ids_servicios_corporales
                            cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                            idsServiciosFaciales = datoVenta.ids_servicios_faciales
                            cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                            descuento = datoVenta.descuento
                            costoTotalAPagar = datoVenta.monto_pagar
                            cliente = datoVenta.cliente_id

                        if cliente == None:
                            nombreClienteTicket = "Momentaneo"
                            idCienteTicket="Sin id"
                        else:
                            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                            for datoCliente in consultaCliente:
                                idCienteTicket = datoCliente.id_cliente
                                nombreCliente = datoCliente.nombre_cliente
                                apellidoCliente = datoCliente.apellidoPaterno_cliente
                            nombreClienteTicket = nombreCliente + " "+apellidoCliente
                            
                            

                        listaCodigosProductos = codigosProductosVenta.split(",")
                        listaCantidadesProductos = cantidadesProductosVenta.split(",")
                        listaIdsServiciosCorporales = idsServiciosCorporales.split(",")
                        listaCantidadesServiciosCorporales = cantidadServiciosCorporales.split(",")
                        listaIdsServiciosFaciales = idsServiciosFaciales.split(",")
                        listaCantidadesServiciosFaciales = cantidadServiciosFaciales.split(",")
                        
                        longitudProductos = len(listaCodigosProductos)
                        longitudServiciosCorporales = len(listaIdsServiciosCorporales)
                        longitudServiciosFaciales = len(listaIdsServiciosFaciales)


                        listaProductos = zip(listaCodigosProductos,listaCantidadesProductos)
                        listaServiciosCorporales = zip(listaIdsServiciosCorporales, listaCantidadesServiciosCorporales)
                        listaServiciosFaciales = zip(listaIdsServiciosFaciales, listaCantidadesServiciosFaciales)

                        if longitudProductos >= 1:
                            for codigo, cantidad in listaProductos:
                                if codigo != "":
                                    strCodigo = str(codigo)
                                    strCantidad = str(cantidad)
                                    consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                                    for datoProductoVenta in consultaProductoVenta:
                                        nombreProducto = datoProductoVenta.nombre_producto
                                        costoIndividualProducto = datoProductoVenta.costo_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoIndividualProducto * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreProducto)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreProducto+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        if longitudServiciosCorporales >=1:
                            for idd, cantidad in listaServiciosCorporales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")

                        if longitudServiciosFaciales >=1:
                            for idd, cantidad in listaServiciosFaciales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        

                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")

                        if descuento == None:
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                            costoTotalPagarCredito = costoTotalAPagar
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago1)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                        else:
                            intDescuento = int(descuento)
                            consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                            for datoDescuento in consultaDescuentos:
                                nombreDescuento = datoDescuento.nombre_descuento
                                porcentajeDescuento = datoDescuento.porcentaje

                            porcentajePagado = 100 - porcentajeDescuento #85
                            totalSinDescuento1 = 100 * costoTotalAPagar
                            totalSinDescuento2 = totalSinDescuento1/porcentajePagado
                            totalSinDescuento2 = round(totalSinDescuento2)

                            primerMulti = porcentajeDescuento * float(totalSinDescuento2)
                            primerDivision = primerMulti/100
                            resultadoDescuento = round(primerDivision)
                            
                            costoTotalAPagarConDescuento = totalSinDescuento2 - resultadoDescuento

                            c.EstablecerTamañoFuente(1, 1)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("Subtotal:  $"+str(totalSinDescuento2)+"\n")
                            c.EscribirTexto("Descuento:  $"+str(resultadoDescuento)+"\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConDescuento)+"\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("Descuento aplicado: -"+str(porcentajeDescuento)+"%- "+str(nombreDescuento)+"\n")
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago1)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                            costoTotalPagarCredito = costoTotalAPagarConDescuento

                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                        c.EscribirTexto("\n")
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Pago en con tarjeta.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("Pago con "+str(tipo_tarjeta)+".\n")
                        c.EscribirTexto("Referencia: "+referencia_tarjeta+".\n")
                        c.EscribirTexto("\n")
                        c.EscribirTexto("Pago a crédito 4 quincenas.\n")
                        c.EscribirTexto("Primer pago recibido.\n")
                        c.EstablecerEnfatizado(False)
                        if restante == 0:
                            c.EscribirTexto("PAGO LIQUIDADO\n")
                        else:
                            restantePorPagar = float(restante)/3
                            restantePorPagar = round(restantePorPagar,2)
                            c.EscribirTexto("Abonos restantes de: $"+str(restantePorPagar)+" MXN.\n")
                            ahora = datetime.now()
                            fechaSegundoPago = ahora + timedelta(days=15)
                            fechaSegundoPago = fechaSegundoPago.strftime('%Y-%m-%d')
                            c.EscribirTexto("Segundo pago el día: "+str(fechaSegundoPago)+".\n")
                        
                    
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                        if nombreClienteTicket == "Momentaneo":
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("Cliente momentaneo.\n")
                        else:
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                        c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        if contadorTickets == 1:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA TIENDA.\n")
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("________________________________________________\n")
                            c.EscribirTexto("Firma de cliente.\n")
                        else:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA CLIENTE.\n")
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        

                        c.Feed(1)
                        c.Corte(1)
                        #c.abrirCajon()
                        c.Pulso(48, 60, 120)
                        print("Imprimiendo...")
                        # Recuerda cambiar por el nombre de tu impresora
                        respuesta = c.imprimirEn("POS80 Printer")
                        if respuesta == True:
                            print("Impresión correcta")
                        else:
                            print(f"Error. El mensaje es: {respuesta}")
                    

            if esConTransferencia:
            
                registrarPago1 = PagosCreditos.objects.filter(id_historialCredito = idPagoCredito).update(fecha_pago1 = fechaPago1,tipo_pago1 ="Transferencia",clave_rastreo_pago_transferencia1=clave_transferencia,monto_pago1 =cantidadPago1) 
                
                if registrarPago1:
                    
                    
                    actualizarEstadoCredito = Creditos.objects.filter(id_credito = idCreditoAPagar).update(monto_pagado = cantidadPago1,monto_restante =restante,estatus =estado) 
                    
                    #IMPRESION DE TICKEEETSSSS

                    #Fecha
                    hoy = datetime.now()
                    hoyFormato = hoy.strftime('%Y/%m/%d')

                    #Consulta de venta
                    consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                    for datoVenta in consultaVenta:
                        empleadoVendedor = datoVenta.empleado_vendedor_id
                        sucursal = datoVenta.sucursal_id
                        cliente = datoVenta.cliente_id
                    #Empleado vendedor
                    consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                    for datoVendedor in consultaEmpleadoVendedor:
                        nombreEmpleado = datoVendedor.nombres
                        apellidoPatEmpleado = datoVendedor.apellido_paterno

                    nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                    #Datos sucurssal
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        telefonoSucursal = datoSucursal.telefono
                        direccionSucursal = datoSucursal.direccion

                    
                    
                    
                    #Hora bien
                    horaVenta = horaVenta.strftime("%H:%M:%S")

                    # Esto es para obtener las impresoras. No es obligatorio hacerlo siempre que se quiera imprimir
                    impresoras = Conector.ConectorV3.obtenerImpresoras()
                    print(f"Las impresoras son: {impresoras}")
                    
                    contadorTickets = 0
                    for x in range(2):
                        contadorTickets = contadorTickets + 1

                        
                        c = Conector.ConectorV3()
                        c.Iniciar()
                        c.Corte(1)
                        
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        # Recuerda que la imagen debe existir y debe ser legible para el plugin. Si no, comenta las líneas
                        c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("TEL: "+telefonoSucursal+"\n")
                        c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")

                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("================================================\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EscribirTexto("PAGO DE VENTA #"+str(idVentaCredito)+"\n")
                        c.EscribirTexto("CRÉDITO #"+str(idCreditoAPagar)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        #Productos vendidos en ese credito

                        consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                        for datoVenta in consultaVenta:
                            codigosProductosVenta = datoVenta.ids_productos
                            cantidadesProductosVenta = datoVenta.cantidades_productos
                            idsServiciosCorporales = datoVenta.ids_servicios_corporales
                            cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                            idsServiciosFaciales = datoVenta.ids_servicios_faciales
                            cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                            descuento = datoVenta.descuento
                            costoTotalAPagar = datoVenta.monto_pagar
                            cliente = datoVenta.cliente_id

                        if cliente == None:
                            nombreClienteTicket = "Momentaneo"
                            idCienteTicket="Sin id"
                        else:
                            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                            for datoCliente in consultaCliente:
                                idCienteTicket = datoCliente.id_cliente
                                nombreCliente = datoCliente.nombre_cliente
                                apellidoCliente = datoCliente.apellidoPaterno_cliente
                            nombreClienteTicket = nombreCliente + " "+apellidoCliente
                            
                            

                        listaCodigosProductos = codigosProductosVenta.split(",")
                        listaCantidadesProductos = cantidadesProductosVenta.split(",")
                        listaIdsServiciosCorporales = idsServiciosCorporales.split(",")
                        listaCantidadesServiciosCorporales = cantidadServiciosCorporales.split(",")
                        listaIdsServiciosFaciales = idsServiciosFaciales.split(",")
                        listaCantidadesServiciosFaciales = cantidadServiciosFaciales.split(",")
                        
                        longitudProductos = len(listaCodigosProductos)
                        longitudServiciosCorporales = len(listaIdsServiciosCorporales)
                        longitudServiciosFaciales = len(listaIdsServiciosFaciales)


                        listaProductos = zip(listaCodigosProductos,listaCantidadesProductos)
                        listaServiciosCorporales = zip(listaIdsServiciosCorporales, listaCantidadesServiciosCorporales)
                        listaServiciosFaciales = zip(listaIdsServiciosFaciales, listaCantidadesServiciosFaciales)

                        if longitudProductos >= 1:
                            for codigo, cantidad in listaProductos:
                                if codigo != "":
                                    strCodigo = str(codigo)
                                    strCantidad = str(cantidad)
                                    consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                                    for datoProductoVenta in consultaProductoVenta:
                                        nombreProducto = datoProductoVenta.nombre_producto
                                        costoIndividualProducto = datoProductoVenta.costo_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoIndividualProducto * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreProducto)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreProducto+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        if longitudServiciosCorporales >=1:
                            for idd, cantidad in listaServiciosCorporales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")

                        if longitudServiciosFaciales >=1:
                            for idd, cantidad in listaServiciosFaciales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        

                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")

                        if descuento == None:
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                            costoTotalPagarCredito = costoTotalAPagar
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago1)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                        else:
                            intDescuento = int(descuento)
                            consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                            for datoDescuento in consultaDescuentos:
                                nombreDescuento = datoDescuento.nombre_descuento
                                porcentajeDescuento = datoDescuento.porcentaje

                            porcentajePagado = 100 - porcentajeDescuento #85
                            totalSinDescuento1 = 100 * costoTotalAPagar
                            totalSinDescuento2 = totalSinDescuento1/porcentajePagado
                            totalSinDescuento2 = round(totalSinDescuento2)

                            primerMulti = porcentajeDescuento * float(totalSinDescuento2)
                            primerDivision = primerMulti/100
                            resultadoDescuento = round(primerDivision)
                            
                            costoTotalAPagarConDescuento = totalSinDescuento2 - resultadoDescuento

                            c.EstablecerTamañoFuente(1, 1)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("Subtotal:  $"+str(totalSinDescuento2)+"\n")
                            c.EscribirTexto("Descuento:  $"+str(resultadoDescuento)+"\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConDescuento)+"\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("Descuento aplicado: -"+str(porcentajeDescuento)+"%- "+str(nombreDescuento)+"\n")
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago1)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                            costoTotalPagarCredito = costoTotalAPagarConDescuento

                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                        c.EscribirTexto("\n")
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Pago en con tarjeta.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("Transferencia.\n")
                        c.EscribirTexto("Clave de rastreo: "+str(clave_transferencia)+".\n")
                        c.EscribirTexto("\n")
                        c.EscribirTexto("Pago a crédito 4 quincenas.\n")
                        c.EscribirTexto("Primer pago recibido.\n")
                        c.EstablecerEnfatizado(False)
                        if restante == 0:
                            c.EscribirTexto("PAGO LIQUIDADO\n")
                        else:
                            restantePorPagar = float(restante)/3
                            restantePorPagar = round(restantePorPagar,2)
                            c.EscribirTexto("Abonos restantes de: $"+str(restantePorPagar)+" MXN.\n")
                            ahora = datetime.now()
                            fechaSegundoPago = ahora + timedelta(days=15)
                            fechaSegundoPago = fechaSegundoPago.strftime('%Y-%m-%d')
                            c.EscribirTexto("Segundo pago el día: "+str(fechaSegundoPago)+".\n")
                        
                    
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                        if nombreClienteTicket == "Momentaneo":
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("Cliente momentaneo.\n")
                        else:
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                        c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        if contadorTickets == 1:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA TIENDA.\n")
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("________________________________________________\n")
                            c.EscribirTexto("Firma de cliente.\n")
                        else:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA CLIENTE.\n")
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        

                        c.Feed(1)
                        c.Corte(1)
                        #c.abrirCajon()
                        c.Pulso(48, 60, 120)
                        print("Imprimiendo...")
                        # Recuerda cambiar por el nombre de tu impresora
                        respuesta = c.imprimirEn("POS80 Printer")
                        if respuesta == True:
                            print("Impresión correcta")
                        else:
                            print(f"Error. El mensaje es: {respuesta}")

                

           
                    
                 
                            
                            
                            
            if actualizarEstadoCredito and registrarPago1:
                request.session['pago1Agregado'] = "Pago de crédito Guardado correctamente!"
                return redirect('/verCreditosClientes/')
            else:
                request.session['pago1NoAgregado'] = "Error en la base de datos, intentelo más tarde.."
                return redirect('/verCreditosClientes/')
            
             
        

    else:
        return render(request,"1 Login/login.html")
    
    
    
      

def guardarPago2(request):
    if "idSesion" in request.session:
        # Variables de sesión
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        idPerfil = idEmpleado
        idConfig = idEmpleado
    
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']
        idEmpleado = request.session['idSesion']
        if request.method == "POST":
            
            

           
            

            idCreditoAPagar = request.POST['idCredito']
            idPagoCredito = request.POST['idPagoCredito']
            cantidadPago2 = request.POST['cantidadPago2']

            fechaPago2 = datetime.now()
            horaVenta= datetime.now().time()
             
            formaPago = request.POST['tipoPago'] #Efectivo,  tarjeta o transferencia
            
            datosCredito = Creditos.objects.filter(id_credito = idCreditoAPagar)
            for dato in datosCredito:
                montoTotalCredito = dato.monto_pagar
                montoRestante = dato.monto_restante
                montoPagado = dato.monto_pagado
                sucursal = dato.sucursal_id
                idVentaCredito = dato.venta_id
                
                
           
                
            floatCantidadPago2 = float(cantidadPago2)
            floatRestante = float(montoRestante)
                
                
           
                
            if floatCantidadPago2 == floatRestante:
                restante = 0
                estado = "Finalizado"
           
                
            
            else:
                restante = montoRestante - float(cantidadPago2)
                estado = "Pendiente"

            actualMontoPagado = float(montoPagado) + float(cantidadPago2)
                
                   
                 
                    
            esConEfectivo = False
            esConTarjeta = False
            esConTransferencia = False

            if formaPago == "Efectivo":
                esConEfectivo = True
            elif formaPago == "Tarjeta":
                esConTarjeta = True
                tipo_tarjeta = request.POST['tipoTarjeta']    
                referencia_tarjeta = request.POST['referenciaTarjeta'] 
                        
            elif formaPago == "Transferencia":
                esConTransferencia = True
                clave_transferencia = request.POST['claveRastreoTransferencia'] 

                    


            if esConEfectivo:
                        
                registrarPago2 = PagosCreditos.objects.filter(id_historialCredito = idPagoCredito).update(fecha_pago2 = fechaPago2,tipo_pago2 ="Efectivo",monto_pago2 =cantidadPago2) 
                
                if registrarPago2:
                    
                    
                    actualizarEstadoCreditoPago2 = Creditos.objects.filter(id_credito = idCreditoAPagar).update(monto_pagado = actualMontoPagado,monto_restante =restante,estatus =estado) 
                    if actualizarEstadoCreditoPago2:
                         
                        tipoMovimiento ="IN"
                        montoMovimiento = float(cantidadPago2)
                        descripcionMovimiento ="Movimiento por abono de crédito " + str(idCreditoAPagar) 
                        fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                        horaMovimiento = datetime.now().time()
                        ingresarCantidadEfectivoAcaja =MovimientosCaja(fecha =fechaMovimiento,hora = horaMovimiento,tipo=tipoMovimiento,monto =montoMovimiento, descripcion=descripcionMovimiento,sucursal =  Sucursales.objects.get(id_sucursal = sucursal),
                                                                            realizado_por = Empleados.objects.get(id_empleado = idEmpleado))
                        ingresarCantidadEfectivoAcaja.save()

                        #IMPRESION DE TICKEEETSSSS

                        #Fecha
                        hoy = datetime.now()
                        hoyFormato = hoy.strftime('%Y/%m/%d')

                        #Consulta de venta
                        consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                        for datoVenta in consultaVenta:
                            empleadoVendedor = datoVenta.empleado_vendedor_id
                            sucursal = datoVenta.sucursal_id
                            cliente = datoVenta.cliente_id
                        #Empleado vendedor
                        consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                        for datoVendedor in consultaEmpleadoVendedor:
                            nombreEmpleado = datoVendedor.nombres
                            apellidoPatEmpleado = datoVendedor.apellido_paterno

                        nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                        #Datos sucurssal
                        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                        for datoSucursal in consultaSucursal:
                            nombreSucursal = datoSucursal.nombre
                            telefonoSucursal = datoSucursal.telefono
                            direccionSucursal = datoSucursal.direccion

                        
                        
                        
                        #Hora bien
                        horaVenta = horaVenta.strftime("%H:%M:%S")

                        # Esto es para obtener las impresoras. No es obligatorio hacerlo siempre que se quiera imprimir
                        impresoras = Conector.ConectorV3.obtenerImpresoras()
                        print(f"Las impresoras son: {impresoras}")
                        
                        contadorTickets = 0
                        for x in range(2):
                            contadorTickets = contadorTickets + 1

                            
                            c = Conector.ConectorV3()
                            c.Iniciar()
                            c.Corte(1)
                            
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            # Recuerda que la imagen debe existir y debe ser legible para el plugin. Si no, comenta las líneas
                            c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EstablecerEnfatizado(True)
                            c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("TEL: "+telefonoSucursal+"\n")
                            c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")

                            c.EstablecerEnfatizado(True)
                            c.EscribirTexto("================================================\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EscribirTexto("PAGO DE VENTA #"+str(idVentaCredito)+"\n")
                            c.EscribirTexto("CRÉDITO #"+str(idCreditoAPagar)+"\n")
                            c.EstablecerEnfatizado(False)
                            c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("\n")
                            c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                            c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                            c.EscribirTexto("\n")

                            #Listado de productos 
                            #Productos vendidos en ese credito

                            consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                            for datoVenta in consultaVenta:
                                codigosProductosVenta = datoVenta.ids_productos
                                cantidadesProductosVenta = datoVenta.cantidades_productos
                                idsServiciosCorporales = datoVenta.ids_servicios_corporales
                                cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                                idsServiciosFaciales = datoVenta.ids_servicios_faciales
                                cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                                descuento = datoVenta.descuento
                                costoTotalAPagar = datoVenta.monto_pagar
                                cliente = datoVenta.cliente_id

                            if cliente == None:
                                nombreClienteTicket = "Momentaneo"
                                idCienteTicket="Sin id"
                            else:
                                consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                                for datoCliente in consultaCliente:
                                    idCienteTicket = datoCliente.id_cliente
                                    nombreCliente = datoCliente.nombre_cliente
                                    apellidoCliente = datoCliente.apellidoPaterno_cliente
                                nombreClienteTicket = nombreCliente + " "+apellidoCliente
                                
                                

                            listaCodigosProductos = codigosProductosVenta.split(",")
                            listaCantidadesProductos = cantidadesProductosVenta.split(",")
                            listaIdsServiciosCorporales = idsServiciosCorporales.split(",")
                            listaCantidadesServiciosCorporales = cantidadServiciosCorporales.split(",")
                            listaIdsServiciosFaciales = idsServiciosFaciales.split(",")
                            listaCantidadesServiciosFaciales = cantidadServiciosFaciales.split(",")
                            
                            longitudProductos = len(listaCodigosProductos)
                            longitudServiciosCorporales = len(listaIdsServiciosCorporales)
                            longitudServiciosFaciales = len(listaIdsServiciosFaciales)


                            listaProductos = zip(listaCodigosProductos,listaCantidadesProductos)
                            listaServiciosCorporales = zip(listaIdsServiciosCorporales, listaCantidadesServiciosCorporales)
                            listaServiciosFaciales = zip(listaIdsServiciosFaciales, listaCantidadesServiciosFaciales)

                            if longitudProductos >= 1:
                                for codigo, cantidad in listaProductos:
                                    if codigo != "":
                                        strCodigo = str(codigo)
                                        strCantidad = str(cantidad)
                                        consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                                        for datoProductoVenta in consultaProductoVenta:
                                            nombreProducto = datoProductoVenta.nombre_producto
                                            costoIndividualProducto = datoProductoVenta.costo_venta

                                        floatCantidad = float(cantidad)
                                        costototalProducto = costoIndividualProducto * floatCantidad
                                        costototalProductoDosDecimales = round(costototalProducto, 2)
                                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                        longitudCostoTotal = int(longitudCostoTotal)

                                        
                                        caracteresProducto = len(nombreProducto)

                                        if longitudCostoTotal == 2:
                                            espacio = 38
                                        if longitudCostoTotal == 2:
                                            espacio = 37
                                        elif longitudCostoTotal == 3:
                                            espacio = 36
                                        elif longitudCostoTotal == 4:
                                            espacio = 35
                                        elif longitudCostoTotal == 5:
                                            espacio = 34
                                        elif longitudCostoTotal == 6:
                                            espacio = 33
                                        numeroEspacios = espacio - int(caracteresProducto)
                                        
                                        espaciosTicket = ""
                                        for x in range(numeroEspacios):
                                            espacioMini = " "
                                            espaciosTicket = espaciosTicket + espacioMini
                                        c.EscribirTexto(strCantidad+" x "+nombreProducto+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                            
                            if longitudServiciosCorporales >=1:
                                for idd, cantidad in listaServiciosCorporales:
                                    if idd != "":
                                        idServicio = int(idd)
                                        strCantidad = str(cantidad)
                                        consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                        for datoServicio in consultaServicio:
                                            nombreServicio = datoServicio.nombre_servicio
                                            costoServicio = datoServicio.precio_venta

                                        floatCantidad = float(cantidad)
                                        costototalProducto = costoServicio * floatCantidad
                                        costototalProductoDosDecimales = round(costototalProducto, 2)
                                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                        longitudCostoTotal = int(longitudCostoTotal)

                                        
                                        caracteresProducto = len(nombreServicio)

                                        if longitudCostoTotal == 2:
                                            espacio = 38
                                        if longitudCostoTotal == 2:
                                            espacio = 37
                                        elif longitudCostoTotal == 3:
                                            espacio = 36
                                        elif longitudCostoTotal == 4:
                                            espacio = 35
                                        elif longitudCostoTotal == 5:
                                            espacio = 34
                                        elif longitudCostoTotal == 6:
                                            espacio = 33
                                        numeroEspacios = espacio - int(caracteresProducto)
                                        
                                        espaciosTicket = ""
                                        for x in range(numeroEspacios):
                                            espacioMini = " "
                                            espaciosTicket = espaciosTicket + espacioMini
                                        c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")

                            if longitudServiciosFaciales >=1:
                                for idd, cantidad in listaServiciosFaciales:
                                    if idd != "":
                                        idServicio = int(idd)
                                        strCantidad = str(cantidad)
                                        consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                        for datoServicio in consultaServicio:
                                            nombreServicio = datoServicio.nombre_servicio
                                            costoServicio = datoServicio.precio_venta

                                        floatCantidad = float(cantidad)
                                        costototalProducto = costoServicio * floatCantidad
                                        costototalProductoDosDecimales = round(costototalProducto, 2)
                                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                        longitudCostoTotal = int(longitudCostoTotal)

                                        
                                        caracteresProducto = len(nombreServicio)

                                        if longitudCostoTotal == 2:
                                            espacio = 38
                                        if longitudCostoTotal == 2:
                                            espacio = 37
                                        elif longitudCostoTotal == 3:
                                            espacio = 36
                                        elif longitudCostoTotal == 4:
                                            espacio = 35
                                        elif longitudCostoTotal == 5:
                                            espacio = 34
                                        elif longitudCostoTotal == 6:
                                            espacio = 33
                                        numeroEspacios = espacio - int(caracteresProducto)
                                        
                                        espaciosTicket = ""
                                        for x in range(numeroEspacios):
                                            espacioMini = " "
                                            espaciosTicket = espaciosTicket + espacioMini
                                        c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                            
                            

                            c.EscribirTexto("\n")
                            c.EscribirTexto("\n")

                            if descuento == None:
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                                costoTotalPagarCredito = costoTotalAPagar
                                c.EscribirTexto("ABONADO: $"+str(cantidadPago2)+"\n")
                                c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                            else:
                                intDescuento = int(descuento)
                                consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                                for datoDescuento in consultaDescuentos:
                                    nombreDescuento = datoDescuento.nombre_descuento
                                    porcentajeDescuento = datoDescuento.porcentaje

                                porcentajePagado = 100 - porcentajeDescuento #85
                                totalSinDescuento1 = 100 * costoTotalAPagar
                                totalSinDescuento2 = totalSinDescuento1/porcentajePagado
                                totalSinDescuento2 = round(totalSinDescuento2)

                                primerMulti = porcentajeDescuento * float(totalSinDescuento2)
                                primerDivision = primerMulti/100
                                resultadoDescuento = round(primerDivision)
                                
                                costoTotalAPagarConDescuento = totalSinDescuento2 - resultadoDescuento

                                c.EstablecerTamañoFuente(1, 1)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("Subtotal:  $"+str(totalSinDescuento2)+"\n")
                                c.EscribirTexto("Descuento:  $"+str(resultadoDescuento)+"\n")
                                c.EstablecerTamañoFuente(2, 2)
                                c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConDescuento)+"\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("Descuento aplicado: -"+str(porcentajeDescuento)+"%- "+str(nombreDescuento)+"\n")
                                c.EscribirTexto("ABONADO: $"+str(cantidadPago2)+"\n")
                                c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                                costoTotalPagarCredito = costoTotalAPagarConDescuento

                            c.EscribirTexto("\n")
                            c.EstablecerEnfatizado(True)
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                            c.EscribirTexto("\n")
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("\n")
                            c.EstablecerEnfatizado(True)
                            c.EscribirTexto("Pago en efectivo.\n")
                            c.EscribirTexto("Pago a crédito 4 quincenas.\n")
                            c.EscribirTexto("Segundo pago recibido.\n")
                            c.EstablecerEnfatizado(False)
                            if restante == 0:
                                c.EscribirTexto("PAGO LIQUIDADO\n")
                            else:
                                restantePorPagar = float(restante)/2
                                restantePorPagar = round(restantePorPagar,2)
                                c.EscribirTexto("Abonos restantes de: $"+str(restantePorPagar)+" MXN.\n")
                                ahora = datetime.now()
                                fechaSegundoPago = ahora + timedelta(days=15)
                                fechaSegundoPago = fechaSegundoPago.strftime('%Y-%m-%d')
                                c.EscribirTexto("Tercer pago el día: "+str(fechaSegundoPago)+".\n")
                            
                        
                            c.EscribirTexto("\n")
                            c.EstablecerEnfatizado(True)
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                            if nombreClienteTicket == "Momentaneo":
                                c.EstablecerEnfatizado(False)
                                c.EscribirTexto("Cliente momentaneo.\n")
                            else:
                                c.EstablecerEnfatizado(False)
                                c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                            c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerEnfatizado(True)
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            if contadorTickets == 1:
                                c.EscribirTexto("\n")
                                c.EscribirTexto("COPIA TIENDA.\n")
                                c.EscribirTexto("\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("________________________________________________\n")
                                c.EscribirTexto("Firma de cliente.\n")
                            else:
                                c.EscribirTexto("\n")
                                c.EscribirTexto("COPIA CLIENTE.\n")
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            

                            c.Feed(1)
                            c.Corte(1)
                            #c.abrirCajon()
                            c.Pulso(48, 60, 120)
                            print("Imprimiendo...")
                            # Recuerda cambiar por el nombre de tu impresora
                            respuesta = c.imprimirEn("POS80 Printer")
                            if respuesta == True:
                                print("Impresión correcta")
                            else:
                                print(f"Error. El mensaje es: {respuesta}")


                
                

            if esConTarjeta:
                    
                        
                registrarPago2 = PagosCreditos.objects.filter(id_historialCredito = idPagoCredito).update(fecha_pago2 = fechaPago2,tipo_pago2 ="Tarjeta",tipo_tarjeta2=tipo_tarjeta,referencia_pago_tarjeta2=referencia_tarjeta,monto_pago2 =cantidadPago2) 
                
                if registrarPago2:
                    
                    
                    actualizarEstadoCreditoPago2 = Creditos.objects.filter(id_credito = idCreditoAPagar).update(monto_pagado = actualMontoPagado,monto_restante =restante,estatus =estado) 
                  
                    #IMPRESION DE TICKEEETSSSS

                    #Fecha
                    hoy = datetime.now()
                    hoyFormato = hoy.strftime('%Y/%m/%d')

                    #Consulta de venta
                    consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                    for datoVenta in consultaVenta:
                        empleadoVendedor = datoVenta.empleado_vendedor_id
                        sucursal = datoVenta.sucursal_id
                        cliente = datoVenta.cliente_id
                    #Empleado vendedor
                    consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                    for datoVendedor in consultaEmpleadoVendedor:
                        nombreEmpleado = datoVendedor.nombres
                        apellidoPatEmpleado = datoVendedor.apellido_paterno

                    nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                    #Datos sucurssal
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        telefonoSucursal = datoSucursal.telefono
                        direccionSucursal = datoSucursal.direccion

                    
                    
                    
                    #Hora bien
                    horaVenta = horaVenta.strftime("%H:%M:%S")

                    # Esto es para obtener las impresoras. No es obligatorio hacerlo siempre que se quiera imprimir
                    impresoras = Conector.ConectorV3.obtenerImpresoras()
                    print(f"Las impresoras son: {impresoras}")
                    
                    contadorTickets = 0
                    for x in range(2):
                        contadorTickets = contadorTickets + 1

                        
                        c = Conector.ConectorV3()
                        c.Iniciar()
                        c.Corte(1)
                        
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        # Recuerda que la imagen debe existir y debe ser legible para el plugin. Si no, comenta las líneas
                        c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("TEL: "+telefonoSucursal+"\n")
                        c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")

                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("================================================\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EscribirTexto("PAGO DE VENTA #"+str(idVentaCredito)+"\n")
                        c.EscribirTexto("CRÉDITO #"+str(idCreditoAPagar)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        #Productos vendidos en ese credito

                        consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                        for datoVenta in consultaVenta:
                            codigosProductosVenta = datoVenta.ids_productos
                            cantidadesProductosVenta = datoVenta.cantidades_productos
                            idsServiciosCorporales = datoVenta.ids_servicios_corporales
                            cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                            idsServiciosFaciales = datoVenta.ids_servicios_faciales
                            cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                            descuento = datoVenta.descuento
                            costoTotalAPagar = datoVenta.monto_pagar
                            cliente = datoVenta.cliente_id

                        if cliente == None:
                            nombreClienteTicket = "Momentaneo"
                            idCienteTicket="Sin id"
                        else:
                            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                            for datoCliente in consultaCliente:
                                idCienteTicket = datoCliente.id_cliente
                                nombreCliente = datoCliente.nombre_cliente
                                apellidoCliente = datoCliente.apellidoPaterno_cliente
                            nombreClienteTicket = nombreCliente + " "+apellidoCliente
                            
                            

                        listaCodigosProductos = codigosProductosVenta.split(",")
                        listaCantidadesProductos = cantidadesProductosVenta.split(",")
                        listaIdsServiciosCorporales = idsServiciosCorporales.split(",")
                        listaCantidadesServiciosCorporales = cantidadServiciosCorporales.split(",")
                        listaIdsServiciosFaciales = idsServiciosFaciales.split(",")
                        listaCantidadesServiciosFaciales = cantidadServiciosFaciales.split(",")
                        
                        longitudProductos = len(listaCodigosProductos)
                        longitudServiciosCorporales = len(listaIdsServiciosCorporales)
                        longitudServiciosFaciales = len(listaIdsServiciosFaciales)


                        listaProductos = zip(listaCodigosProductos,listaCantidadesProductos)
                        listaServiciosCorporales = zip(listaIdsServiciosCorporales, listaCantidadesServiciosCorporales)
                        listaServiciosFaciales = zip(listaIdsServiciosFaciales, listaCantidadesServiciosFaciales)

                        if longitudProductos >= 1:
                            for codigo, cantidad in listaProductos:
                                if codigo != "":
                                    strCodigo = str(codigo)
                                    strCantidad = str(cantidad)
                                    consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                                    for datoProductoVenta in consultaProductoVenta:
                                        nombreProducto = datoProductoVenta.nombre_producto
                                        costoIndividualProducto = datoProductoVenta.costo_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoIndividualProducto * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreProducto)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreProducto+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        if longitudServiciosCorporales >=1:
                            for idd, cantidad in listaServiciosCorporales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")

                        if longitudServiciosFaciales >=1:
                            for idd, cantidad in listaServiciosFaciales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        

                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")

                        if descuento == None:
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                            costoTotalPagarCredito = costoTotalAPagar
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago2)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                        else:
                            intDescuento = int(descuento)
                            consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                            for datoDescuento in consultaDescuentos:
                                nombreDescuento = datoDescuento.nombre_descuento
                                porcentajeDescuento = datoDescuento.porcentaje

                            porcentajePagado = 100 - porcentajeDescuento #85
                            totalSinDescuento1 = 100 * costoTotalAPagar
                            totalSinDescuento2 = totalSinDescuento1/porcentajePagado
                            totalSinDescuento2 = round(totalSinDescuento2)

                            primerMulti = porcentajeDescuento * float(totalSinDescuento2)
                            primerDivision = primerMulti/100
                            resultadoDescuento = round(primerDivision)
                            
                            costoTotalAPagarConDescuento = totalSinDescuento2 - resultadoDescuento

                            c.EstablecerTamañoFuente(1, 1)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("Subtotal:  $"+str(totalSinDescuento2)+"\n")
                            c.EscribirTexto("Descuento:  $"+str(resultadoDescuento)+"\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConDescuento)+"\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("Descuento aplicado: -"+str(porcentajeDescuento)+"%- "+str(nombreDescuento)+"\n")
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago2)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                            costoTotalPagarCredito = costoTotalAPagarConDescuento

                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                        c.EscribirTexto("\n")
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Pago en con tarjeta.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("Pago con "+str(tipo_tarjeta)+".\n")
                        c.EscribirTexto("Referencia: "+referencia_tarjeta+".\n")
                        c.EscribirTexto("Segundo pago recibido.\n")
                        c.EstablecerEnfatizado(False)
                        if restante == 0:
                            c.EscribirTexto("PAGO LIQUIDADO\n")
                        else:
                            restantePorPagar = float(restante)/2
                            restantePorPagar = round(restantePorPagar,2)
                            c.EscribirTexto("Abonos restantes de: $"+str(restantePorPagar)+" MXN.\n")
                            ahora = datetime.now()
                            fechaSegundoPago = ahora + timedelta(days=15)
                            fechaSegundoPago = fechaSegundoPago.strftime('%Y-%m-%d')
                            c.EscribirTexto("Tercer pago el día: "+str(fechaSegundoPago)+".\n")
                        
                    
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                        if nombreClienteTicket == "Momentaneo":
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("Cliente momentaneo.\n")
                        else:
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                        c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        if contadorTickets == 1:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA TIENDA.\n")
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("________________________________________________\n")
                            c.EscribirTexto("Firma de cliente.\n")
                        else:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA CLIENTE.\n")
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        

                        c.Feed(1)
                        c.Corte(1)
                        #c.abrirCajon()
                        c.Pulso(48, 60, 120)
                        print("Imprimiendo...")
                        # Recuerda cambiar por el nombre de tu impresora
                        respuesta = c.imprimirEn("POS80 Printer")
                        if respuesta == True:
                            print("Impresión correcta")
                        else:
                            print(f"Error. El mensaje es: {respuesta}")

            if esConTransferencia:
            
                registrarPago2 = PagosCreditos.objects.filter(id_historialCredito = idPagoCredito).update(fecha_pago2 = fechaPago2,tipo_pago2 ="Transferencia",clave_rastreo_pago_transferencia2=clave_transferencia,monto_pago2 =cantidadPago2) 
                
                if registrarPago2:
                    
                    
                    actualizarEstadoCreditoPago2 = Creditos.objects.filter(id_credito = idCreditoAPagar).update(monto_pagado = actualMontoPagado,monto_restante =restante,estatus =estado) 

                    #Fecha
                    hoy = datetime.now()
                    hoyFormato = hoy.strftime('%Y/%m/%d')

                    #Consulta de venta
                    consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                    for datoVenta in consultaVenta:
                        empleadoVendedor = datoVenta.empleado_vendedor_id
                        sucursal = datoVenta.sucursal_id
                        cliente = datoVenta.cliente_id
                    #Empleado vendedor
                    consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                    for datoVendedor in consultaEmpleadoVendedor:
                        nombreEmpleado = datoVendedor.nombres
                        apellidoPatEmpleado = datoVendedor.apellido_paterno

                    nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                    #Datos sucurssal
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        telefonoSucursal = datoSucursal.telefono
                        direccionSucursal = datoSucursal.direccion

                    
                    
                    
                    #Hora bien
                    horaVenta = horaVenta.strftime("%H:%M:%S")

                    # Esto es para obtener las impresoras. No es obligatorio hacerlo siempre que se quiera imprimir
                    impresoras = Conector.ConectorV3.obtenerImpresoras()
                    print(f"Las impresoras son: {impresoras}")
                    
                    contadorTickets = 0
                    for x in range(2):
                        contadorTickets = contadorTickets + 1

                        
                        c = Conector.ConectorV3()
                        c.Iniciar()
                        c.Corte(1)
                        
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        # Recuerda que la imagen debe existir y debe ser legible para el plugin. Si no, comenta las líneas
                        c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("TEL: "+telefonoSucursal+"\n")
                        c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")

                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("================================================\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EscribirTexto("PAGO DE VENTA #"+str(idVentaCredito)+"\n")
                        c.EscribirTexto("CRÉDITO #"+str(idCreditoAPagar)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        #Productos vendidos en ese credito

                        consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                        for datoVenta in consultaVenta:
                            codigosProductosVenta = datoVenta.ids_productos
                            cantidadesProductosVenta = datoVenta.cantidades_productos
                            idsServiciosCorporales = datoVenta.ids_servicios_corporales
                            cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                            idsServiciosFaciales = datoVenta.ids_servicios_faciales
                            cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                            descuento = datoVenta.descuento
                            costoTotalAPagar = datoVenta.monto_pagar
                            cliente = datoVenta.cliente_id

                        if cliente == None:
                            nombreClienteTicket = "Momentaneo"
                            idCienteTicket="Sin id"
                        else:
                            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                            for datoCliente in consultaCliente:
                                idCienteTicket = datoCliente.id_cliente
                                nombreCliente = datoCliente.nombre_cliente
                                apellidoCliente = datoCliente.apellidoPaterno_cliente
                            nombreClienteTicket = nombreCliente + " "+apellidoCliente
                            
                            

                        listaCodigosProductos = codigosProductosVenta.split(",")
                        listaCantidadesProductos = cantidadesProductosVenta.split(",")
                        listaIdsServiciosCorporales = idsServiciosCorporales.split(",")
                        listaCantidadesServiciosCorporales = cantidadServiciosCorporales.split(",")
                        listaIdsServiciosFaciales = idsServiciosFaciales.split(",")
                        listaCantidadesServiciosFaciales = cantidadServiciosFaciales.split(",")
                        
                        longitudProductos = len(listaCodigosProductos)
                        longitudServiciosCorporales = len(listaIdsServiciosCorporales)
                        longitudServiciosFaciales = len(listaIdsServiciosFaciales)


                        listaProductos = zip(listaCodigosProductos,listaCantidadesProductos)
                        listaServiciosCorporales = zip(listaIdsServiciosCorporales, listaCantidadesServiciosCorporales)
                        listaServiciosFaciales = zip(listaIdsServiciosFaciales, listaCantidadesServiciosFaciales)

                        if longitudProductos >= 1:
                            for codigo, cantidad in listaProductos:
                                if codigo != "":
                                    strCodigo = str(codigo)
                                    strCantidad = str(cantidad)
                                    consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                                    for datoProductoVenta in consultaProductoVenta:
                                        nombreProducto = datoProductoVenta.nombre_producto
                                        costoIndividualProducto = datoProductoVenta.costo_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoIndividualProducto * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreProducto)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreProducto+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        if longitudServiciosCorporales >=1:
                            for idd, cantidad in listaServiciosCorporales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")

                        if longitudServiciosFaciales >=1:
                            for idd, cantidad in listaServiciosFaciales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        

                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")

                        if descuento == None:
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                            costoTotalPagarCredito = costoTotalAPagar
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago2)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                        else:
                            intDescuento = int(descuento)
                            consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                            for datoDescuento in consultaDescuentos:
                                nombreDescuento = datoDescuento.nombre_descuento
                                porcentajeDescuento = datoDescuento.porcentaje

                            porcentajePagado = 100 - porcentajeDescuento #85
                            totalSinDescuento1 = 100 * costoTotalAPagar
                            totalSinDescuento2 = totalSinDescuento1/porcentajePagado
                            totalSinDescuento2 = round(totalSinDescuento2)

                            primerMulti = porcentajeDescuento * float(totalSinDescuento2)
                            primerDivision = primerMulti/100
                            resultadoDescuento = round(primerDivision)
                            
                            costoTotalAPagarConDescuento = totalSinDescuento2 - resultadoDescuento

                            c.EstablecerTamañoFuente(1, 1)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("Subtotal:  $"+str(totalSinDescuento2)+"\n")
                            c.EscribirTexto("Descuento:  $"+str(resultadoDescuento)+"\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConDescuento)+"\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("Descuento aplicado: -"+str(porcentajeDescuento)+"%- "+str(nombreDescuento)+"\n")
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago2)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                            costoTotalPagarCredito = costoTotalAPagarConDescuento

                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                        c.EscribirTexto("\n")
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Pago en con Transferencia.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("Transferencia.\n")
                        c.EscribirTexto("Clave de rastreo: "+str(clave_transferencia)+".\n")
                        c.EscribirTexto("Segundo pago recibido.\n")
                        c.EstablecerEnfatizado(False)
                        if restante == 0:
                            c.EscribirTexto("PAGO LIQUIDADO\n")
                        else:
                            restantePorPagar = float(restante)/2
                            restantePorPagar = round(restantePorPagar,2)
                            c.EscribirTexto("Abonos restantes de: $"+str(restantePorPagar)+" MXN.\n")
                            ahora = datetime.now()
                            fechaSegundoPago = ahora + timedelta(days=15)
                            fechaSegundoPago = fechaSegundoPago.strftime('%Y-%m-%d')
                            c.EscribirTexto("Tercer pago el día: "+str(fechaSegundoPago)+".\n")
                        
                    
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                        if nombreClienteTicket == "Momentaneo":
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("Cliente momentaneo.\n")
                        else:
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                        c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        if contadorTickets == 1:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA TIENDA.\n")
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("________________________________________________\n")
                            c.EscribirTexto("Firma de cliente.\n")
                        else:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA CLIENTE.\n")
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        

                        c.Feed(1)
                        c.Corte(1)
                        #c.abrirCajon()
                        c.Pulso(48, 60, 120)
                        print("Imprimiendo...")
                        # Recuerda cambiar por el nombre de tu impresora
                        respuesta = c.imprimirEn("POS80 Printer")
                        if respuesta == True:
                            print("Impresión correcta")
                        else:
                            print(f"Error. El mensaje es: {respuesta}")

                

           
                    
                 
                            
                            
                            
            if actualizarEstadoCreditoPago2 and registrarPago2:
                request.session['pago2Agregado'] = "Pago de crédito Guardado correctamente!"
                return redirect('/verCreditosClientes/')
            else:
                request.session['pago2NoAgregado'] = "Error en la base de datos, intentelo más tarde.."
                return redirect('/verCreditosClientes/')
            
             
        


    else:
        return render(request,"1 Login/login.html")
    
    
    


def guardarPago3(request):
    if "idSesion" in request.session:
        # Variables de sesión
        idEmpleado = request.session['idSesion']
        
        if request.method == "POST":
            
            

            idCreditoAPagar = request.POST['idCredito']
            idPagoCredito = request.POST['idPagoCredito']
            cantidadPago3 = request.POST['cantidadPago3']

            fechaPago1 = datetime.now()
            horaVenta= datetime.now().time()
            
             
            formaPago = request.POST['tipoPago'] #Efectivo,  tarjeta o transferencia
            
            datosCredito = Creditos.objects.filter(id_credito = idCreditoAPagar)
            for dato in datosCredito:
                montoRestante = dato.monto_restante
                sucursal = dato.sucursal_id
                montoPagado = dato.monto_pagado
                idVentaCredito = dato.venta_id
                
            floatCantidadPago3 = float(cantidadPago3)
            floatRestante = float(montoRestante)
                
                
           
                
            if floatCantidadPago3 == floatRestante:
                restante = 0
                estado = "Finalizado"
           
                
            
            else:
                restante = montoRestante - float(cantidadPago3)
                estado = "Pendiente"
                
            actualMontoPagado = float(montoPagado) + float(cantidadPago3)
                 
                    
            esConEfectivo = False
            esConTarjeta = False
            esConTransferencia = False

            if formaPago == "Efectivo":
                esConEfectivo = True
            elif formaPago == "Tarjeta":
                esConTarjeta = True
                tipo_tarjeta = request.POST['tipoTarjeta']    
                referencia_tarjeta = request.POST['referenciaTarjeta'] 
                        
            elif formaPago == "Transferencia":
                esConTransferencia = True
                clave_transferencia = request.POST['claveRastreoTransferencia'] 

                    


            if esConEfectivo:
                        
                registrarPago3 = PagosCreditos.objects.filter(id_historialCredito = idPagoCredito).update(fecha_pago3 = fechaPago1,tipo_pago3 ="Efectivo",monto_pago3 =cantidadPago3) 
                
                if registrarPago3:
                    
                    
                    actualizarEstadoCredito = Creditos.objects.filter(id_credito = idCreditoAPagar).update(monto_pagado = actualMontoPagado,monto_restante =restante,estatus =estado) 
                    if actualizarEstadoCredito:
                         
                        tipoMovimiento ="IN"
                        montoMovimiento = float(cantidadPago3)
                        descripcionMovimiento ="Movimiento por abono de crédito " + str(idCreditoAPagar) 
                        fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                        horaMovimiento = datetime.now().time()
                        ingresarCantidadEfectivoAcaja =MovimientosCaja(fecha =fechaMovimiento,hora = horaMovimiento,tipo=tipoMovimiento,monto =montoMovimiento, descripcion=descripcionMovimiento,sucursal =  Sucursales.objects.get(id_sucursal = sucursal),
                                                                            realizado_por = Empleados.objects.get(id_empleado = idEmpleado))
                        ingresarCantidadEfectivoAcaja.save()

                         #IMPRESION DE TICKEEETSSSS

                        #Fecha
                        hoy = datetime.now()
                        hoyFormato = hoy.strftime('%Y/%m/%d')

                        #Consulta de venta
                        consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                        for datoVenta in consultaVenta:
                            empleadoVendedor = datoVenta.empleado_vendedor_id
                            sucursal = datoVenta.sucursal_id
                            cliente = datoVenta.cliente_id
                        #Empleado vendedor
                        consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                        for datoVendedor in consultaEmpleadoVendedor:
                            nombreEmpleado = datoVendedor.nombres
                            apellidoPatEmpleado = datoVendedor.apellido_paterno

                        nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                        #Datos sucurssal
                        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                        for datoSucursal in consultaSucursal:
                            nombreSucursal = datoSucursal.nombre
                            telefonoSucursal = datoSucursal.telefono
                            direccionSucursal = datoSucursal.direccion

                        
                        
                        
                        #Hora bien
                        horaVenta = horaVenta.strftime("%H:%M:%S")

                        # Esto es para obtener las impresoras. No es obligatorio hacerlo siempre que se quiera imprimir
                        impresoras = Conector.ConectorV3.obtenerImpresoras()
                        print(f"Las impresoras son: {impresoras}")
                        
                        contadorTickets = 0
                        for x in range(2):
                            contadorTickets = contadorTickets + 1

                            
                            c = Conector.ConectorV3()
                            c.Iniciar()
                            c.Corte(1)
                            
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            # Recuerda que la imagen debe existir y debe ser legible para el plugin. Si no, comenta las líneas
                            c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EstablecerEnfatizado(True)
                            c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("TEL: "+telefonoSucursal+"\n")
                            c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")

                            c.EstablecerEnfatizado(True)
                            c.EscribirTexto("================================================\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EscribirTexto("PAGO DE VENTA #"+str(idVentaCredito)+"\n")
                            c.EscribirTexto("CRÉDITO #"+str(idCreditoAPagar)+"\n")
                            c.EstablecerEnfatizado(False)
                            c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("\n")
                            c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                            c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                            c.EscribirTexto("\n")

                            #Listado de productos 
                            #Productos vendidos en ese credito

                            consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                            for datoVenta in consultaVenta:
                                codigosProductosVenta = datoVenta.ids_productos
                                cantidadesProductosVenta = datoVenta.cantidades_productos
                                idsServiciosCorporales = datoVenta.ids_servicios_corporales
                                cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                                idsServiciosFaciales = datoVenta.ids_servicios_faciales
                                cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                                descuento = datoVenta.descuento
                                costoTotalAPagar = datoVenta.monto_pagar
                                cliente = datoVenta.cliente_id

                            if cliente == None:
                                nombreClienteTicket = "Momentaneo"
                                idCienteTicket="Sin id"
                            else:
                                consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                                for datoCliente in consultaCliente:
                                    idCienteTicket = datoCliente.id_cliente
                                    nombreCliente = datoCliente.nombre_cliente
                                    apellidoCliente = datoCliente.apellidoPaterno_cliente
                                nombreClienteTicket = nombreCliente + " "+apellidoCliente
                                
                                

                            listaCodigosProductos = codigosProductosVenta.split(",")
                            listaCantidadesProductos = cantidadesProductosVenta.split(",")
                            listaIdsServiciosCorporales = idsServiciosCorporales.split(",")
                            listaCantidadesServiciosCorporales = cantidadServiciosCorporales.split(",")
                            listaIdsServiciosFaciales = idsServiciosFaciales.split(",")
                            listaCantidadesServiciosFaciales = cantidadServiciosFaciales.split(",")
                            
                            longitudProductos = len(listaCodigosProductos)
                            longitudServiciosCorporales = len(listaIdsServiciosCorporales)
                            longitudServiciosFaciales = len(listaIdsServiciosFaciales)


                            listaProductos = zip(listaCodigosProductos,listaCantidadesProductos)
                            listaServiciosCorporales = zip(listaIdsServiciosCorporales, listaCantidadesServiciosCorporales)
                            listaServiciosFaciales = zip(listaIdsServiciosFaciales, listaCantidadesServiciosFaciales)

                            if longitudProductos >= 1:
                                for codigo, cantidad in listaProductos:
                                    if codigo != "":
                                        strCodigo = str(codigo)
                                        strCantidad = str(cantidad)
                                        consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                                        for datoProductoVenta in consultaProductoVenta:
                                            nombreProducto = datoProductoVenta.nombre_producto
                                            costoIndividualProducto = datoProductoVenta.costo_venta

                                        floatCantidad = float(cantidad)
                                        costototalProducto = costoIndividualProducto * floatCantidad
                                        costototalProductoDosDecimales = round(costototalProducto, 2)
                                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                        longitudCostoTotal = int(longitudCostoTotal)

                                        
                                        caracteresProducto = len(nombreProducto)

                                        if longitudCostoTotal == 2:
                                            espacio = 38
                                        if longitudCostoTotal == 2:
                                            espacio = 37
                                        elif longitudCostoTotal == 3:
                                            espacio = 36
                                        elif longitudCostoTotal == 4:
                                            espacio = 35
                                        elif longitudCostoTotal == 5:
                                            espacio = 34
                                        elif longitudCostoTotal == 6:
                                            espacio = 33
                                        numeroEspacios = espacio - int(caracteresProducto)
                                        
                                        espaciosTicket = ""
                                        for x in range(numeroEspacios):
                                            espacioMini = " "
                                            espaciosTicket = espaciosTicket + espacioMini
                                        c.EscribirTexto(strCantidad+" x "+nombreProducto+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                            
                            if longitudServiciosCorporales >=1:
                                for idd, cantidad in listaServiciosCorporales:
                                    if idd != "":
                                        idServicio = int(idd)
                                        strCantidad = str(cantidad)
                                        consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                        for datoServicio in consultaServicio:
                                            nombreServicio = datoServicio.nombre_servicio
                                            costoServicio = datoServicio.precio_venta

                                        floatCantidad = float(cantidad)
                                        costototalProducto = costoServicio * floatCantidad
                                        costototalProductoDosDecimales = round(costototalProducto, 2)
                                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                        longitudCostoTotal = int(longitudCostoTotal)

                                        
                                        caracteresProducto = len(nombreServicio)

                                        if longitudCostoTotal == 2:
                                            espacio = 38
                                        if longitudCostoTotal == 2:
                                            espacio = 37
                                        elif longitudCostoTotal == 3:
                                            espacio = 36
                                        elif longitudCostoTotal == 4:
                                            espacio = 35
                                        elif longitudCostoTotal == 5:
                                            espacio = 34
                                        elif longitudCostoTotal == 6:
                                            espacio = 33
                                        numeroEspacios = espacio - int(caracteresProducto)
                                        
                                        espaciosTicket = ""
                                        for x in range(numeroEspacios):
                                            espacioMini = " "
                                            espaciosTicket = espaciosTicket + espacioMini
                                        c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")

                            if longitudServiciosFaciales >=1:
                                for idd, cantidad in listaServiciosFaciales:
                                    if idd != "":
                                        idServicio = int(idd)
                                        strCantidad = str(cantidad)
                                        consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                        for datoServicio in consultaServicio:
                                            nombreServicio = datoServicio.nombre_servicio
                                            costoServicio = datoServicio.precio_venta

                                        floatCantidad = float(cantidad)
                                        costototalProducto = costoServicio * floatCantidad
                                        costototalProductoDosDecimales = round(costototalProducto, 2)
                                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                        longitudCostoTotal = int(longitudCostoTotal)

                                        
                                        caracteresProducto = len(nombreServicio)

                                        if longitudCostoTotal == 2:
                                            espacio = 38
                                        if longitudCostoTotal == 2:
                                            espacio = 37
                                        elif longitudCostoTotal == 3:
                                            espacio = 36
                                        elif longitudCostoTotal == 4:
                                            espacio = 35
                                        elif longitudCostoTotal == 5:
                                            espacio = 34
                                        elif longitudCostoTotal == 6:
                                            espacio = 33
                                        numeroEspacios = espacio - int(caracteresProducto)
                                        
                                        espaciosTicket = ""
                                        for x in range(numeroEspacios):
                                            espacioMini = " "
                                            espaciosTicket = espaciosTicket + espacioMini
                                        c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                            
                            

                            c.EscribirTexto("\n")
                            c.EscribirTexto("\n")

                            if descuento == None:
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                                costoTotalPagarCredito = costoTotalAPagar
                                c.EscribirTexto("ABONADO: $"+str(cantidadPago3)+"\n")
                                c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                            else:
                                intDescuento = int(descuento)
                                consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                                for datoDescuento in consultaDescuentos:
                                    nombreDescuento = datoDescuento.nombre_descuento
                                    porcentajeDescuento = datoDescuento.porcentaje

                                porcentajePagado = 100 - porcentajeDescuento #85
                                totalSinDescuento1 = 100 * costoTotalAPagar
                                totalSinDescuento2 = totalSinDescuento1/porcentajePagado
                                totalSinDescuento2 = round(totalSinDescuento2)

                                primerMulti = porcentajeDescuento * float(totalSinDescuento2)
                                primerDivision = primerMulti/100
                                resultadoDescuento = round(primerDivision)
                                
                                costoTotalAPagarConDescuento = totalSinDescuento2 - resultadoDescuento

                                c.EstablecerTamañoFuente(1, 1)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("Subtotal:  $"+str(totalSinDescuento2)+"\n")
                                c.EscribirTexto("Descuento:  $"+str(resultadoDescuento)+"\n")
                                c.EstablecerTamañoFuente(2, 2)
                                c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConDescuento)+"\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("Descuento aplicado: -"+str(porcentajeDescuento)+"%- "+str(nombreDescuento)+"\n")
                                c.EscribirTexto("ABONADO: $"+str(cantidadPago3)+"\n")
                                c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                                costoTotalPagarCredito = costoTotalAPagarConDescuento

                            c.EscribirTexto("\n")
                            c.EstablecerEnfatizado(True)
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                            c.EscribirTexto("\n")
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("\n")
                            c.EstablecerEnfatizado(True)
                            c.EscribirTexto("Pago en efectivo.\n")
                            c.EscribirTexto("Pago a crédito 4 quincenas.\n")
                            c.EscribirTexto("Tercer pago recibido.\n")
                            c.EstablecerEnfatizado(False)
                            if restante == 0:
                                c.EscribirTexto("PAGO LIQUIDADO\n")
                            else:
                                restantePorPagar = float(restante)
                                restantePorPagar = round(restantePorPagar,2)
                                c.EscribirTexto("Abonos restantes de: $"+str(restantePorPagar)+" MXN.\n")
                                ahora = datetime.now()
                                fechaSegundoPago = ahora + timedelta(days=15)
                                fechaSegundoPago = fechaSegundoPago.strftime('%Y-%m-%d')
                                c.EscribirTexto("Cuarto pago el día: "+str(fechaSegundoPago)+".\n")
                            
                        
                            c.EscribirTexto("\n")
                            c.EstablecerEnfatizado(True)
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                            if nombreClienteTicket == "Momentaneo":
                                c.EstablecerEnfatizado(False)
                                c.EscribirTexto("Cliente momentaneo.\n")
                            else:
                                c.EstablecerEnfatizado(False)
                                c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                            c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerEnfatizado(True)
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            if contadorTickets == 1:
                                c.EscribirTexto("\n")
                                c.EscribirTexto("COPIA TIENDA.\n")
                                c.EscribirTexto("\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("________________________________________________\n")
                                c.EscribirTexto("Firma de cliente.\n")
                            else:
                                c.EscribirTexto("\n")
                                c.EscribirTexto("COPIA CLIENTE.\n")
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            

                            c.Feed(1)
                            c.Corte(1)
                            #c.abrirCajon()
                            c.Pulso(48, 60, 120)
                            print("Imprimiendo...")
                            # Recuerda cambiar por el nombre de tu impresora
                            respuesta = c.imprimirEn("POS80 Printer")
                            if respuesta == True:
                                print("Impresión correcta")
                            else:
                                print(f"Error. El mensaje es: {respuesta}")


            if esConTarjeta:
                    
                        
                registrarPago3 = PagosCreditos.objects.filter(id_historialCredito = idPagoCredito).update(fecha_pago3 = fechaPago1,tipo_pago3 ="Tarjeta",tipo_tarjeta3=tipo_tarjeta,referencia_pago_tarjeta3=referencia_tarjeta,monto_pago3 =cantidadPago3) 
                
                if registrarPago3:
                    
                    
                    actualizarEstadoCredito = Creditos.objects.filter(id_credito = idCreditoAPagar).update(monto_pagado = actualMontoPagado,monto_restante =restante,estatus =estado) 

                    #IMPRESION DE TICKEEETSSSS

                    #Fecha
                    hoy = datetime.now()
                    hoyFormato = hoy.strftime('%Y/%m/%d')

                    #Consulta de venta
                    consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                    for datoVenta in consultaVenta:
                        empleadoVendedor = datoVenta.empleado_vendedor_id
                        sucursal = datoVenta.sucursal_id
                        cliente = datoVenta.cliente_id
                    #Empleado vendedor
                    consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                    for datoVendedor in consultaEmpleadoVendedor:
                        nombreEmpleado = datoVendedor.nombres
                        apellidoPatEmpleado = datoVendedor.apellido_paterno

                    nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                    #Datos sucurssal
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        telefonoSucursal = datoSucursal.telefono
                        direccionSucursal = datoSucursal.direccion

                    
                    
                    
                    #Hora bien
                    horaVenta = horaVenta.strftime("%H:%M:%S")

                    # Esto es para obtener las impresoras. No es obligatorio hacerlo siempre que se quiera imprimir
                    impresoras = Conector.ConectorV3.obtenerImpresoras()
                    print(f"Las impresoras son: {impresoras}")
                    
                    contadorTickets = 0
                    for x in range(2):
                        contadorTickets = contadorTickets + 1

                        
                        c = Conector.ConectorV3()
                        c.Iniciar()
                        c.Corte(1)
                        
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        # Recuerda que la imagen debe existir y debe ser legible para el plugin. Si no, comenta las líneas
                        c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("TEL: "+telefonoSucursal+"\n")
                        c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")

                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("================================================\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EscribirTexto("PAGO DE VENTA #"+str(idVentaCredito)+"\n")
                        c.EscribirTexto("CRÉDITO #"+str(idCreditoAPagar)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        #Productos vendidos en ese credito

                        consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                        for datoVenta in consultaVenta:
                            codigosProductosVenta = datoVenta.ids_productos
                            cantidadesProductosVenta = datoVenta.cantidades_productos
                            idsServiciosCorporales = datoVenta.ids_servicios_corporales
                            cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                            idsServiciosFaciales = datoVenta.ids_servicios_faciales
                            cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                            descuento = datoVenta.descuento
                            costoTotalAPagar = datoVenta.monto_pagar
                            cliente = datoVenta.cliente_id

                        if cliente == None:
                            nombreClienteTicket = "Momentaneo"
                            idCienteTicket="Sin id"
                        else:
                            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                            for datoCliente in consultaCliente:
                                idCienteTicket = datoCliente.id_cliente
                                nombreCliente = datoCliente.nombre_cliente
                                apellidoCliente = datoCliente.apellidoPaterno_cliente
                            nombreClienteTicket = nombreCliente + " "+apellidoCliente
                            
                            

                        listaCodigosProductos = codigosProductosVenta.split(",")
                        listaCantidadesProductos = cantidadesProductosVenta.split(",")
                        listaIdsServiciosCorporales = idsServiciosCorporales.split(",")
                        listaCantidadesServiciosCorporales = cantidadServiciosCorporales.split(",")
                        listaIdsServiciosFaciales = idsServiciosFaciales.split(",")
                        listaCantidadesServiciosFaciales = cantidadServiciosFaciales.split(",")
                        
                        longitudProductos = len(listaCodigosProductos)
                        longitudServiciosCorporales = len(listaIdsServiciosCorporales)
                        longitudServiciosFaciales = len(listaIdsServiciosFaciales)


                        listaProductos = zip(listaCodigosProductos,listaCantidadesProductos)
                        listaServiciosCorporales = zip(listaIdsServiciosCorporales, listaCantidadesServiciosCorporales)
                        listaServiciosFaciales = zip(listaIdsServiciosFaciales, listaCantidadesServiciosFaciales)

                        if longitudProductos >= 1:
                            for codigo, cantidad in listaProductos:
                                if codigo != "":
                                    strCodigo = str(codigo)
                                    strCantidad = str(cantidad)
                                    consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                                    for datoProductoVenta in consultaProductoVenta:
                                        nombreProducto = datoProductoVenta.nombre_producto
                                        costoIndividualProducto = datoProductoVenta.costo_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoIndividualProducto * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreProducto)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreProducto+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        if longitudServiciosCorporales >=1:
                            for idd, cantidad in listaServiciosCorporales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")

                        if longitudServiciosFaciales >=1:
                            for idd, cantidad in listaServiciosFaciales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        

                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")

                        if descuento == None:
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                            costoTotalPagarCredito = costoTotalAPagar
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago3)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                        else:
                            intDescuento = int(descuento)
                            consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                            for datoDescuento in consultaDescuentos:
                                nombreDescuento = datoDescuento.nombre_descuento
                                porcentajeDescuento = datoDescuento.porcentaje

                            porcentajePagado = 100 - porcentajeDescuento #85
                            totalSinDescuento1 = 100 * costoTotalAPagar
                            totalSinDescuento2 = totalSinDescuento1/porcentajePagado
                            totalSinDescuento2 = round(totalSinDescuento2)

                            primerMulti = porcentajeDescuento * float(totalSinDescuento2)
                            primerDivision = primerMulti/100
                            resultadoDescuento = round(primerDivision)
                            
                            costoTotalAPagarConDescuento = totalSinDescuento2 - resultadoDescuento

                            c.EstablecerTamañoFuente(1, 1)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("Subtotal:  $"+str(totalSinDescuento2)+"\n")
                            c.EscribirTexto("Descuento:  $"+str(resultadoDescuento)+"\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConDescuento)+"\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("Descuento aplicado: -"+str(porcentajeDescuento)+"%- "+str(nombreDescuento)+"\n")
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago3)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                            costoTotalPagarCredito = costoTotalAPagarConDescuento

                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                        c.EscribirTexto("\n")
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Pago en con tarjeta.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("Pago con "+str(tipo_tarjeta)+".\n")
                        c.EscribirTexto("Referencia: "+referencia_tarjeta+".\n")
                        c.EscribirTexto("Tercer pago recibido.\n")
                        c.EstablecerEnfatizado(False)
                        if restante == 0:
                            c.EscribirTexto("PAGO LIQUIDADO\n")
                        else:
                            restantePorPagar = float(restante)/2
                            restantePorPagar = round(restantePorPagar,2)
                            c.EscribirTexto("Abonos restantes de: $"+str(restantePorPagar)+" MXN.\n")
                            ahora = datetime.now()
                            fechaSegundoPago = ahora + timedelta(days=15)
                            fechaSegundoPago = fechaSegundoPago.strftime('%Y-%m-%d')
                            c.EscribirTexto("Cuarto pago el día: "+str(fechaSegundoPago)+".\n")
                        
                    
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                        if nombreClienteTicket == "Momentaneo":
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("Cliente momentaneo.\n")
                        else:
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                        c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        if contadorTickets == 1:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA TIENDA.\n")
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("________________________________________________\n")
                            c.EscribirTexto("Firma de cliente.\n")
                        else:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA CLIENTE.\n")
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        

                        c.Feed(1)
                        c.Corte(1)
                        #c.abrirCajon()
                        c.Pulso(48, 60, 120)
                        print("Imprimiendo...")
                        # Recuerda cambiar por el nombre de tu impresora
                        respuesta = c.imprimirEn("POS80 Printer")
                        if respuesta == True:
                            print("Impresión correcta")
                        else:
                            print(f"Error. El mensaje es: {respuesta}")
                    

            if esConTransferencia:
            
                registrarPago3 = PagosCreditos.objects.filter(id_historialCredito = idPagoCredito).update(fecha_pago3 = fechaPago1,tipo_pago3 ="Transferencia",clave_rastreo_pago_transferencia3=clave_transferencia,monto_pago3 =cantidadPago3) 
                
                if registrarPago3:
                    
                    
                    actualizarEstadoCredito = Creditos.objects.filter(id_credito = idCreditoAPagar).update(monto_pagado = actualMontoPagado,monto_restante =restante,estatus =estado) 
                    
                    #Fecha
                    hoy = datetime.now()
                    hoyFormato = hoy.strftime('%Y/%m/%d')

                    #Consulta de venta
                    consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                    for datoVenta in consultaVenta:
                        empleadoVendedor = datoVenta.empleado_vendedor_id
                        sucursal = datoVenta.sucursal_id
                        cliente = datoVenta.cliente_id
                    #Empleado vendedor
                    consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                    for datoVendedor in consultaEmpleadoVendedor:
                        nombreEmpleado = datoVendedor.nombres
                        apellidoPatEmpleado = datoVendedor.apellido_paterno

                    nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                    #Datos sucurssal
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        telefonoSucursal = datoSucursal.telefono
                        direccionSucursal = datoSucursal.direccion

                    
                    
                    
                    #Hora bien
                    horaVenta = horaVenta.strftime("%H:%M:%S")

                    # Esto es para obtener las impresoras. No es obligatorio hacerlo siempre que se quiera imprimir
                    impresoras = Conector.ConectorV3.obtenerImpresoras()
                    print(f"Las impresoras son: {impresoras}")
                    
                    contadorTickets = 0
                    for x in range(2):
                        contadorTickets = contadorTickets + 1

                        
                        c = Conector.ConectorV3()
                        c.Iniciar()
                        c.Corte(1)
                        
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        # Recuerda que la imagen debe existir y debe ser legible para el plugin. Si no, comenta las líneas
                        c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("TEL: "+telefonoSucursal+"\n")
                        c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")

                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("================================================\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EscribirTexto("PAGO DE VENTA #"+str(idVentaCredito)+"\n")
                        c.EscribirTexto("CRÉDITO #"+str(idCreditoAPagar)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        #Productos vendidos en ese credito

                        consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                        for datoVenta in consultaVenta:
                            codigosProductosVenta = datoVenta.ids_productos
                            cantidadesProductosVenta = datoVenta.cantidades_productos
                            idsServiciosCorporales = datoVenta.ids_servicios_corporales
                            cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                            idsServiciosFaciales = datoVenta.ids_servicios_faciales
                            cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                            descuento = datoVenta.descuento
                            costoTotalAPagar = datoVenta.monto_pagar
                            cliente = datoVenta.cliente_id

                        if cliente == None:
                            nombreClienteTicket = "Momentaneo"
                            idCienteTicket="Sin id"
                        else:
                            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                            for datoCliente in consultaCliente:
                                idCienteTicket = datoCliente.id_cliente
                                nombreCliente = datoCliente.nombre_cliente
                                apellidoCliente = datoCliente.apellidoPaterno_cliente
                            nombreClienteTicket = nombreCliente + " "+apellidoCliente
                            
                            

                        listaCodigosProductos = codigosProductosVenta.split(",")
                        listaCantidadesProductos = cantidadesProductosVenta.split(",")
                        listaIdsServiciosCorporales = idsServiciosCorporales.split(",")
                        listaCantidadesServiciosCorporales = cantidadServiciosCorporales.split(",")
                        listaIdsServiciosFaciales = idsServiciosFaciales.split(",")
                        listaCantidadesServiciosFaciales = cantidadServiciosFaciales.split(",")
                        
                        longitudProductos = len(listaCodigosProductos)
                        longitudServiciosCorporales = len(listaIdsServiciosCorporales)
                        longitudServiciosFaciales = len(listaIdsServiciosFaciales)


                        listaProductos = zip(listaCodigosProductos,listaCantidadesProductos)
                        listaServiciosCorporales = zip(listaIdsServiciosCorporales, listaCantidadesServiciosCorporales)
                        listaServiciosFaciales = zip(listaIdsServiciosFaciales, listaCantidadesServiciosFaciales)

                        if longitudProductos >= 1:
                            for codigo, cantidad in listaProductos:
                                if codigo != "":
                                    strCodigo = str(codigo)
                                    strCantidad = str(cantidad)
                                    consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                                    for datoProductoVenta in consultaProductoVenta:
                                        nombreProducto = datoProductoVenta.nombre_producto
                                        costoIndividualProducto = datoProductoVenta.costo_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoIndividualProducto * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreProducto)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreProducto+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        if longitudServiciosCorporales >=1:
                            for idd, cantidad in listaServiciosCorporales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")

                        if longitudServiciosFaciales >=1:
                            for idd, cantidad in listaServiciosFaciales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        

                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")

                        if descuento == None:
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                            costoTotalPagarCredito = costoTotalAPagar
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago3)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                        else:
                            intDescuento = int(descuento)
                            consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                            for datoDescuento in consultaDescuentos:
                                nombreDescuento = datoDescuento.nombre_descuento
                                porcentajeDescuento = datoDescuento.porcentaje

                            porcentajePagado = 100 - porcentajeDescuento #85
                            totalSinDescuento1 = 100 * costoTotalAPagar
                            totalSinDescuento2 = totalSinDescuento1/porcentajePagado
                            totalSinDescuento2 = round(totalSinDescuento2)

                            primerMulti = porcentajeDescuento * float(totalSinDescuento2)
                            primerDivision = primerMulti/100
                            resultadoDescuento = round(primerDivision)
                            
                            costoTotalAPagarConDescuento = totalSinDescuento2 - resultadoDescuento

                            c.EstablecerTamañoFuente(1, 1)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("Subtotal:  $"+str(totalSinDescuento2)+"\n")
                            c.EscribirTexto("Descuento:  $"+str(resultadoDescuento)+"\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConDescuento)+"\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("Descuento aplicado: -"+str(porcentajeDescuento)+"%- "+str(nombreDescuento)+"\n")
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago3)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                            costoTotalPagarCredito = costoTotalAPagarConDescuento

                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                        c.EscribirTexto("\n")
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Pago en con Transferencia.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("Transferencia.\n")
                        c.EscribirTexto("Clave de rastreo: "+str(clave_transferencia)+".\n")
                        c.EscribirTexto("Tercer pago recibido.\n")
                        c.EstablecerEnfatizado(False)
                        if restante == 0:
                            c.EscribirTexto("PAGO LIQUIDADO\n")
                        else:
                            restantePorPagar = float(restante)/2
                            restantePorPagar = round(restantePorPagar,2)
                            c.EscribirTexto("Abonos restantes de: $"+str(restantePorPagar)+" MXN.\n")
                            ahora = datetime.now()
                            fechaSegundoPago = ahora + timedelta(days=15)
                            fechaSegundoPago = fechaSegundoPago.strftime('%Y-%m-%d')
                            c.EscribirTexto("Cuarto pago el día: "+str(fechaSegundoPago)+".\n")
                        
                    
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                        if nombreClienteTicket == "Momentaneo":
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("Cliente momentaneo.\n")
                        else:
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                        c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        if contadorTickets == 1:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA TIENDA.\n")
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("________________________________________________\n")
                            c.EscribirTexto("Firma de cliente.\n")
                        else:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA CLIENTE.\n")
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        

                        c.Feed(1)
                        c.Corte(1)
                        #c.abrirCajon()
                        c.Pulso(48, 60, 120)
                        print("Imprimiendo...")
                        # Recuerda cambiar por el nombre de tu impresora
                        respuesta = c.imprimirEn("POS80 Printer")
                        if respuesta == True:
                            print("Impresión correcta")
                        else:
                            print(f"Error. El mensaje es: {respuesta}")

                

           
                    
                 
                            
                            
                            
            if actualizarEstadoCredito and registrarPago3:
                request.session['pago3Agregado'] = "Tercer pago de crédito Guardado correctamente!"
                return redirect('/verCreditosClientes/')
            else:
                request.session['pago3NoAgregado'] = "Error en la base de datos, intentelo más tarde.."
                return redirect('/verCreditosClientes/')
            
             
        

    else:
        return render(request,"1 Login/login.html")
    
    
    




def guardarPago4(request):
    if "idSesion" in request.session:
        # Variables de sesión
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        idPerfil = idEmpleado
        idConfig = idEmpleado
    
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']
        idEmpleado = request.session['idSesion']
        if request.method == "POST":
            
            
            

            idCreditoAPagar = request.POST['idCredito']
            idPagoCredito = request.POST['idPagoCredito']
            cantidadPago4 = request.POST['cantidadPago4']

            fechaPago4 = datetime.now()
            horaVenta= datetime.now().time()
             
            formaPago = request.POST['tipoPago'] #Efectivo,  tarjeta o transferencia
            
            datosCredito = Creditos.objects.filter(id_credito = idCreditoAPagar)
            for dato in datosCredito:
                montoTotalCredito = dato.monto_pagar
                montoRestante = dato.monto_restante
                montoPagado = dato.monto_pagado
                sucursal = dato.sucursal_id
                idVentaCredito = dato.venta_id

            floatCantidadPago4 = float(cantidadPago4)
            floatRestante = float(montoRestante)
                
                
           
                
            if floatCantidadPago4 == floatRestante:
                restante = 0
                estado = "Finalizado"
            
            else:
                restante = montoRestante - float(cantidadPago4)
                estado = "Pendiente"
                
            actualMontoPagado = float(montoPagado) + float(cantidadPago4)
                 
                    
            esConEfectivo = False
            esConTarjeta = False
            esConTransferencia = False

            if formaPago == "Efectivo":
                esConEfectivo = True
            elif formaPago == "Tarjeta":
                esConTarjeta = True
                tipo_tarjeta = request.POST['tipoTarjeta']    
                referencia_tarjeta = request.POST['referenciaTarjeta'] 
                        
            elif formaPago == "Transferencia":
                esConTransferencia = True
                clave_transferencia = request.POST['claveRastreoTransferencia'] 

                    


            if esConEfectivo:
                        
                registrarPago4 = PagosCreditos.objects.filter(id_historialCredito = idPagoCredito).update(fecha_pago4 = fechaPago4,tipo_pago4 ="Efectivo",monto_pago4 =cantidadPago4) 
                
                if registrarPago4:
                    
                    
                    actualizarEstadoCreditoPago4 = Creditos.objects.filter(id_credito = idCreditoAPagar).update(monto_pagado = actualMontoPagado,monto_restante =restante,estatus =estado) 
                    if actualizarEstadoCreditoPago4:
                         
                        tipoMovimiento ="IN"
                        montoMovimiento = float(cantidadPago4)
                        descripcionMovimiento ="Movimiento por abono de crédito " + str(idCreditoAPagar) 
                        fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                        horaMovimiento = datetime.now().time()
                        ingresarCantidadEfectivoAcaja =MovimientosCaja(fecha =fechaMovimiento,hora = horaMovimiento,tipo=tipoMovimiento,monto =montoMovimiento, descripcion=descripcionMovimiento,sucursal =  Sucursales.objects.get(id_sucursal = sucursal),
                                                                            realizado_por = Empleados.objects.get(id_empleado = idEmpleado))
                        ingresarCantidadEfectivoAcaja.save()

                         #IMPRESION DE TICKEEETSSSS

                        #Fecha
                        hoy = datetime.now()
                        hoyFormato = hoy.strftime('%Y/%m/%d')

                        #Consulta de venta
                        consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                        for datoVenta in consultaVenta:
                            empleadoVendedor = datoVenta.empleado_vendedor_id
                            sucursal = datoVenta.sucursal_id
                            cliente = datoVenta.cliente_id
                        #Empleado vendedor
                        consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                        for datoVendedor in consultaEmpleadoVendedor:
                            nombreEmpleado = datoVendedor.nombres
                            apellidoPatEmpleado = datoVendedor.apellido_paterno

                        nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                        #Datos sucurssal
                        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                        for datoSucursal in consultaSucursal:
                            nombreSucursal = datoSucursal.nombre
                            telefonoSucursal = datoSucursal.telefono
                            direccionSucursal = datoSucursal.direccion

                        
                        
                        
                        #Hora bien
                        horaVenta = horaVenta.strftime("%H:%M:%S")

                        # Esto es para obtener las impresoras. No es obligatorio hacerlo siempre que se quiera imprimir
                        impresoras = Conector.ConectorV3.obtenerImpresoras()
                        print(f"Las impresoras son: {impresoras}")
                        
                        contadorTickets = 0
                        for x in range(2):
                            contadorTickets = contadorTickets + 1

                            
                            c = Conector.ConectorV3()
                            c.Iniciar()
                            c.Corte(1)
                            
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            # Recuerda que la imagen debe existir y debe ser legible para el plugin. Si no, comenta las líneas
                            c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EstablecerEnfatizado(True)
                            c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("TEL: "+telefonoSucursal+"\n")
                            c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")

                            c.EstablecerEnfatizado(True)
                            c.EscribirTexto("================================================\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EscribirTexto("PAGO DE VENTA #"+str(idVentaCredito)+"\n")
                            c.EscribirTexto("CRÉDITO #"+str(idCreditoAPagar)+"\n")
                            c.EstablecerEnfatizado(False)
                            c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("\n")
                            c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                            c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                            c.EscribirTexto("\n")

                            #Listado de productos 
                            #Productos vendidos en ese credito

                            consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                            for datoVenta in consultaVenta:
                                codigosProductosVenta = datoVenta.ids_productos
                                cantidadesProductosVenta = datoVenta.cantidades_productos
                                idsServiciosCorporales = datoVenta.ids_servicios_corporales
                                cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                                idsServiciosFaciales = datoVenta.ids_servicios_faciales
                                cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                                descuento = datoVenta.descuento
                                costoTotalAPagar = datoVenta.monto_pagar
                                cliente = datoVenta.cliente_id

                            if cliente == None:
                                nombreClienteTicket = "Momentaneo"
                                idCienteTicket="Sin id"
                            else:
                                consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                                for datoCliente in consultaCliente:
                                    idCienteTicket = datoCliente.id_cliente
                                    nombreCliente = datoCliente.nombre_cliente
                                    apellidoCliente = datoCliente.apellidoPaterno_cliente
                                nombreClienteTicket = nombreCliente + " "+apellidoCliente
                                
                                

                            listaCodigosProductos = codigosProductosVenta.split(",")
                            listaCantidadesProductos = cantidadesProductosVenta.split(",")
                            listaIdsServiciosCorporales = idsServiciosCorporales.split(",")
                            listaCantidadesServiciosCorporales = cantidadServiciosCorporales.split(",")
                            listaIdsServiciosFaciales = idsServiciosFaciales.split(",")
                            listaCantidadesServiciosFaciales = cantidadServiciosFaciales.split(",")
                            
                            longitudProductos = len(listaCodigosProductos)
                            longitudServiciosCorporales = len(listaIdsServiciosCorporales)
                            longitudServiciosFaciales = len(listaIdsServiciosFaciales)


                            listaProductos = zip(listaCodigosProductos,listaCantidadesProductos)
                            listaServiciosCorporales = zip(listaIdsServiciosCorporales, listaCantidadesServiciosCorporales)
                            listaServiciosFaciales = zip(listaIdsServiciosFaciales, listaCantidadesServiciosFaciales)

                            if longitudProductos >= 1:
                                for codigo, cantidad in listaProductos:
                                    if codigo != "":
                                        strCodigo = str(codigo)
                                        strCantidad = str(cantidad)
                                        consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                                        for datoProductoVenta in consultaProductoVenta:
                                            nombreProducto = datoProductoVenta.nombre_producto
                                            costoIndividualProducto = datoProductoVenta.costo_venta

                                        floatCantidad = float(cantidad)
                                        costototalProducto = costoIndividualProducto * floatCantidad
                                        costototalProductoDosDecimales = round(costototalProducto, 2)
                                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                        longitudCostoTotal = int(longitudCostoTotal)

                                        
                                        caracteresProducto = len(nombreProducto)

                                        if longitudCostoTotal == 2:
                                            espacio = 38
                                        if longitudCostoTotal == 2:
                                            espacio = 37
                                        elif longitudCostoTotal == 3:
                                            espacio = 36
                                        elif longitudCostoTotal == 4:
                                            espacio = 35
                                        elif longitudCostoTotal == 5:
                                            espacio = 34
                                        elif longitudCostoTotal == 6:
                                            espacio = 33
                                        numeroEspacios = espacio - int(caracteresProducto)
                                        
                                        espaciosTicket = ""
                                        for x in range(numeroEspacios):
                                            espacioMini = " "
                                            espaciosTicket = espaciosTicket + espacioMini
                                        c.EscribirTexto(strCantidad+" x "+nombreProducto+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                            
                            if longitudServiciosCorporales >=1:
                                for idd, cantidad in listaServiciosCorporales:
                                    if idd != "":
                                        idServicio = int(idd)
                                        strCantidad = str(cantidad)
                                        consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                        for datoServicio in consultaServicio:
                                            nombreServicio = datoServicio.nombre_servicio
                                            costoServicio = datoServicio.precio_venta

                                        floatCantidad = float(cantidad)
                                        costototalProducto = costoServicio * floatCantidad
                                        costototalProductoDosDecimales = round(costototalProducto, 2)
                                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                        longitudCostoTotal = int(longitudCostoTotal)

                                        
                                        caracteresProducto = len(nombreServicio)

                                        if longitudCostoTotal == 2:
                                            espacio = 38
                                        if longitudCostoTotal == 2:
                                            espacio = 37
                                        elif longitudCostoTotal == 3:
                                            espacio = 36
                                        elif longitudCostoTotal == 4:
                                            espacio = 35
                                        elif longitudCostoTotal == 5:
                                            espacio = 34
                                        elif longitudCostoTotal == 6:
                                            espacio = 33
                                        numeroEspacios = espacio - int(caracteresProducto)
                                        
                                        espaciosTicket = ""
                                        for x in range(numeroEspacios):
                                            espacioMini = " "
                                            espaciosTicket = espaciosTicket + espacioMini
                                        c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")

                            if longitudServiciosFaciales >=1:
                                for idd, cantidad in listaServiciosFaciales:
                                    if idd != "":
                                        idServicio = int(idd)
                                        strCantidad = str(cantidad)
                                        consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                        for datoServicio in consultaServicio:
                                            nombreServicio = datoServicio.nombre_servicio
                                            costoServicio = datoServicio.precio_venta

                                        floatCantidad = float(cantidad)
                                        costototalProducto = costoServicio * floatCantidad
                                        costototalProductoDosDecimales = round(costototalProducto, 2)
                                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                        longitudCostoTotal = int(longitudCostoTotal)

                                        
                                        caracteresProducto = len(nombreServicio)

                                        if longitudCostoTotal == 2:
                                            espacio = 38
                                        if longitudCostoTotal == 2:
                                            espacio = 37
                                        elif longitudCostoTotal == 3:
                                            espacio = 36
                                        elif longitudCostoTotal == 4:
                                            espacio = 35
                                        elif longitudCostoTotal == 5:
                                            espacio = 34
                                        elif longitudCostoTotal == 6:
                                            espacio = 33
                                        numeroEspacios = espacio - int(caracteresProducto)
                                        
                                        espaciosTicket = ""
                                        for x in range(numeroEspacios):
                                            espacioMini = " "
                                            espaciosTicket = espaciosTicket + espacioMini
                                        c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                            
                            

                            c.EscribirTexto("\n")
                            c.EscribirTexto("\n")

                            if descuento == None:
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                                costoTotalPagarCredito = costoTotalAPagar
                                c.EscribirTexto("ABONADO: $"+str(cantidadPago4)+"\n")
                                c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                            else:
                                intDescuento = int(descuento)
                                consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                                for datoDescuento in consultaDescuentos:
                                    nombreDescuento = datoDescuento.nombre_descuento
                                    porcentajeDescuento = datoDescuento.porcentaje

                                porcentajePagado = 100 - porcentajeDescuento #85
                                totalSinDescuento1 = 100 * costoTotalAPagar
                                totalSinDescuento2 = totalSinDescuento1/porcentajePagado
                                totalSinDescuento2 = round(totalSinDescuento2)

                                primerMulti = porcentajeDescuento * float(totalSinDescuento2)
                                primerDivision = primerMulti/100
                                resultadoDescuento = round(primerDivision)
                                
                                costoTotalAPagarConDescuento = totalSinDescuento2 - resultadoDescuento

                                c.EstablecerTamañoFuente(1, 1)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("Subtotal:  $"+str(totalSinDescuento2)+"\n")
                                c.EscribirTexto("Descuento:  $"+str(resultadoDescuento)+"\n")
                                c.EstablecerTamañoFuente(2, 2)
                                c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConDescuento)+"\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("Descuento aplicado: -"+str(porcentajeDescuento)+"%- "+str(nombreDescuento)+"\n")
                                c.EscribirTexto("ABONADO: $"+str(cantidadPago4)+"\n")
                                c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                                costoTotalPagarCredito = costoTotalAPagarConDescuento

                            c.EscribirTexto("\n")
                            c.EstablecerEnfatizado(True)
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                            c.EscribirTexto("\n")
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("\n")
                            c.EstablecerEnfatizado(True)
                            c.EscribirTexto("Pago en efectivo.\n")
                            c.EscribirTexto("Cuarto pago recibido.\n")
                            c.EstablecerEnfatizado(False)
                            if restante == 0:
                                c.EscribirTexto("PAGO LIQUIDADO\n")
                            
                            
                        
                            c.EscribirTexto("\n")
                            c.EstablecerEnfatizado(True)
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                            if nombreClienteTicket == "Momentaneo":
                                c.EstablecerEnfatizado(False)
                                c.EscribirTexto("Cliente momentaneo.\n")
                            else:
                                c.EstablecerEnfatizado(False)
                                c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                            c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerEnfatizado(True)
                            c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                            if contadorTickets == 1:
                                c.EscribirTexto("\n")
                                c.EscribirTexto("COPIA TIENDA.\n")
                                c.EscribirTexto("\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("________________________________________________\n")
                                c.EscribirTexto("Firma de cliente.\n")
                            else:
                                c.EscribirTexto("\n")
                                c.EscribirTexto("COPIA CLIENTE.\n")
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            

                            c.Feed(1)
                            c.Corte(1)
                            #c.abrirCajon()
                            c.Pulso(48, 60, 120)
                            print("Imprimiendo...")
                            # Recuerda cambiar por el nombre de tu impresora
                            respuesta = c.imprimirEn("POS80 Printer")
                            if respuesta == True:
                                print("Impresión correcta")
                            else:
                                print(f"Error. El mensaje es: {respuesta}")
                
                

            if esConTarjeta:
                    
                        
                registrarPago4 = PagosCreditos.objects.filter(id_historialCredito = idPagoCredito).update(fecha_pago4 = fechaPago4,tipo_pago4="Tarjeta",tipo_tarjeta4=tipo_tarjeta,referencia_pago_tarjeta4=referencia_tarjeta,monto_pago4 =cantidadPago4) 
                
                if registrarPago4:
                    
                    
                    actualizarEstadoCreditoPago4 = Creditos.objects.filter(id_credito = idCreditoAPagar).update(monto_pagado = actualMontoPagado,monto_restante =restante,estatus =estado) 

                    #IMPRESION DE TICKEEETSSSS

                    #Fecha
                    hoy = datetime.now()
                    hoyFormato = hoy.strftime('%Y/%m/%d')

                    #Consulta de venta
                    consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                    for datoVenta in consultaVenta:
                        empleadoVendedor = datoVenta.empleado_vendedor_id
                        sucursal = datoVenta.sucursal_id
                        cliente = datoVenta.cliente_id
                    #Empleado vendedor
                    consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                    for datoVendedor in consultaEmpleadoVendedor:
                        nombreEmpleado = datoVendedor.nombres
                        apellidoPatEmpleado = datoVendedor.apellido_paterno

                    nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                    #Datos sucurssal
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        telefonoSucursal = datoSucursal.telefono
                        direccionSucursal = datoSucursal.direccion

                    
                    
                    
                    #Hora bien
                    horaVenta = horaVenta.strftime("%H:%M:%S")

                    # Esto es para obtener las impresoras. No es obligatorio hacerlo siempre que se quiera imprimir
                    impresoras = Conector.ConectorV3.obtenerImpresoras()
                    print(f"Las impresoras son: {impresoras}")
                    
                    contadorTickets = 0
                    for x in range(2):
                        contadorTickets = contadorTickets + 1

                        
                        c = Conector.ConectorV3()
                        c.Iniciar()
                        c.Corte(1)
                        
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        # Recuerda que la imagen debe existir y debe ser legible para el plugin. Si no, comenta las líneas
                        c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("TEL: "+telefonoSucursal+"\n")
                        c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")

                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("================================================\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EscribirTexto("PAGO DE VENTA #"+str(idVentaCredito)+"\n")
                        c.EscribirTexto("CRÉDITO #"+str(idCreditoAPagar)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        #Productos vendidos en ese credito

                        consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                        for datoVenta in consultaVenta:
                            codigosProductosVenta = datoVenta.ids_productos
                            cantidadesProductosVenta = datoVenta.cantidades_productos
                            idsServiciosCorporales = datoVenta.ids_servicios_corporales
                            cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                            idsServiciosFaciales = datoVenta.ids_servicios_faciales
                            cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                            descuento = datoVenta.descuento
                            costoTotalAPagar = datoVenta.monto_pagar
                            cliente = datoVenta.cliente_id

                        if cliente == None:
                            nombreClienteTicket = "Momentaneo"
                            idCienteTicket="Sin id"
                        else:
                            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                            for datoCliente in consultaCliente:
                                idCienteTicket = datoCliente.id_cliente
                                nombreCliente = datoCliente.nombre_cliente
                                apellidoCliente = datoCliente.apellidoPaterno_cliente
                            nombreClienteTicket = nombreCliente + " "+apellidoCliente
                            
                            

                        listaCodigosProductos = codigosProductosVenta.split(",")
                        listaCantidadesProductos = cantidadesProductosVenta.split(",")
                        listaIdsServiciosCorporales = idsServiciosCorporales.split(",")
                        listaCantidadesServiciosCorporales = cantidadServiciosCorporales.split(",")
                        listaIdsServiciosFaciales = idsServiciosFaciales.split(",")
                        listaCantidadesServiciosFaciales = cantidadServiciosFaciales.split(",")
                        
                        longitudProductos = len(listaCodigosProductos)
                        longitudServiciosCorporales = len(listaIdsServiciosCorporales)
                        longitudServiciosFaciales = len(listaIdsServiciosFaciales)


                        listaProductos = zip(listaCodigosProductos,listaCantidadesProductos)
                        listaServiciosCorporales = zip(listaIdsServiciosCorporales, listaCantidadesServiciosCorporales)
                        listaServiciosFaciales = zip(listaIdsServiciosFaciales, listaCantidadesServiciosFaciales)

                        if longitudProductos >= 1:
                            for codigo, cantidad in listaProductos:
                                if codigo != "":
                                    strCodigo = str(codigo)
                                    strCantidad = str(cantidad)
                                    consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                                    for datoProductoVenta in consultaProductoVenta:
                                        nombreProducto = datoProductoVenta.nombre_producto
                                        costoIndividualProducto = datoProductoVenta.costo_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoIndividualProducto * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreProducto)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreProducto+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        if longitudServiciosCorporales >=1:
                            for idd, cantidad in listaServiciosCorporales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")

                        if longitudServiciosFaciales >=1:
                            for idd, cantidad in listaServiciosFaciales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        

                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")

                        if descuento == None:
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                            costoTotalPagarCredito = costoTotalAPagar
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago4)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                        else:
                            intDescuento = int(descuento)
                            consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                            for datoDescuento in consultaDescuentos:
                                nombreDescuento = datoDescuento.nombre_descuento
                                porcentajeDescuento = datoDescuento.porcentaje

                            porcentajePagado = 100 - porcentajeDescuento #85
                            totalSinDescuento1 = 100 * costoTotalAPagar
                            totalSinDescuento2 = totalSinDescuento1/porcentajePagado
                            totalSinDescuento2 = round(totalSinDescuento2)

                            primerMulti = porcentajeDescuento * float(totalSinDescuento2)
                            primerDivision = primerMulti/100
                            resultadoDescuento = round(primerDivision)
                            
                            costoTotalAPagarConDescuento = totalSinDescuento2 - resultadoDescuento

                            c.EstablecerTamañoFuente(1, 1)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("Subtotal:  $"+str(totalSinDescuento2)+"\n")
                            c.EscribirTexto("Descuento:  $"+str(resultadoDescuento)+"\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConDescuento)+"\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("Descuento aplicado: -"+str(porcentajeDescuento)+"%- "+str(nombreDescuento)+"\n")
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago4)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                            costoTotalPagarCredito = costoTotalAPagarConDescuento

                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                        c.EscribirTexto("\n")
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Pago en con tarjeta.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("Pago con "+str(tipo_tarjeta)+".\n")
                        c.EscribirTexto("Referencia: "+referencia_tarjeta+".\n")
                        c.EscribirTexto("Cuarto pago recibido.\n")
                        c.EstablecerEnfatizado(False)
                        if restante == 0:
                            c.EscribirTexto("PAGO LIQUIDADO\n")
                       
                        
                    
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                        if nombreClienteTicket == "Momentaneo":
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("Cliente momentaneo.\n")
                        else:
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                        c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        if contadorTickets == 1:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA TIENDA.\n")
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("________________________________________________\n")
                            c.EscribirTexto("Firma de cliente.\n")
                        else:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA CLIENTE.\n")
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        

                        c.Feed(1)
                        c.Corte(1)
                        #c.abrirCajon()
                        c.Pulso(48, 60, 120)
                        print("Imprimiendo...")
                        # Recuerda cambiar por el nombre de tu impresora
                        respuesta = c.imprimirEn("POS80 Printer")
                        if respuesta == True:
                            print("Impresión correcta")
                        else:
                            print(f"Error. El mensaje es: {respuesta}")
                    

            if esConTransferencia:
            
                registrarPago4 = PagosCreditos.objects.filter(id_historialCredito = idPagoCredito).update(fecha_pago4 = fechaPago4,tipo_pago4 ="Transferencia",clave_rastreo_pago_transferencia4=clave_transferencia,monto_pago4 =cantidadPago4) 
                
                if registrarPago4:
                    
                    
                    actualizarEstadoCreditoPago4 = Creditos.objects.filter(id_credito = idCreditoAPagar).update(monto_pagado = actualMontoPagado,monto_restante =restante,estatus =estado) 


                     #Fecha
                    hoy = datetime.now()
                    hoyFormato = hoy.strftime('%Y/%m/%d')

                    #Consulta de venta
                    consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                    for datoVenta in consultaVenta:
                        empleadoVendedor = datoVenta.empleado_vendedor_id
                        sucursal = datoVenta.sucursal_id
                        cliente = datoVenta.cliente_id
                    #Empleado vendedor
                    consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                    for datoVendedor in consultaEmpleadoVendedor:
                        nombreEmpleado = datoVendedor.nombres
                        apellidoPatEmpleado = datoVendedor.apellido_paterno

                    nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                    #Datos sucurssal
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        telefonoSucursal = datoSucursal.telefono
                        direccionSucursal = datoSucursal.direccion

                    
                    
                    
                    #Hora bien
                    horaVenta = horaVenta.strftime("%H:%M:%S")

                    # Esto es para obtener las impresoras. No es obligatorio hacerlo siempre que se quiera imprimir
                    impresoras = Conector.ConectorV3.obtenerImpresoras()
                    print(f"Las impresoras son: {impresoras}")
                    
                    contadorTickets = 0
                    for x in range(2):
                        contadorTickets = contadorTickets + 1

                        
                        c = Conector.ConectorV3()
                        c.Iniciar()
                        c.Corte(1)
                        
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        # Recuerda que la imagen debe existir y debe ser legible para el plugin. Si no, comenta las líneas
                        c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("TEL: "+telefonoSucursal+"\n")
                        c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")

                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("================================================\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EscribirTexto("PAGO DE VENTA #"+str(idVentaCredito)+"\n")
                        c.EscribirTexto("CRÉDITO #"+str(idCreditoAPagar)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        #Productos vendidos en ese credito

                        consultaVenta = Ventas.objects.filter(id_venta = idVentaCredito)
                        for datoVenta in consultaVenta:
                            codigosProductosVenta = datoVenta.ids_productos
                            cantidadesProductosVenta = datoVenta.cantidades_productos
                            idsServiciosCorporales = datoVenta.ids_servicios_corporales
                            cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                            idsServiciosFaciales = datoVenta.ids_servicios_faciales
                            cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                            descuento = datoVenta.descuento
                            costoTotalAPagar = datoVenta.monto_pagar
                            cliente = datoVenta.cliente_id

                        if cliente == None:
                            nombreClienteTicket = "Momentaneo"
                            idCienteTicket="Sin id"
                        else:
                            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                            for datoCliente in consultaCliente:
                                idCienteTicket = datoCliente.id_cliente
                                nombreCliente = datoCliente.nombre_cliente
                                apellidoCliente = datoCliente.apellidoPaterno_cliente
                            nombreClienteTicket = nombreCliente + " "+apellidoCliente
                            
                            

                        listaCodigosProductos = codigosProductosVenta.split(",")
                        listaCantidadesProductos = cantidadesProductosVenta.split(",")
                        listaIdsServiciosCorporales = idsServiciosCorporales.split(",")
                        listaCantidadesServiciosCorporales = cantidadServiciosCorporales.split(",")
                        listaIdsServiciosFaciales = idsServiciosFaciales.split(",")
                        listaCantidadesServiciosFaciales = cantidadServiciosFaciales.split(",")
                        
                        longitudProductos = len(listaCodigosProductos)
                        longitudServiciosCorporales = len(listaIdsServiciosCorporales)
                        longitudServiciosFaciales = len(listaIdsServiciosFaciales)


                        listaProductos = zip(listaCodigosProductos,listaCantidadesProductos)
                        listaServiciosCorporales = zip(listaIdsServiciosCorporales, listaCantidadesServiciosCorporales)
                        listaServiciosFaciales = zip(listaIdsServiciosFaciales, listaCantidadesServiciosFaciales)

                        if longitudProductos >= 1:
                            for codigo, cantidad in listaProductos:
                                if codigo != "":
                                    strCodigo = str(codigo)
                                    strCantidad = str(cantidad)
                                    consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                                    for datoProductoVenta in consultaProductoVenta:
                                        nombreProducto = datoProductoVenta.nombre_producto
                                        costoIndividualProducto = datoProductoVenta.costo_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoIndividualProducto * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreProducto)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreProducto+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        if longitudServiciosCorporales >=1:
                            for idd, cantidad in listaServiciosCorporales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")

                        if longitudServiciosFaciales >=1:
                            for idd, cantidad in listaServiciosFaciales:
                                if idd != "":
                                    idServicio = int(idd)
                                    strCantidad = str(cantidad)
                                    consultaServicio = Servicios.objects.filter(id_servicio = idServicio)
                                    for datoServicio in consultaServicio:
                                        nombreServicio = datoServicio.nombre_servicio
                                        costoServicio = datoServicio.precio_venta

                                    floatCantidad = float(cantidad)
                                    costototalProducto = costoServicio * floatCantidad
                                    costototalProductoDosDecimales = round(costototalProducto, 2)
                                    costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                                    costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                                    longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                                    longitudCostoTotal = int(longitudCostoTotal)

                                    
                                    caracteresProducto = len(nombreServicio)

                                    if longitudCostoTotal == 2:
                                        espacio = 38
                                    if longitudCostoTotal == 2:
                                        espacio = 37
                                    elif longitudCostoTotal == 3:
                                        espacio = 36
                                    elif longitudCostoTotal == 4:
                                        espacio = 35
                                    elif longitudCostoTotal == 5:
                                        espacio = 34
                                    elif longitudCostoTotal == 6:
                                        espacio = 33
                                    numeroEspacios = espacio - int(caracteresProducto)
                                    
                                    espaciosTicket = ""
                                    for x in range(numeroEspacios):
                                        espacioMini = " "
                                        espaciosTicket = espaciosTicket + espacioMini
                                    c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")
                        
                        

                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")

                        if descuento == None:
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                            costoTotalPagarCredito = costoTotalAPagar
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago4)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                        else:
                            intDescuento = int(descuento)
                            consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                            for datoDescuento in consultaDescuentos:
                                nombreDescuento = datoDescuento.nombre_descuento
                                porcentajeDescuento = datoDescuento.porcentaje

                            porcentajePagado = 100 - porcentajeDescuento #85
                            totalSinDescuento1 = 100 * costoTotalAPagar
                            totalSinDescuento2 = totalSinDescuento1/porcentajePagado
                            totalSinDescuento2 = round(totalSinDescuento2)

                            primerMulti = porcentajeDescuento * float(totalSinDescuento2)
                            primerDivision = primerMulti/100
                            resultadoDescuento = round(primerDivision)
                            
                            costoTotalAPagarConDescuento = totalSinDescuento2 - resultadoDescuento

                            c.EstablecerTamañoFuente(1, 1)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("Subtotal:  $"+str(totalSinDescuento2)+"\n")
                            c.EscribirTexto("Descuento:  $"+str(resultadoDescuento)+"\n")
                            c.EstablecerTamañoFuente(2, 2)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConDescuento)+"\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("Descuento aplicado: -"+str(porcentajeDescuento)+"%- "+str(nombreDescuento)+"\n")
                            c.EscribirTexto("ABONADO: $"+str(cantidadPago4)+"\n")
                            c.EscribirTexto("RESTANTE: $"+str(restante)+"\n")
                            costoTotalPagarCredito = costoTotalAPagarConDescuento

                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                        c.EscribirTexto("\n")
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Pago en con Transferencia.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("Transferencia.\n")
                        c.EscribirTexto("Clave de rastreo: "+str(clave_transferencia)+".\n")
                        c.EscribirTexto("Cuarto pago recibido.\n")
                        c.EstablecerEnfatizado(False)
                        if restante == 0:
                            c.EscribirTexto("PAGO LIQUIDADO\n")
                        
                        
                    
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                        if nombreClienteTicket == "Momentaneo":
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("Cliente momentaneo.\n")
                        else:
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                        c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        if contadorTickets == 1:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA TIENDA.\n")
                            c.EscribirTexto("\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("________________________________________________\n")
                            c.EscribirTexto("Firma de cliente.\n")
                        else:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA CLIENTE.\n")
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1, 1)
                        

                        c.Feed(1)
                        c.Corte(1)
                        #c.abrirCajon()
                        c.Pulso(48, 60, 120)
                        print("Imprimiendo...")
                        # Recuerda cambiar por el nombre de tu impresora
                        respuesta = c.imprimirEn("POS80 Printer")
                        if respuesta == True:
                            print("Impresión correcta")
                        else:
                            print(f"Error. El mensaje es: {respuesta}") 

                

           
                    
                 
                            
                            
                            
            if actualizarEstadoCreditoPago4 and registrarPago4:
                request.session['pago4Agregado'] = "Pago de crédito Guardado correctamente!"
                return redirect('/verCreditosClientes/')
            else:
                request.session['pago4NoAgregado'] = "Error en la base de datos, intentelo más tarde.."
                return redirect('/verCreditosClientes/')
            
            
            

             
        

    else:
        return render(request,"1 Login/login.html")
    
    