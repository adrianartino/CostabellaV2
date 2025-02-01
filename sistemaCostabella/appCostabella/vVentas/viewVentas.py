
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

import json
# Librerías de fecha
from datetime import date, datetime, time, timedelta

#Plugin impresora termica
from appCostabella import Conector
# Importacion de modelos
from appCostabella.models import (Clientes, ConfiguracionCredito, Creditos, Descuentos,
                                  Empleados, 
                                  MovimientosCaja, PagosCreditos,
                                  PaquetesPromocionTratamientos, Permisos,
                                  ProductosGasto, ProductosRenta,
                                  ProductosVenta, Rentas, Servicios,
                                  ServiciosProductosGasto, Sucursales,
                                  Tratamientos, Ventas,)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)


def ventas(request):

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
        
        contadorVentasEfectivo = 0
        contadorVentasTarjeta = 0
        contadorVentasTransferencia = 0
        listaVentasEnEfectivoContador = Ventas.objects.filter(tipo_pago = "Efectivo")
        for contador in listaVentasEnEfectivoContador:
            contadorVentasEfectivo = contadorVentasEfectivo +1
            
            
        listaVentasEnTarjetaContador = Ventas.objects.filter(tipo_pago = "Tarjeta")
        for contador in listaVentasEnTarjetaContador:
            contadorVentasTarjeta = contadorVentasTarjeta +1
            
        listaVentasEnTransferenciaContador = Ventas.objects.filter(tipo_pago = "Transferencia")
        for contador in listaVentasEnTransferenciaContador:
            contadorVentasTransferencia = contadorVentasTransferencia +1
        
        #Consultas Todas las ventas.
        
        listaventasTotales = Ventas.objects.all()   #WTF AQUI xD
        quienVendio = [] #id, nombre y sucursal del empleado
        clientes = [] #Nombre
        sucursales = []
        #Descuentos
        booleanDescuento = []
        totalesSinDescuento = []
        descuentos = []
        datosDescuentos = []
        #Productos
        boolProductosVenta = []
        datosProductosVenta = []
        #Servicios Faciales
        boolServiciosCoorporales = []
        datosServiciosCoorporales = []
        #Servicios Corporales
        boolServiciosFaciales = []
        datosServiciosFaciales = []

        #Tratamientos
        boolTratamientos = []
        datosTratamientos = []

        #Paquetes tratamientos
        boolPaquetesTratamientos = []
        datosPaquetesTratamientos = []
        
        #Creditos 
        boolCredito = []
        idsCreditos = []
        boolPagado = []
        
        concepto = []
        contadorVenta = 0
        for venta in listaventasTotales:
            contadorVenta = contadorVenta+1
            idVenta = venta.id_venta
            empleado_vendedor = venta.empleado_vendedor_id
            cliente = venta.cliente_id
            sucursal = venta.sucursal_id
            descuento = venta.descuento_id
            monto_total_pagado = venta.monto_pagar
            codigosProductos = venta.ids_productos
            serviciosCorporales = venta.ids_servicios_corporales
            serviciosFaciales = venta.ids_servicios_faciales
            idTratamiento = venta.id_tratamiento_vendido_id
            idPaquete = venta.id_paquete_promo_vendido_id
            
            credito = venta.credito
            if credito == "N":
                boolCredito.append("Sin credito")
                idsCreditos.append("Sin credito")
                boolPagado.append("Sin credito")
            else:
                boolCredito.append("Si")
                consultaCredito = Creditos.objects.filter(venta_id__id_venta = idVenta)
                if consultaCredito:
                    for datoCredito in consultaCredito:
                        idCredito = datoCredito.id_credito
                        restante = datoCredito.monto_restante
                    idsCreditos.append(idCredito)
                    if restante == 0:
                        boolPagado.append("Si")
                    else:
                        boolPagado.append("No")
                else:
                    idsCreditos.append("error")
                    boolPagado.append("error")
                
            

            #Datos empleado vendedor
            consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleado_vendedor)
            for datoEmpleadoVendedor in consultaEmpleadoVendedor:
                idEmpleado = datoEmpleadoVendedor.id_empleado
                nombreEmpleado = datoEmpleadoVendedor.nombres
                
            quienVendio.append([idEmpleado, nombreEmpleado])

            #Datos cliente
            if cliente == None:
                clientes.append("Cliente Momentaneo")
            else:
                consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                for datoCliente in consultaCliente:
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoCliente = datoCliente.apellidoPaterno_cliente

                    nombreCompletoCliente = nombreCliente + " "+ apellidoCliente
                    clientes.append(nombreCompletoCliente)
                    
            #Datos sucursal 
            consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
            for datoSucursal in consultaSucursal:
                nombreSucursal = datoSucursal.nombre
            sucursales.append(nombreSucursal)
            
            #Datos descuento
            if descuento == None:
                booleanDescuento.append("Sin descuento")
                totalesSinDescuento.append("Total normal")
                descuentos.append("jeje")
                datosDescuentos.append("sin datos")
            else:
                booleanDescuento.append("Con descuento")
                consultaDescuento = Descuentos.objects.filter(id_descuento = descuento)
                
                for datoDescuento in consultaDescuento:
                    porcentaje = datoDescuento.porcentaje
                    nombreDescuento = datoDescuento.nombre_descuento
                datosDescuentos.append([porcentaje,nombreDescuento])

                intPorcentaje = int(porcentaje)
                    
                restaParaSaberCuantoSePago = 100 - intPorcentaje  #85
                
                restaConPunto = "."+str(restaParaSaberCuantoSePago) #.85
                
                costoReal = monto_total_pagado/float(restaConPunto) #376.470588
                
                costoRealRedondeado = round(costoReal)
                totalesSinDescuento.append(costoRealRedondeado)
                
                porcentajeDescuento = "."+str(intPorcentaje) #.15
                descuento = costoReal*float(porcentajeDescuento)
                
                descuentoRedondeado = round(descuento)
                descuentos.append(descuentoRedondeado)
                
             #Datos Productos comprados
            #if codigosProductos == "":
            if not codigosProductos:  # Verifica si codigosProductos es None o una cadena vacía    
                boolProductosVenta.append("Sin productos comprados")
                datosProductosVenta.append("Sin productos")
                concepto.append("Sin concepto")
            else:
                boolProductosVenta.append("Productos Comprados")
                cantidadesProductos = venta.cantidades_productos
                
                datosProductos = []
                arregloCodigos = codigosProductos.split(",")
                arregloCantidades = cantidadesProductos.split(",")
                listaProductosEfectivo = zip(arregloCodigos, arregloCantidades)
                for codigo, cantidad in listaProductosEfectivo:
                    codigoProducto = str(codigo)
                    cantidadProducto = str(cantidad)
                    if "PV" in codigoProducto:
                        concepto.append("Venta")
                        consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
                    else:
                        concepto.append("Renta")
                        consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigoProducto)
                    for datoProducto in consultaProducto:
                        nombrePro = datoProducto.nombre_producto
                        
                    consultaProducto= ProductosRenta.objects.filter(codigo_producto = codigoProducto)
                    for datoProducto in consultaProducto:
                        nombrePro = datoProducto.nombre_producto
                    
                    
                    datosProductos.append([codigoProducto,nombrePro,cantidadProducto])
                datosProductosVenta.append(datosProductos)

                
            #Datos Servicios Coorporales
            if not serviciosCorporales:
                boolServiciosCoorporales.append("Sin servicios coorporales")
                datosServiciosCoorporales.append("Sin productos")
            else:
                boolServiciosCoorporales.append("Servicios coorporales Comprados")
                cantidadesServiciosCorporales = venta.cantidades_servicios_corporales
                
                datosServiciosCorp = []
                arregloIdsServiciosCorporales = serviciosCorporales.split(",")
                arregloCantidadesServiciosCorporales = cantidadesServiciosCorporales.split(",")
                listaServiciosCorporalesEfectivo = zip(arregloIdsServiciosCorporales, arregloCantidadesServiciosCorporales)
                for idd, cantidad in listaServiciosCorporalesEfectivo:
                    intIdProducto = int(idd)
                    strIdProducto = str(idd)
                    cantidadProducto = str(cantidad)
                    consultaServicio = Servicios.objects.filter(id_servicio = intIdProducto)
                    for datoServicio in consultaServicio:
                        nombreServicio = datoServicio.nombre_servicio
                    
                    datosServiciosCorp.append([strIdProducto,nombreServicio,cantidadProducto])
                datosServiciosCoorporales.append(datosServiciosCorp)
                
            #Datos Servicios Faciales
            if not serviciosFaciales:
                boolServiciosFaciales.append("Sin servicios faciales")
                datosServiciosFaciales.append("Sin servicios")
            else:
                
                boolServiciosFaciales.append("Servicios coorporales Comprados")
                cantidadesServiciosFacialesEfectivo = venta.cantidades_servicios_faciales
                
                datosServicios = []
                arregloIdsServiciosFaciales = serviciosFaciales.split(",")
                arregloCantidadesServiciosFaciales = cantidadesServiciosFacialesEfectivo.split(",")
                listaServiciosFacialesEfectivo = zip(arregloIdsServiciosFaciales, arregloCantidadesServiciosFaciales)
                for idd, cantidad in listaServiciosFacialesEfectivo:
                    intIdProducto = int(idd)
                    strIdProducto = str(idd)
                    cantidadProducto = str(cantidad)
                    consultaServicio = Servicios.objects.filter(id_servicio = intIdProducto)
                    for datoServicio in consultaServicio:
                        nombreServicio = datoServicio.nombre_servicio
                    
                    datosServicios.append([strIdProducto,nombreServicio,cantidadProducto])
                datosServiciosFaciales.append(datosServicios)

            #DATOS TRATAMIENTO  
            if idTratamiento == None:
                boolTratamientos.append("Sin tratamiento")
                datosTratamientos.append("Sin tratamientos")
            else:
                boolTratamientos.append("Tratamiento comprado")
                consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)

                datosTratamiento1 = []
                for datoTratamiento in consultaTratamiento:
                    codigoTratamiento = datoTratamiento.codigo_tratamiento
                    tipoTratamiento = datoTratamiento.tipo_tratamiento
                    nombreTratamiento = datoTratamiento.nombre_tratamiento
                    datosTratamiento1.append([codigoTratamiento, tipoTratamiento, nombreTratamiento])
                datosTratamientos.append(datosTratamiento1)

            #datos paquete
            if idPaquete == None:
                boolPaquetesTratamientos.append("Sin paquete de tratamientos")
                datosPaquetesTratamientos.append("Sin paquete de tratamientos")
            else:
                boolPaquetesTratamientos.append("Paquete comprado")
                consultaPaquete = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idPaquete)

                datosPaquete = []
                for datoPaquete in consultaPaquete:
                    nombrePaquete = datoPaquete.nombre_paquete
                    sesionesPaquete = datoPaquete.numero_sesiones
                    precioPaquete = datoPaquete.precio_por_paquete 
                    datosPaquete.append([nombrePaquete, sesionesPaquete,precioPaquete])
                datosPaquetesTratamientos.append(datosPaquete)


        listaVentas = zip(listaventasTotales, quienVendio, clientes, sucursales, booleanDescuento,totalesSinDescuento, descuentos,datosDescuentos, boolProductosVenta,
         datosProductosVenta, boolServiciosCoorporales, datosServiciosCoorporales, boolServiciosFaciales, datosServiciosFaciales, boolCredito, idsCreditos,boolPagado,
          concepto,boolTratamientos,datosTratamientos, boolPaquetesTratamientos, datosPaquetesTratamientos)
        
       
       
        
        

        
        
        
        #Consultas EFECTIVOOOO 
        
        listaVentasEnEfectivo = Ventas.objects.filter(tipo_pago = "Efectivo")
        quienVendioEfectivo = [] #id, nombre y sucursal del empleado
        clienteEfectivo = [] #Nombre
        sucursalesEfectivo = []
        #Descuentos
        booleanDescuentoEfectivo = []
        totalesSinDescuentoEfectivo = []
        descuentosEfectivo = []
        datosDescuentosEfectivo = []
        #Productos
        boolProductosVentaEfectivo = []
        datosProductosVentaEfectivo = []
        #Servicios Faciales
        boolServiciosCoorporalesEfectivo = []
        datosServiciosCoorporalesEfectivo = []
        #Servicios Corporales
        boolServiciosFacialesEfectivo = []
        datosServiciosFacialesEfectivo = []
        #Tratamientos
        boolTratamientosEfectivo = []
        datosTratamientosEfectivo = []

        #PaquetesTratamientos
        boolPaquetesTratamientosEfectivo = []
        datosPaquetesTratamientosEfectivo = []
        
        #Creditos 
        boolCreditoEfectivo = []
        idsCreditosEfectivo = []
        boolPagadoEfectivo = []
        
        for ventaEfectivo in listaVentasEnEfectivo:
            idVenta = ventaEfectivo.id_venta
            empleado_vendedor = ventaEfectivo.empleado_vendedor_id
            cliente = ventaEfectivo.cliente_id
            sucursal = ventaEfectivo.sucursal_id
            descuento = ventaEfectivo.descuento_id
            monto_total_pagado = ventaEfectivo.monto_pagar
            codigosProductos = ventaEfectivo.ids_productos
            serviciosCorporales = ventaEfectivo.ids_servicios_corporales
            serviciosFaciales = ventaEfectivo.ids_servicios_faciales
            idTratamiento = ventaEfectivo.id_tratamiento_vendido_id
            idPaquete = ventaEfectivo.id_paquete_promo_vendido_id

            
            credito = ventaEfectivo.credito
            if credito == "N":
                boolCreditoEfectivo.append("Sin credito")
                idsCreditosEfectivo.append("Sin credito")
                boolPagadoEfectivo.append("Sin credito")
            else:
                boolCreditoEfectivo.append("Si")
                consultaCredito = Creditos.objects.filter(venta_id__id_venta = idVenta)
                if consultaCredito:
                    for datoCredito in consultaCredito:
                        idCredito = datoCredito.id_credito
                        restante = datoCredito.monto_restante
                    idsCreditosEfectivo.append(idCredito)
                    if restante == 0:
                        boolPagadoEfectivo.append("Si")
                    else:
                        boolPagadoEfectivo.append("No")
                else:
                    idsCreditosEfectivo.append("error")
                
            

            #Datos empleado vendedor
            consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleado_vendedor)
            for datoEmpleadoVendedor in consultaEmpleadoVendedor:
                idEmpleado = datoEmpleadoVendedor.id_empleado
                nombreEmpleado = datoEmpleadoVendedor.nombres
                
            quienVendioEfectivo.append([idEmpleado, nombreEmpleado])

            #Datos cliente
            if cliente == None:
                clienteEfectivo.append("Cliente Momentaneo")
            else:
                consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                for datoCliente in consultaCliente:
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoCliente = datoCliente.apellidoPaterno_cliente

                    nombreCompletoCliente = nombreCliente + " "+ apellidoCliente
                    clienteEfectivo.append(nombreCompletoCliente)
                    
            #Datos sucursal 
            consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
            for datoSucursal in consultaSucursal:
                nombreSucursal = datoSucursal.nombre
            sucursalesEfectivo.append(nombreSucursal)
            
            #Datos descuento
            if descuento == None:
                booleanDescuentoEfectivo.append("Sin descuento")
                totalesSinDescuentoEfectivo.append("Total normal")
                descuentosEfectivo.append("jeje")
                datosDescuentosEfectivo.append("sin datos")
            else:
                booleanDescuentoEfectivo.append("Con descuento")
                consultaDescuento = Descuentos.objects.filter(id_descuento = descuento)
                
                for datoDescuento in consultaDescuento:
                    porcentaje = datoDescuento.porcentaje
                    nombreDescuento = datoDescuento.nombre_descuento
                datosDescuentosEfectivo.append([porcentaje,nombreDescuento])

                intPorcentaje = int(porcentaje)
                    
                restaParaSaberCuantoSePago = 100 - intPorcentaje  #85
                
                restaConPunto = "."+str(restaParaSaberCuantoSePago) #.85
                
                costoReal = monto_total_pagado/float(restaConPunto) #376.470588
                
                costoRealRedondeado = round(costoReal)
                totalesSinDescuentoEfectivo.append(costoRealRedondeado)
                
                porcentajeDescuento = "."+str(intPorcentaje) #.15
                descuento = costoReal*float(porcentajeDescuento)
                
                descuentoRedondeado = round(descuento)
                descuentosEfectivo.append(descuentoRedondeado)
                
            #Datos Productos comprados
            if not codigosProductos:
                boolProductosVentaEfectivo.append("Sin productos comprados")
                datosProductosVentaEfectivo.append("Sin productos")
            else:
                boolProductosVentaEfectivo.append("Productos Comprados")
                cantidadesProductos = ventaEfectivo.cantidades_productos
                
                datosProductos = []
                arregloCodigos = codigosProductos.split(",")
                arregloCantidades = cantidadesProductos.split(",")
                listaProductosEfectivo = zip(arregloCodigos, arregloCantidades)
                for codigo, cantidad in listaProductosEfectivo:
                    codigoProducto = str(codigo)
                    cantidadProducto = str(cantidad)
                    consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
                    for datoProducto in consultaProducto:
                        nombrePro = datoProducto.nombre_producto
                        
                    consultaProducto= ProductosRenta.objects.filter(codigo_producto = codigoProducto)
                    for datoProducto in consultaProducto:
                        nombrePro = datoProducto.nombre_producto
                    
                    
                    datosProductos.append([codigoProducto,nombrePro,cantidadProducto])
                datosProductosVentaEfectivo.append(datosProductos)
                
            #Datos Servicios Coorporales
            if  not serviciosCorporales:
                boolServiciosCoorporalesEfectivo.append("Sin servicios coorporales")
                datosServiciosCoorporalesEfectivo.append("Sin productos")
            else:
                boolServiciosCoorporalesEfectivo.append("Servicios coorporales Comprados")
                cantidadesServiciosCorporales = ventaEfectivo.cantidades_servicios_corporales
                
                datosServicios = []
                arregloIdsServiciosCorporales = serviciosCorporales.split(",")
                arregloCantidadesServiciosCorporales = cantidadesServiciosCorporales.split(",")
                listaServiciosCorporalesEfectivo = zip(arregloIdsServiciosCorporales, arregloCantidadesServiciosCorporales)
                for idd, cantidad in listaServiciosCorporalesEfectivo:
                    intIdProducto = int(idd)
                    strIdProducto = str(idd)
                    cantidadProducto = str(cantidad)
                    consultaServicio = Servicios.objects.filter(id_servicio = intIdProducto)
                    for datoServicio in consultaServicio:
                        nombreServicio = datoServicio.nombre_servicio
                    
                    datosServicios.append([strIdProducto,nombreServicio,cantidadProducto])
                datosServiciosCoorporalesEfectivo.append(datosServicios)
                
            #Datos Servicios Faciales
            if not serviciosFaciales:
                boolServiciosFacialesEfectivo.append("Sin servicios faciales")
                datosServiciosFacialesEfectivo.append("Sin servicios")
            else:
                boolServiciosFacialesEfectivo.append("Servicios coorporales Comprados")
                cantidadesServiciosFacialesEfectivo = ventaEfectivo.cantidades_servicios_faciales
                
                datosServicios = []
                arregloIdsServiciosFaciales = serviciosFaciales.split(",")
                arregloCantidadesServiciosFaciales = cantidadesServiciosFacialesEfectivo.split(",")
                listaServiciosFacialesEfectivo = zip(arregloIdsServiciosCorporales, arregloCantidadesServiciosCorporales)
                for idd, cantidad in listaServiciosFacialesEfectivo:
                    intIdProducto = int(idd)
                    strIdProducto = str(idd)
                    cantidadProducto = str(cantidad)
                    consultaServicio = Servicios.objects.filter(id_servicio = intIdProducto)
                    for datoServicio in consultaServicio:
                        nombreServicio = datoServicio.nombre_servicio
                    
                    datosServicios.append([strIdProducto,nombreServicio,cantidadProducto])
                datosServiciosFacialesEfectivo.append(datosServicios)
            
            #DATOS TRATAMIENTO  
            if idTratamiento == None:
                boolTratamientosEfectivo.append("Sin tratamiento")
                datosTratamientosEfectivo.append("Sin tratamientos")
            else:
                boolTratamientosEfectivo.append("Tratamiento comprado")
                consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)

                datosTratamiento1 = []
                for datoTratamiento in consultaTratamiento:
                    codigoTratamiento = datoTratamiento.codigo_tratamiento
                    tipoTratamiento = datoTratamiento.tipo_tratamiento
                    nombreTratamiento = datoTratamiento.nombre_tratamiento
                    datosTratamiento1.append([codigoTratamiento, tipoTratamiento, nombreTratamiento])
                datosTratamientosEfectivo.append(datosTratamiento1)

            #datos paquete
            if idPaquete == None:
                boolPaquetesTratamientosEfectivo.append("Sin paquete de tratamientos")
                datosPaquetesTratamientosEfectivo.append("Sin paquete de tratamientos")
            else:
                boolPaquetesTratamientosEfectivo.append("Paquete comprado")
                consultaPaquete = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idPaquete)

                datosPaquete = []
                for datoPaquete in consultaPaquete:
                    nombrePaquete = datoPaquete.nombre_paquete
                    sesionesPaquete = datoPaquete.numero_sesiones
                    precioPaquete = datoPaquete.precio_por_paquete 
                    datosPaquete.append([nombrePaquete, sesionesPaquete,precioPaquete])
                datosPaquetesTratamientosEfectivo.append(datosPaquete)


        listaEfectivo = zip(listaVentasEnEfectivo, quienVendioEfectivo, clienteEfectivo, sucursalesEfectivo, booleanDescuentoEfectivo,totalesSinDescuentoEfectivo, descuentosEfectivo,datosDescuentosEfectivo, boolProductosVentaEfectivo, datosProductosVentaEfectivo, boolServiciosCoorporalesEfectivo, datosServiciosCoorporalesEfectivo, boolServiciosFacialesEfectivo, datosServiciosFacialesEfectivo,
        boolTratamientosEfectivo,datosTratamientosEfectivo,boolPaquetesTratamientosEfectivo,datosPaquetesTratamientosEfectivo)
            

        #Consultas TARJETA
        
        listaVentasConTarjeta = Ventas.objects.filter(tipo_pago = "Tarjeta")
        quienVendioTarjeta = [] #id, nombre y sucursal del empleado
        listaClientesTarjeta = [] #Nombre
        sucursalesTarjeta = []
        tiposTarjetas = []
        referencias = []
        #Descuentos
        booleanDescuentoTarjeta = []
        totalesSinDescuentoTarjeta = []
        descuentosTarjeta = []
        datosDescuentosTarjeta= []
        #Productos
        boolProductosVentaTarjeta = []
        datosProductosVentaTarjeta = []
        #Servicios Faciales
        boolServiciosCoorporalesTarjeta = []
        datosServiciosCoorporalesTarjeta = []
        #Servicios Corporales
        boolServiciosFacialesTarjeta = []
        datosServiciosFacialesTarjeta = []
        #Tratamientos
        boolTratamientosTarjeta = []
        datosTratamientosTarjeta = []

        #PaquetesTratamientos
        boolPaquetesTratamientosTarjeta = []
        datosPaquetesTratamientosTarjeta = []
        
        for ventaTarjeta in listaVentasConTarjeta:
            empleado_vendedorTarjeta = ventaTarjeta.empleado_vendedor_id
            clienteTarjeta = ventaTarjeta.cliente_id
            sucursalTarjeta  = ventaTarjeta.sucursal_id
            tipoTarjeta = ventaTarjeta.tipo_tarjeta
            referenciaTarjeta = ventaTarjeta.referencia_pago_tarjeta
            descuentoTarjeta  = ventaTarjeta.descuento_id
            monto_total_pagadoTarjeta  = ventaTarjeta.monto_pagar
            codigosProductosTarjeta  = ventaTarjeta.ids_productos
            serviciosCorporalesTarjeta  = ventaTarjeta.ids_servicios_corporales
            serviciosFacialesTarjeta  = ventaTarjeta.ids_servicios_faciales
            idTratamiento = ventaTarjeta.id_tratamiento_vendido_id
            idPaquete = ventaTarjeta.id_paquete_promo_vendido_id
            

            #Datos empleado vendedor
            consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleado_vendedorTarjeta)
            for datoEmpleadoVendedor in consultaEmpleadoVendedor:
                idEmpleado = datoEmpleadoVendedor.id_empleado
                nombreEmpleado = datoEmpleadoVendedor.nombres
                
            quienVendioTarjeta.append([idEmpleado, nombreEmpleado])
            
            tiposTarjetas.append(tipoTarjeta)
            referencias.append(referenciaTarjeta)
            

            #Datos cliente
            if clienteTarjeta == None:
                listaClientesTarjeta.append("Cliente Momentaneo")
            else:
                consultaCliente = Clientes.objects.filter(id_cliente = clienteTarjeta)
                for datoCliente in consultaCliente:
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoCliente = datoCliente.apellidoPaterno_cliente

                    nombreCompletoCliente = nombreCliente + " "+ apellidoCliente
                    listaClientesTarjeta.append(nombreCompletoCliente)
                    
            #Datos sucursal 
            consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalTarjeta)
            for datoSucursal in consultaSucursal:
                nombreSucursal = datoSucursal.nombre
            sucursalesTarjeta.append(nombreSucursal)
            
            #Datos descuento
            if descuentoTarjeta == None:
                booleanDescuentoTarjeta.append("Sin descuento")
                totalesSinDescuentoTarjeta.append("Total normal")
                descuentosTarjeta.append("jeje")
                datosDescuentosTarjeta.append("nada")
            else:
                booleanDescuentoTarjeta.append("Con descuento")
                consultaDescuento = Descuentos.objects.filter(id_descuento = descuentoTarjeta)
                
                for datoDescuento in consultaDescuento:
                    porcentaje = datoDescuento.porcentaje
                    nombreDescuento = datoDescuento.nombre_descuento
                datosDescuentosTarjeta.append([porcentaje,nombreDescuento])
                intPorcentaje = int(porcentaje)
                    
                restaParaSaberCuantoSePago = 100 - intPorcentaje  #85
                
                restaConPunto = "."+str(restaParaSaberCuantoSePago) #.85
                
                costoReal = monto_total_pagadoTarjeta/float(restaConPunto) #376.470588
                
                costoRealRedondeado = round(costoReal)
                totalesSinDescuentoTarjeta.append(costoRealRedondeado)
                
                porcentajeDescuento = "."+str(intPorcentaje) #.15
                descuento = costoReal*float(porcentajeDescuento)
                
                descuentoRedondeado = round(descuento)
                descuentosTarjeta.append(descuentoRedondeado)
                
            #Datos Productos comprados
            if codigosProductosTarjeta == "":
                boolProductosVentaTarjeta.append("Sin productos comprados")
                datosProductosVentaTarjeta.append("Sin productos")
            else:
                boolProductosVentaTarjeta.append("Productos Comprados")
                cantidadesProductos = ventaTarjeta.cantidades_productos
                
                datosProductosTarjeta = []
                arregloCodigosTarjetas = codigosProductosTarjeta.split(",")
                arregloCantidadestarjetas = cantidadesProductos.split(",")
                listaProductosTarjeta = zip(arregloCodigosTarjetas, arregloCantidadestarjetas)
                for codigoT, cantidadT in listaProductosTarjeta:
                    codigoProductoTarjeta = str(codigoT)
                    cantidadProductoTarjeta = str(cantidadT)
                    consultaProductotarjeta = ProductosVenta.objects.filter(codigo_producto = codigoProductoTarjeta)
                    for datoProducto in consultaProductotarjeta:
                        nombreProTarjeta = datoProducto.nombre_producto
                        
                    consultaProductotarjeta = ProductosRenta.objects.filter(codigo_producto = codigoProductoTarjeta)
                    for datoProducto in consultaProductotarjeta:
                        nombreProTarjeta = datoProducto.nombre_producto
                    
                    datosProductosTarjeta.append([codigoProductoTarjeta,nombreProTarjeta,cantidadProductoTarjeta])
                datosProductosVentaTarjeta.append(datosProductosTarjeta)
                
            #Datos Servicios Coorporales
            if serviciosCorporalesTarjeta == "":
                boolServiciosCoorporalesTarjeta.append("Sin servicios coorporales")
                datosServiciosCoorporalesTarjeta.append("Sin productos")
            else:
                boolServiciosCoorporalesTarjeta.append("Servicios coorporales Comprados")
                cantidadesServiciosCorporales = ventaTarjeta.cantidades_servicios_corporales
                
                datosServicios = []
                arregloIdsServiciosCorporales = serviciosCorporalesTarjeta.split(",")
                arregloCantidadesServiciosCorporales = cantidadesServiciosCorporales.split(",")
                listaServiciosCorporalesTarjeta = zip(arregloIdsServiciosCorporales, arregloCantidadesServiciosCorporales)
                for idd, cantidad in listaServiciosCorporalesTarjeta:
                    intIdProducto = int(idd)
                    strIdProducto = str(idd)
                    cantidadProducto = str(cantidad)
                    consultaServicio = Servicios.objects.filter(id_servicio = intIdProducto)
                    for datoServicio in consultaServicio:
                        nombreServicio = datoServicio.nombre_servicio
                    
                    datosServicios.append([strIdProducto,nombreServicio,cantidadProducto])
                datosServiciosCoorporalesTarjeta.append(datosServicios)
                
            #Datos Servicios Faciales
            if serviciosFacialesTarjeta == "":
                boolServiciosFacialesTarjeta.append("Sin servicios faciales")
                datosServiciosFacialesTarjeta.append("Sin servicios")
            else:
                boolServiciosFacialesTarjeta.append("Servicios coorporales Comprados")
                cantidadesServiciosFaciales = ventaTarjeta.cantidades_servicios_faciales
                
                datosServicios = []
                arregloIdsServiciosFaciales = serviciosFacialesTarjeta.split(",")
                arregloCantidadesServiciosFaciales = cantidadesServiciosFaciales.split(",")
                listaServiciosFacialesTarjeta = zip(arregloIdsServiciosFaciales, arregloCantidadesServiciosFaciales)
                for idd, cantidad in listaServiciosFacialesTarjeta:
                    intIdProducto = int(idd)
                    strIdProducto = str(idd)
                    cantidadProducto = str(cantidad)
                    consultaServicio = Servicios.objects.filter(id_servicio = intIdProducto)
                    for datoServicio in consultaServicio:
                        nombreServicio = datoServicio.nombre_servicio
                    
                    datosServicios.append([strIdProducto,nombreServicio,cantidadProducto])
                datosServiciosFacialesTarjeta.append(datosServicios)
                
            #DATOS TRATAMIENTO  
            if idTratamiento == None:
                boolTratamientosTarjeta.append("Sin tratamiento")
                datosTratamientosTarjeta.append("Sin tratamientos")
            else:
                boolTratamientosTarjeta.append("Tratamiento comprado")
                consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)

                datosTratamiento1 = []
                for datoTratamiento in consultaTratamiento:
                    codigoTratamiento = datoTratamiento.codigo_tratamiento
                    tipoTratamiento = datoTratamiento.tipo_tratamiento
                    nombreTratamiento = datoTratamiento.nombre_tratamiento
                    datosTratamiento1.append([codigoTratamiento, tipoTratamiento, nombreTratamiento])
                datosTratamientosTarjeta.append(datosTratamiento1)

            #datos paquete
            if idPaquete == None:
                boolPaquetesTratamientosTarjeta.append("Sin paquete de tratamientos")
                datosPaquetesTratamientosTarjeta.append("Sin paquete de tratamientos")
            else:
                boolPaquetesTratamientosTarjeta.append("Paquete comprado")
                consultaPaquete = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idPaquete)

                datosPaquete = []
                for datoPaquete in consultaPaquete:
                    nombrePaquete = datoPaquete.nombre_paquete
                    sesionesPaquete = datoPaquete.numero_sesiones
                    precioPaquete = datoPaquete.precio_por_paquete 
                    datosPaquete.append([nombrePaquete, sesionesPaquete,precioPaquete])
                datosPaquetesTratamientosTarjeta.append(datosPaquete)


        listatarjeta = zip(listaVentasConTarjeta, quienVendioTarjeta, listaClientesTarjeta, sucursalesTarjeta,tiposTarjetas,referencias,booleanDescuentoTarjeta, totalesSinDescuentoTarjeta, descuentosTarjeta,datosDescuentosTarjeta, boolProductosVentaTarjeta, datosProductosVentaTarjeta, boolServiciosCoorporalesTarjeta, datosServiciosCoorporalesTarjeta, boolServiciosFacialesTarjeta, datosServiciosFacialesTarjeta,
        boolTratamientosTarjeta, datosTratamientosTarjeta, boolPaquetesTratamientosTarjeta, datosPaquetesTratamientosTarjeta)

        #Consultas TRANSFERENCIA
        
        listaVentasConTransferencia = Ventas.objects.filter(tipo_pago = "Transferencia")
        quienVendioTransferencia = [] #id, nombre y sucursal del empleado
        listaClientesTransferencia = [] #Nombre
        sucursalesTransferencia = []
        
        clavesRastreo = []
        #Descuentos
        booleanDescuentoTransferencia = []
        totalesSinDescuentoTransferencia = []
        descuentosTransferencia = []
        datosDescuentosTransferencia = []
        #Productos
        boolProductosVentaTransferencia = []
        datosProductosVentaTransferencia = []
        #Servicios Faciales
        boolServiciosCoorporalesTransferencia = []
        datosServiciosCoorporalesTransferencia = []
        #Servicios Corporales
        boolServiciosFacialesTransferencia = []
        datosServiciosFacialesTransferencia = []
        #Tratamientos
        boolTratamientosTransferencia = []
        datosTratamientosTransferencia = []

        #PaquetesTratamientos
        boolPaquetesTratamientosTransferencia = []
        datosPaquetesTratamientosTransferencia = []

        
        for ventaTransferencia in listaVentasConTransferencia:
            empleado_vendedorTransferencia = ventaTransferencia.empleado_vendedor_id
            clienteTransferencia = ventaTransferencia.cliente_id
            sucursalTransferencia  = ventaTransferencia.sucursal_id
           
            claveRastreoTransferencia = ventaTransferencia.clave_rastreo_transferencia
            descuentoTransferencia  = ventaTransferencia.descuento_id
            monto_total_pagadoTransferencia  = ventaTransferencia.monto_pagar
            codigosProductosTransferencia  = ventaTransferencia.ids_productos
            serviciosCorporalesTransferencia  = ventaTransferencia.ids_servicios_corporales
            serviciosFacialesTransferencia  = ventaTransferencia.ids_servicios_faciales
            idTratamiento = ventaTransferencia.id_tratamiento_vendido_id
            idPaquete = ventaTransferencia.id_paquete_promo_vendido_id
            

            #Datos empleado vendedor
            consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleado_vendedorTransferencia)
            for datoEmpleadoVendedor in consultaEmpleadoVendedor:
                idEmpleado = datoEmpleadoVendedor.id_empleado
                nombreEmpleado = datoEmpleadoVendedor.nombres
                
            quienVendioTransferencia.append([idEmpleado, nombreEmpleado])
            
         
            clavesRastreo.append(claveRastreoTransferencia)
            

            #Datos cliente
            if clienteTransferencia == None:
                listaClientesTransferencia.append("Cliente Momentaneo")
            else:
                consultaCliente = Clientes.objects.filter(id_cliente = clienteTransferencia)
                for datoCliente in consultaCliente:
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoCliente = datoCliente.apellidoPaterno_cliente

                    nombreCompletoCliente = nombreCliente + " "+ apellidoCliente
                    listaClientesTransferencia.append(nombreCompletoCliente)
                    
            #Datos sucursal 
            consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalTransferencia)
            for datoSucursal in consultaSucursal:
                nombreSucursal = datoSucursal.nombre
            sucursalesTransferencia.append(nombreSucursal)
            
            #Datos descuento
            if descuentoTransferencia == None:
                booleanDescuentoTransferencia.append("Sin descuento")
                totalesSinDescuentoTransferencia.append("Total normal")
                descuentosTransferencia.append("jeje")
                datosDescuentosTransferencia.append("nada")
            else:
                booleanDescuentoTransferencia.append("Con descuento")
                consultaDescuento = Descuentos.objects.filter(id_descuento = descuentoTransferencia)
                
                for datoDescuento in consultaDescuento:
                    porcentaje = datoDescuento.porcentaje
                    nombreDescuento = datoDescuento.nombre_descuento
                datosDescuentosTransferencia.append([porcentaje,nombreDescuento])
                intPorcentaje = int(porcentaje)
                    
                restaParaSaberCuantoSePago = 100 - intPorcentaje  #85
                
                restaConPunto = "."+str(restaParaSaberCuantoSePago) #.85
                
                costoReal = monto_total_pagadoTarjeta/float(restaConPunto) #376.470588
                
                costoRealRedondeado = round(costoReal)
                totalesSinDescuentoTransferencia.append(costoRealRedondeado)
                
                porcentajeDescuento = "."+str(intPorcentaje) #.15
                descuento = costoReal*float(porcentajeDescuento)
                
                descuentoRedondeado = round(descuento)
                descuentosTransferencia.append(descuentoRedondeado)
                
            #Datos Productos comprados
            if codigosProductosTransferencia == "":
                boolProductosVentaTransferencia.append("Sin productos comprados")
                datosProductosVentaTransferencia.append("Sin productos")
            else:
                boolProductosVentaTransferencia.append("Productos Comprados")
                cantidadesProductosTransferencia = ventaTransferencia.cantidades_productos
                
                datosProductosTransferencia = []
                arregloCodigosTransferencia = codigosProductosTransferencia.split(",")
                arregloCantidadesTransferencia = cantidadesProductosTransferencia.split(",")
                listaProductosTransferencia = zip(arregloCodigosTransferencia, arregloCantidadesTransferencia)
                for codigoTr, cantidadTr in listaProductosTransferencia:
                    codigoProductoTransferencia = str(codigoTr)
                    cantidadProductoTransferencia = str(cantidadTr)
                    consultaProductoTransferencia = ProductosVenta.objects.filter(codigo_producto = codigoProductoTransferencia)
                    for datoProducto in consultaProductoTransferencia:
                        nombreProTransferencia = datoProducto.nombre_producto
                        
                    consultaProductoTransferencia = ProductosRenta.objects.filter(codigo_producto = codigoProductoTransferencia)
                    for datoProducto in consultaProductoTransferencia:
                        nombreProTransferencia = datoProducto.nombre_producto
                    
                    datosProductosTransferencia.append([codigoProductoTransferencia,nombreProTransferencia,cantidadProductoTransferencia])
                datosProductosVentaTransferencia.append(datosProductosTransferencia)
                
            #Datos Servicios Coorporales
            if serviciosCorporalesTransferencia == "":
                boolServiciosCoorporalesTransferencia.append("Sin servicios coorporales")
                datosServiciosCoorporalesTransferencia.append("Sin productos")
            else:
                boolServiciosCoorporalesTransferencia.append("Servicios coorporales Comprados")
                cantidadesServiciosCorporales = ventaTransferencia.cantidades_servicios_corporales
                
                datosServicios = []
                arregloIdsServiciosCorporales = serviciosCorporalesTransferencia.split(",")
                arregloCantidadesServiciosCorporales = cantidadesServiciosCorporales.split(",")
                listaServiciosCorporalesTransferencia = zip(arregloIdsServiciosCorporales, arregloCantidadesServiciosCorporales)
                for idd, cantidad in listaServiciosCorporalesTransferencia:
                    intIdProducto = int(idd)
                    strIdProducto = str(idd)
                    cantidadProducto = str(cantidad)
                    consultaServicio = Servicios.objects.filter(id_servicio = intIdProducto)
                    for datoServicio in consultaServicio:
                        nombreServicio = datoServicio.nombre_servicio
                    
                    datosServicios.append([strIdProducto,nombreServicio,cantidadProducto])
                datosServiciosCoorporalesTransferencia.append(datosServicios)
                
            #Datos Servicios Faciales
            if serviciosFacialesTransferencia == "":
                boolServiciosFacialesTransferencia.append("Sin servicios faciales")
                datosServiciosFacialesTransferencia.append("Sin servicios")
            else:
                boolServiciosFacialesTransferencia.append("Servicios coorporales Comprados")
                cantidadesServiciosFaciales = ventaTransferencia.cantidades_servicios_faciales
                
                datosServicios = []
                arregloIdsServiciosFaciales = serviciosFacialesTransferencia.split(",")
                arregloCantidadesServiciosFaciales = cantidadesServiciosFaciales.split(",")
                listaServiciosFacialesTransferencia = zip(arregloIdsServiciosFaciales, arregloCantidadesServiciosFaciales)
                for idd, cantidad in listaServiciosFacialesTransferencia:
                    intIdProducto = int(idd)
                    strIdProducto = str(idd)
                    cantidadProducto = str(cantidad)
                    consultaServicio = Servicios.objects.filter(id_servicio = intIdProducto)
                    for datoServicio in consultaServicio:
                        nombreServicio = datoServicio.nombre_servicio
                    
                    datosServicios.append([strIdProducto,nombreServicio,cantidadProducto])
                datosServiciosFacialesTransferencia.append(datosServicios)
            
            #DATOS TRATAMIENTO  
            if idTratamiento == None:
                boolTratamientosTransferencia.append("Sin tratamiento")
                datosTratamientosTransferencia.append("Sin tratamientos")
            else:
                boolTratamientosTransferencia.append("Tratamiento comprado")
                consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)

                datosTratamiento1 = []
                for datoTratamiento in consultaTratamiento:
                    codigoTratamiento = datoTratamiento.codigo_tratamiento
                    tipoTratamiento = datoTratamiento.tipo_tratamiento
                    nombreTratamiento = datoTratamiento.nombre_tratamiento
                    datosTratamiento1.append([codigoTratamiento, tipoTratamiento, nombreTratamiento])
                datosTratamientosTransferencia.append(datosTratamiento1)

            #datos paquete
            if idPaquete == None:
                boolPaquetesTratamientosTransferencia.append("Sin paquete de tratamientos")
                datosPaquetesTratamientosTransferencia.append("Sin paquete de tratamientos")
            else:
                boolPaquetesTratamientosTransferencia.append("Paquete comprado")
                consultaPaquete = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idPaquete)

                datosPaquete = []
                for datoPaquete in consultaPaquete:
                    nombrePaquete = datoPaquete.nombre_paquete
                    sesionesPaquete = datoPaquete.numero_sesiones
                    precioPaquete = datoPaquete.precio_por_paquete 
                    datosPaquete.append([nombrePaquete, sesionesPaquete,precioPaquete])
                datosPaquetesTratamientosTransferencia.append(datosPaquete)
        
        listaTransferencia = zip(listaVentasConTransferencia, quienVendioTransferencia, listaClientesTransferencia, sucursalesTransferencia,clavesRastreo,booleanDescuentoTransferencia, totalesSinDescuentoTransferencia, descuentosTransferencia,datosDescuentosTransferencia, boolProductosVentaTransferencia, datosProductosVentaTransferencia, boolServiciosCoorporalesTransferencia, datosServiciosCoorporalesTransferencia, boolServiciosFacialesTransferencia, datosServiciosFacialesTransferencia,
        boolTratamientosTransferencia,datosTratamientosTransferencia,boolPaquetesTratamientosTransferencia,datosPaquetesTratamientosTransferencia)



        
        
        if "ventaAgregada" in request.session:
            ventaAgregada = request.session['ventaAgregada']
            del request.session['ventaAgregada']
            return render(request, "13 Ventas/ventas.html", {"ventaAgregada":ventaAgregada,"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaVentas":listaVentas,
         "listaEfectivo":listaEfectivo, "listatarjeta":listatarjeta, "notificacionRenta":notificacionRenta,"listaTransferencia":listaTransferencia,"datosProductosVentaEfectivo":datosProductosVentaEfectivo,"contadorVentasEfectivo":contadorVentasEfectivo,"contadorVentasTarjeta":contadorVentasTarjeta,"contadorVentasTransferencia":contadorVentasTarjeta, "notificacionCita":notificacionCita})
        if "ventaNoAgregada" in request.session:
            ventaNoAgregada = request.session['ventaNoAgregada']
            del request.session['ventaNoAgregada']
            return render(request, "13 Ventas/ventas.html", {"ventaNoAgregada":ventaNoAgregada,"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaVentas":listaVentas,
         "listaEfectivo":listaEfectivo, "listatarjeta":listatarjeta, "notificacionRenta":notificacionRenta,"listaTransferencia":listaTransferencia,"datosProductosVentaEfectivo":datosProductosVentaEfectivo,"contadorVentasEfectivo":contadorVentasEfectivo,"contadorVentasTarjeta":contadorVentasTarjeta,"contadorVentasTransferencia":contadorVentasTarjeta, "notificacionCita":notificacionCita})
        
        if "ventaCancelacionCita" in request.session:
            ventaCancelacionCita = request.session["ventaCancelacionCita"]
            del request.session["ventaCancelacionCita"]
            return render(request, "13 Ventas/ventas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaVentas":listaVentas,
            "listaEfectivo":listaEfectivo, "listatarjeta":listatarjeta, "notificacionRenta":notificacionRenta,"listaTransferencia":listaTransferencia,"datosProductosVentaEfectivo":datosProductosVentaEfectivo,"contadorVentasEfectivo":contadorVentasEfectivo,"contadorVentasTarjeta":contadorVentasTarjeta,"contadorVentasTransferencia":contadorVentasTarjeta, "notificacionCita":notificacionCita, "ventaCancelacionCita":ventaCancelacionCita})

        

        return render(request, "13 Ventas/ventas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaVentas":listaVentas,
         "listaEfectivo":listaEfectivo, "listatarjeta":listatarjeta, "notificacionRenta":notificacionRenta,"listaTransferencia":listaTransferencia,"datosProductosVentaEfectivo":datosProductosVentaEfectivo,"contadorVentasEfectivo":contadorVentasEfectivo,"contadorVentasTarjeta":contadorVentasTarjeta,"contadorVentasTransferencia":contadorVentasTarjeta, "notificacionCita":notificacionCita})
        
    else:
        return render(request,"1 Login/login.html")
   
   
def realizarVenta(request):

    if "idSesion" in request.session:

        # Variables de sesión
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        idPerfil = idEmpleado
        idConfig = idEmpleado
    
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']

        # Variable para Menu
        estaEnAltaEmpleado = True

        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]
           #notificacionRentas
        notificacionRenta = notificacionRentas(request)

        #notificacionCitas
        notificacionCita = notificacionCitas(request)

        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)


        
        # retornar productos
        productosVentas = ProductosVenta.objects.all()
        
        if request.method == "POST":
        
            
                
            sucursal = request.POST['sucursal'] #Requerido
            fechaAlta = datetime.today().strftime('%Y-%m-%d') #Requerido
            #fechaAlta = datetime.now()
            
            datosSucursalSeleccinoada = Sucursales.objects.filter(id_sucursal =sucursal)
            for sucursalId in datosSucursalSeleccinoada:
                idSeleccionada = sucursalId.id_sucursal
                nombreSucursalSeleccionada = sucursalId.nombre
                
            
            productosVenta = ProductosVenta.objects.filter(sucursal_id__id_sucursal = idSeleccionada, cantidad__gte=1)
            productosVentaJava = ProductosVenta.objects.filter(sucursal_id__id_sucursal = idSeleccionada)
           
            concepto =""
            
            data = [i.json() for i in ProductosVenta.objects.filter(sucursal_id__id_sucursal = idSeleccionada)]
            clientes = Clientes.objects.filter(estado ="A")
            datosVendedor = Empleados.objects.filter(id_empleado =idEmpleado ) 
              
            descuentos = Descuentos.objects.all() 
           
            dataServicios = [i.jsonServicios() for i in Servicios.objects.filter(sucursal_id__id_sucursal = idSeleccionada)]
            serviciosVenta = Servicios.objects.filter(sucursal_id__id_sucursal = idSeleccionada)

            datosServiciosQueSePuedenVender = []
            datosServiciosQueSePuedenVenderJava = []
            productosXServicio = []
            for servicio in serviciosVenta:
                idServicio = servicio.id_servicio
                tipo = servicio.tipo_servicio
                nombre = servicio.nombre_servicio
                precio_venta = servicio.precio_venta


                consultaProductosQueUtilizaElServicio = ServiciosProductosGasto.objects.filter(servicio = idServicio) #2 pos. 


                servicioSePuedeVender = False
                productosQueUtiliza = []
                cuantosCaben = []
                for producto in consultaProductosQueUtilizaElServicio:
                    idProducto = producto.producto_gasto_id
                    cantidadQueSeUtilizaAlVender = producto.cantidad #Si se vende, se utiliza 1 producto
                    consultaDatosProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                    for datoProducto in consultaDatosProducto:
                        cantidadEnExistencia = datoProducto.cantidad # 4 unidades
                        nombreProducto = datoProducto.nombre_producto
                        codigo = datoProducto.codigo_producto
                    if cantidadEnExistencia >= cantidadQueSeUtilizaAlVender:
                        division = cantidadEnExistencia/cantidadQueSeUtilizaAlVender
                        divisionRedondeada = round(division)
                        cuantosCaben.append(divisionRedondeada)
                        #Si se puede vendeeeeerr... 
                        servicioSePuedeVender = True
                        #Guardar los productos
                        productosQueUtiliza.append([codigo,nombreProducto,cantidadQueSeUtilizaAlVender])
                    else:
                        #No se puede venderrrrr.... 
                        servicioSePuedeVender = False
                
                if servicioSePuedeVender == True:
                    menor = cuantosCaben[0]
                    for dato in cuantosCaben:
                        if dato < menor:
                            menor = dato
                        
                    
                    datosServiciosQueSePuedenVender.append([idServicio,tipo, nombre, precio_venta,menor])
                    datosServiciosQueSePuedenVenderJava.append([idServicio,tipo, nombre, precio_venta,menor])
                    productosXServicio.append(productosQueUtiliza)
                    

            listaZipeada = zip(datosServiciosQueSePuedenVender, productosXServicio)
            
            limiteCreditoSucursal = ConfiguracionCredito.objects.filter(sucursal_id__id_sucursal = idSeleccionada)
            montoLimite =0
           
            montoLimiteStr =""
            for limite in limiteCreditoSucursal:
                if limite.activo == "S":
                    montoLimite = float(limite.limite_credito)
              
                    montoLimiteStr =str(limite.limite_credito)
            limitesClientes = []
            for cliente in clientes:
                idCliente = cliente.id_cliente
                consultaCreditosPendientes = Creditos.objects.filter(cliente_id__id_cliente = idCliente, estatus ="Pendiente")
                creditoFaltantePorPagar= 0
                creditoLibre = 0
                creditoSolicitado =0
                creditoPagado = 0
                for credito in consultaCreditosPendientes:
                    montoTotal = credito.monto_pagar
                    montoPagado = credito.monto_pagado
                    montoRestante = credito.monto_restante
                    
                    creditoSolicitado = creditoSolicitado + montoTotal
                    creditoPagado = creditoPagado + montoPagado
                    creditoFaltantePorPagar = creditoFaltantePorPagar + montoRestante
                
                creditoLibre = montoLimite - creditoFaltantePorPagar
                limitesClientes.append([creditoLibre,creditoFaltantePorPagar])

            
            listaLimites = zip (clientes,limitesClientes)
                


           

               

            

        return render(request, "13 Ventas/realizarVenta.html", {"consultaPermisos":consultaPermisos,"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "productosVenta":productosVenta,
                                                                "serviciosVenta":serviciosVenta,"clientes":clientes,"datosVendedor":datosVendedor,"data":json.dumps(data),"productosVentaJava":productosVentaJava,"descuentos":descuentos, "dataServicios":json.dumps(dataServicios), "listaZipeada":listaZipeada,
                                                                "datosServiciosQueSePuedenVenderJava":datosServiciosQueSePuedenVenderJava, "sucursal":sucursal,"listaLimites":listaLimites,"montoLimiteStr":montoLimiteStr,
                                                                "notificacionRenta":notificacionRenta, "nombreSucursalSeleccionada":nombreSucursalSeleccionada, "notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")
    
    
def seleccionarSucursalVentas(request):

    if "idSesion" in request.session:

        # Variables de sesión
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        idPerfil = idEmpleado
        idConfig = idEmpleado
    
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']

        # Variable para Menu
        estaEnAltaEmpleado = True

        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]
           #notificacionRentas
        notificacionRenta = notificacionRentas(request)

        #notificacionCitas
        notificacionCita = notificacionCitas(request)


        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)

        sucursales = []
        if tipoUsuario == "esAdmin":
        # retornar sucursales
            listsucursales = Sucursales.objects.all()
            for dato in listsucursales:
                idSucursal =dato.id_sucursal
                nombreSucursal = dato.nombre
                direccionSucursal = dato.direccion
                sucursales.append([idSucursal,nombreSucursal, direccionSucursal])

        else:
          
            empleado = Empleados.objects.filter(id_empleado =idEmpleado)
            for sucursal in empleado:
                idSucursal =sucursal.id_sucursal_id
                
            datoSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
            for dato in datoSucursal:
                nombreSucursal = dato.nombre
                direccionSucursal = dato.direccion
            sucursales.append([idSucursal, nombreSucursal, direccionSucursal])
        
        datosVendedor = Empleados.objects.filter(id_empleado =idEmpleado )
        
        
      

        return render(request, "13 Ventas/seleccionarSucursalVentas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "sucursales":sucursales,
                                                                            "datosVendedor":datosVendedor,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")
    
def guardarVenta(request):
    if "idSesion" in request.session:
      
        idEmpleado = request.session['idSesion']
        if request.method == "POST":
            
            

            nameInput = "checkboxCredito"
            ventaEnCredito = False
            if request.POST.get(nameInput, False): #Credito Checkeado
                ventaEnCredito = True
            elif request.POST.get(nameInput, True): #Credito No checkeado
                ventaEnCredito = False

            esConEfectivo = False
            esConTarjeta = False
            esConTransferencia = False

            comentariosExtras = request.POST['comentarios']

            descuento = request.POST['descuento'] 

            if ventaEnCredito == False:  #No es una venta a credito, venta normal..

                fechaVenta = datetime.now() #La fecha con hora
                horaVenta= datetime.now().time()
                
                formaPago = request.POST['tipoPago'] #Efectivo,  tarjeta o transferencia
                sucursal = request.POST['idSucursal']
                if comentariosExtras == "":
                    comentarios = "Sin comentarios"
                else:
                    comentarios = comentariosExtras
                
                

                if formaPago == "Efectivo":
                    esConEfectivo = True
                elif formaPago == "Tarjeta":
                    esConTarjeta = True
                    tipo_tarjeta = request.POST['tipoTarjeta']    
                    referencia_tarjeta = request.POST['referenciaTarjeta'] 
                    
                elif formaPago == "Transferencia":
                    esConTransferencia = True
                    clave_transferencia = request.POST['claveRastreoTransferencia'] 

                empleadoVendedor = idEmpleado
               
                clienteMandado = request.POST['clienteSeleccionado'] #Puede ser un id de cliente o puede ser clienteMomentaneo
                if clienteMandado == "clienteMomentaneo":
                    cliente= "clienteMomentaneo"
                else:
                    arregloCliente = clienteMandado.split("-")
                    cliente = int(arregloCliente[0])
                 
                stringCodigosProductos = request.POST['codigosProductosVenta']
                stringCantidadedsProductos = request.POST['cantidadesProductosVenta']
                arregloProductosServiciosMandados = stringCodigosProductos.split(',')
                arregloCantidadesProductosServiciosMandados = stringCantidadedsProductos.split(',')
                productosVenta = []
                cantidadesProductosVenta = []
                serviciosCoporales =[]
                cantidadesServiciosCorporales = []
                serviciosFaciales = []
                cantidadesServiciosFaciales =[]
                
                lista = zip(arregloProductosServiciosMandados,arregloCantidadesProductosServiciosMandados)
                for pro_ser , cantidad in lista:
                    stringVenta = str(pro_ser)
               
                    intCantidad =int(cantidad)
                    if "PV" in stringVenta:
                        productosVenta.append(stringVenta)
                        cantidadesProductosVenta.append(intCantidad)
                    else:
                        intVenta = int(pro_ser)
                        datosServicios = Servicios.objects.filter(id_servicio = intVenta)
                        for dato in datosServicios:
                            tipoServicio = dato.tipo_servicio
                        if tipoServicio == "Facial":
                            serviciosFaciales.append(stringVenta)
                            cantidadesServiciosFaciales.append(intCantidad)
                        elif tipoServicio == "Corporal":
                            serviciosCoporales.append(stringVenta)
                            cantidadesServiciosCorporales.append(intCantidad)
                    
                listaProductosVenta =""
                cantidadesListaProductosVenta =""
                listaServiciosCorporales =""
                cantidadesListaServiciosCorporales =""
                listaServiciosFaciales =""
                cantidadesListaServiciosFaciales =""
                
                lProductos =zip(productosVenta,cantidadesProductosVenta)
                lProductos2 = zip(productosVenta,cantidadesProductosVenta)
                lProductos4 = zip(productosVenta,cantidadesProductosVenta)
                lServiciosCorporales =zip(serviciosCoporales,cantidadesServiciosCorporales)
                lServiciosCorporales2 = zip(serviciosCoporales,cantidadesServiciosCorporales)
                lServiciosFaciales =zip(serviciosFaciales,cantidadesServiciosFaciales)
                lServiciosFaciales2 =zip(serviciosFaciales,cantidadesServiciosFaciales)
                
                contadorProductos = 0
                for p,c in lProductos:
                    stringProducto =str(p)
                    stringCantidad =str(c)
                    contadorProductos =contadorProductos +1
                    if contadorProductos == 1:
                        listaProductosVenta=stringProducto
                        cantidadesListaProductosVenta =stringCantidad
                    else:
                        listaProductosVenta += "," + stringProducto 
                        cantidadesListaProductosVenta += "," + stringCantidad
                        
                contadorSerCorporal = 0
                for sCor, c in lServiciosCorporales:
                    stringServicioCorporal =str(sCor)
                    stringCantidadSerCorporal =str(c)
                    contadorSerCorporal = contadorSerCorporal +1
                    if contadorSerCorporal == 1:
                        listaServiciosCorporales=stringServicioCorporal
                        cantidadesListaServiciosCorporales =stringCantidadSerCorporal
                    else:
                        listaServiciosCorporales += "," + stringServicioCorporal
                        cantidadesListaServiciosCorporales += "," + stringCantidadSerCorporal
                
                contadorSerFacial = 0
                for sFac,c in lServiciosFaciales:
                    stringServicioFacial = str(sFac)
                    stringCantidadSerFacial = str(c)
                    contadorSerFacial = contadorSerFacial + 1
                    if contadorSerFacial == 1:
                        listaServiciosFaciales =stringServicioFacial
                        cantidadesListaServiciosFaciales =stringCantidadSerFacial
                    else:
                        listaServiciosFaciales += "," + stringServicioFacial
                        cantidadesListaServiciosFaciales += "," + stringCantidadSerFacial
                        
                    
                        
                        

                costoTotalAPagar = request.POST['costoTotalAPagar']

                #VAMOS A GUARDAR QUE NO EN CRÉDITO Y DEJAR NULO EL ID DEL CREDITO QUE ES FOREIGN KEY


                

                if descuento == "SinDescuento":
                    elCostoEsElMismo = True
                else:
                    consultaDescuento = Descuentos.objects.filter(porcentaje = descuento)
                    valorDescuento = 0
                    for datoDescuento in consultaDescuento:
                        valorDescuento = datoDescuento.porcentaje
                    stringDescuento = "."+str(valorDescuento)
                    floatDescuento = float(stringDescuento) #.15

                    multiplicacionResta = float(costoTotalAPagar) * floatDescuento
                    multiplicacionRestaConDosDecimales = round(multiplicacionResta, 2)
                    redondeoMulti = round(multiplicacionRestaConDosDecimales)

                    restaDescuento = float(costoTotalAPagar) - redondeoMulti
                    restaDescuentoDosDecimales = round(restaDescuento, 2)
                    redondeoRestaFinal = round(restaDescuentoDosDecimales)


                    costoTotalAPagar = redondeoRestaFinal

                #RegistrarProducto

                if esConEfectivo:
                    if cliente == "clienteMomentaneo":
                        if descuento == "SinDescuento":
                            registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                            tipo_pago = formaPago, 
                            empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                            ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                            monto_pagar = costoTotalAPagar, credito = "N",
                            comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                        else:
                            registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                            tipo_pago = formaPago, 
                            empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                            ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                            monto_pagar = costoTotalAPagar, credito = "N", 
                            descuento = Descuentos.objects.get(porcentaje = descuento),
                            comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    else:
                        if descuento == "SinDescuento":
                            registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                            tipo_pago = formaPago, 
                            empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                            cliente = Clientes.objects.get(id_cliente = cliente),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                            ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                            monto_pagar = costoTotalAPagar, credito = "N",
                            comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                        else:
                            registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                            tipo_pago = formaPago, 
                            empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                            cliente = Clientes.objects.get(id_cliente = cliente),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                            ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                            monto_pagar = costoTotalAPagar, credito = "N",
                            descuento = Descuentos.objects.get(porcentaje = descuento),
                            comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal))

                    #registrar movimiento en caja
                  
                   


                if esConTarjeta:
                    if cliente == "clienteMomentaneo":
                        if descuento == "SinDescuento":
                            registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                            tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta,
                            empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                            ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                            monto_pagar = costoTotalAPagar, credito = "N",
                            comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                        else:
                            registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                            tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta,
                            empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                            ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                            monto_pagar = costoTotalAPagar, credito = "N",
                            descuento = Descuentos.objects.get(porcentaje = descuento),
                            comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    else:
                        if descuento == "SinDescuento":
                            registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                            tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta,
                            empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                            cliente = Clientes.objects.get(id_cliente = cliente),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                            ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                            monto_pagar = costoTotalAPagar, credito = "N",
                            comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                        else:
                            registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                            tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta,
                            empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                            cliente = Clientes.objects.get(id_cliente = cliente),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                            ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                            monto_pagar = costoTotalAPagar, credito = "N",
                            descuento = Descuentos.objects.get(porcentaje = descuento),
                            comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                            
                        
                    


                if esConTransferencia:
                    if cliente == "clienteMomentaneo":
                        if descuento == "SinDescuento":
                            registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                            tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                            empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                            ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                            monto_pagar = costoTotalAPagar, credito = "N")
                        else:
                            registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                            tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                            empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                            ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                            monto_pagar = costoTotalAPagar, credito = "N",
                            descuento = Descuentos.objects.get(porcentaje = descuento))
                        
                    else:
                        if descuento == "SinDescuento":
                            registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                            tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                            empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                            cliente = Clientes.objects.get(id_cliente = cliente),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                            ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                            monto_pagar = costoTotalAPagar, credito = "N")
                        else:
                            registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                            tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                            empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                            cliente = Clientes.objects.get(id_cliente = cliente),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                            ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                            monto_pagar = costoTotalAPagar, credito = "N",
                            descuento = Descuentos.objects.get(porcentaje = descuento))
                        

                
                registroVenta.save()
                
            elif ventaEnCredito == True: #Venta a credito..
                
                fechaVenta = datetime.now() #La fecha con hora
                horaVenta= datetime.now().time()
               
                sucursal = request.POST['idSucursal']
                comentariosExtras = request.POST['comentarios']
                
                if comentariosExtras == "":
                    comentarios = "Sin comentarios"
                else:
                    comentarios = comentariosExtras
                 

                empleadoVendedor = idEmpleado
               
                clienteMandado = request.POST['clienteSeleccionado'] #Puede ser un id de cliente o puede ser clienteMomentaneo
                arregloCliente = clienteMandado.split("-")
                cliente = int(arregloCliente[0])
                 
                stringCodigosProductos = request.POST['codigosProductosVenta']# String "PV1000,1"
                stringCantidadedsProductos = request.POST['cantidadesProductosVenta']
                
                arregloProductosServiciosMandados = stringCodigosProductos.split(',')
                arregloCantidadesProductosServiciosMandados = stringCantidadedsProductos.split(',')
                productosVenta = []
                cantidadesProductosVenta = []
                serviciosCoporales =[]
                cantidadesServiciosCorporales = []
                serviciosFaciales = []
                cantidadesServiciosFaciales =[]
                
                lista = zip(arregloProductosServiciosMandados,arregloCantidadesProductosServiciosMandados)
                for pro_ser , cantidad in lista:
                    stringVenta = str(pro_ser)
               
                    intCantidad =int(cantidad)
                    if "PV" in stringVenta:
                        productosVenta.append(stringVenta)
                        cantidadesProductosVenta.append(intCantidad)
                    else:
                        intVenta = int(pro_ser)
                        datosServicios = Servicios.objects.filter(id_servicio = intVenta)
                        for dato in datosServicios:
                            tipoServicio = dato.tipo_servicio
                        if tipoServicio == "Facial":
                            serviciosFaciales.append(stringVenta)
                            cantidadesServiciosFaciales.append(intCantidad)
                        elif tipoServicio == "Corporal":
                            serviciosCoporales.append(stringVenta)
                            cantidadesServiciosCorporales.append(intCantidad)
                    
                listaProductosVenta =""
                cantidadesListaProductosVenta =""
                listaServiciosCorporales =""
                cantidadesListaServiciosCorporales =""
                listaServiciosFaciales =""
                cantidadesListaServiciosFaciales =""
                
                lProductos =zip(productosVenta,cantidadesProductosVenta)
                lProductos2 = zip(productosVenta,cantidadesProductosVenta)
                lProductos3 = zip(productosVenta,cantidadesProductosVenta)
                lProductos4 = zip(productosVenta,cantidadesProductosVenta)
                lServiciosCorporales =zip(serviciosCoporales,cantidadesServiciosCorporales)
                lServiciosCorporales2 = zip(serviciosCoporales,cantidadesServiciosCorporales)
                lServiciosFaciales =zip(serviciosFaciales,cantidadesServiciosFaciales)
                lServiciosFaciales2 =zip(serviciosFaciales,cantidadesServiciosFaciales)
                
                contadorProductos = 0
                for p,c in lProductos:
                    stringProducto =str(p)
                    stringCantidad =str(c)
                    contadorProductos =contadorProductos +1
                    if contadorProductos == 1:
                        listaProductosVenta=stringProducto
                        cantidadesListaProductosVenta =stringCantidad
                    else:
                        listaProductosVenta += "," + stringProducto 
                        cantidadesListaProductosVenta += "," + stringCantidad
                        
                contadorSerCorporal = 0
                for sCor, c in lServiciosCorporales:
                    stringServicioCorporal =str(sCor)
                    stringCantidadSerCorporal =str(c)
                    contadorSerCorporal = contadorSerCorporal +1
                    if contadorSerCorporal == 1:
                        listaServiciosCorporales=stringServicioCorporal
                        cantidadesListaServiciosCorporales =stringCantidadSerCorporal
                    else:
                        listaServiciosCorporales += "," + stringServicioCorporal
                        cantidadesListaServiciosCorporales += "," + stringCantidadSerCorporal
                
                contadorSerFacial = 0
                for sFac,c in lServiciosFaciales:
                    stringServicioFacial = str(sFac)
                    stringCantidadSerFacial = str(c)
                    contadorSerFacial = contadorSerFacial + 1
                    if contadorSerFacial == 1:
                        listaServiciosFaciales =stringServicioFacial
                        cantidadesListaServiciosFaciales =stringCantidadSerFacial
                    else:
                        listaServiciosFaciales += "," + stringServicioFacial
                        cantidadesListaServiciosFaciales += "," + stringCantidadSerFacial
                        
                    
                        
                        

                costoTotalAPagar = request.POST['costoTotalAPagar']
                #COSTO TOTAL ES 88

                #VAMOS A GUARDAR QUE NO EN CRÉDITO Y DEJAR NULO EL ID DEL CREDITO QUE ES FOREIGN KEY


                descuento = request.POST['descuento'] 

                if descuento == "SinDescuento":
                    elCostoEsElMismo = True
                    #Se suma el 20% del total
                else:
                    consultaDescuento = Descuentos.objects.filter(porcentaje = descuento)
                    valorDescuento = 0
                    for datoDescuento in consultaDescuento:
                        valorDescuento = datoDescuento.porcentaje
                    stringDescuento = "."+str(valorDescuento)
                    floatDescuento = float(stringDescuento) #.15

                    multiplicacionResta = float(costoTotalAPagar) * floatDescuento
                    multiplicacionRestaConDosDecimales = round(multiplicacionResta, 2)
                    redondeoMulti = round(multiplicacionRestaConDosDecimales)

                    restaDescuento = float(costoTotalAPagar) - redondeoMulti
                    restaDescuentoDosDecimales = round(restaDescuento, 2)
                    redondeoRestaFinal = round(restaDescuentoDosDecimales)


                    costoTotalAPagar = redondeoRestaFinal

                #RegistrarProducto
                costoTotalAPagarConElVeinte = float(costoTotalAPagar) * 1.20
                costoTotalAPagarConElVeinteRedondeado = round(costoTotalAPagarConElVeinte)

                
                if cliente == "clienteMomentaneo":
                    if descuento == "SinDescuento":

                        registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                        empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                        ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                        ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                        ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                        monto_pagar = costoTotalAPagar, credito = "S",
                        comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal))

                        esACredito = True
                    else:
                        registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                        empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                        ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                        ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                        ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                        monto_pagar = costoTotalAPagar, credito = "S", 
                        descuento = Descuentos.objects.get(porcentaje = descuento),
                        comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    
                        esACredito = True
                else:
                   
                    if descuento == "SinDescuento":

                        registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                        empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                        ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                        ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                        ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                        monto_pagar = costoTotalAPagarConElVeinteRedondeado, credito = "S",
                        cliente = Clientes.objects.get(id_cliente = cliente),
                        comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal))

                        ventaEnCredito = True
                    else:
                        registroVenta = Ventas(fecha_venta = fechaVenta,  hora_venta =horaVenta,
                        empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                        ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                        ids_servicios_corporales =listaServiciosCorporales, cantidades_servicios_corporales =cantidadesListaServiciosCorporales,
                        ids_servicios_faciales =listaServiciosFaciales, cantidades_servicios_faciales =cantidadesListaServiciosFaciales,
                        monto_pagar = costoTotalAPagarConElVeinteRedondeado, credito = "S",
                        cliente = Clientes.objects.get(id_cliente = cliente),
                        descuento = Descuentos.objects.get(porcentaje = descuento),
                        comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    
                        esACredito = True
                  
                   

                        

                
                registroVenta.save()

                
                

                
            

            if registroVenta and esConEfectivo:
                ultimoId = 0
                ventasTotalesEfectivo = Ventas.objects.filter(tipo_pago ="Efectivo")
                for venta in ventasTotalesEfectivo:
                    ultimoId = venta.id_venta
                tipoMovimiento ="IN"
                montoMovimiento = float(costoTotalAPagar)
                descripcionMovimiento ="Movimiento por venta " + str(ultimoId)
                fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                horaMovimiento = datetime.now().time()
                ingresarCantidadEfectivoAcaja =MovimientosCaja(fecha =fechaMovimiento,hora = horaMovimiento,tipo=tipoMovimiento,monto =montoMovimiento, descripcion=descripcionMovimiento,sucursal =  Sucursales.objects.get(id_sucursal = sucursal),
                                                                       realizado_por = Empleados.objects.get(id_empleado = empleadoVendedor))
                ingresarCantidadEfectivoAcaja.save()

                request.session['ventaAgregada'] = "La venta ha sido agregada satisfactoriamente!"

                #Descontar los proudctos..
                if listaProductosVenta == "":
                    sinProductos = True
                else:
                    for codigo, cantidad in lProductos2:
                        strCodigo = str(codigo)
                        intCantidad = int(cantidad)

                        consultaProducto = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                        for dato in consultaProducto:
                            cantidadActualEnExistencia = dato.cantidad
                        actualizacionCantidad = cantidadActualEnExistencia - intCantidad

                        actualizarProducto = ProductosVenta.objects.filter(codigo_producto = strCodigo).update(cantidad = actualizacionCantidad)
                
                if listaServiciosCorporales == "":
                    sinServiciosCorporales = True
                else:
                    for idd, cantidad in lServiciosCorporales2:
                        intid = int(idd)
                        intCantidad = int(cantidad)

                        consultaServicioProductos = ServiciosProductosGasto.objects.filter(servicio_id__id_servicio = intid)
                        if consultaServicioProductos:
                            sinProductos = False

                            idsProductosQueUtilizaElServicio = []
                            for producto in consultaServicioProductos:
                                idProducto = producto.producto_gasto_id
                                cantidadUtilizada = producto.cantidad

                                idsProductosQueUtilizaElServicio.append([idProducto, cantidadUtilizada])

                            for productoCorporal in idsProductosQueUtilizaElServicio:
                                idProductoSC = int(productoCorporal[0])
                                cantidadPSC = int(productoCorporal[1])

                                consultaProducto = ProductosGasto.objects.filter(id_producto = idProductoSC)
                                for dato in consultaProducto:
                                    cantidadActualEnExistencia = dato.cantidad
                                    cuantificable = dato.contenido_cuantificable  #N O S
                                
                                if cuantificable == "S":
                                    cantidadARestar = intCantidad * cantidadPSC
                                    actualizacionCantidad = cantidadActualEnExistencia - cantidadARestar

                                    actualizarProducto = ProductosGasto.objects.filter(id_producto = idProductoSC).update(cantidad = actualizacionCantidad)
                        else:
                            sinProductos = True

                        

                if listaServiciosFaciales == "":
                    sinServiciosFaciales = True
                else:
                    for idFacial, cantidadFacial in lServiciosFaciales2:
                        intidFacial = int(idFacial)
                        intCantidadFacial = int(cantidadFacial)

                        consultaServicioProductos = ServiciosProductosGasto.objects.filter(servicio_id__id_servicio = intidFacial)
                        if consultaServicioProductos:
                            sinProductos = False

                            idsProductosQueUtilizaElServicio = []
                            for producto in consultaServicioProductos:
                                idProducto = producto.producto_gasto_id
                                cantidadUtilizada = producto.cantidad

                                idsProductosQueUtilizaElServicio.append([idProducto, cantidadUtilizada])

                            for productoFacial in idsProductosQueUtilizaElServicio:
                                idProductoSF = int(productoFacial[0])
                                cantidadPSF = int(productoFacial[1])

                                consultaProducto = ProductosGasto.objects.filter(id_producto = idProductoSF)
                                for dato in consultaProducto:
                                    cantidadActualEnExistencia = dato.cantidad
                                    cuantificable = dato.contenido_cuantificable  #N O S
                                
                                if cuantificable == "S":
                                    cantidadARestar = intCantidadFacial * cantidadPSF
                                    actualizacionCantidad = cantidadActualEnExistencia - cantidadARestar

                                    actualizarProducto = ProductosGasto.objects.filter(id_producto = idProductoSF).update(cantidad = actualizacionCantidad)
                        else:
                            sinProductos = True

                
                #IMPRESION DE TICKEEETSSSS
                #Ultimo id de venta
                consultaVentas = Ventas.objects.all()
                ultimoIdVenta = 0
                for venta in consultaVentas:
                    ultimoIdVenta = venta.id_venta

                #Fecha
                hoy = datetime.now()
                hoyFormato = hoy.strftime('%Y/%m/%d')

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

                #DatosCliente
                if cliente == "clienteMomentaneo":
                    nombreClienteTicket = "Momentaneo"

                else:
                    consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                    for datoCliente in consultaCliente:
                        idCienteTicket = datoCliente.id_cliente
                        nombreCliente = datoCliente.nombre_cliente
                        apellidoCliente = datoCliente.apellidoPaterno_cliente

                    nombreClienteTicket = nombreCliente + " " + apellidoCliente
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
                    c.EscribirTexto("VENTA #"+str(ultimoIdVenta)+"\n")
                    c.EstablecerEnfatizado(False)
                    c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                    c.EstablecerTamañoFuente(1, 1)
                    c.EscribirTexto("\n")
                    c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                    c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                    c.EscribirTexto("\n")

                    #Listado de productos 
                    #Productos venta
                    lProductos3 = zip(productosVenta,cantidadesProductosVenta)
                    
                    lServiciosFaciales3 =zip(serviciosFaciales,cantidadesServiciosFaciales)
                    for codigo, cantidad in lProductos3:
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

                        if longitudCostoTotal == 1:
                            espacio = 38
                        elif longitudCostoTotal == 2:
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


                    #Servicios Corporales
                    lServiciosCorporales3 = zip(serviciosCoporales,cantidadesServiciosCorporales)
                    for idd, cantidad in lServiciosCorporales3:
                        idServicioCorporal = int(idd)
                        strCantidad = str(cantidad)
                        consultaServicio = Servicios.objects.filter(id_servicio = idServicioCorporal)
                        for datoServicio in consultaServicio:
                            nombreServicio = datoServicio.nombre_servicio
                            costoIndividual = datoServicio.precio_venta

                        floatCantidad = float(cantidad)
                        costototalProducto = costoIndividual * floatCantidad
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

                    #Servicios Faciales
                    lServiciosFaciales3 = zip(serviciosFaciales,cantidadesServiciosFaciales)
                    for idd, cantidad in lServiciosFaciales3:
                        idServicioFacial = int(idd)
                        strCantidad = str(cantidad)
                        consultaServicio = Servicios.objects.filter(id_servicio = idServicioFacial)
                        for datoServicio in consultaServicio:
                            nombreServicio = datoServicio.nombre_servicio
                            costoIndividual = datoServicio.precio_venta

                        floatCantidad = float(cantidad)
                        costototalProducto = costoIndividual * floatCantidad
                        costototalProductoDosDecimales = round(costototalProducto, 2)
                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                        longitudCostoTotal = int(longitudCostoTotal)

                        
                        caracteresProducto = len(nombreServicio)

                        if longitudCostoTotal == 1:
                            espacio = 39
                        if longitudCostoTotal == 2:
                            espacio = 38
                        elif longitudCostoTotal == 3:
                            espacio = 37
                        elif longitudCostoTotal == 4:
                            espacio = 36
                        elif longitudCostoTotal == 5:
                            espacio = 33
                        elif longitudCostoTotal == 6:
                            espacio = 32
                        numeroEspacios = espacio - int(caracteresProducto)
                        
                        espaciosTicket = ""
                        for x in range(numeroEspacios):
                            espacioMini = " "
                            espaciosTicket = espaciosTicket + espacioMini
                        c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")



                    
                    c.EscribirTexto("\n")
                    c.EscribirTexto("\n")
                    
                    if descuento == "SinDescuento":
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                        c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
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

                    c.EscribirTexto("\n")
                    c.EstablecerEnfatizado(True)
                    c.EstablecerTamañoFuente(1, 1)
                    c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                    c.EscribirTexto("\n")
                    c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                    c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                    c.EstablecerEnfatizado(False)
                    c.EscribirTexto("\n")
                    if esConEfectivo:
                        c.EscribirTexto("Pago en efectivo.\n")
                    elif esConTarjeta:
                        c.EscribirTexto("Pago con "+str(tipo_tarjeta)+".\n")
                        c.EscribirTexto("Referencia: "+referencia_tarjeta+".\n")
                    elif esConTransferencia:
                        c.EscribirTexto("Transferencia.\n")
                        c.EscribirTexto("Clave de rastreo: "+str(clave_transferencia)+".\n")
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
                    

                #Verificar si el nombre de producto existe en los productos para renta, y en caso de que si, cambiar el estatus
                for producto, cantidad in lProductos4:
                    codigoProducto = str(producto)
                    consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
                    for datoProducto in consultaProducto:
                        nombreProducto = datoProducto.nombre_producto

                    #Consulta a ver si algun producto renta tiene ese mismo nombre, y cambiarle el estatus
                    consultaProductoRenta = ProductosRenta.objects.filter(nombre_producto = nombreProducto)
                    if consultaProductoRenta:
                        actualizacionVestido = ProductosRenta.objects.filter(nombre_producto = nombreProducto).update(estado_renta = "Vendido")

                return redirect('/ventas/')
                
            if registroVenta:
                            
                request.session['ventaAgregada'] = "La venta ha sido agregada satisfactoriamente!"

                #Descontar los proudctos..
                if listaProductosVenta == "":
                    sinProductos = True
                else:
                    for codigo, cantidad in lProductos2:
                        strCodigo = str(codigo)
                        intCantidad = int(cantidad)

                        consultaProducto = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                        for dato in consultaProducto:
                            cantidadActualEnExistencia = dato.cantidad
                        actualizacionCantidad = cantidadActualEnExistencia - intCantidad

                        actualizarProducto = ProductosVenta.objects.filter(codigo_producto = strCodigo).update(cantidad = actualizacionCantidad)
                
                if listaServiciosCorporales == "":
                    sinServiciosCorporales = True
                else:
                    for idd, cantidad in lServiciosCorporales2:
                        intid = int(idd)
                        intCantidad = int(cantidad)

                        consultaServicioProductos = ServiciosProductosGasto.objects.filter(servicio_id__id_servicio = intid)
                        if consultaServicioProductos:
                            sinProductos = False

                            idsProductosQueUtilizaElServicio = []
                            for producto in consultaServicioProductos:
                                idProducto = producto.producto_gasto_id
                                cantidadUtilizada = producto.cantidad

                                idsProductosQueUtilizaElServicio.append([idProducto, cantidadUtilizada])

                            for productoCorporal in idsProductosQueUtilizaElServicio:
                                idProductoSC = int(productoCorporal[0])
                                cantidadPSC = int(productoCorporal[1])

                                consultaProducto = ProductosGasto.objects.filter(id_producto = idProductoSC)
                                for dato in consultaProducto:
                                    cantidadActualEnExistencia = dato.cantidad
                                    cuantificable = dato.contenido_cuantificable  #N O S
                                
                                if cuantificable == "S":
                                    cantidadARestar = intCantidad * cantidadPSC
                                    actualizacionCantidad = cantidadActualEnExistencia - cantidadARestar

                                    actualizarProducto = ProductosGasto.objects.filter(id_producto = idProductoSC).update(cantidad = actualizacionCantidad)
                        else:
                            sinProductos = True

                        

                if listaServiciosFaciales == "":
                    sinServiciosFaciales = True
                else:
                    for idFacial, cantidadFacial in lServiciosFaciales2:
                        intidFacial = int(idFacial)
                        intCantidadFacial = int(cantidadFacial)

                        consultaServicioProductos = ServiciosProductosGasto.objects.filter(servicio_id__id_servicio = intidFacial)
                        if consultaServicioProductos:
                            sinProductos = False

                            idsProductosQueUtilizaElServicio = []
                            for producto in consultaServicioProductos:
                                idProducto = producto.producto_gasto_id
                                cantidadUtilizada = producto.cantidad

                                idsProductosQueUtilizaElServicio.append([idProducto, cantidadUtilizada])

                            for productoFacial in idsProductosQueUtilizaElServicio:
                                idProductoSF = int(productoFacial[0])
                                cantidadPSF = int(productoFacial[1])

                                consultaProducto = ProductosGasto.objects.filter(id_producto = idProductoSF)
                                for dato in consultaProducto:
                                    cantidadActualEnExistencia = dato.cantidad
                                    cuantificable = dato.contenido_cuantificable  #N O S
                                
                                if cuantificable == "S":
                                    cantidadARestar = intCantidadFacial * cantidadPSF
                                    actualizacionCantidad = cantidadActualEnExistencia - cantidadARestar

                                    actualizarProducto = ProductosGasto.objects.filter(id_producto = idProductoSF).update(cantidad = actualizacionCantidad)
                        else:
                            sinProductos = True

                if ventaEnCredito: #Guardar el registro del crédito

                     
                    ultimoidVenta = 0
                    totalesVentas = Ventas.objects.all()
                    for venta in totalesVentas:
                        ultimoidVenta = venta.id_venta

                    registroCredito = Creditos(fecha_venta_credito = fechaVenta,
                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                    cliente = Clientes.objects.get(id_cliente = cliente),
                    concepto_credito = "Venta",
                    descripcion_credito = comentarios,
                    monto_pagar = costoTotalAPagarConElVeinteRedondeado,
                    monto_pagado = 0,
                    monto_restante = costoTotalAPagarConElVeinteRedondeado,
                    estatus = "Pendiente",
                    sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                    venta = Ventas.objects.get(id_venta = ultimoidVenta))

                    registroCredito.save()

                    if registroCredito:
                        ultimoCredito = 0
                        consultaCreditos = Creditos.objects.filter(estatus="Pendiente")
                        for credito in consultaCreditos:
                            ultimoCredito = credito.id_credito
                        guardarPagosCredito = PagosCreditos(id_credito = Creditos.objects.get(id_credito = ultimoCredito))
                        guardarPagosCredito.save()

                    request.session['ventaAgregada'] = "La venta con crédito ha sido agregada satisfactoriamente!"
                    

                    #IMPRESION DE TICKEEETSSSS
                    #Ultimo id de venta
                    consultaVentas = Ventas.objects.all()
                    ultimoIdVenta = 0
                    for venta in consultaVentas:
                        ultimoIdVenta = venta.id_venta

                    #Fecha
                    hoy = datetime.now()
                    hoyFormato = hoy.strftime('%Y/%m/%d')

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

                    #DatosCliente
                    if cliente == "clienteMomentaneo":
                        nombreClienteTicket = "Momentaneo"

                    else:
                        consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                        for datoCliente in consultaCliente:
                            idCienteTicket = datoCliente.id_cliente
                            nombreCliente = datoCliente.nombre_cliente
                            apellidoCliente = datoCliente.apellidoPaterno_cliente

                        nombreClienteTicket = nombreCliente + " " + apellidoCliente
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
                        c.EscribirTexto("VENTA A CRÉDITO #"+str(ultimoIdVenta)+"\n")
                        c.EscribirTexto("CRÉDITO #"+str(ultimoCredito)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        #Productos venta
                        lProductos3 = zip(productosVenta,cantidadesProductosVenta)
                        
                        lServiciosFaciales3 =zip(serviciosFaciales,cantidadesServiciosFaciales)
                        for codigo, cantidad in lProductos3:
                            strCodigo = str(codigo)
                            strCantidad = str(cantidad)
                            consultaProductoVenta = ProductosVenta.objects.filter(codigo_producto = strCodigo)
                            for datoProductoVenta in consultaProductoVenta:
                                nombreProducto = datoProductoVenta.nombre_producto
                                costoIndividualProducto = datoProductoVenta.costo_venta

                            floatCantidad = float(cantidad)
                            costototalProducto = costoIndividualProducto * floatCantidad
                            costototalProductoDosDecimales = round(costototalProducto, 2)
                            costototalProductoDosDecimalesConElVeinte = costototalProductoDosDecimales * 1.20
                            costototalProductoDosDecimalesConElVeinteRedondeada = round(costototalProductoDosDecimalesConElVeinte)
                            costototalProductoDosDecimales = str(costototalProductoDosDecimalesConElVeinteRedondeada)

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


                        #Servicios Corporales
                        lServiciosCorporales3 = zip(serviciosCoporales,cantidadesServiciosCorporales)
                        for idd, cantidad in lServiciosCorporales3:
                            idServicioCorporal = int(idd)
                            strCantidad = str(cantidad)
                            consultaServicio = Servicios.objects.filter(id_servicio = idServicioCorporal)
                            for datoServicio in consultaServicio:
                                nombreServicio = datoServicio.nombre_servicio
                                costoIndividual = datoServicio.precio_venta

                            floatCantidad = float(cantidad)
                            costototalProducto = costoIndividual * floatCantidad
                            costototalProductoDosDecimales = round(costototalProducto, 2)
                            costototalProductoDosDecimalesConElVeinte = costototalProductoDosDecimales * 1.20 
                            costototalProductoDosDecimalesConElVeinteRedondeada = round(costototalProductoDosDecimalesConElVeinte)
                            costototalProductoDosDecimales = str(costototalProductoDosDecimalesConElVeinteRedondeada)

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

                        #Servicios Faciales
                        lServiciosFaciales3 = zip(serviciosFaciales,cantidadesServiciosFaciales)
                        for idd, cantidad in lServiciosFaciales3:
                            idServicioFacial = int(idd)
                            strCantidad = str(cantidad)
                            consultaServicio = Servicios.objects.filter(id_servicio = idServicioFacial)
                            for datoServicio in consultaServicio:
                                nombreServicio = datoServicio.nombre_servicio
                                costoIndividual = datoServicio.precio_venta

                            floatCantidad = float(cantidad)
                            costototalProducto = costoIndividual * floatCantidad
                            costototalProductoDosDecimales = round(costototalProducto, 2)
                            costototalProductoDosDecimalesConElVeinte = costototalProductoDosDecimales * 1.20
                            costototalProductoDosDecimalesConElVeinteRedondeada = round(costototalProductoDosDecimales)

                            costototalProductoDosDecimales = str(costototalProductoDosDecimalesConElVeinteRedondeada)

                            costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                            longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                            longitudCostoTotal = int(longitudCostoTotal)

                            
                            caracteresProducto = len(nombreServicio)

                            if longitudCostoTotal == 1:
                                espacio = 39
                            if longitudCostoTotal == 2:
                                espacio = 38
                            elif longitudCostoTotal == 3:
                                espacio = 37
                            elif longitudCostoTotal == 4:
                                espacio = 36
                            elif longitudCostoTotal == 5:
                                espacio = 33
                            elif longitudCostoTotal == 6:
                                espacio = 32
                            numeroEspacios = espacio - int(caracteresProducto)
                            
                            espaciosTicket = ""
                            for x in range(numeroEspacios):
                                espacioMini = " "
                                espaciosTicket = espaciosTicket + espacioMini
                            c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")



                        
                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")

                        if descuento == "SinDescuento":
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagarConElVeinteRedondeado)+"\n")
                            costoTotalPagarCredito = costoTotalAPagarConElVeinteRedondeado
                        else:
                            intDescuento = int(descuento)
                            consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                            for datoDescuento in consultaDescuentos:
                                nombreDescuento = datoDescuento.nombre_descuento
                                porcentajeDescuento = datoDescuento.porcentaje

                            porcentajePagado = 100 - porcentajeDescuento #85
                            totalSinDescuento1 = 100 * costoTotalAPagarConElVeinteRedondeado
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
                        c.EscribirTexto("Pago a crédito 4 quincenas.\n")
                        c.EstablecerEnfatizado(False)
                        abono = float(costoTotalPagarCredito)/4
                        c.EscribirTexto("Abonos de: $"+str(abono)+" MXN.\n")
                        ahora = datetime.now()
                        fechaPrimerPago = ahora + timedelta(days=15)
                        fechaPrimerPago = fechaPrimerPago.strftime('%Y-%m-%d')
                        c.EscribirTexto("Primer pago el día: "+str(fechaPrimerPago)+".\n")
                        
                       
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

                else:
                    #IMPRESION DE TICKEEETSSSS
                    #Ultimo id de venta
                    consultaVentas = Ventas.objects.all()
                    ultimoIdVenta = 0
                    for venta in consultaVentas:
                        ultimoIdVenta = venta.id_venta

                    #Fecha
                    hoy = datetime.now()
                    hoyFormato = hoy.strftime('%Y/%m/%d')

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

                    #DatosCliente
                    if cliente == "clienteMomentaneo":
                        nombreClienteTicket = "Momentaneo"

                    else:
                        consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                        for datoCliente in consultaCliente:
                            idCienteTicket = datoCliente.id_cliente
                            nombreCliente = datoCliente.nombre_cliente
                            apellidoCliente = datoCliente.apellidoPaterno_cliente

                        nombreClienteTicket = nombreCliente + " " + apellidoCliente
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
                        c.EscribirTexto("VENTA #"+str(ultimoIdVenta)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        #Productos venta
                        lProductos3 = zip(productosVenta,cantidadesProductosVenta)
                        
                        lServiciosFaciales3 =zip(serviciosFaciales,cantidadesServiciosFaciales)
                        for codigo, cantidad in lProductos3:
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


                        #Servicios Corporales
                        lServiciosCorporales3 = zip(serviciosCoporales,cantidadesServiciosCorporales)
                        for idd, cantidad in lServiciosCorporales3:
                            idServicioCorporal = int(idd)
                            strCantidad = str(cantidad)
                            consultaServicio = Servicios.objects.filter(id_servicio = idServicioCorporal)
                            for datoServicio in consultaServicio:
                                nombreServicio = datoServicio.nombre_servicio
                                costoIndividual = datoServicio.precio_venta

                            floatCantidad = float(cantidad)
                            costototalProducto = costoIndividual * floatCantidad
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

                        #Servicios Faciales
                        lServiciosFaciales3 = zip(serviciosFaciales,cantidadesServiciosFaciales)
                        for idd, cantidad in lServiciosFaciales3:
                            idServicioFacial = int(idd)
                            strCantidad = str(cantidad)
                            consultaServicio = Servicios.objects.filter(id_servicio = idServicioFacial)
                            for datoServicio in consultaServicio:
                                nombreServicio = datoServicio.nombre_servicio
                                costoIndividual = datoServicio.precio_venta

                            floatCantidad = float(cantidad)
                            costototalProducto = costoIndividual * floatCantidad
                            costototalProductoDosDecimales = round(costototalProducto, 2)
                            costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                            costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                            longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                            longitudCostoTotal = int(longitudCostoTotal)

                            
                            caracteresProducto = len(nombreServicio)

                            if longitudCostoTotal == 1:
                                espacio = 39
                            if longitudCostoTotal == 2:
                                espacio = 38
                            elif longitudCostoTotal == 3:
                                espacio = 37
                            elif longitudCostoTotal == 4:
                                espacio = 36
                            elif longitudCostoTotal == 5:
                                espacio = 33
                            elif longitudCostoTotal == 6:
                                espacio = 32
                            numeroEspacios = espacio - int(caracteresProducto)
                            
                            espaciosTicket = ""
                            for x in range(numeroEspacios):
                                espacioMini = " "
                                espaciosTicket = espaciosTicket + espacioMini
                            c.EscribirTexto(strCantidad+" x "+nombreServicio+espaciosTicket+str(costototalProductoDosDecimales)+"\n")



                        
                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")

                        if descuento == "SinDescuento":
                            c.EstablecerTamañoFuente(2, 2)
                            c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                            c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
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


                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                        c.EscribirTexto("\n")
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("\n")
                        if esConEfectivo:
                            c.EscribirTexto("Pago en efectivo.\n")
                        elif esConTarjeta:
                            c.EscribirTexto("Pago con "+str(tipo_tarjeta)+".\n")
                            c.EscribirTexto("Referencia: "+referencia_tarjeta+".\n")
                        elif esConTransferencia:
                            c.EscribirTexto("Transferencia.\n")
                            c.EscribirTexto("Clave de rastreo: "+str(clave_transferencia)+".\n")
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


                #Verificar si el nombre de producto existe en los productos para renta, y en caso de que si, cambiar el estatus
                for producto, cantidad in lProductos4:
                    codigoProducto = str(producto)
                    consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
                    for datoProducto in consultaProducto:
                        nombreProducto = datoProducto.nombre_producto

                    #Consulta a ver si algun producto renta tiene ese mismo nombre, y cambiarle el estatus
                    consultaProductoRenta = ProductosRenta.objects.filter(nombre_producto = nombreProducto)
                    if consultaProductoRenta:
                        actualizacionVestido = ProductosRenta.objects.filter(nombre_producto = nombreProducto).update(estado_renta = "Vendido")


                return redirect('/ventas/')
                        
                        
            else:
                request.session['ventaNoAgregada'] = "Error en la base de datos, intentelo más tarde.."
                return redirect('/ventas/')

    else:
        return render(request,"1 Login/login.html")

def infoVenta(request):

    if "idSesion" in request.session:

        # Variables de sesión
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        idPerfil = idEmpleado
        idConfig = idEmpleado
    
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']

        # Variable para Menu
        estaEnAltaEmpleado = True

        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]
        
           #notificacionRentas
        notificacionRenta = notificacionRentas(request)

        #notificacionCitas
        notificacionCita = notificacionCitas(request)

        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)

       
        if request.method == "POST":
            idVenta = request.POST['idVenta']
            consultaVenta = Ventas.objects.filter(id_venta = idVenta)
            
            for datoVenta in consultaVenta:
                #Datos sucursal
                idSucursal = datoVenta.sucursal_id
                consultaSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
                    direccionSucursal = datoSucursal.direccion
                
                #Datos vendedor
                idEmpleadoVendedor = datoVenta.empleado_vendedor_id
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoVendedor)
                for datoEmpleado in consultaEmpleado:
                    nombreEmpleado = datoEmpleado.nombres
                    apellidoPaterno = datoEmpleado.apellido_paterno
                    puestoEmpleado = datoEmpleado.puesto
                nombreCompletoEmpleadoVendedor = nombreEmpleado + " " + apellidoPaterno
                
                #Fecha y hora venta
                fechaVenta = datoVenta.fecha_venta
                horaVenta = datoVenta.hora_venta
                
                #Datos del cliente
                idCliente = datoVenta.cliente_id
                if idCliente == None:
                    nombreCliente = "Sin cliente"
                    telefonoCliente = "Sin telefono"
                    correoCliente = "Sin correo"
                    tipoCliente = "Sin tipo cliente"
                else:
                    consultaCliente = Clientes.objects.filter(id_cliente = idCliente)
                    for datoCliente in consultaCliente:
                        nombreCliente = datoCliente.nombre_cliente
                        apellidoPaternoCliente = datoCliente.apellidoPaterno_cliente
                        nombreCliente = nombreCliente +" "+apellidoPaternoCliente
                        telefonoCliente = datoCliente.telefono
                        if telefonoCliente == None:
                           telefonoCliente = "Sin telefono"
                            
                        correoCliente = datoCliente.correo
                        if correoCliente == None:
                           correoCliente = "Sin telefono"
                           
                    #Tipo de cliente
                    tipoCliente = ""
                    
                    cantidadCompras = 0
                    consultaCompras = Ventas.objects.filter(cliente_id__id_cliente = idCliente, credito="N")
                    for compra in consultaCompras:
                        cantidadCompras = cantidadCompras + 1

                    numeroCreditos = 0
                    creditosCliente = Creditos.objects.filter(cliente_id__id_cliente = idCliente , concepto_credito = "Venta")
                    for credito in creditosCliente:
                        numeroCreditos = numeroCreditos +1
                        
                    numeroRentas = 0
                    rentasCliente = Rentas.objects.filter(cliente_id__id_cliente =idCliente)
                    for renta in rentasCliente:
                        numeroRentas = numeroRentas + 1
                
                    sumaCantidades = int(cantidadCompras) + int(numeroCreditos) + int(numeroRentas)
                    if sumaCantidades <= 3:
                        tipoCliente = "POSIBLE CONSUMIDOR"
                    elif sumaCantidades > 3 and sumaCantidades <=6:
                        tipoCliente = "CLIENTE POTENCIAL"
                    elif sumaCantidades > 6 and sumaCantidades <=9:
                        tipoCliente = "CLIENTE FRECUENTE"
                    elif sumaCantidades > 9:
                        tipoCliente = "SUPER CLIENTE"
                        
                #Datos de los productos
                boolVentaProductos = False
                boolVentaServicios = False
                codigosProductos = datoVenta.ids_productos
                infoProductos = []
                boolProductoRenta = False
                if codigosProductos == "":
                    boolVentaProductos = False
                    infoProductos = None
                else:
                    boolVentaProductos = True
                    cantidadProductos = datoVenta.cantidades_productos
                    
                    arrayProductos = codigosProductos.split(",")
                    arrayCantidadesProductos = cantidadProductos.split(",")
                    
                    listaProductosCantidades = zip(arrayProductos,arrayCantidadesProductos)
                    
                    for producto, cantidad in listaProductosCantidades:
                        codigoProducto = str(producto)
                        cantidadStringProducto = str(cantidad)  
                        cantidadIntProducto = int(cantidad)
                        
                        if "PR" in codigoProducto:
                            boolProductoRenta = True
                            boolVentaServicios = False
                            consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigoProducto)
                            for datoProducto in consultaProducto:
                                idProducto = datoProducto.id_producto
                                nombreProducto = datoProducto.nombre_producto   
                                imagenProducto = datoProducto.imagen_producto
                                costoVenta = datoProducto.costo_renta
                        else:
                            boolProductoRenta = False
                        
                            consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
                            for datoProducto in consultaProducto:
                                idProducto = datoProducto.id_producto
                                nombreProducto = datoProducto.nombre_producto   
                                imagenProducto = datoProducto.imagen_producto
                                costoVenta = datoProducto.costo_venta
                        subtotalProducto = costoVenta * float(cantidadIntProducto)
                        infoProductos.append([idProducto,codigoProducto, nombreProducto,imagenProducto,costoVenta, cantidadStringProducto, subtotalProducto])
                        
                                       
                
                #Datos de los servicios
                idServiciosCorporales = datoVenta.ids_servicios_corporales
                idServiciosFaciales = datoVenta.ids_servicios_faciales
                infoServicios = []
                if idServiciosCorporales == "" and idServiciosCorporales == "":
                    boolVentaServicios = False
                    infoServicios = None
                else:
                    boolVentaServicios = True
                    
                    
                    if idServiciosCorporales == "":
                        serviciosCorporales = False
                    else:
                        serviciosCorporales = True
                        
                    if idServiciosFaciales == "":
                        serviciosFaciales = False
                    else:
                        serviciosFaciales = False
                    
                    if serviciosCorporales:
                        cantidadServiciosCorporales = datoVenta.cantidades_servicios_corporales
                        
                        arrayServiciosCorporales = idServiciosCorporales.split(",")
                        arrayCantidadServiciosCorporales = cantidadServiciosCorporales.split(",")
                        
                        listaServiciosCorporales = zip(arrayServiciosCorporales,arrayCantidadServiciosCorporales)
                        
                        #Servicios corporales
                        for sc, csc in listaServiciosCorporales:
                            idServicioCorporal = int(sc)
                            cantidadStringServicioCorporal = str(csc)  
                            cantidadIntServicioCorporal = int(csc)
                            
                            consultaServicio = Servicios.objects.filter(id_servicio = idServicioCorporal)
                            for datoServicio in consultaServicio:
                                idServicio = datoServicio.id_servicio
                                nombreServicio = datoServicio.nombre_servicio 
                                tipoServicio = datoServicio.tipo_servicio
                                descripcionServicio = datoServicio.descripcion_servicio
                                costoVenta = datoServicio.precio_venta
                            subtotalServicio = costoVenta * float(cantidadIntServicioCorporal)
                            infoServicios.append([idServicio, tipoServicio,nombreServicio,descripcionServicio,costoVenta, cantidadStringServicioCorporal, subtotalServicio])
                    
                    if serviciosFaciales:
                        
                        
                        cantidadServiciosFaciales = datoVenta.cantidades_servicios_faciales
                        
                    
                        
                        
                        arrayServiciosFaciales = idServiciosFaciales.split(",")
                        arrayCantidadServiciosFaciales = cantidadServiciosFaciales.split(",")
                        
                        listaServiciosFaciales = zip(arrayServiciosFaciales,arrayCantidadServiciosFaciales)
                        
                    
                        #Servicios corporales
                        for sf, csf in listaServiciosFaciales:
                            idServicioFacial = int(sf)
                            cantidadStringServicioFacial = str(csf)  
                            cantidadIntServicioFacial = int(csf)
                            
                            consultaServicio = Servicios.objects.filter(id_servicio = idServicioFacial)
                            for datoServicio in consultaServicio:
                                idServicio = datoServicio.id_servicio
                                nombreServicio = datoServicio.nombre_servicio 
                                tipoServicio = datoServicio.tipo_servicio
                                descripcionServicio = datoServicio.descripcion_servicio
                                costoVenta = datoServicio.precio_venta
                            subtotalServicio = costoVenta * float(cantidadIntServicioCorporal)
                            infoServicios.append([idServicio,tipoServicio,nombreServicio ,descripcionServicio,costoVenta, cantidadStringServicioCorporal, subtotalServicio])
                    
                #Comentarios
                comentarios = datoVenta.comentariosVenta

                #Tipo de pago
                tipoPago = datoVenta.tipo_pago
                tipo_tarjeta = datoVenta.tipo_tarjeta
                referencia_pago_tarjeta = datoVenta.referencia_pago_tarjeta
                clave_rastreo_transferencia = datoVenta.clave_rastreo_transferencia
                
                
                totalPagado = datoVenta.monto_pagar
                descuento = datoVenta.descuento_id
                boolDescuento = False
                
                nombreDescuento = ""
                totalDescuento = 0
                totalSinDescuento = 0
                
                
                if descuento == None:
                    boolDescuento = False
                    
                    
                    nombreDescuento = ""
                    totalDescuento = 0
                    totalSinDescuento = 0
                else:
                    boolDescuento = True
                    consultaDescuento = Descuentos.objects.filter(id_descuento = descuento)
                    for datoDescuento in consultaDescuento:
                        nombre_descuento = datoDescuento.nombre_descuento
                        montoDescuento = datoDescuento.porcentaje
                        
                    nombreDescuento = nombre_descuento + " - " + str(montoDescuento)+"%"
                    restita = (100 - montoDescuento)
                    totalSinDescuento = (100 * totalPagado) / restita  #60
                    
                    porcentaje = "."+str(montoDescuento)
                    floatPorcentaje = float(porcentaje)
                    totalDescuento = totalSinDescuento * floatPorcentaje
                    
                    
            

            
          
          
            return render(request, "13 Ventas/infoVenta.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado,"notificacionRenta":notificacionRenta,
                                                                "idVenta":idVenta, "nombreSucursal":nombreSucursal, "direccionSucursal":direccionSucursal,
                                                                "nombreCompletoEmpleadoVendedor":nombreCompletoEmpleadoVendedor, "puestoEmpleado":puestoEmpleado,
                                                                "fechaVenta":fechaVenta, "horaVenta":horaVenta,"nombreCliente":nombreCliente, "telefonoCliente":telefonoCliente,
                                                                "correoCliente":correoCliente, "tipoCliente":tipoCliente, "comentarios":comentarios,
                                                                "boolVentaProductos":boolVentaProductos,"boolProductoRenta":boolProductoRenta,"infoProductos":infoProductos, "boolVentaServicios":boolVentaServicios, "infoServicios":infoServicios, "tipoPago":tipoPago,
                                                                "tipo_tarjeta":tipo_tarjeta,"referencia_pago_tarjeta":referencia_pago_tarjeta,"clave_rastreo_transferencia":clave_rastreo_transferencia,
                                                                "boolDescuento":boolDescuento, "nombreDescuento":nombreDescuento,"totalDescuento":totalDescuento, "totalSinDescuento":totalSinDescuento, "totalPagado":totalPagado, "notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")
