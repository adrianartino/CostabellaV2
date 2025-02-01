
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

import json
# Librerías de fecha
from datetime import date, datetime, time, timedelta

#Para mandar telegram
import telepot
#Plugin impresora termica
from appCostabella import Conector, keysBotCostabella
# Importacion de modelos
from appCostabella.models import (Clientes,Creditos, Empleados, MovimientosCaja, PagosCreditos, Permisos, ProductosRenta, Rentas, Sucursales, Ventas)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)
from dateutil.relativedelta import relativedelta

from django.db.models import Q
from zebra import Zebra

def rentas(request):

    if "idSesion" in request.session:

       # Variables de sesión
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']
        idPerfil = idEmpleado
        idConfig = idEmpleado
       

        
        agregados = []
        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]
           #notificacionRentas
        notificacionRenta = notificacionRentas(request)

        #notificacionCitas
        notificacionCita = notificacionCitas(request)
        
        #permisosEmpleado
        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)
        
        
        
        contadorApartadas = 0
        contadorPendientes = 0
        contadorFinalizadasSin = 0
        contadorFinalizadasCon = 0
        rentasApartadas = Rentas.objects.filter(estado_devolucion = "A")
        rentasPendientes = Rentas.objects.filter(estado_devolucion = "P")
        rentasFinalizadasSinCuota = Rentas.objects.filter(estado_devolucion = "F", cuota_retraso ="No")
        rentasFinalizadasCuota = Rentas.objects.filter(estado_devolucion = "F", cuota_retraso ="Si")
        
        for pendiente in rentasPendientes:
            contadorPendientes = contadorPendientes + 1
        for finalizadaSin in rentasFinalizadasSinCuota:
            contadorFinalizadasSin = contadorFinalizadasSin + 1
            
        for finalizadaCon in rentasFinalizadasCuota:
            contadorFinalizadasCon = contadorFinalizadasCon + 1
            
        for apartada in rentasApartadas:
            contadorApartadas = contadorApartadas + 1
            
        #------------------- rentas APARTADAS------------------------------------#
        clientesApartadas =[]
        datosProductosRentaApartados=[]
        encargadosApartados = []
        
        sucursalesApartados = []
     
        for renT in rentasApartadas:
            idCliente = renT.cliente_id
            idsProductos = renT.codigos_productos_renta
            encargado_renta = renT.realizado_por_id
            
            
            datosCliente = Clientes.objects.filter(id_cliente= idCliente)
            for datoC in datosCliente:
                idC = str(datoC.id_cliente)
                nombreC = datoC.nombre_cliente
                apellidoPat = datoC.apellidoPaterno_cliente
                apellidoMat = datoC.apellidoMaterno_cliente
            datosCompletosCliente = idC + " " + nombreC + " " + apellidoPat + " " + apellidoMat
            clientesApartadas.append(datosCompletosCliente)
            
            
            datosEncargado = Empleados.objects.filter(id_empleado = encargado_renta)
            for datoE in datosEncargado:
                nombres = datoE.nombres
                apellidoPaterno = datoE.apellido_paterno
                apellidoMaterno = datoE.apellido_materno
            datosCompletoEncargado = nombres + " " + apellidoPaterno + " " + apellidoMaterno
            encargadosApartados.append(datosCompletoEncargado)
            
            datosProductos = []
            arregloCodigos = idsProductos.split(",")
          
         
            for codigo in arregloCodigos:
                codigoProducto = str(codigo)
               
                consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigoProducto)
                for datoProducto in consultaProducto:
                    nombrePro = datoProducto.nombre_producto
                    imagenProducto = datoProducto.imagen_producto
                    idSucursal = datoProducto.sucursal_id
                 
                    
                datosProductos.append([codigoProducto,nombrePro,imagenProducto])
            datosProductosRentaApartados.append(datosProductos)
            
            sucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
            for dato in sucursal:
                nombreSucursal = dato.nombre
            sucursalesApartados.append(nombreSucursal)
            
        
        listaApartados = zip(rentasApartadas,clientesApartadas,datosProductosRentaApartados,encargadosApartados,sucursalesApartados)
        listaApartadosEntregarAclienteModal = zip(rentasApartadas,clientesApartadas,datosProductosRentaApartados,encargadosApartados,sucursalesApartados)
        listaApartadosEntregarAclienteModalJS = zip(rentasApartadas,clientesApartadas,datosProductosRentaApartados,encargadosApartados,sucursalesApartados)
        
        
        #------------------- rentas PENDIENTES------------------------------------#
        clientesPendientes =[]
        datosProductosRentaPendientes=[]
        encargadosPendientes = []
        
        sucursalesPendientes = []
        idSucursalesPendientes = []
     
        for renT in rentasPendientes:
            idCliente = renT.cliente_id
            idsProductos = renT.codigos_productos_renta
            encargado_renta = renT.realizado_por_id
            
            
            datosCliente = Clientes.objects.filter(id_cliente= idCliente)
            for datoC in datosCliente:
                idC = str(datoC.id_cliente)
                nombreC = datoC.nombre_cliente
                apellidoPat = datoC.apellidoPaterno_cliente
                apellidoMat = datoC.apellidoMaterno_cliente
            datosCompletosCliente = idC + " " + nombreC + " " + apellidoPat + " " + apellidoMat
            clientesPendientes.append(datosCompletosCliente)
            
            
            datosEncargado = Empleados.objects.filter(id_empleado = encargado_renta)
            for datoE in datosEncargado:
                nombres = datoE.nombres
                apellidoPaterno = datoE.apellido_paterno
                apellidoMaterno = datoE.apellido_materno
            datosCompletoEncargado = nombres + " " + apellidoPaterno + " " + apellidoMaterno
            encargadosPendientes.append(datosCompletoEncargado)
            
            datosProductos = []
            arregloCodigos = idsProductos.split(",")
          
         
            for codigo in arregloCodigos:
                codigoProducto = str(codigo)
               
                consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigoProducto)
                for datoProducto in consultaProducto:
                    nombrePro = datoProducto.nombre_producto
                    idSucursal = datoProducto.sucursal_id
                 
                    
                datosProductos.append([codigoProducto,nombrePro])
            datosProductosRentaPendientes.append(datosProductos)
            
            sucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
            for dato in sucursal:
                nombreSucursal = dato.nombre
            idSucursalesPendientes.append(idSucursal)
            sucursalesPendientes.append(nombreSucursal)
            
        
        listaPendientes = zip(rentasPendientes,clientesPendientes,datosProductosRentaPendientes,encargadosPendientes,sucursalesPendientes)
        listaPendientesDevolucionPorClienteModal = zip(rentasPendientes,clientesPendientes,datosProductosRentaPendientes,encargadosPendientes,sucursalesPendientes, idSucursalesPendientes)
        listaPendientesDevolucionPorClienteModal2 = zip(rentasPendientes,clientesPendientes,datosProductosRentaPendientes,encargadosPendientes,sucursalesPendientes)
        listaPendientesDevolucionPorClienteJS = zip(rentasPendientes,clientesPendientes,datosProductosRentaPendientes,encargadosPendientes,sucursalesPendientes)
        
        
        
        
        #------------------- rentas FINALIZADAS sin cuota------------------------------------#
        clientesFinalSinCuota =[]
        datosProductosRentaFinalSinCuota=[]
        encargadosFinalSinCuota = []
        
        sucursalesFinalSinCuota = []
     
        for renT in rentasFinalizadasSinCuota:
            idCliente = renT.cliente_id
            idsProductos = renT.codigos_productos_renta
            encargado_renta = renT.realizado_por_id
            
            
            datosCliente = Clientes.objects.filter(id_cliente= idCliente)
            for datoC in datosCliente:
                idC = str(datoC.id_cliente)
                nombreC = datoC.nombre_cliente
                apellidoPat = datoC.apellidoPaterno_cliente
                apellidoMat = datoC.apellidoMaterno_cliente
            datosCompletosCliente = idC + " " + nombreC + " " + apellidoPat + " " + apellidoMat
            clientesFinalSinCuota.append(datosCompletosCliente)
            
            
            datosEncargado = Empleados.objects.filter(id_empleado = encargado_renta)
            for datoE in datosEncargado:
                nombres = datoE.nombres
                apellidoPaterno = datoE.apellido_paterno
                apellidoMaterno = datoE.apellido_materno
            datosCompletoEncargado = nombres + " " + apellidoPaterno + " " + apellidoMaterno
            encargadosFinalSinCuota.append(datosCompletoEncargado)
            
            datosProductos = []
            arregloCodigos = idsProductos.split(",")
          
         
            for codigo in arregloCodigos:
                codigoProducto = str(codigo)
               
                consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigoProducto)
                for datoProducto in consultaProducto:
                    nombrePro = datoProducto.nombre_producto
                    idSucursal = datoProducto.sucursal_id
                 
                    
                datosProductos.append([codigoProducto,nombrePro])
            datosProductosRentaFinalSinCuota.append(datosProductos)
            
            sucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
            for dato in sucursal:
                nombreSucursal = dato.nombre
            sucursalesFinalSinCuota.append(nombreSucursal)
            
        
        listaFinalizadasSinCuota = zip(rentasFinalizadasSinCuota,clientesFinalSinCuota,datosProductosRentaFinalSinCuota,encargadosFinalSinCuota,sucursalesFinalSinCuota)
        
        
         
        #------------------- rentas FINALIZADAS con cuota------------------------------------#
        clientesFinalCuota =[]
        datosProductosRentaFinalCuota=[]
        encargadosFinalCuota = []
        
        sucursalesFinalCuota = []
     
        for renT in rentasFinalizadasCuota:
            idCliente = renT.cliente_id
            idsProductos = renT.codigos_productos_renta
            encargado_renta = renT.realizado_por_id
            
            
            datosCliente = Clientes.objects.filter(id_cliente= idCliente)
            for datoC in datosCliente:
                idC = str(datoC.id_cliente)
                nombreC = datoC.nombre_cliente
                apellidoPat = datoC.apellidoPaterno_cliente
                apellidoMat = datoC.apellidoMaterno_cliente
            datosCompletosCliente = idC + " " + nombreC + " " + apellidoPat + " " + apellidoMat
            clientesFinalCuota.append(datosCompletosCliente)
            
            
            datosEncargado = Empleados.objects.filter(id_empleado = encargado_renta)
            for datoE in datosEncargado:
                nombres = datoE.nombres
                apellidoPaterno = datoE.apellido_paterno
                apellidoMaterno = datoE.apellido_materno
            datosCompletoEncargado = nombres + " " + apellidoPaterno + " " + apellidoMaterno
            encargadosFinalCuota.append(datosCompletoEncargado)
            
            datosProductos = []
            arregloCodigos = idsProductos.split(",")
          
         
            for codigo in arregloCodigos:
                codigoProducto = str(codigo)
               
                consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigoProducto)
                for datoProducto in consultaProducto:
                    nombrePro = datoProducto.nombre_producto
                    idSucursala = datoProducto.sucursal_id
                 
                    
                datosProductos.append([codigoProducto,nombrePro])
            datosProductosRentaFinalCuota.append(datosProductos)
            
            sucursal = Sucursales.objects.filter(id_sucursal = idSucursala)
            for dato in sucursal:
                nombreSucursal = dato.nombre
            sucursalesFinalCuota.append(nombreSucursal)
            
        
        listaFinalizadasCuota = zip(rentasFinalizadasCuota,clientesFinalCuota,datosProductosRentaFinalCuota,encargadosFinalCuota,sucursalesFinalCuota)
        listaFinalizadasCuotaModal = zip(rentasFinalizadasCuota,clientesFinalCuota,datosProductosRentaFinalCuota,encargadosFinalCuota,sucursalesFinalCuota)
        listaFinalizadasCuotaModalJS = zip(rentasFinalizadasCuota,clientesFinalCuota,datosProductosRentaFinalCuota,encargadosFinalCuota,sucursalesFinalCuota)
       
       
        
            
       
        

            
        if "rentasEnviadas" in request.session:
            rentasEnviadas = request.session['rentasEnviadas']
            del request.session['rentasEnviadas']
            return render(request, "9 Rentas/rentas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,
                                                        "contadorApartadas":contadorApartadas,"contadorPendientes":contadorPendientes,"contadorFinalizadasSin":contadorFinalizadasSin,"contadorFinalizadasCon":contadorFinalizadasCon,"listaApartados":listaApartados,"listaPendientes":listaPendientes,
                                                        "listaApartadosEntregarAclienteModal":listaApartadosEntregarAclienteModal,"listaPendientesDevolucionPorClienteModal":listaPendientesDevolucionPorClienteModal,"listaPendientesDevolucionPorClienteModal2":listaPendientesDevolucionPorClienteModal2,
                                                        "listaPendientesDevolucionPorClienteJS":listaPendientesDevolucionPorClienteJS,"listaFinalizadasSinCuota":listaFinalizadasSinCuota,"listaFinalizadasCuota":listaFinalizadasCuota,
                                                        "listaFinalizadasCuotaModal":listaFinalizadasCuotaModal,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita, "listaApartadosEntregarAclienteModalJS":listaApartadosEntregarAclienteModalJS, "listaFinalizadasCuotaModalJS":listaFinalizadasCuotaModalJS,
                                                        "rentasEnviadas":rentasEnviadas
                                                    
            })
            
        
            
        return render(request, "9 Rentas/rentas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,
                                                        "contadorApartadas":contadorApartadas,"contadorPendientes":contadorPendientes,"contadorFinalizadasSin":contadorFinalizadasSin,"contadorFinalizadasCon":contadorFinalizadasCon,"listaApartados":listaApartados,"listaPendientes":listaPendientes,
                                                        "listaApartadosEntregarAclienteModal":listaApartadosEntregarAclienteModal,"listaPendientesDevolucionPorClienteModal":listaPendientesDevolucionPorClienteModal,"listaPendientesDevolucionPorClienteModal2":listaPendientesDevolucionPorClienteModal2,
                                                        "listaPendientesDevolucionPorClienteJS":listaPendientesDevolucionPorClienteJS,"listaFinalizadasSinCuota":listaFinalizadasSinCuota,"listaFinalizadasCuota":listaFinalizadasCuota,
                                                        "listaFinalizadasCuotaModal":listaFinalizadasCuotaModal,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita, "listaApartadosEntregarAclienteModalJS":listaApartadosEntregarAclienteModalJS, "listaFinalizadasCuotaModalJS":listaFinalizadasCuotaModalJS
                                                    
        })
    
    else:
        return render(request,"1 Login/login.html")

def altaRenta(request):

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
       
               
            sucursal = request.POST['sucursal'] #Sucursal donde se hará la renta
            
            datosSucursalSeleccinoada = Sucursales.objects.filter(id_sucursal =sucursal)
            for sucursalId in datosSucursalSeleccinoada:
                idSeleccionada = sucursalId.id_sucursal
                nombreSucursalSeleccionada = sucursalId.nombre
                
            
            productosRenta = ProductosRenta.objects.filter(sucursal_id__id_sucursal = idSeleccionada, cantidad__gte=1, estado_renta = "Sin rentar") 
            productosRentaJava = ProductosRenta.objects.filter(sucursal_id__id_sucursal = idSeleccionada, cantidad__gte=1, estado_renta = "Sin rentar") 
           
            
            dataProductosRenta = [i.jsonRenta() for i in ProductosRenta.objects.filter(sucursal_id__id_sucursal = idSeleccionada) ]
            clientes = Clientes.objects.all()
            datosVendedor = Empleados.objects.filter(id_empleado =idEmpleado ) 
              
            
           


           

               

            

        return render(request, "9 Rentas/altaRenta.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "productosRenta":productosRenta,
                                                                "clientes":clientes,"datosVendedor":datosVendedor,"data":json.dumps(dataProductosRenta),"productosRentaJava":productosRentaJava,"sucursal":sucursal,"notificacionRenta":notificacionRenta,"nombreSucursalSeleccionada":nombreSucursalSeleccionada, "notificacionCita":notificacionCita})
    
    else:
        return render(request,"1 Login/login.html")

def entregarRentaApartada(request):

    if "idSesion" in request.session:
        idEmpleado = request.session['idSesion']

        if request.method == "POST":
            idRentaEntregaAcliente = request.POST['idRentaEntregaAcliente']
            costoRestanteApagar = request.POST['costoRestanteApagar']
            fechaEntregaAcliente = datetime.now()
            
            fecha = datetime.strptime(str(fechaEntregaAcliente), "%Y-%m-%d %H:%M:%S.%f").date()
            fechas = fecha + timedelta(days=3)
            
            
         
            fechaLimiteDevolucionCuota =fechas +  timedelta(days=7)
            strfechaLimiteDevolucionCuota = str(fechaLimiteDevolucionCuota)
          
            formaPago = request.POST['tipoPago'] #Efectivo,  tarjeta o transferencia
            sucursal = request.POST['idSucursal']
              
                    
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
            

         

            infoRenta = Rentas.objects.filter(id_renta = idRentaEntregaAcliente)
            
            for dato in infoRenta:
                cliente = dato.cliente_id
                abonado = dato.monto_pago_apartado
              
                idsProductos = dato.codigos_productos_renta
                cantidadesProductos = "1"
                codigoVestido = dato.codigos_productos_renta

                consultaVestido = ProductosRenta.objects.filter(codigo_producto = codigoVestido)
                for datoVestido in consultaVestido:
                    sucursal = datoVestido.sucursal_id
                
            datosCliente = Clientes.objects.filter(id_cliente= cliente)
            for datoC in datosCliente:
                idC = str(datoC.id_cliente)
                nombreC = datoC.nombre_cliente
                apellidoPat = datoC.apellidoPaterno_cliente
                apellidoMat = datoC.apellidoMaterno_cliente
            datosCompletosCliente = idC + " " + nombreC + " " + apellidoPat + " " + apellidoMat
            
         
            pagoFinalRestante = float(abonado) - float(costoRestanteApagar)

          
              
            arregloProductos = idsProductos.split(',')
                
                
            
            
            
            
            
         
            horaVenta= datetime.now().time()
                
            #primerFecha= fechaDevolucion
            #segundaFecha = fechaFinalRenta

            #formato1 = datetime.strptime(primerFecha, '%Y-%m-%d')
            #formato2 = datetime.strptime(str(segundaFecha), '%Y-%m-%d')
            
            #if formato1 > formato2:
                #retraso_renta = "S"
                #actualizacionRenta = Rentas.objects.filter(id_renta = idRentaEditar).update(fecha_devolucion = fechaDevolucion,estado_devolucion = "F",descripcion_devolucion = observacionesDevolucion,cuota_retraso =retraso_renta)
            
                
            #else:
                #retraso_renta ="N"
                #actualizacionRenta = Rentas.objects.filter(id_renta = idRentaEditar).update(fecha_devolucion = fechaDevolucion,estado_devolucion = "F",descripcion_devolucion = observacionesDevolucion,cuota_retraso =retraso_renta)
            
            entregaRenta = Rentas.objects.filter(id_renta = idRentaEntregaAcliente).update(fecha_entrega_renta = fecha,estado_devolucion = "P",
                                                                                           fecha_limite_devolucion =fechas,fecha_limite_devolucion_cuota =strfechaLimiteDevolucionCuota,
                                                                                           monto_pago_apartado=abonado,monto_pago_restante= costoRestanteApagar,monto_restante =pagoFinalRestante,realizado_por =idEmpleado)
            
            if esConEfectivo:
                        
                registroVenta = Ventas(fecha_venta = fecha,  hora_venta =horaVenta,
                tipo_pago = formaPago, 
                empleado_vendedor = Empleados.objects.get(id_empleado = idEmpleado),
                cliente = Clientes.objects.get(id_cliente = cliente),
                ids_productos = idsProductos, cantidades_productos = cantidadesProductos,
                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                monto_pagar = costoRestanteApagar, credito = "S",
                comentariosVenta = "Se realizo venta por motivo de renta con apartado", sucursal = Sucursales.objects.get(id_sucursal = sucursal))

            if esConTarjeta:
                    
                        
                registroVenta = Ventas(fecha_venta = fecha,  hora_venta =horaVenta,
                tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta,
                empleado_vendedor = Empleados.objects.get(id_empleado = idEmpleado),
                cliente = Clientes.objects.get(id_cliente = cliente),
                ids_productos = idsProductos, cantidades_productos = cantidadesProductos,
                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                monto_pagar = costoRestanteApagar, credito = "S",
                comentariosVenta = "Se realizo venta por motivo de renta con apartado", sucursal = Sucursales.objects.get(id_sucursal = sucursal))
    

            if esConTransferencia:
            
                registroVenta = Ventas(fecha_venta = fecha,  hora_venta =horaVenta,
                tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                empleado_vendedor = Empleados.objects.get(id_empleado = idEmpleado),
                cliente = Clientes.objects.get(id_cliente = cliente),
                ids_productos = idsProductos, cantidades_productos = cantidadesProductos,
                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                monto_pagar = costoRestanteApagar, credito = "S",comentariosVenta = "Se realizo venta por motivo de renta con apartado", sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                        

            registroVenta.save()
            
            if entregaRenta and registroVenta: 
                
                for productoRenta in arregloProductos:
                        codigo = str(productoRenta)
                        actualizacionEstado = ProductosRenta.objects.filter(codigo_producto = codigo).update(estado_renta = "En renta")  
                
                if esConEfectivo:
                     
                    tipoMovimiento ="IN"
                    montoMovimiento = float(costoRestanteApagar)
                    descripcionMovimiento ="Movimiento por liquidación de renta  " + idRentaEntregaAcliente + " por el cliente " + datosCompletosCliente 
                    fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                    horaMovimiento = datetime.now().time()
                    ingresarCantidadEfectivoAcaja =MovimientosCaja(fecha =fechaMovimiento,hora = horaMovimiento,tipo=tipoMovimiento,monto =montoMovimiento, descripcion=descripcionMovimiento,sucursal =  Sucursales.objects.get(id_sucursal = sucursal),
                                                                                realizado_por = Empleados.objects.get(id_empleado = idEmpleado))
                    ingresarCantidadEfectivoAcaja.save()
                    if ingresarCantidadEfectivoAcaja:
                        montoLiquidacionCredito = float(costoRestanteApagar)
                        credito = Creditos.objects.filter(renta_id = idRentaEntregaAcliente, cliente_id =idC)
                        if credito:
                            for c in credito:
                                idCredito = c.id_credito
                                abonadoCredito =c.monto_pagado
                            creditoMontoFinal = abonadoCredito - montoLiquidacionCredito
                            saldarCredito = Creditos.objects.filter(renta_id = idRentaEntregaAcliente, cliente_id =idC).update(monto_restante = creditoMontoFinal,estatus ="Finalizado")
                            if saldarCredito:
                                ingresarSegundoPagoCreditoSaldado = PagosCreditos.objects.filter(id_credito_id =idCredito).update(fecha_pago2=fecha,tipo_pago2="Efectivo",monto_pago2=montoLiquidacionCredito)
                            
                if esConTarjeta:
                    
                    montoLiquidacionCredito = float(costoRestanteApagar)
                    credito = Creditos.objects.filter(renta_id = idRentaEntregaAcliente, cliente_id =idC)
                    if credito:
                        for c in credito:
                            idCredito = c.id_credito
                            abonadoCredito =c.monto_pagado
                        creditoMontoFinal = abonadoCredito - montoLiquidacionCredito
                        saldarCredito = Creditos.objects.filter(renta_id = idRentaEntregaAcliente, cliente_id =idC).update(monto_restante = creditoMontoFinal,estatus ="Finalizado")
                        if saldarCredito:
                            ingresarSegundoPagoCreditoSaldado = PagosCreditos.objects.filter(id_credito_id =idCredito).update(fecha_pago2=fecha,tipo_pago2="Tarjeta",tipo_tarjeta2=tipo_tarjeta,referencia_pago_tarjeta2=
                                                                                                                          referencia_tarjeta,monto_pago2=montoLiquidacionCredito)
                        
                if esConTransferencia:
                    
                    montoLiquidacionCredito = float(costoRestanteApagar)
                    credito = Creditos.objects.filter(renta_id = idRentaEntregaAcliente, cliente_id =idC)
                    if credito:
                        for c in credito:
                            idCredito = c.id_credito
                            abonadoCredito =c.monto_pagado
                        creditoMontoFinal = abonadoCredito - montoLiquidacionCredito
                        saldarCredito = Creditos.objects.filter(renta_id = idRentaEntregaAcliente, cliente_id =idC).update(monto_restante = creditoMontoFinal,estatus ="Finalizado")
                        if saldarCredito:
                            ingresarSegundoPagoCreditoSaldado = PagosCreditos.objects.filter(id_credito_id =idCredito).update(fecha_pago2=fecha,tipo_pago2="Transferencia",clave_rastreo_pago_transferencia2=
                                                                                                                          clave_transferencia,monto_pago2=montoLiquidacionCredito)
                    
                
                #IMPRESION DE TICKEEETSSSS
                #Ultimo id de venta
                consultaVentas = Ventas.objects.all()
                ultimoIdVenta = 0
                for venta in consultaVentas:
                    ultimoIdVenta = venta.id_venta

                #ultimo id de renta
                consultaRentas = Rentas.objects.all()
                ultimoIdRenta = 0
                for renta in consultaRentas:
                    ultimoIdRenta = renta.id_renta

                #Fecha
                hoy = datetime.now()
                hoyFormato = hoy.strftime('%Y/%m/%d')

                #Empleado vendedor
                empleadoVendedor = idEmpleado
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
                    c.EscribirTexto("RENTA #"+str(ultimoIdRenta)+"\n")
                    c.EscribirTexto("VENTA #"+str(ultimoIdVenta)+"\n")
                    c.EstablecerEnfatizado(False)
                    c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                    c.EstablecerTamañoFuente(1, 1)
                    c.EscribirTexto("\n")
                    c.EscribirTexto(str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                    c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                    c.EscribirTexto("\n")

                    #Listado de productos 
                    #Productos venta
                    
                    consultaProductoRenta = ProductosRenta.objects.filter(codigo_producto = codigoVestido)
                    for datoProductoRenta in consultaProductoRenta:
                        nombreProducto = datoProductoRenta.nombre_producto
                        costoIndividualProducto = datoProductoRenta.costo_renta

                    costoIndividualProductoDecimales = str(costoIndividualProducto)

                    costoTotalProductoDivididoEnElPunto = costoIndividualProductoDecimales.split(".")
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
                    c.EscribirTexto("1 x "+nombreProducto+espaciosTicket+str(costoRestanteApagar)+"\n")


                    

                    
                    c.EscribirTexto("\n")
                    c.EscribirTexto("\n")
                    
                    restantePorPagar = float(costoIndividualProducto) - float(costoRestanteApagar)                               
                    c.EstablecerTamañoFuente(2, 2)
                    c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                    c.EscribirTexto("TOTAL PAGADO RESTANTE:  $"+str(costoRestanteApagar)+"\n")
                    c.EstablecerTamañoFuente(1, 1)
                    c.EscribirTexto("TOTAL VESTIDO:  $"+str(costoIndividualProducto)+"\n")
                    c.EscribirTexto("\n")
                    c.EstablecerTamañoFuente(2, 2)
                    c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                    c.EscribirTexto("RECEPCIÓN DEL VESTIDO\n")
                    c.EstablecerTamañoFuente(1, 1)
                    c.EscribirTexto("EL DÍA: "+str(fechas)+"\n")
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
                    ##c.abrirCajon()
                    c.Pulso(48, 60, 120)
                    print("Imprimiendo...")
                    # Recuerda cambiar por el nombre de tu impresora
                    respuesta = c.imprimirEn("POS80 Printer")
                    if respuesta == True:
                        print("Impresión correcta")
                    else:
                        print(f"Error. El mensaje es: {respuesta}")

               
                #Entregar Renta
                try:
                    tokenTelegram = keysBotCostabella.tokenBotCostabellaRentas
                    botCostabella = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCostabella.idGrupo
                    
                    mensaje = " \U0001F457 VESTIDO ENTREGADO \U0001F457 \n El cliente "+nombreClienteTicket+" ha recogido el vestido "+nombreProducto+" el día "+hoyFormato+" en la sucursal "+nombreSucursal+" correspondiente a la renta "+str(ultimoIdRenta)
                    botCostabella.sendMessage(idGrupoTelegram,mensaje)
                except:
                    print("An exception occurred")
                
                request.session['rentaEntregada'] = "La renta número " + idRentaEntregaAcliente  +  " ha sido entregada al cliente " + datosCompletosCliente + "  correctamente!"
            return redirect('/verCalendarioRentas/') 
        
def verCalendarioRentas(request):

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

        fechaMesAnterior = datetime.now()-relativedelta(months =1)
        añoAnterior = fechaMesAnterior.strftime("%Y")
        mesAnterior = fechaMesAnterior.strftime("%m")
        fechaMesAnterior = añoAnterior + "-"+mesAnterior+"-01"
        fechaMesDespues = datetime.now() + relativedelta(months =1)
        añoDespues= fechaMesDespues.strftime("%Y")
        mesDespues = fechaMesDespues.strftime("%m")
        fechaMesDespues = añoDespues + "-"+mesDespues+"-15"
        
        totalRentasCalendarioEntregar= Rentas.objects.filter(fecha_entrega_renta__range=[fechaMesAnterior,fechaMesDespues], fecha_limite_devolucion__range=[fechaMesAnterior,fechaMesDespues], estado_devolucion = "A")

        mensajesBarraEntrega =[]
        descripcionBarraEntrega = []
        fechasEntregaEntrega = []
        claseColorEntrega = []

        for rentaEnregar in totalRentasCalendarioEntregar:
            idRenta = rentaEnregar.id_renta
            cliente = rentaEnregar.cliente_id
            productoRentado = rentaEnregar.codigos_productos_renta
            fechaApartado = rentaEnregar.fecha_apartado
            fechaEntrega = rentaEnregar.fecha_entrega_renta

            #Fechas en texto
            fechaRentaTipoDate = datetime.strftime(fechaEntrega, '%Y-%m-%d')
            
            mesesDic = {
                "01":'Enero',
                "02":'Febrero',
                "03":'Marzo',
                "04":'Abril',
                "05":'Mayo',
                "06":'Junio',
                "07":'Julio',
                "08":'Agosto',
                "09":'Septiembre',
                "10":'Octubre',
                "11":'Noviembre',
                "12":'Diciembre'
            }
            
            mesApartado = datetime.strftime(fechaApartado, '%m')
            diaApartado = datetime.strftime(fechaApartado, '%d')
            añoApartado = datetime.strftime(fechaApartado, '%Y')

            mesEnTexto = mesesDic[str(mesApartado)]
            fechaApartadoMensaje = diaApartado + " de "+mesEnTexto+ " del " + añoApartado

            mesEntrega = datetime.strftime(fechaEntrega, '%m')
            diaEntrega = datetime.strftime(fechaEntrega, '%d')
            añoEntrega = datetime.strftime(fechaEntrega, '%Y')

        
            mesEnTextoFinal = mesesDic[str(mesEntrega)]
            fechaEntregaMensaje = diaEntrega + " de "+mesEnTextoFinal+ " del " + añoEntrega

            #Datos del cliente
            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
            for datoCliente in consultaCliente:
                nombreCliente = datoCliente.nombre_cliente
                apellidoPaterno = datoCliente.apellidoPaterno_cliente
            
            nombreCompletoCliente = nombreCliente + " " + apellidoPaterno

            #Datos de producto rentado
            consultaProductoRentado = ProductosRenta.objects.filter(codigo_producto = productoRentado)
            for datoProducto in consultaProductoRentado:
                codigoProducto = datoProducto.codigo_producto
                nombreProducto = datoProducto.nombre_producto
                idSucursal = datoProducto.sucursal_id
            
            consultaIdSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
            for datoSucursal in consultaIdSucursal:
                nombreSucursal = datoSucursal.nombre
            
            mensajeBarra = "ID:"+str(idRenta)+" - "+nombreSucursal+" - Entrega de vestido "+codigoProducto+" a "+nombreCompletoCliente+" Cliente N°"+str(cliente)+"."

            colorClase = "fc-event-info"
           
            descripcion = "Entrega pendiente del vestido "+codigoProducto+" "+nombreProducto+", se apartó el día "+fechaApartadoMensaje+" y el cliente deberá recogerlo el dia "+fechaEntregaMensaje+". Estatus = Apartado"
                    

            mensajesBarraEntrega.append(mensajeBarra)
            descripcionBarraEntrega.append(descripcion)
            fechasEntregaEntrega.append(fechaRentaTipoDate)
            claseColorEntrega.append(colorClase)
        
        listaRentasEntregaCalendario = zip(mensajesBarraEntrega, descripcionBarraEntrega, fechasEntregaEntrega, claseColorEntrega)


        totalRentasCalendario= Rentas.objects.filter(fecha_entrega_renta__range=[fechaMesAnterior,fechaMesDespues], fecha_limite_devolucion__range=[fechaMesAnterior,fechaMesDespues], estado_devolucion = "P")

        mensajesBarra =[]
        descripcionBarra = []
        fechasEntrega = []
        fechaFinalPrestamoMasUnDia = []
        claseColor = []

        for renta in totalRentasCalendario:
            idRenta = renta.id_renta
            cliente = renta.cliente_id
            productoRentado = renta.codigos_productos_renta
            fechaRenta = renta.fecha_entrega_renta
            fechaFinal = renta.fecha_limite_devolucion
            fechaFinalMasUno = fechaFinal+ timedelta(days =1)
            
            estado = renta.estado_devolucion
            cuota = renta.cuota_retraso

            #Fechas en texto
            fechaRentaTipoDate = datetime.strftime(fechaRenta, '%Y-%m-%d')
            fechaFinalStrTipoDate = datetime.strftime(fechaFinalMasUno,'%Y-%m-%d')

            mes = datetime.strftime(fechaRenta, '%m')
            dia = datetime.strftime(fechaRenta, '%d')
            año = datetime.strftime(fechaRenta, '%Y')

            mesesDic = {
                "01":'Enero',
                "02":'Febrero',
                "03":'Marzo',
                "04":'Abril',
                "05":'Mayo',
                "06":'Junio',
                "07":'Julio',
                "08":'Agosto',
                "09":'Septiembre',
                "10":'Octubre',
                "11":'Noviembre',
                "12":'Diciembre'
            }

            mesEnTexto = mesesDic[str(mes)]
            fechaRentaMensaje = dia + " de "+mesEnTexto+ " del " + año

            mesFinal = datetime.strftime(fechaFinal, '%m')
            diaFinal = datetime.strftime(fechaFinal, '%d')
            añoFinal = datetime.strftime(fechaFinal, '%Y')

        
            mesEnTextoFinal = mesesDic[str(mesFinal)]
            fechaRentaFinalMensaje = diaFinal + " de "+mesEnTextoFinal+ " del " + añoFinal

            #Datos del cliente
            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
            for datoCliente in consultaCliente:
                nombreCliente = datoCliente.nombre_cliente
                apellidoPaterno = datoCliente.apellidoPaterno_cliente
            
            nombreCompletoCliente = nombreCliente + " " + apellidoPaterno

            #Datos de producto rentado
            consultaProductoRentado = ProductosRenta.objects.filter(codigo_producto = productoRentado)
            for datoProducto in consultaProductoRentado:
                codigoProducto = datoProducto.codigo_producto
                nombreProducto = datoProducto.nombre_producto
                idSucursal = datoProducto.sucursal_id
            
            consultaIdSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
            for datoSucursal in consultaIdSucursal:
                nombreSucursal = datoSucursal.nombre
            
            mensajeBarra = "ID:"+str(idRenta)+" - "+nombreSucursal+" - Renta de vestido "+codigoProducto+" a "+nombreCompletoCliente+" Cliente N°"+str(cliente)+"."

            colorClase = ""
            if estado == "F": #Finalizada o devuelta
                fechaDevolucion = renta.fecha_devolucion

                mesdev = datetime.strftime(fechaDevolucion, '%m')
                diadev = datetime.strftime(fechaDevolucion, '%d')
                añodev = datetime.strftime(fechaDevolucion, '%Y')

                mesEnTextoDev = mesesDic[str(mesdev)]
                fechaDevMensaje = diadev + " de "+mesEnTextoDev+ " del " + añodev

                

                if cuota == "S":
                    descripcion = "La entrega del vestido "+codigoProducto+" "+nombreProducto+"se realizó el día "+fechaRentaMensaje+" y se devolvió con cuota el dia "+fechaDevMensaje+". Estatus = Devuelto"
                    colorClase = "fc-event-warning"
                else:
                    colorClase = "fc-event-success"
                    descripcion = "La entrega del vestido "+codigoProducto+" "+nombreProducto+"se realizó el día "+fechaRentaMensaje+" y se devolvió sin cuota el dia "+fechaDevMensaje+". Estatus = Devuelto"
            else:#Pendiente de entregar
                descripcion = "La entrega del vestido "+codigoProducto+" "+nombreProducto+"se realizó el día "+fechaRentaMensaje+" y la fecha programada de devolución es el dia "+fechaRentaFinalMensaje+". Estatus = No devuelto"
                colorClase = "fc-event-danger"

            mensajesBarra.append(mensajeBarra)
            descripcionBarra.append(descripcion)
            fechasEntrega.append(fechaRentaTipoDate)
            fechaFinalPrestamoMasUnDia.append(fechaFinalStrTipoDate)
            claseColor.append(colorClase)
        
        listaRentasCalendario = zip(mensajesBarra, descripcionBarra, fechasEntrega, fechaFinalPrestamoMasUnDia, claseColor)


        if "rentaAgregada" in request.session:
            rentaAgregada = request.session['rentaAgregada']
            del request.session['rentaAgregada']
            return render(request, "9 Rentas/verCalendarioRentas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                    
                                                        "rentaAgregada":rentaAgregada,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })
            
        if "rentaNoAgregada" in request.session:
            rentaNoAgregada = request.session['rentaNoAgregada']
            del request.session['rentaNoAgregada']
            return render(request, "9 Rentas/verCalendarioRentas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                    
                                                        "rentaNoAgregada":rentaNoAgregada,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })
        
        
        if "rentaEntregada" in request.session:
            rentaEntregada = request.session['rentaEntregada']
            del request.session['rentaEntregada']
            return render(request, "9 Rentas/verCalendarioRentas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                    
                                                        "rentaEntregada":rentaEntregada,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })
            
        if "recibirRentaPendiente" in request.session:
            recibirRentaPendiente = request.session['recibirRentaPendiente']
            del request.session['recibirRentaPendiente']
            return render(request, "9 Rentas/verCalendarioRentas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                    
                                                        "recibirRentaPendiente":recibirRentaPendiente,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })
            
        if "rentaCuotaPagada" in request.session:
            rentaCuotaPagada = request.session['rentaCuotaPagada']
            del request.session['rentaCuotaPagada']
            return render(request, "9 Rentas/verCalendarioRentas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                    
                                                        "rentaCuotaPagada":rentaCuotaPagada,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })
        
        if "recibirRentaPendienteConCuota" in request.session:
            recibirRentaPendienteConCuota = request.session["recibirRentaPendienteConCuota"]
            del request.session["recibirRentaPendienteConCuota"]
            return render(request, "9 Rentas/verCalendarioRentas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                    
                                                        "recibirRentaPendienteConCuota":recibirRentaPendienteConCuota,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })
        
        

            
            
            
        
            
        return render(request, "9 Rentas/verCalendarioRentas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaRentasEntregaCalendario":listaRentasEntregaCalendario, "listaRentasCalendario":listaRentasCalendario,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
    
    else:
        return render(request,"1 Login/login.html")
    
    
def seleccionarSucursalRentas(request):

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
        
         #permisosEmpleado
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
        
        
      

        return render(request, "9 Rentas/seleccionarSucursalRentas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "sucursales":sucursales,
                                                                            "datosVendedor":datosVendedor,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")


def guardarRentas(request):
    if "idSesion" in request.session:
        # Variables de sesión
        idEmpleado = request.session['idSesion']
        if request.method == "POST":
            
            

            nameInput = "checkboxApartado"
            rentaApartada = False
            if request.POST.get(nameInput, False): #Apartado Checkeado
                rentaApartada = True
            elif request.POST.get(nameInput, True): #Apartado No checkeado
                rentaApartada = False

            cliente = request.POST['clienteSeleccionado'] #Puede ser un id de cliente o puede ser clienteMomentaneo
            stringCodigosProductos = request.POST['codigosProductosRenta']# String "PV1000,1"
            arregloProductos = stringCodigosProductos.split(',')

            fechaApartado = datetime.now()
            horaVenta= datetime.now().time()
            fechaEntregaVestido = request.POST['fechaEntregaVestido']
            fecha = datetime.strptime(fechaEntregaVestido, "%Y-%m-%d").date()
            fechas = fecha + timedelta(days=3)
            
            comentariosExtras = request.POST['comentarios']
                
            if comentariosExtras == "":
                comentarios = "Sin comentarios"
            else:
                comentarios = comentariosExtras
            
            
            #limiteDev = timedelta(days=3)
            #fechaLimiteDevolucion = int(fechaEntregaVestido)+int(limiteDev)
            #limiteDevCuota = timedelta(days=7)
            fechaLimiteDevolucionCuota =fechas +  timedelta(days=7)
            strfechaLimiteDevolucionCuota = str(fechaLimiteDevolucionCuota)

         

            costoTotalRenta = 0
            for productoRenta in arregloProductos:
                codigo = str(productoRenta)
                consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigo)   
                for datoProducto in consultaProducto:
                    costoRenta = datoProducto.costo_renta
                costoTotalRenta = costoTotalRenta + costoRenta


             
             
            empleadoVendedor = idEmpleado
            minimo = costoTotalRenta/2
            if rentaApartada == True: 
                montoAbono = request.POST['cantidadAbono']
                montoRestante = costoTotalRenta - float(montoAbono)
                
                
         
                    
                        
                registroRenta = Rentas(cliente = Clientes.objects.get(id_cliente = cliente), codigos_productos_renta = stringCodigosProductos,
                fecha_apartado = fechaApartado, fecha_entrega_renta = fechaEntregaVestido, fecha_limite_devolucion = fechas,fecha_limite_devolucion_cuota = strfechaLimiteDevolucionCuota
                , estado_devolucion = "A", cuota_retraso = "N", monto_total_renta=costoTotalRenta, monto_min_apartado = minimo, monto_pago_apartado = montoAbono, 
                monto_restante = montoRestante,monto_pago_restante = 0,comentarios_renta =comentarios, realizado_por = Empleados.objects.get(id_empleado = empleadoVendedor))
                registroRenta.save()

                if registroRenta:
                    for productoRenta in arregloProductos:
                        codigo = str(productoRenta)
                        actualizacionEstado = ProductosRenta.objects.filter(codigo_producto = codigo).update(estado_renta = "Apartado")  
                            
                            
                    formaPago = request.POST['tipoPago'] #Efectivo,  tarjeta o transferencia
                    sucursal = request.POST['idSucursal']
              
                    
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

                    
                
                
                    
                    arregloProductos = stringCodigosProductos.split(',')
                    productosVenta = []
                    cantidadesProductosVenta = [1]
        
                    
                    
                    for pro_ser in arregloProductos:
                        stringVenta = str(pro_ser)
                
                        intCantidad =int(1)
                        if "PR" in stringVenta:
                            productosVenta.append(stringVenta)
                            cantidadesProductosVenta.append(intCantidad)
                    
                        
                    listaProductosVenta =""
                    cantidadesListaProductosVenta =""
                
                    
                    lProductos =zip(productosVenta,cantidadesProductosVenta)
                    lProductos2 = zip(productosVenta,cantidadesProductosVenta)
            
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
                

                    #RegistrarProducto

                    if esConEfectivo:
                        
                                registroVenta = Ventas(fecha_venta = fechaApartado,  hora_venta =horaVenta,
                                tipo_pago = formaPago, 
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                cliente = Clientes.objects.get(id_cliente = cliente),
                                ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                monto_pagar = montoAbono, credito = "S",
                                comentariosVenta = "Se realizo venta por motivo de renta con apartado", sucursal = Sucursales.objects.get(id_sucursal = sucursal))

                    if esConTarjeta:
                    
                        
                                registroVenta = Ventas(fecha_venta = fechaApartado,  hora_venta =horaVenta,
                                tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta,
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                cliente = Clientes.objects.get(id_cliente = cliente),
                                ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                monto_pagar = montoAbono, credito = "S",
                                comentariosVenta = "Se realizo venta por motivo de renta con apartado", sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    

                    if esConTransferencia:
            
                                registroVenta = Ventas(fecha_venta = fechaApartado,  hora_venta =horaVenta,
                                tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                cliente = Clientes.objects.get(id_cliente = cliente),
                                ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                monto_pagar = montoAbono, credito = "S",comentariosVenta = "Se realizo venta por motivo de renta con apartado", sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                        

                    registroVenta.save()
                    
                    if registroVenta:
                        if esConEfectivo:
                            ultimoId = 0
                            ventasTotalesEfectivo = Ventas.objects.filter(tipo_pago ="Efectivo")
                            for venta in ventasTotalesEfectivo:
                                ultimoId = venta.id_venta
                            tipoMovimiento ="IN"
                            montoMovimiento = float(montoAbono)
                            descripcionMovimiento ="Movimiento por venta " + str(ultimoId) + " de renta con abono"
                            fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                            horaMovimiento = datetime.now().time()
                            ingresarCantidadEfectivoAcaja =MovimientosCaja(fecha =fechaMovimiento,hora = horaMovimiento,tipo=tipoMovimiento,monto =montoMovimiento, descripcion=descripcionMovimiento,sucursal =  Sucursales.objects.get(id_sucursal = sucursal),
                                                                                realizado_por = Empleados.objects.get(id_empleado = empleadoVendedor))
                            ingresarCantidadEfectivoAcaja.save()
                            
                            ultimoIdRenta = 0
                            rentasTotales = Rentas.objects.filter(estado_devolucion ="A",cliente =Clientes.objects.get(id_cliente = cliente))
                            for renta in rentasTotales:
                                ultimoIdRenta = renta.id_renta
                            
                            ventaApartadaCredito = Creditos(fecha_venta_credito=fechaApartado,empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),cliente =Clientes.objects.get(id_cliente = cliente),
                                                            
                                                            renta =Rentas.objects.get(id_renta = ultimoIdRenta),venta = Ventas.objects.get(id_venta = ultimoId),monto_pagar=costoTotalRenta,monto_pagado=montoAbono,monto_restante =montoRestante,concepto_credito="Renta",descripcion_credito="Crédito por renta " + str(ultimoIdRenta) ,estatus="Pendiente",
                                                            sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                            ventaApartadaCredito.save()
                            if ventaApartadaCredito:
                                ultimoIdCredito = 0
                                creditosTotales = Creditos.objects.filter(cliente =Clientes.objects.get(id_cliente = cliente))
                                for credito in creditosTotales:
                                    ultimoIdCredito = credito.id_credito
                                ingresarPrimerPago = PagosCreditos(id_credito=Creditos.objects.get(id_credito = ultimoIdCredito),fecha_pago1 =fechaApartado,tipo_pago1 ="Efectivo",monto_pago1=montoAbono)
                                ingresarPrimerPago.save()
                            
                            #IMPRESION DE TICKEEETSSSS
                            #Ultimo id de venta
                            consultaVentas = Ventas.objects.all()
                            ultimoIdVenta = 0
                            for venta in consultaVentas:
                                ultimoIdVenta = venta.id_venta

                            #ultimo id de renta
                            consultaRentas = Rentas.objects.all()
                            ultimoIdRenta = 0
                            for renta in consultaRentas:
                                ultimoIdRenta = renta.id_renta

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
                                c.EscribirTexto("RENTA #"+str(ultimoIdRenta)+"\n")
                                c.EscribirTexto("VENTA #"+str(ultimoIdVenta)+"\n")
                                c.EstablecerEnfatizado(False)
                                c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("\n")
                                c.EscribirTexto(str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                                c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                                c.EscribirTexto("\n")

                                #Listado de productos 
                                #Productos venta
                                
                                consultaProductoRenta = ProductosRenta.objects.filter(codigo_producto = stringCodigosProductos)
                                for datoProductoRenta in consultaProductoRenta:
                                    nombreProducto = datoProductoRenta.nombre_producto
                                    costoIndividualProducto = datoProductoRenta.costo_renta

                                costoIndividualProductoDecimales = str(costoIndividualProducto)

                                costoTotalProductoDivididoEnElPunto = costoIndividualProductoDecimales.split(".")
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
                                c.EscribirTexto("1 x "+nombreProducto+espaciosTicket+str(montoAbono)+"\n")


                                

                                
                                c.EscribirTexto("\n")
                                c.EscribirTexto("\n")
                                
                                restantePorPagar = float(costoIndividualProducto) - float(montoAbono)                               
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("TOTAL ABONADO:  $"+str(montoAbono)+"\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("TOTAL VESTIDO:  $"+str(costoIndividualProducto)+"\n")
                                c.EscribirTexto("TOTAL RESTANTE:  $"+str(restantePorPagar)+"\n")
                                c.EscribirTexto("\n")
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                                c.EscribirTexto("ENTREGA DEL VESTIDO\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("EL DÍA: "+str(fechaEntregaVestido)+"\n")
                                c.EstablecerEnfatizado(True)
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                                c.EscribirTexto("\n")
                                c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                                c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                                c.EstablecerEnfatizado(False)
                                c.EscribirTexto("\n")
                                c.EscribirTexto("Pago en efectivo.\n")
                                c.EscribirTexto("\n")
                                c.EstablecerEnfatizado(True)
                                c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                                c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                                
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

                            
                            #Renta Apartada Efectivo

                            
                            #Mandar Mensaje Por Telegram

                            try:
                                tokenTelegram = keysBotCostabella.tokenBotCostabellaRentas
                                botCostabella = telepot.Bot(tokenTelegram)

                                idGrupoTelegram = keysBotCostabella.idGrupo
                                
                                mensaje = " \U0001F457 RENTA APARTADA \U0001F457 \n El cliente "+nombreClienteTicket+" ha apartado el vestido "+nombreProducto+" para entregarlo el día "+fechaEntregaVestido+" en la sucursal "+nombreSucursal
                                botCostabella.sendMessage(idGrupoTelegram,mensaje)
                            except:
                                print("An exception occurred")

                                
                            request.session['rentaAgregada'] = "Renta Agregada Satisfactoriamente!"
                            return redirect('/verCalendarioRentas/')
                                
                        if esConTarjeta:
                            ultimoId = 0
                            ventasTotalesEfectivo = Ventas.objects.filter(tipo_pago ="Tarjeta")
                            for venta in ventasTotalesEfectivo:
                                ultimoId = venta.id_venta

                            ultimoIdRenta = 0
                            rentasTotales = Rentas.objects.filter(estado_devolucion ="A",cliente =Clientes.objects.get(id_cliente = cliente))
                            for renta in rentasTotales:
                                ultimoIdRenta = renta.id_renta
                            
                            ventaApartadaCredito = Creditos(fecha_venta_credito=fechaApartado,empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),cliente =Clientes.objects.get(id_cliente = cliente),
                                                              renta =Rentas.objects.get(id_renta = ultimoIdRenta),venta = Ventas.objects.get(id_venta = ultimoId),monto_pagar=costoTotalRenta,monto_pagado=montoAbono,monto_restante =montoRestante,concepto_credito="Renta",descripcion_credito="Crédito por renta " + str(ultimoIdRenta) ,estatus="Pendiente",
                                                            sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                            ventaApartadaCredito.save()
                            if ventaApartadaCredito:
                                ultimoIdCredito = 0
                                creditosTotales = Creditos.objects.filter(cliente =Clientes.objects.get(id_cliente = cliente))
                                for credito in creditosTotales:
                                    ultimoIdCredito = credito.id_credito
                                ingresarPrimerPago = PagosCreditos(id_credito=Creditos.objects.get(id_credito = ultimoIdCredito),fecha_pago1 =fechaApartado,tipo_pago1 ="Tarjeta",tipo_tarjeta1 =tipo_tarjeta,referencia_pago_tarjeta1=referencia_tarjeta,monto_pago1=montoAbono)
                                ingresarPrimerPago.save()

                            #IMPRESION DE TICKEEETSSSS
                            #Ultimo id de venta
                            consultaVentas = Ventas.objects.all()
                            ultimoIdVenta = 0
                            for venta in consultaVentas:
                                ultimoIdVenta = venta.id_venta

                            consultaRentas = Rentas.objects.all()
                            ultimoIdRenta = 0
                            for renta in consultaRentas:
                                ultimoIdRenta = renta.id_renta

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
                                c.EscribirTexto("ANTICIPO/APARTADO RENTA #"+str(ultimoIdRenta)+"\n")
                                c.EscribirTexto("VENTA #"+str(ultimoIdVenta)+"\n")
                                c.EstablecerEnfatizado(False)
                                c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("\n")
                                c.EscribirTexto(str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                                c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                                c.EscribirTexto("\n")

                                #Listado de productos 
                                #Productos venta
                                
                                consultaProductoRenta = ProductosRenta.objects.filter(codigo_producto = stringCodigosProductos)
                                for datoProductoRenta in consultaProductoRenta:
                                    nombreProducto = datoProductoRenta.nombre_producto
                                    costoIndividualProducto = datoProductoRenta.costo_renta

                                costoIndividualProductoDecimales = str(costoIndividualProducto)

                                costoTotalProductoDivididoEnElPunto = costoIndividualProductoDecimales.split(".")
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
                                c.EscribirTexto("1 x "+nombreProducto+espaciosTicket+str(montoAbono)+"\n")


                                

                                
                                c.EscribirTexto("\n")
                                c.EscribirTexto("\n")
                                
                                restantePorPagar = float(costoIndividualProducto) - float(montoAbono)                               
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("TOTAL ABONADO:  $"+str(montoAbono)+"\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("TOTAL VESTIDO:  $"+str(costoIndividualProducto)+"\n")
                                c.EscribirTexto("TOTAL RESTANTE:  $"+str(restantePorPagar)+"\n")
                                c.EscribirTexto("\n")
                                c.EstablecerEnfatizado(True)
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                                c.EscribirTexto("ENTREGA DEL VESTIDO\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("EL DÍA: "+str(fechaEntregaVestido)+"\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                                c.EscribirTexto("\n")
                                c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                                c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                                c.EstablecerEnfatizado(False)
                                c.EscribirTexto("\n")
                                c.EscribirTexto("Pago con "+str(tipo_tarjeta)+".\n")
                                c.EscribirTexto("Referencia: "+referencia_tarjeta+".\n")
                                c.EscribirTexto("\n")
                                c.EstablecerEnfatizado(True)
                                c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                                c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                                
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
                            
                            #Renta Apartada pagada con Tarjeta
                            try:
                                tokenTelegram = keysBotCostabella.tokenBotCostabellaRentas
                                botCostabella = telepot.Bot(tokenTelegram)

                                idGrupoTelegram = keysBotCostabella.idGrupo
                                
                                mensaje = " \U0001F457 RENTA APARTADA \U0001F457 \n El cliente "+nombreClienteTicket+" ha apartado el vestido "+nombreProducto+" para entregarlo el día "+fechaEntregaVestido+" en la sucursal "+nombreSucursal
                                botCostabella.sendMessage(idGrupoTelegram,mensaje)
                            except:
                                print("An exception occurred")

                            request.session['rentaAgregada'] = "Renta Agregada Satisfactoriamente!"
                            return redirect('/verCalendarioRentas/')
                     
                                
                        if esConTransferencia:
                            ultimoId = 0
                            ventasTotalesEfectivo = Ventas.objects.filter(tipo_pago ="Transferencia")
                            for venta in ventasTotalesEfectivo:
                                ultimoId = venta.id_venta

                            ultimoIdRenta = 0
                            rentasTotales = Rentas.objects.filter(estado_devolucion ="A",cliente =Clientes.objects.get(id_cliente = cliente))
                            for renta in rentasTotales:
                                ultimoIdRenta = renta.id_renta
                            
                            ventaApartadaCredito = Creditos(fecha_venta_credito=fechaApartado,empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),cliente =Clientes.objects.get(id_cliente = cliente),
                                                              renta =Rentas.objects.get(id_renta = ultimoIdRenta),venta = Ventas.objects.get(id_venta = ultimoId),monto_pagar=costoTotalRenta,monto_pagado=montoAbono,monto_restante =montoRestante,concepto_credito="Renta",descripcion_credito="Crédito por renta " + str(ultimoIdRenta) ,estatus="Pendiente",
                                                            sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                            ventaApartadaCredito.save()
                            if ventaApartadaCredito:
                                ultimoIdCredito = 0
                                creditosTotales = Creditos.objects.filter(cliente =Clientes.objects.get(id_cliente = cliente))
                                for credito in creditosTotales:
                                    ultimoIdCredito = credito.id_credito
                                ingresarPrimerPago = PagosCreditos(id_credito=Creditos.objects.get(id_credito = ultimoIdCredito),fecha_pago1 =fechaApartado,tipo_pago1 ="Transferencia",clave_rastreo_pago_transferencia1 =clave_transferencia,monto_pago1=montoAbono)
                                ingresarPrimerPago.save()
                            
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
                            
                            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                            for datoCliente in consultaCliente:
                                idCienteTicket = datoCliente.id_cliente
                                nombreCliente = datoCliente.nombre_cliente
                                apellidoCliente = datoCliente.apellidoPaterno_cliente

                            consultaRentas = Rentas.objects.all()
                            ultimoIdRenta = 0
                            for renta in consultaRentas:
                                ultimoIdRenta = renta.id_renta

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
                                c.EscribirTexto("ANTICIPO/APARTADO RENTA #"+str(ultimoIdRenta)+"\n")
                                c.EscribirTexto("VENTA #"+str(ultimoIdVenta)+"\n")
                                c.EstablecerEnfatizado(False)
                                c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("\n")
                                c.EscribirTexto(str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                                c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                                c.EscribirTexto("\n")

                                #Listado de productos 
                                #Productos venta
                                
                                consultaProductoRenta = ProductosRenta.objects.filter(codigo_producto = stringCodigosProductos)
                                for datoProductoRenta in consultaProductoRenta:
                                    nombreProducto = datoProductoRenta.nombre_producto
                                    costoIndividualProducto = datoProductoRenta.costo_renta

                                costoIndividualProductoDecimales = str(costoIndividualProducto)

                                costoTotalProductoDivididoEnElPunto = costoIndividualProductoDecimales.split(".")
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
                                c.EscribirTexto("1 x "+nombreProducto+espaciosTicket+str(montoAbono)+"\n")


                                

                                
                                c.EscribirTexto("\n")
                                c.EscribirTexto("\n")
                                
                                restantePorPagar = float(costoIndividualProducto) - float(montoAbono)                               
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("TOTAL ABONADO:  $"+str(montoAbono)+"\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("TOTAL VESTIDO:  $"+str(costoIndividualProducto)+"\n")
                                c.EscribirTexto("TOTAL RESTANTE:  $"+str(restantePorPagar)+"\n")
                                c.EscribirTexto("\n")
                                c.EstablecerEnfatizado(True)
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                                c.EscribirTexto("ENTREGA DEL VESTIDO\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("EL DÍA: "+str(fechaEntregaVestido)+"\n")
                                c.EstablecerTamañoFuente(1, 1)
                                c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                                c.EscribirTexto("\n")
                                c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                                c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                                c.EstablecerEnfatizado(False)
                                c.EscribirTexto("\n")
                                c.EscribirTexto("Transferencia.\n")
                                c.EscribirTexto("Clave de rastreo: "+str(clave_transferencia)+".\n")
                                c.EscribirTexto("\n")
                                c.EstablecerEnfatizado(True)
                                c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                                c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                                
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

                            #Renta Pagada con Transferencia
                            try:
                                tokenTelegram = keysBotCostabella.tokenBotCostabellaRentas
                                botCostabella = telepot.Bot(tokenTelegram)

                                idGrupoTelegram = keysBotCostabella.idGrupo
                                
                                mensaje = " \U0001F457 RENTA APARTADA \U0001F457 \n El cliente "+nombreClienteTicket+" ha apartado el vestido "+nombreProducto+" para entregarlo el día "+fechaEntregaVestido+" en la sucursal "+nombreSucursal
                                botCostabella.sendMessage(idGrupoTelegram,mensaje)
                            except:
                                print("An exception occurred")

                            request.session['rentaAgregada'] = "Renta Agregada Satisfactoriamente!"
                            return redirect('/verCalendarioRentas/')
                            
                            
                  
                      
                            

           
               
            else:  #Renta liquidada
                montoAbono = costoTotalRenta
                montoRestante = 0
             
             
             
                    
                    
                registroRenta = Rentas(cliente = Clientes.objects.get(id_cliente = cliente), codigos_productos_renta = stringCodigosProductos,
                fecha_apartado = fechaApartado, fecha_entrega_renta = fechaEntregaVestido, fecha_limite_devolucion = fechas,fecha_limite_devolucion_cuota = strfechaLimiteDevolucionCuota
                , estado_devolucion = "A", cuota_retraso = "N", monto_total_renta=costoTotalRenta, monto_min_apartado = minimo, monto_pago_apartado = montoAbono, 
                monto_restante = montoRestante,comentarios_renta =comentarios, realizado_por = Empleados.objects.get(id_empleado = empleadoVendedor))
                registroRenta.save()

                if registroRenta:
                    for productoRenta in arregloProductos:
                        codigo = str(productoRenta)
                        actualizacionEstado = ProductosRenta.objects.filter(codigo_producto = codigo).update(estado_renta = "En renta") 
                        
                       
               

                    
                    
                    formaPago = request.POST['tipoPago'] #Efectivo,  tarjeta o transferencia
                    sucursal = request.POST['idSucursal']
              
                    
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

                    
                
                
                    
                    arregloProductos = stringCodigosProductos.split(',')
                    productosVenta = []
                    cantidadesProductosVenta = [1]
        
                    
                    
                    for pro_ser in arregloProductos:
                        stringVenta = str(pro_ser)
                
                        intCantidad =int(1)
                        if "PR" in stringVenta:
                            productosVenta.append(stringVenta)
                            cantidadesProductosVenta.append(intCantidad)
                    
                        
                    listaProductosVenta =""
                    cantidadesListaProductosVenta =""
                
                    
                    lProductos =zip(productosVenta,cantidadesProductosVenta)
                    lProductos2 = zip(productosVenta,cantidadesProductosVenta)
            
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
                

                    #RegistrarProducto

                    if esConEfectivo:
                        
                                registroVenta = Ventas(fecha_venta = fechaApartado,  hora_venta =horaVenta,
                                tipo_pago = formaPago, 
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                cliente = Clientes.objects.get(id_cliente = cliente),
                                ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                monto_pagar = costoTotalRenta, credito = "N",
                                comentariosVenta = "Se realizo venta por motivo de renta sin apartado", sucursal = Sucursales.objects.get(id_sucursal = sucursal))

                    if esConTarjeta:
                    
                        
                                registroVenta = Ventas(fecha_venta = fechaApartado,  hora_venta =horaVenta,
                                tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta,
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                cliente = Clientes.objects.get(id_cliente = cliente),
                                ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                monto_pagar = costoTotalRenta, credito = "N",
                                comentariosVenta = "Se realizo venta por motivo de renta sin apartado", sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    

                    if esConTransferencia:
            
                                registroVenta = Ventas(fecha_venta = fechaApartado,  hora_venta =horaVenta,
                                tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                cliente = Clientes.objects.get(id_cliente = cliente),
                                ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                monto_pagar = costoTotalRenta, credito = "N", comentariosVenta = "Se realizo venta por motivo de renta sin apartado", sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                        

                    registroVenta.save()
                    
                    
                    if registroVenta and esConEfectivo:
                        ultimoId = 0
                        ventasTotalesEfectivo = Ventas.objects.filter(tipo_pago ="Efectivo")
                        for venta in ventasTotalesEfectivo:
                            ultimoId = venta.id_venta
                        tipoMovimiento ="IN"
                        montoMovimiento = float(costoTotalRenta)
                        descripcionMovimiento ="Movimiento por venta " + str(ultimoId) + "   de renta con pago completo "
                        fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                        horaMovimiento = datetime.now().time()
                        ingresarCantidadEfectivoAcaja =MovimientosCaja(fecha =fechaMovimiento,hora = horaMovimiento,tipo=tipoMovimiento,monto =montoMovimiento, descripcion=descripcionMovimiento,sucursal =  Sucursales.objects.get(id_sucursal = sucursal),
                                                                            realizado_por = Empleados.objects.get(id_empleado = empleadoVendedor))
                        ingresarCantidadEfectivoAcaja.save()
                 
                            
                            
                    #IMPRESION DE TICKEEETSSSS
                    #Ultimo id de venta
                    consultaVentas = Ventas.objects.all()
                    ultimoIdVenta = 0
                    for venta in consultaVentas:
                        ultimoIdVenta = venta.id_venta

                    #Ultimo id de renta
                    ultimoIdRenta = 0
                    consultaRentas = Rentas.objects.all()
                    for renta in consultaRentas:
                        ultimoIdRenta = renta.id_renta
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
                        c.EscribirTexto("APARTADO RENTA #"+str(ultimoIdRenta)+"\n")
                        c.EscribirTexto("VENTA #"+str(ultimoIdVenta)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        #Productos venta
                        
                        consultaProductoRenta = ProductosRenta.objects.filter(codigo_producto = stringCodigosProductos)
                        for datoProductoRenta in consultaProductoRenta:
                            nombreProducto = datoProductoRenta.nombre_producto
                            costoIndividualProducto = datoProductoRenta.costo_renta

                        costoIndividualProductoDecimales = str(costoIndividualProducto)

                        costoTotalProductoDivididoEnElPunto = costoIndividualProductoDecimales.split(".")
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
                        c.EscribirTexto("1 x "+nombreProducto+espaciosTicket+str(montoAbono)+"\n")


                        

                        
                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")
                        
                        restantePorPagar = float(costoIndividualProducto) - float(montoAbono)                               
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                        c.EscribirTexto("TOTAL:  $"+str(montoAbono)+"\n")
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("TOTAL VESTIDO:  $"+str(costoIndividualProducto)+"\n")
                        c.EscribirTexto("Pago de renta liquidado.\n")
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.EscribirTexto("ENTREGA DEL VESTIDO\n")
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("EL DÍA: "+str(fechaEntregaVestido)+"\n")
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
                    #Renta Liquidada pagada con Efectivo
                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabellaRentas
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo
                        
                        mensaje = " \U0001F457 RENTA APARTADA LIQUIDADA \U0001F457 \n El cliente "+nombreClienteTicket+" ha apartado el vestido "+nombreProducto+" para entregarlo el día "+fechaEntregaVestido+" en la sucursal "+nombreSucursal
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")

                    request.session['rentaAgregada'] = "Renta Agregada Satisfactoriamente!"
                    return redirect('/verCalendarioRentas/')
                else:
                    request.session['rentaNoAgregada'] = "Error en la base de datos, intentelo más tarde.."
                    return redirect('/seleccionarSucursalRentas/')
            
             
        

    else:
        return render(request,"1 Login/login.html")
    
    
def recibirRentaDevolucionCliente(request):

    if "idSesion" in request.session:
        idEmpleado = request.session['idSesion']

        if request.method == "POST":
            idRentaDevolucionPorcliente = request.POST['idRentaDevolucionPorcliente']
            comentarios = request.POST['comentarios']
          
            sucursal = request.POST['idSucursal']
            fechaDevolucion = request.POST['fechaDevolucionVestido']
            
         
            
            
            datosRenta = Rentas.objects.filter(id_renta = idRentaDevolucionPorcliente)
            for renta in datosRenta:
                fechaDevolucionLimiteCuota = renta.fecha_limite_devolucion_cuota
                retrasada = renta.cuota_retraso
                codigoVestido = renta.codigos_productos_renta
                montoTotal = renta.monto_total_renta
                cliente = renta.cliente_id
                idsProductos = renta.codigos_productos_renta

            montoTotalRentaCodigoBarras = montoTotal

            datosCliente = Clientes.objects.filter(id_cliente = cliente)
            for clienteDatos in datosCliente:
                nombreCliente = clienteDatos.nombre_cliente
                apellidosPaternoCliente = clienteDatos.apellidoPaterno_cliente
            nombreCompletoCliente = nombreCliente+" "+apellidosPaternoCliente
            
                


            datosCodigo = ProductosRenta.objects.filter(codigo_producto = codigoVestido)
            for datos in datosCodigo:
                nombreVestido = datos.nombre_producto
                idSucursal = datos.sucursal_id
            datoSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
            for sucursalDato in datoSucursal:
                nombreSucursal = sucursalDato.nombre
            

            
            montoCuota = montoTotal * 2    
            
            primerFecha= fechaDevolucion
            segundaFecha = fechaDevolucionLimiteCuota

            formato1 = datetime.strptime(primerFecha, '%Y-%m-%d')  #Fecha de cuando entrego
            formato2 = datetime.strptime(str(segundaFecha), '%Y-%m-%d') #Fecha límite que tenia para entregar..
                        
                    
            if formato1 >= formato2:
                conCuota = "Si"
                recibirRentaPendiente = Rentas.objects.filter(id_renta = idRentaDevolucionPorcliente).update(fecha_devolucion = fechaDevolucion,estado_devolucion = "F",descripcion_devolucion = comentarios,cuota_retraso ="Si",
                                                                                                                   monto_cuota= montoCuota,cuota_saldada="No")
             
            elif formato1 < formato2:
                conCuota = "No"
                
                recibirRentaPendiente = Rentas.objects.filter(id_renta = idRentaDevolucionPorcliente).update(fecha_devolucion = fechaDevolucion,estado_devolucion = "F",descripcion_devolucion = comentarios,cuota_retraso ="No")
                    
         
            #Pago por daño
            nameCheckboxDaño = "checkBoxDanio"+str(idRentaDevolucionPorcliente)
            if request.POST.get(nameCheckboxDaño,False): #checkbox chequeado
                pagoPorDaño = "Si"
            elif request.POST.get(nameCheckboxDaño,True): #checkbox deschequeado
                pagoPorDaño = "No"


            if pagoPorDaño == "Si":
                nivelDaño = 0
                nameSelectTipoDaño = "selectTipoDaño"+str(idRentaDevolucionPorcliente)
                selectTipoDaño = request.POST[nameSelectTipoDaño]

                if selectTipoDaño == "Leve":
                    nivelDaño = 500
                    nivelDañoFloat = float(nivelDaño)
                elif selectTipoDaño == "Grave":
                    nivelDaño = 1000
                    nivelDañoFloat = float(nivelDaño)

                nameTipoPago = "selectTipoPagoDaño"+str(idRentaDevolucionPorcliente)
                tipoPago = request.POST[nameTipoPago]

                esConEfectivo = False
                esConTarjeta = False
                esConTransferencia = False
                if tipoPago == "Efectivo":
                    esConEfectivo = True
                elif tipoPago == "Tarjeta":
                    esConTarjeta = True
                    
                    nameTipoTarjeta = "tipoTarjetaDaño"+str(idRentaDevolucionPorcliente)
                    tipoTarjeta = request.POST[nameTipoTarjeta]
                    nameReferenciaTarjeta = "referenciaTarjetaDaño"+str(idRentaDevolucionPorcliente)
                    referenciaBancaria = request.POST[nameReferenciaTarjeta]

                elif tipoPago == "Transferencia":
                    esConTransferencia = True
                    claveRastreoTransferencia = "claveRastreoTransferencia"+str(idRentaDevolucionPorcliente)
                #Fecha y hora
                fechaVenta = datetime.now() #La fecha con hora
                horaVenta= datetime.now().time()

                empleadoVendedor = idEmpleado

                comentarioDañito = "Pago por daño a vestido en la renta #"+str(idRentaDevolucionPorcliente)


                if esConEfectivo:
                    #Generar venta
                    
                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                    tipo_pago = tipoPago, 
                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                    cliente = Clientes.objects.get(id_cliente = cliente),
                    ids_productos = "", cantidades_productos = "",
                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                    monto_pagar = nivelDañoFloat, credito = "N",
                    comentariosVenta = comentarioDañito, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    #Generar movimiento de caja
                    registroVenta.save()

                    ultimoId = 0
                    ventasTotalesEfectivo = Ventas.objects.filter(tipo_pago ="Efectivo")
                    for venta in ventasTotalesEfectivo:
                        ultimoId = venta.id_venta
                    tipoMovimiento ="IN"
                    descripcionMovimiento ="Movimiento por daño a vestido, venta " + str(ultimoId)
                    fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                    horaMovimiento = datetime.now().time()
                    ingresarCantidadEfectivoAcaja =MovimientosCaja(fecha =fechaMovimiento,hora = horaMovimiento,tipo=tipoMovimiento,monto =nivelDañoFloat, descripcion=descripcionMovimiento,sucursal =  Sucursales.objects.get(id_sucursal = sucursal),
                                                                        realizado_por = Empleados.objects.get(id_empleado = empleadoVendedor))
                    ingresarCantidadEfectivoAcaja.save()

                
                if esConTarjeta:   
                    #Generar venta
                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                    tipo_pago = tipoPago, 
                    tipo_tarjeta = tipoTarjeta,
                    referencia_pago_tarjeta = referenciaBancaria,
                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                    cliente = Clientes.objects.get(id_cliente = cliente),
                    ids_productos = "", cantidades_productos = "",
                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                    monto_pagar = nivelDañoFloat, credito = "N",
                    comentariosVenta = comentarioDañito, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    #Generar movimiento de caja
                    registroVenta.save()
                    
                if esConTransferencia:

                    #Generar venta
                    #Generar venta
                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                    tipo_pago = tipoPago, 
                    clave_rastreo_transferencia = claveRastreoTransferencia,
                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                    cliente = Clientes.objects.get(id_cliente = cliente),
                    ids_productos = "", cantidades_productos = "",
                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                    monto_pagar = nivelDañoFloat, credito = "N",
                    comentariosVenta = comentarioDañito, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    #Generar movimiento de caja
                    registroVenta.save()
                
            datosCliente = Clientes.objects.filter(id_cliente= cliente)
            for datoC in datosCliente:
                idC = str(datoC.id_cliente)
                nombreC = datoC.nombre_cliente
                apellidoPat = datoC.apellidoPaterno_cliente
                apellidoMat = datoC.apellidoMaterno_cliente
            datosCompletosCliente = idC + " " + nombreC + " " + apellidoPat + " " + apellidoMat
            
            arregloProductos = idsProductos.split(',')
        
            

            if recibirRentaPendiente and pagoPorDaño == "Si":   #Si se recibe la renta pendiente y hay un daño..
                
                for productoRenta in arregloProductos:
                    codigo = str(productoRenta)
                    actualizacionEstado = ProductosRenta.objects.filter(codigo_producto = codigo).update(estado_renta = "Sin rentar")  
                
                #Imprimir ticket..

                #Ultimo id de venta
                consultaVentas = Ventas.objects.all()
                ultimoIdVenta = 0
                for venta in consultaVentas:
                    ultimoIdVenta = venta.id_venta

                #Fecha
                hoy = datetime.now()
                hoyFormato = hoy.strftime('%Y/%m/%d')
                horaVenta= datetime.now().time()

                #Empleado vendedor
                empleadoVendedor = idEmpleado
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
                    c.EscribirTexto("RENTA #"+str(idRentaDevolucionPorcliente)+"\n")
                    c.EscribirTexto("CUOTA POR DAÑO "+str(selectTipoDaño)+"\n")
                    c.EscribirTexto("VENTA #"+str(ultimoIdVenta)+"\n")
                    c.EstablecerEnfatizado(False)
                    c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                    c.EstablecerTamañoFuente(1, 1)
                    c.EscribirTexto("\n")
                    c.EscribirTexto(str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                    c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                    c.EscribirTexto("\n")

                    #Listado de productos 
                    #Productos venta
                    
                    consultaProductoRenta = ProductosRenta.objects.filter(codigo_producto = codigoVestido)
                    for datoProductoRenta in consultaProductoRenta:
                        nombreProducto = datoProductoRenta.nombre_producto

                    costoIndividualProductoDecimales = str(nivelDañoFloat)

                    costoTotalProductoDivididoEnElPunto = costoIndividualProductoDecimales.split(".")
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
                    c.EscribirTexto("1 x "+nombreProducto+espaciosTicket+str(costoIndividualProductoDecimales)+"\n")


                    

                    
                    c.EscribirTexto("\n")
                    c.EscribirTexto("\n")
                    c.EscribirTexto("TOTAL PAGADO:  $"+str(nivelDañoFloat)+"\n")
                    c.EscribirTexto("\n")
                    c.EstablecerTamañoFuente(2, 2)
                    c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                    c.EscribirTexto("RECEPCIÓN DEL VESTIDO\n")
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
                        c.EscribirTexto("Pago con "+str(tipoTarjeta)+".\n")
                        c.EscribirTexto("Referencia: "+referenciaBancaria+".\n")
                    elif esConTransferencia:
                        c.EscribirTexto("Transferencia.\n")
                        c.EscribirTexto("Clave de rastreo: "+str(claveRastreoTransferencia)+".\n")
                    c.EscribirTexto("\n")
                    c.EstablecerEnfatizado(True)
                    c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                    c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                    
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


                


                #recibir el vestido con daños
                if conCuota == "Si":
                    #recibido a destiempo con daño
                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabellaRentas
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo
                        
                        mensaje = " \U0001F457 RENTA RECIBIDA CON RETRASO Y DAÑO \U0001F457 \n El cliente "+nombreClienteTicket+" ha entregado el vestido "+nombreProducto+" con daño, después de la fecha límite en la sucursal "+nombreSucursal
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")
                    request.session['recibirRentaPendienteConCuota'] = "La renta número " + idRentaDevolucionPorcliente  +  " del cliente " + datosCompletosCliente + "  ha sido recibida correctamente! Aplica cuota!, Pago por daño recibido!"
                else:
                    #recibido a tiempo con daño
                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabellaRentas
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo
                        
                        mensaje = " \U0001F457 RENTA RECIBIDA A TIEMPO Y CON DAÑO \U0001F457 \n El cliente "+nombreClienteTicket+" ha entregado el vestido "+nombreProducto+" con daño a tiempo en la sucursal "+nombreSucursal
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")
                    request.session['recibirRentaPendiente'] = "La renta número " + idRentaDevolucionPorcliente  +  " del cliente " + datosCompletosCliente + "  ha sido recibida correctamente! Pago por daño recibido!"


            #Recibir vestido sin daños
            if recibirRentaPendiente:

                for productoRenta in arregloProductos:
                    codigo = str(productoRenta)
                    actualizacionEstado = ProductosRenta.objects.filter(codigo_producto = codigo).update(estado_renta = "Sin rentar")  
                
                
                #recibir vestido después de la fecha limite
                if conCuota == "Si":
                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabellaRentas
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo
                        
                        mensaje = " \U0001F457 RENTA RECIBIDA CON RETRASO \U0001F457 \n El cliente "+nombreCompletoCliente+" ha entregado el vestido "+nombreVestido+" después de la fecha límite en la sucursal "+nombreSucursal
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")
                    request.session['recibirRentaPendienteConCuota'] = "La renta número " + idRentaDevolucionPorcliente  +  " del cliente " + datosCompletosCliente + "  ha sido recibida correctamente! Aplica cuota!"
                else:
                    #recibir el vestido a tiempo
                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabellaRentas
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo
                        
                        mensaje = " \U0001F457 RENTA ENTREGADA A TIEMPO \U0001F457 \n El cliente "+nombreCompletoCliente+" ha entregado el vestido "+nombreVestido+" a tiempo en la sucursal "+nombreSucursal
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")
                    request.session['recibirRentaPendiente'] = "La renta número " + idRentaDevolucionPorcliente  +  " del cliente " + datosCompletosCliente + "  ha sido recibida correctamente!"
            
            #ImprimirEtiquetas
            fechaHoy = date.today()
            cantidadEtiquetas = int(1)
            
            primerDigitoCodigo = codigoVestido[2]
            segundoDigitoCodigo = codigoVestido[3]
            tercerDigitoCodigo = codigoVestido[4]
            cuartoDigitoCodigo = codigoVestido[5]
            
            numeroCompletoCodigo = primerDigitoCodigo + segundoDigitoCodigo + tercerDigitoCodigo + cuartoDigitoCodigo
            codigoCompletoImprimir = str(numeroCompletoCodigo)

            for x in range(cantidadEtiquetas):
                label = ("^XA~TA000~JSN^LT0^MNW^MTD^PON^PMN^LH0,0^JMA^PR2,2~SD30^JUS^LRN^CI0^XZ^XA^MMT^PW406^LL0203^LS0^FO0,160^GFA,00768,00768,00012,:Z64:eJxjYKAnYD/i3n5/zsfzIDb/u/f3z99tf98AZLOlJd69e/d44gEgm+/d+//n/v17fACs3vf+/TvmBw+A1T/uP7//8UMQm4EtgfGADAMjmM33gPGBHQMzmM3iABLjb4CKA9l89PCXvPzH57bHIWz+/7u/J4J9xcAge/9CeeEdiDjf/d2/baFs+fufy3nPQdX3/37/E6oeCNgZGOFsZgZuOJuB8TzCPsZz1PbBSAUAlzNF0w==:6D8B^FO128,128^GFA,01920,01920,00020,:Z64:eJztkT1Lw0Ach+8uoRdDKR2rtE2wy9mpHQotCCp+gRQaOwmCq0OkVh0KnukgBPETOJx1CefiR2jtUOjuKqGCrgFB3Opd2sGXDuKiQ39wy3MP9/L7AzDPPH8dNINBaFnJqlpNfoRUmvSruj5dv4o5g1nfkc4/XZvEXSOo285LL2xhGAqSIGTIONM54yPWSbi+YKWnyttuj0ILZrOLvczgQrCcu3Kba1PE0VJZO2Wu/JFyVgnWFFqyrXR5sR/uKYIhl7A8onnP14h2x0jk4eLgVaH3di3lpPpBS3oKKnodBDj3SaFsXvnSw4nG5aMCm/XDVaeQ3uhieZ63fE494XHCzBiNmsTpRqY3hra9fRzsP2x2VcnK1wttFwmvMrzxkavLO8JnA8dw0z4yjHF4ghNRByMd6cjjohgGdF2TCA5ALL5j2zUAuwDE05HnAqSZnPjR5DQy9TAMtqoHkaA6Uw/w6b547qRuddL2D+c2y5tnnv+bd/8tZhU=:C773^FO8,97^GB391,0,2^FS^BY2,3,61^FT295,29^BCI,,Y,N^FD>:PR>5"+codigoCompletoImprimir+"^FS^FT398,178^A0I,14,14^FH\^FD"+str(fechaHoy)+"^FS^FT236,119^A0I,14,14^FH\^FD"+nombreVestido+"^FS^FT237,143^A0I,11,12^FH\^FDNombre vestido:^FS^FT376,143^A0I,17,16^FH\^FDCosto de renta^FS^FT376,110^A0I,28,28^FH\^FD$ "+str(montoTotalRentaCodigoBarras)+" ^FS^PQ1,0,1,Y^XZ")
                
                z = Zebra('ZDesigner GC420d')
                z.output(label)
            
            return redirect('/verCalendarioRentas/') 
        
        
    
    else:
        return render(request,"1 Login/login.html")
    
def recibirPagoCuota(request):

    if "idSesion" in request.session:
        idEmpleado = request.session['idSesion']

        if request.method == "POST":
            idRentaPagoCuota = request.POST['idRentaPagoCuota']

            consultaRenta = Rentas.objects.filter(id_renta = idRentaPagoCuota)
            for datosRenta in consultaRenta:
                codigoProducto = datosRenta.codigos_productos_renta
            
            consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigoProducto)
            for datoProducto in consultaProducto:
                sucursal = datoProducto.sucursal_id
         
          
          
            formaPagoCuota = request.POST['tipoPago'] #Efectivo,  tarjeta o transferencia
            montoCuota =request.POST['montoCuota']
           
            
            fechaPagoCuota = datetime.today().strftime('%Y-%m-%d')
            horaPago = datetime.now().time()
            
          
                    
            esConEfectivo = False
            esConTarjeta = False
            esConTransferencia = False

            if formaPagoCuota == "Efectivo":
                esConEfectivo = True
            elif formaPagoCuota == "Tarjeta":
                esConTarjeta = True
                tipo_tarjeta = request.POST['tipoTarjetaCuota']    
                referencia_tarjeta = request.POST['referenciaTarjeta'] 
                        
            elif formaPagoCuota == "Transferencia":
                esConTransferencia = True
                clave_transferencia = request.POST['claveRastreoTransferencia']            
            

         

            infoRenta = Rentas.objects.filter(id_renta = idRentaPagoCuota)
            
            for dato in infoRenta:
                cliente = dato.cliente_id
                abonado = dato.monto_pago_apartado
              
                idsProductos = dato.codigos_productos_renta
                
            datosCliente = Clientes.objects.filter(id_cliente= cliente)
            for datoC in datosCliente:
                idC = str(datoC.id_cliente)
                nombreC = datoC.nombre_cliente
                apellidoPat = datoC.apellidoPaterno_cliente
                apellidoMat = datoC.apellidoMaterno_cliente
            datosCompletosCliente = idC + " " + nombreC + " " + apellidoPat + " " + apellidoMat
            
         
            
                
                
             
            pagoCuotaRenta = Rentas.objects.filter(id_renta = idRentaPagoCuota).update(monto_cuota = montoCuota,cuota_saldada = "Si",
                                                                                           realizado_por =idEmpleado)
            
            arregloProductos = idsProductos.split(',')
            productosVenta = []
            cantidadesProductosVenta = [1]
        
                    
                    
            for pro_ser in arregloProductos:
                stringVenta = str(pro_ser)
                
                intCantidad =int(1)
                if "PR" in stringVenta:
                    productosVenta.append(stringVenta)
                    cantidadesProductosVenta.append(intCantidad)
                    
                        
            listaProductosVenta =""
            cantidadesListaProductosVenta =""
                
                    
            lProductos =zip(productosVenta,cantidadesProductosVenta)
            lProductos2 = zip(productosVenta,cantidadesProductosVenta)
            
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
            
            
            
            if pagoCuotaRenta: 
                
               
                
                if esConEfectivo:
                    
                    registroVenta = Ventas(fecha_venta = fechaPagoCuota, hora_venta =horaPago,
                            tipo_pago = formaPagoCuota, 
                            empleado_vendedor = Empleados.objects.get(id_empleado = idEmpleado), cliente = Clientes.objects.get(id_cliente = cliente),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                            ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                            monto_pagar = montoCuota, credito = "N",cuota="S",
                            comentariosVenta = "Se ingreso efectivo por motivo de cuota de renta " + idRentaPagoCuota, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    registroVenta.save()
                    if registroVenta:
                        tipoMovimiento ="IN"
                        montoMovimiento = float(montoCuota)
                        descripcionMovimiento ="Movimiento por cuota de renta  " + idRentaPagoCuota + " por el cliente " + datosCompletosCliente 
                        fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                        horaMovimiento = datetime.now().time()
                        ingresarCantidadEfectivoAcaja =MovimientosCaja(fecha =fechaMovimiento,hora = horaMovimiento,tipo=tipoMovimiento,monto =montoMovimiento, descripcion=descripcionMovimiento,sucursal =  Sucursales.objects.get(id_sucursal = sucursal),
                                                                                    realizado_por = Empleados.objects.get(id_empleado = idEmpleado))
                        ingresarCantidadEfectivoAcaja.save()
                 
                            
                if esConTarjeta:
                    registroVenta = Ventas(fecha_venta = fechaPagoCuota,  hora_venta =horaPago,
                            tipo_pago = formaPagoCuota, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta,
                            empleado_vendedor = Empleados.objects.get(id_empleado = idEmpleado),
                            cliente = Clientes.objects.get(id_cliente = cliente),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                            ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                            monto_pagar = montoCuota, credito = "N",cuota="S",
                            comentariosVenta = "Se ingreso efectivo por motivo de cuota de renta " + idRentaPagoCuota, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    registroVenta.save()
                    
                 
                        
                if esConTransferencia:
                    registroVenta = Ventas(fecha_venta = fechaPagoCuota,  hora_venta =horaPago,
                            tipo_pago = formaPagoCuota, clave_rastreo_transferencia = clave_transferencia,
                            empleado_vendedor = Empleados.objects.get(id_empleado = idEmpleado),
                            cliente = Clientes.objects.get(id_cliente = cliente),
                            ids_productos = listaProductosVenta, cantidades_productos = cantidadesListaProductosVenta,
                            ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                            ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                            monto_pagar = montoCuota, credito = "N",cuota="S",comentariosVenta = "Se ingreso efectivo por motivo de cuota de renta " + idRentaPagoCuota, sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    
                    registroVenta.save()
                    
                
                if registroVenta:
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
                    empleadoVendedor = idEmpleado
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
                    
                    consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                    for datoCliente in consultaCliente:
                        idCienteTicket = datoCliente.id_cliente
                        nombreCliente = datoCliente.nombre_cliente
                        apellidoCliente = datoCliente.apellidoPaterno_cliente

                    nombreClienteTicket = nombreCliente + " " + apellidoCliente
                    #Hora bien
                    horaVenta= datetime.now().time()
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
                        c.EscribirTexto("CUOTA DE RENTA #"+str(idRentaPagoCuota)+" \n")
                        c.EscribirTexto("VENTA #"+str(ultimoIdVenta)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        #Productos venta
                        
                        consultaProductoRenta = ProductosRenta.objects.filter(codigo_producto = codigoProducto)
                        for datoProductoRenta in consultaProductoRenta:
                            nombreProducto = datoProductoRenta.nombre_producto
                            costoIndividualProducto = datoProductoRenta.costo_renta

                        costoIndividualProductoDecimales = str(costoIndividualProducto)

                        costoTotalProductoDivididoEnElPunto = costoIndividualProductoDecimales.split(".")
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
                        c.EscribirTexto("1 x "+nombreProducto+espaciosTicket+str(montoCuota)+"\n")


                        

                        
                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")
                        
                        restantePorPagar = float(costoIndividualProducto) - float(montoCuota)                               
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                        c.EscribirTexto("TOTAL DE CUOTA:  $"+str(montoCuota)+"\n")
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("TOTAL VESTIDO:  $"+str(costoIndividualProducto)+"\n")
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
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
               
                
                request.session['rentaCuotaPagada'] = "La cuota de la renta número " + idRentaPagoCuota  +  " ha sido saldada por el  " + datosCompletosCliente + "  correctamente!"
            return redirect('/verCalendarioRentas/') 
        
     
    
    else:
        return render(request,"1 Login/login.html")
    

def notificacionRentasDeHoy(request):
     #Si ya existe una sesion al teclear login...
    if "idSesion" in request.session:
        idEmpleado = request.session['idSesion']
        tipoUsuario = request.session['tipoUsuario']
        datosEmpleado = Empleados.objects.filter(id_empleado =idEmpleado)
        for empleado in datosEmpleado:
            sucursal = empleado.id_sucursal_id
            nombreEmpleado = empleado.nombres
        
        datosSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
        for dato in datosSucursal:
            nombreSucursalita = dato.nombre
        
        fechaHoy = date.today()
        rentas = Rentas.objects.filter(Q(fecha_entrega_renta =  fechaHoy) | Q(fecha_limite_devolucion = fechaHoy))

        rentasNotificacion =[]
        mensajeRentas = ""
        for renta in rentas:
            idRenta = renta.id_renta
            #cliente
            cliente = renta.cliente_id
            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
            for datoCliente in consultaCliente:
                nombreCliente = datoCliente.nombre_cliente
                apellidoCliente = datoCliente.apellidoPaterno_cliente
            nombreCompletoCliente = nombreCliente+" "+apellidoCliente

            #Vestido y sucursal
            vestido = renta.codigos_productos_renta
            consultaVestido = ProductosRenta.objects.filter(codigo_producto = vestido)
            for datoVestido in consultaVestido:
                codigoVestido = datoVestido.codigo_producto
                nombreVestido = datoVestido.nombre_producto
                sucursalVestido = datoVestido.sucursal_id
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalVestido)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
            
            #Estado de renta
            estado = renta.estado_devolucion

            

    
            
            rentasNotificacion.append([idRenta,nombreSucursal,nombreCompletoCliente, codigoVestido, nombreVestido, estado])  

            
            contador = 0
            for renta in rentasNotificacion:
                idRenta = renta[0]
                nombreSucursal = renta[1]
                nombreCompletoCliente = renta[2]
                codigoVestido = renta[3]
                nombreVestido = renta[4]
                estado = renta[5]

                contador = contador + 1
                if contador == 1:
                    if estado == "A": #Apartado a
                        mensajeRentas = "\U0001f457 Renta #"+str(idRenta)+" en "+str(nombreSucursal)+" a "+(nombreCompletoCliente) +" -- \U0001F91D Entrega de vestido "+str(codigoVestido) + " "+nombreVestido+"."
                    elif estado == "P": #Pendiente de devolver
                        mensajeRentas = "\U0001f457 Renta #"+str(idRenta)+" en "+str(nombreSucursal)+" a "+(nombreCompletoCliente) +" -- \U0001F4CC Devolución de vestido "+str(codigoVestido) + " "+nombreVestido+"."
                else:
                    if estado == "A": #Apartado a
                        mensajeRentas = mensajeRentas+", \n"+"\U0001f457 Renta #"+str(idRenta)+" en "+str(nombreSucursal)+" a "+(nombreCompletoCliente) +" -- \U0001F91D Entrega de vestido "+str(codigoVestido) + " "+nombreVestido+"."
                    elif estado == "P":#Pendiente de devolver
                        mensajeRentas = mensajeRentas +", \n" +"\U0001f457 Renta #"+str(idRenta)+" en "+str(nombreSucursal)+" a "+(nombreCompletoCliente) +" -- \U0001F4CC Devolución de vestido "+str(codigoVestido) + " "+nombreVestido+"."
        try:
            tokenTelegram = keysBotCostabella.tokenBotCostabellaRentas
            botCostabella = telepot.Bot(tokenTelegram)

            idGrupoTelegram = keysBotCostabella.idGrupo
            
            mensaje = "Hola \U0001F44B! \nLa empleada "+nombreEmpleado+" ha generado un aviso de rentas del día!.\nEste es el itinerario de hoy:\n"+mensajeRentas
            botCostabella.sendMessage(idGrupoTelegram,mensaje)
        except:
            print("An exception occurred")

        request.session["rentasEnviadas"] = "Se ha notificado a los administradores sobre las rentas del día!"
        return redirect("/rentas/")
        
        
        
              
        
    # Si no hay una sesion iniciada..
    else:
        return render(request, "1 Login/login.html")

