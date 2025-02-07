
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

# Librerías de fecha
from datetime import date, datetime, time, timedelta

# Importacion de modelos
from appCostabella.models import (Citas, Clientes, ConfiguracionCredito, Creditos, Descuentos, Empleados, PagosCreditos, Permisos, ProductosRenta,
                                  ProductosVenta, Rentas, Servicios, Sucursales, Ventas)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)
from django.db.models import Q

def verClientes(request):

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

        
        clientes = Clientes.objects.all()
        

        contadorActivos = 0
        contadorBloqueados = 0
        clientesActivos = Clientes.objects.filter(estado = "A")
        clientesBloqueados = Clientes.objects.filter(estado = "B")
        
        for activo in clientesActivos:
            contadorActivos = contadorActivos + 1
        for inactivo in clientesBloqueados:
            contadorBloqueados = contadorBloqueados + 1

        #AQUI EMPIEZAAAAAAAAAAAAAAAAAAAAAAA
        empleadosQueAgregaron = []
        datosClientes = []
        for cliente in clientes:
            idCliente = cliente.id_cliente
            nombre = cliente.nombre_cliente
            apellidoPat = cliente.apellidoPaterno_cliente
            apellidoMat = cliente.apellidoMaterno_cliente
            correo = cliente.correo
            telefono = cliente.telefono
            direccion = cliente.direccion
            if cliente.estado == "A":
                estado = "Activo"
            elif cliente.estado == "B":
                estado = "Bloqueado"
            fechaAgregado = cliente.fecha_agregado
            id_empleadoQueAgrego = cliente.agregado_por_id
            
            consultaEmpleado = Empleados.objects.filter(id_empleado = id_empleadoQueAgrego)
            for dato in consultaEmpleado:
                idEmpleadoAgrego = dato.id_empleado
                nombres = dato.nombres
                apellido = dato.apellido_paterno
            empleadoCompleto = str(idEmpleadoAgrego) + " - " + nombres + " " + apellido
 
            
            datosClientes.append([idCliente, nombre, apellidoPat, apellidoMat, correo, telefono, direccion, estado, fechaAgregado])
            empleadosQueAgregaron.append([idEmpleadoAgrego,empleadoCompleto])
            
        #CLIENTES ACTIVOS
        empleadosQueAgregaronActivos = []
        datosClientesActivos = []
        for clienteActivos in clientesActivos:
            idClienteActivos = clienteActivos.id_cliente
            nombreActivos = clienteActivos.nombre_cliente
            apellidoPatActivos = clienteActivos.apellidoPaterno_cliente
            apellidoMatActivos = clienteActivos.apellidoMaterno_cliente
            correoActivos = clienteActivos.correo
            telefonoActivos = clienteActivos.telefono
            direccionActivos = clienteActivos.direccion
            if clienteActivos.estado == "A":
                estadoA = "Activo"
            elif clienteActivos.estado == "B":
                estadoA = "Bloqueado"
            fechaAgregadoActivos = clienteActivos.fecha_agregado
            id_empleadoQueAgregoActivos = clienteActivos.agregado_por_id
            
            consultaEmpleadoActivos = Empleados.objects.filter(id_empleado = id_empleadoQueAgregoActivos)
            for datoActivos in consultaEmpleadoActivos:
                idEmpleadoAgregoActivos = datoActivos.id_empleado
                nombresActivos = datoActivos.nombres
                apellidoActivos = datoActivos.apellido_paterno
            empleadoCompletoActivos = str(idEmpleadoAgregoActivos) + " - " + nombresActivos + " " + apellidoActivos
 
            
            datosClientesActivos.append([idClienteActivos, nombreActivos, apellidoPatActivos, apellidoMatActivos, correoActivos, telefonoActivos, direccionActivos, estadoA, fechaAgregadoActivos])
            empleadosQueAgregaronActivos.append([idEmpleadoAgregoActivos,empleadoCompletoActivos])
        
        #CLIENTES BLOQUEADOS
        empleadosQueAgregaronBloqueados = []
        datosClientesBloqueados = []
        for clienteBloqueados in clientesBloqueados:
            idClienteBloqueados = clienteBloqueados.id_cliente
            nombreBloqueados = clienteBloqueados.nombre_cliente
            apellidoPatBloqueados = clienteBloqueados.apellidoPaterno_cliente
            apellidoMatBloqueados = clienteBloqueados.apellidoMaterno_cliente
            correoBloqueados = clienteBloqueados.correo
            telefonoBloqueados = clienteBloqueados.telefono
            direccionBloqueados = clienteBloqueados.direccion
            if clienteBloqueados.estado == "A":
                estadoB = "Activo"
            elif clienteBloqueados.estado == "B":
                estadoB = "Bloqueado"
            fechaAgregadoBloqueados = clienteBloqueados.fecha_agregado
            id_empleadoQueAgregoBloqueados = clienteBloqueados.agregado_por_id
            
            consultaEmpleadoBloqueados = Empleados.objects.filter(id_empleado = id_empleadoQueAgregoBloqueados)
            for datoBloqueados in consultaEmpleadoBloqueados:
                idEmpleadoAgregoBloqueados = datoBloqueados.id_empleado
                nombresBloqueados = datoBloqueados.nombres
                apellidoBloqueados = datoBloqueados.apellido_paterno
            empleadoCompletoBloqueados = str(idEmpleadoAgregoBloqueados) + " - " + nombresBloqueados + " " + apellidoBloqueados
 
            
            datosClientesBloqueados.append([idClienteBloqueados, nombreBloqueados, apellidoPatBloqueados, apellidoMatBloqueados, correoBloqueados, telefonoBloqueados, direccionBloqueados, estadoB, fechaAgregadoBloqueados])
            empleadosQueAgregaronBloqueados.append([idEmpleadoAgregoBloqueados,empleadoCompletoBloqueados])
            
        
            

        # 3 LISTAS   
        listaClientes = zip (datosClientes, empleadosQueAgregaron)
        listaClientesActivos = zip (datosClientesActivos, empleadosQueAgregaronActivos)
        listaClientesBloqueados = zip (datosClientesBloqueados, empleadosQueAgregaronBloqueados)

        if 'clienteActualizado' in request.session:
            mensaje = request.session['clienteActualizado']
            del request.session['clienteActualizado']

            return render(request, "5 Clientes/verClientes.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaClientes": listaClientes,
        "contadorActivos":contadorActivos, "contadorBloqueados":contadorBloqueados, "mensaje":mensaje,"listaClientesActivos":listaClientesActivos,"listaClientesBloqueados":listaClientesBloqueados,"notificacionRenta":notificacionRenta,"notificacionCita":notificacionCita, })

        return render(request, "5 Clientes/verClientes.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "listaClientes": listaClientes,
        "contadorActivos":contadorActivos, "contadorBloqueados":contadorBloqueados,"listaClientesActivos":listaClientesActivos,"listaClientesBloqueados":listaClientesBloqueados,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita,})
    else:
        return render(request,"1 Login/login.html")

def altaCliente(request):

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
            nombresCliente = request.POST['nombresCliente']
            apellidoPatCliente = request.POST['apellidoPatCliente']
            apellidoMatCliente = request.POST['apellidoMatCliente']
            telefonoCliente = request.POST['telefonoCliente']
            correoCliente = request.POST['correoCliente']
            direccionCliente = request.POST['direccionCliente']
         
            fechaAgregado = datetime.today().strftime('%Y-%m-%d')
            
            if telefonoCliente == "":
            
                registroCliente = Clientes(nombre_cliente = nombresCliente, apellidoPaterno_cliente = apellidoPatCliente, apellidoMaterno_cliente = apellidoMatCliente, correo = correoCliente, telefono = "Sin número de teléfono",
                                       direccion = direccionCliente, fecha_agregado = fechaAgregado, agregado_por = Empleados.objects.get(id_empleado = idEmpleado), estado ="A", credito_libre = "S")
            
            elif correoCliente == "":

                registroCliente = Clientes(nombre_cliente = nombresCliente, apellidoPaterno_cliente = apellidoPatCliente, apellidoMaterno_cliente = apellidoMatCliente, correo = "Sin correo electrónico", telefono = telefonoCliente,
                                       direccion = direccionCliente, fecha_agregado = fechaAgregado, agregado_por = Empleados.objects.get(id_empleado = idEmpleado), estado ="A",credito_libre = "S")
            elif telefonoCliente == "" and correoCliente == "":
                registroCliente = Clientes(nombre_cliente = nombresCliente, apellidoPaterno_cliente = apellidoPatCliente, apellidoMaterno_cliente = apellidoMatCliente, correo = "Sin correo electrónico", telefono = "Sin número de teléfono",
                                       direccion = direccionCliente, fecha_agregado = fechaAgregado, agregado_por = Empleados.objects.get(id_empleado = idEmpleado), estado ="A",credito_libre = "S")
            else:
                registroCliente = Clientes(nombre_cliente = nombresCliente, apellidoPaterno_cliente = apellidoPatCliente, apellidoMaterno_cliente = apellidoMatCliente, correo = correoCliente, telefono = telefonoCliente,
                                       direccion = direccionCliente, fecha_agregado = fechaAgregado, agregado_por = Empleados.objects.get(id_empleado = idEmpleado), estado ="A",credito_libre = "S")
                
            registroCliente.save()

            if registroCliente:
                    clienteAgregado = "El cliente "+ nombresCliente + " ha sido agregado satisfactoriamente!"
                    return render(request, "5 Clientes/altaCliente.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado, "idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "clienteAgregado":clienteAgregado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
            else:
                    clienteNoAgregado = "Error en la base de datos, intentelo más tarde.."
                    return render(request, "5 Clientes/altaCliente.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "clienteNoAgregado":clienteNoAgregado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})

        return render(request, "5 Clientes/altaCliente.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")

def bloqueoCliente(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idClienteBaja = request.POST['idClienteBaja']

            consultaCliente = Clientes.objects.filter(id_cliente = idClienteBaja)

            for dato in consultaCliente:
                nombre = dato.nombre_cliente


            actualizacionCliente = Clientes.objects.filter(id_cliente = idClienteBaja).update(estado="B")
            
            if actualizacionCliente:    
                request.session['clienteActualizado'] = "El cliente " + nombre + " ha sido bloqueado satisfactoriamente!"
                return redirect('/verClientes/')

def activoCliente(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idClienteAlta = request.POST['idClienteAlta']

            consultaCliente = Clientes.objects.filter(id_cliente = idClienteAlta)

            for dato in consultaCliente:
                nombre = dato.nombre_cliente


            actualizacionCliente = Clientes.objects.filter(id_cliente = idClienteAlta).update(estado="A")
            
            if actualizacionCliente:    
                request.session['clienteActualizado'] = "El cliente " + nombre + " se ha activado satisfactoriamente!"
                return redirect('/verClientes/')

def infoCliente(request):

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

        
        clienteInfo = []
        
        if request.method == "POST":
            idCliente = request.POST['idInfoCliente']
            
            datosCliente = Clientes.objects.filter(id_cliente = idCliente)
            
            for dato in datosCliente:
                idC = dato.id_cliente
                idClienteEstatus = dato.id_cliente
                idClienteTelefono = dato.id_cliente
                nombres = dato.nombre_cliente
                apellidoP = dato.apellidoPaterno_cliente
                apellidoM = dato.apellidoMaterno_cliente
                correo = dato.correo
                correo2 = dato.correo
                telefono = dato.telefono
                telefonoParaActualizar = dato.telefono
                direccion = dato.direccion
                fechaAgrego = dato.fecha_agregado
                estado = dato.estado
                estado2 = dato.estado
                persona_agrego = dato.agregado_por_id
            
                
                clienteCompleto = nombres + " " + apellidoP
                letrasCliente = nombres[0]+apellidoP[0]
                
                personaAgrego = Empleados.objects.filter(id_empleado = persona_agrego)
                
                for datoAgrego in personaAgrego:
                    nombre = datoAgrego.nombres
                    apellidoPat = datoAgrego.apellido_paterno
                    
                completoAgrego = nombre + " " + apellidoPat
                
                clienteInfo.append([idC,nombres,apellidoP,apellidoM,correo,telefono,direccion, fechaAgrego,estado,completoAgrego])
            
            #CANTIDADES COMPRAS
            cantidadCompras = 0
            totalComprado = 0
            consultaCompras = Ventas.objects.filter(cliente_id__id_cliente = idCliente, credito="N")
            for compra in consultaCompras:
                montoCompra = compra.monto_pagar
                totalComprado = totalComprado + montoCompra
                cantidadCompras = cantidadCompras + 1

            #COMPRAS REALIZADAS POR CLIENTE
            listaVentasCliente = Ventas.objects.filter(cliente = idCliente, credito="N")
            quienVendioCliente = [] #id, nombre y sucursal del empleado
            sucursalesVentaCliente = []
            tipos_pagos = []
            pagos_tarjeta = []
            pagos_transferencia = []
            #Descuentos
            booleanDescuentoVentaCliente = []
            totalesSinDescuentoVentaCliente = []
            descuentosVentaCliente  = []
            datosDescuentosVentaCliente  = []
            #Productos
            boolProductosVentaCliente  = []
            datosProductosVentaCliente  = []
            #Servicios Faciales
            boolServiciosCoorporalesVentaCliente  = []
            datosServiciosCoorporalesVentaCliente  = []
            #Servicios Corporales
            boolServiciosFacialesVentaCliente  = []
            datosServiciosFacialesVentaCliente  = []
            
            for ventaCliente in listaVentasCliente:
                empleado_vendedor = ventaCliente.empleado_vendedor_id
                tipo_pago = ventaCliente.tipo_pago
                sucursal = ventaCliente.sucursal_id
                descuento = ventaCliente.descuento_id
                monto_total_pagado = ventaCliente.monto_pagar
                codigosProductos = ventaCliente.ids_productos
                serviciosCorporales = ventaCliente.ids_servicios_corporales
                serviciosFaciales = ventaCliente.ids_servicios_faciales
                

                #Datos empleado vendedor
                consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleado_vendedor)
                for datoEmpleadoVendedor in consultaEmpleadoVendedor:
                    idEmpleado = datoEmpleadoVendedor.id_empleado
                    nombreEmpleado = datoEmpleadoVendedor.nombres
                    
                quienVendioCliente.append([idEmpleado, nombreEmpleado])

                tipos_pagos.append(tipo_pago)
                if tipo_pago == "Efectivo":
                    pagos_tarjeta.append("nada")
                    pagos_transferencia.append("nada")
                elif tipo_pago == "Tarjeta":
                    tipo_tarjeta = ventaCliente.tipo_tarjeta
                    referencia = ventaCliente.referencia_pago_tarjeta
                    pagos_tarjeta.append([tipo_tarjeta, referencia])
                    pagos_transferencia.append("nada")
                elif tipo_pago == "Transferencia":
                    clave_rastreo = ventaCliente.clave_rastreo_transferencia
                    pagos_tarjeta.append("nada")
                    pagos_transferencia.append(clave_rastreo)

                #Datos sucursal 
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
                sucursalesVentaCliente.append(nombreSucursal)
                
                #Datos descuento
                if descuento == None:
                    booleanDescuentoVentaCliente.append("Sin descuento")
                    totalesSinDescuentoVentaCliente.append("Total normal")
                    descuentosVentaCliente.append("jeje")
                    datosDescuentosVentaCliente.append("sin datos")
                else:
                    booleanDescuentoVentaCliente.append("Con descuento")
                    consultaDescuento = Descuentos.objects.filter(id_descuento = descuento)
                    
                    for datoDescuento in consultaDescuento:
                        porcentaje = datoDescuento.porcentaje
                        nombreDescuento = datoDescuento.nombre_descuento
                    datosDescuentosVentaCliente.append([porcentaje,nombreDescuento])

                    intPorcentaje = int(porcentaje)
                        
                    restaParaSaberCuantoSePago = 100 - intPorcentaje  #85
                    
                    restaConPunto = "."+str(restaParaSaberCuantoSePago) #.85
                    
                    costoReal = monto_total_pagado/float(restaConPunto) #376.470588
                    
                    costoRealRedondeado = round(costoReal)
                    totalesSinDescuentoVentaCliente.append(costoRealRedondeado)
                    
                    porcentajeDescuento = "."+str(intPorcentaje) #.15
                    descuento = costoReal*float(porcentajeDescuento)
                    
                    descuentoRedondeado = round(descuento)
                    descuentosVentaCliente.append(descuentoRedondeado)
                    
                #Datos Productos comprados
                if not codigosProductos:
                    boolProductosVentaCliente.append("Sin productos comprados")
                    datosProductosVentaCliente.append("Sin productos")
                else:
                    boolProductosVentaCliente.append("Productos Comprados")
                    cantidadesProductos = ventaCliente.cantidades_productos
                    
                    datosProductos = []
                    arregloCodigos = codigosProductos.split(",")
                    arregloCantidades = cantidadesProductos.split(",")
                    listaProductosEfectivo = zip(arregloCodigos, arregloCantidades)
                    for codigo, cantidad in listaProductosEfectivo:
                        codigoProducto = str(codigo)
                        cantidadProducto = str(cantidad)
                        consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
                        nombrePro = ""
                        for datoProducto in consultaProducto:
                            nombrePro = datoProducto.nombre_producto
                        
                        datosProductos.append([codigoProducto,nombrePro,cantidadProducto])
                    datosProductosVentaCliente.append(datosProductos)
                    
                #Datos Servicios Coorporales
                if not serviciosCorporales:
                    boolServiciosCoorporalesVentaCliente.append("Sin servicios coorporales")
                    datosServiciosCoorporalesVentaCliente.append("Sin productos")
                else:
                    boolServiciosCoorporalesVentaCliente.append("Servicios coorporales Comprados")
                    cantidadesServiciosCorporales = ventaCliente.cantidades_servicios_corporales
                    
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
                    datosServiciosCoorporalesVentaCliente.append(datosServicios)
                    
                #Datos Servicios Faciales
                if not serviciosFaciales:
                    boolServiciosFacialesVentaCliente.append("Sin servicios faciales")
                    datosServiciosFacialesVentaCliente.append("Sin servicios")
                else:
                    boolServiciosFacialesVentaCliente.append("Servicios coorporales Comprados")
                    cantidadesServiciosFacialesEfectivo = ventaCliente.cantidades_servicios_faciales
                    
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
                    datosServiciosFacialesVentaCliente.append(datosServicios)
                    
            listaVentasCliente = zip(listaVentasCliente, 
            quienVendioCliente, 
            sucursalesVentaCliente,
            tipos_pagos, 
            pagos_tarjeta, 
            pagos_transferencia,
             booleanDescuentoVentaCliente,
             totalesSinDescuentoVentaCliente, 
             descuentosVentaCliente,
             datosDescuentosVentaCliente, 
             boolProductosVentaCliente, 
             datosProductosVentaCliente, 
             boolServiciosCoorporalesVentaCliente,
             datosServiciosCoorporalesVentaCliente, 
             boolServiciosFacialesVentaCliente, 
             datosServiciosFacialesVentaCliente)
            
            
        #Creeeditooosss Pendientes....................................
            vendedor = []
            sucursalesCredito =[]
            fechasCreditosPendientes = []
            estatusPago = []
            fechasPago = []
            productosCredito = []
            serviciosCorpCredito = []
            serviciosFacCredito = []

            cantiadCreditosPendientes = 0
            creditosPendientesCliente = Creditos.objects.filter(cliente_id__id_cliente= idCliente, estatus= "Pendiente")
            if creditosPendientesCliente:
                for credito in creditosPendientesCliente:
                    
                    idvendedor = credito.empleado_vendedor_id
                    idsucursal = credito.sucursal_id
                    id_credito = credito.id_credito
                    idVenta = credito.venta_id
                    idRenta = credito.renta_id

                    


                    
                    datosVendedor = Empleados.objects.filter(id_empleado = idvendedor)
                    for dato in datosVendedor:
                        nombreVendedor = dato.nombres
                        apellidoPvendedor = dato.apellido_paterno
                    completoVendedor = str(idvendedor) + " " + nombreVendedor + " " + apellidoPvendedor
                    vendedor.append(completoVendedor)
                    
                    datosSucursalCredito = Sucursales.objects.filter(id_sucursal = idsucursal)
                    for dato in datosSucursalCredito:
                        nombreSucursalCredito = dato.nombre
                    sucursalesCredito.append(nombreSucursalCredito)

                    fechaAltaCredito = credito.fecha_venta_credito
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

                            estatusPago1 = "Se pagaron $ "  + str(pago1) + "MXN el día "
                            fechaPago1 = pago.fecha_pago1
                            
                            
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
                        
                    if idVenta != None:
                        
                        consultaVenta = Ventas.objects.filter(id_venta = idVenta)

                        for dato in consultaVenta:
                            codigosProductos = dato.ids_productos
                            cantidadesProductos = dato.cantidades_productos

                            codigosServiciosCorporales = dato.ids_servicios_corporales
                            cantidadesServiciosCorporales = dato.cantidades_servicios_corporales

                            idsServiciosFaciales = dato.ids_servicios_faciales
                            cantidadesServiciosFaciales = dato.cantidades_servicios_faciales

                            comrpoProductos = False
                            comproServiciosCorporales = False
                            comproServiciosFaciales = False

                            if codigosProductos == "":
                                comrpoProductos = False
                            else:
                                comrpoProductos = True
                                arregloCodigosProductos = codigosProductos.split(",")
                                arregloCantidadesProductos = cantidadesProductos.split(",")
                                listaProductos = zip(arregloCodigosProductos, arregloCantidadesProductos)

                            if codigosServiciosCorporales == "":
                                comproServiciosCorporales = False
                            else:
                                comproServiciosCorporales = True
                                arregloCodigosServiciosCoporales = codigosServiciosCorporales.split(",")
                                arregloCantidadesServiciosCorporales = cantidadesServiciosCorporales.split(",")
                                listaServiciosCorporales = zip(arregloCodigosServiciosCoporales, arregloCantidadesServiciosCorporales)
                            
                            if idsServiciosFaciales == "":
                                comproServiciosFaciales = False
                            else:
                                comproServiciosFaciales = True
                                arregloIdsServiciosFaciales = idsServiciosFaciales.split(",")
                                arregloCantidadesServiciosFaciales = cantidadesServiciosFaciales.split(",")
                                listaServiciosFaciales = zip(arregloIdsServiciosFaciales,arregloCantidadesServiciosFaciales)

                            #zipeadas
                            
                        
                        

                            listitaProductos = []
                            listtitaServiciosCorporales = []
                            listitaServiciosFaciales = []
                            #Productos
                            if comrpoProductos == True:
                                contadorProductos = 0
                                for producto, cantidad in listaProductos:
                                    contadorProductos = contadorProductos +1
                                    
                                    codigo = str(producto)
                                    if contadorProductos == 1:
                                        if "PV" in codigo:
                                            cantiadCreditosPendientes = cantiadCreditosPendientes +1
                                    cantidadProducto = str(cantidad)
                                    if "PR" in codigo:
                                        consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigo)
                                    else:
                                        consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigo)
                                    for datoProducto in consultaProducto:
                                        nombreProducto = datoProducto.nombre_producto
                                    listitaProductos.append([codigo,nombreProducto, cantidadProducto])
                        
                            

                            if comproServiciosCorporales == True:
                                for servicioCorp, cantCorp in listaServiciosCorporales:
                                    idServicioCorporal = int(servicioCorp)
                                    stridServicioCorporal = str(servicioCorp)
                                    cantidadServicioCorporal = str(cantCorp)

                                    consultaServicioCorporal = Servicios.objects.filter(tipo_servicio = "Corporal", id_servicio = idServicioCorporal)

                                    for datoCorporal in consultaServicioCorporal:
                                        nombreServicioCorporal = datoCorporal.nombre_servicio

                                    listtitaServiciosCorporales.append([stridServicioCorporal, nombreServicioCorporal, cantidadServicioCorporal])
                            
                            if comproServiciosFaciales == True:
                                for servicioFacial, cantFacial in listaServiciosFaciales:
                                    idServicioFacial = int(servicioFacial)
                                    stridServicioFacial = str(servicioFacial)
                                    cantidadServicioFacial = str(cantFacial)

                                    consultaServicioFacial = Servicios.objects.filter(tipo_servicio = "Facial", id_servicio = idServicioFacial)

                                    for datoFacial in consultaServicioFacial:
                                        nombreServicioFacial = datoFacial.nombre_servicio

                                    listitaServiciosFaciales.append([stridServicioFacial, nombreServicioFacial, cantidadServicioFacial])

                            productosCredito.append(listitaProductos)
                            serviciosCorpCredito.append(listtitaServiciosCorporales)
                            serviciosFacCredito.append(listitaServiciosFaciales)

                            
                    
                    listaCreditosPendientesCliente = zip(creditosPendientesCliente,vendedor,sucursalesCredito, fechasCreditosPendientes, estatusPago, fechasPago, productosCredito, serviciosCorpCredito, serviciosFacCredito)
            else:
                listaCreditosPendientesCliente = None
                
        #Reentaaasssss Pendientes...........................................
            cantidadRentasPendientes = 0
            rentasPendientesCliente = Rentas.objects.filter(Q(estado_devolucion =  "A") | Q(estado_devolucion =  "P"), cliente_id__id_cliente =idCliente,)
            if rentasPendientesCliente:    
                datosProductosRentaPendientesCliente=[]
                encargadosPendientesCliente = []
            
                sucursalesPendientesCliente = []
        
                for renT in rentasPendientesCliente:
                    cantidadRentasPendientes = cantidadRentasPendientes + 1
                    
                    idsProductos = renT.codigos_productos_renta
                    encargado_renta = renT.realizado_por_id
                        
                        
                        
                        
                        
                    datosEncargado = Empleados.objects.filter(id_empleado = encargado_renta)
                    for datoE in datosEncargado:
                        nombres = datoE.nombres
                        apellidoPaterno = datoE.apellido_paterno
                        apellidoMaterno = datoE.apellido_materno
                    datosCompletoEncargado = nombres + " " + apellidoPaterno + " " + apellidoMaterno
                    encargadosPendientesCliente.append(datosCompletoEncargado)
                        
                    datosProductos = []
                    arregloCodigos = idsProductos.split(",")
                    
                    
                    for codigo in arregloCodigos:
                        codigoProducto = str(codigo)
                        
                        consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigoProducto)
                        for datoProducto in consultaProducto:
                            nombrePro = datoProducto.nombre_producto
                            idSucursal = datoProducto.sucursal_id
                            imagen = datoProducto.imagen_producto
                            
                                
                        datosProductos.append([codigoProducto,nombrePro,imagen])
                    datosProductosRentaPendientesCliente.append(datosProductos)
                        
                    sucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
                    for dato in sucursal:
                        nombreSucursal = dato.nombre
                    sucursalesPendientesCliente.append(nombreSucursal)
                        
                listaRentasPendientesCliente = zip (rentasPendientesCliente,datosProductosRentaPendientesCliente,encargadosPendientesCliente,sucursalesPendientesCliente)
                        
            else:
                listaRentasPendientesCliente = None
                      
                      

        #Todos los creditos del cliente
            creditosCliente = Creditos.objects.filter(cliente_id__id_cliente = idCliente , concepto_credito = "Venta")
            numeroCreditos = 0
            totalCredito = 0
            
            
            productosCreditoTotal = []
            serviciosCorporalesTotal = []
            serviciosFacialesTotal = []
            boolEstatusCreditoTotal = []
            fechasPagoCreditoTotal = []
            realizadoPorCreditoTotal = []
            sucursalPorCreditoTotal = []
            
            for credito in creditosCliente:
                numeroCreditos = numeroCreditos +1
                montoCredito = credito.monto_pagar
                totalCredito = totalCredito + montoCredito
                id_credito = credito.id_credito
                
                
                #Realizado por
                empleado_vendedor = credito.empleado_vendedor_id
                consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = empleado_vendedor )
                for datoVendedor in consultaEmpleadoVendedor:
                    nombreVendedor = datoVendedor.nombres
                    apellido = datoVendedor.apellido_paterno
                nombreCompletoVendedor = nombreVendedor + " " + apellido
                realizadoPorCreditoTotal.append(nombreCompletoVendedor)
                
                #sucursal
                sucursal_credito_total = credito.sucursal_id
                sucursalCreditoTotal = Sucursales.objects.filter(id_sucursal = sucursal_credito_total)
                for suc in sucursalCreditoTotal:
                    idSucursalCliente = suc.id_sucursal
                    nombreSucursalCreditoTotal = suc.nombre
                sucursalPorCreditoTotal.append(nombreSucursalCreditoTotal)
                
                #boolEstatusCredito
                estatusCredito = credito.estatus
                boolEstatusCreditoTotal.append(estatusCredito)
                datosPagos = PagosCreditos.objects.filter(id_credito__id_credito = id_credito)
                
                if estatusCredito == "Pendiente":
                     
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

                            estatusPago1 = "Se pagaron $ "  + str(pago1) + "MXN el día "
                            fechaPago1 = pago.fecha_pago1
                            
                            
                        if pago2 == None:
                            estatusPago2 = "Pendiente"
                            fechaPago2 = "Sin fecha"
                        else:
                            estatusPago2 = "Se pagaron $ "  + str(pago2) + "MXN el día "+str(fechaPago2)
                            fechaPago2 = pago.fecha_pago2
                            
                        if pago3 == None:
                            estatusPago3 = "Pendiente"
                            fechaPago3 = "Sin fecha"
                        else:
                            estatusPago3 = "Se pagaron $ "  + str(pago3) + "MXN el día "+str(fechaPago3)
                            fechaPago3 = pago.fecha_pago3
                            
                            
                        if pago4 == None:
                            estatusPago4 = "Pendiente"
                            fechaPago4 = "Sin fecha"
                        else:
                            estatusPago4 = "Se pagaron $ "  + str(pago4) + "MXN el día "+str(fechaPago4)
                            fechaPago4 = pago.fecha_pago4
                            
                        fechasPagoCreditoTotal.append([fechaPago1,estatusPago1,fechaPago2,estatusPago2,fechaPago3,estatusPago3,fechaPago4,estatusPago4])
                else: #Si el credito ya se pago..
                    for datosPago in datosPagos:
                        fechaPago1 = datosPago.fecha_pago1
                        fechaPago2 = datosPago.fecha_pago2
                        fechaPago3 = datosPago.fecha_pago3
                        fechaPago4 = datosPago.fecha_pago4
                        
                        if fechaPago1 != None:#Si hay una fecha del pago
                            monto_pago1 = datosPago.monto_pago1
                        else:
                            fechaPago1 = ""
                            monto_pago1 = ""
                            
                            
                            
                        if fechaPago2 != None:#Si hay una fecha del pago
                            monto_pago2 = datosPago.monto_pago2
                        else:
                            fechaPago2 = ""
                            monto_pago2 = ""
                            
                        if fechaPago3 != None:#Si hay una fecha del pago
                            monto_pago3 = datosPago.monto_pago3
                        else:
                            fechaPago3 = ""
                            monto_pago3 = ""
                           
                        if fechaPago4 != None:#Si hay una fecha del pago
                            monto_pago4 = datosPago.monto_pago4
                        else:
                            fechaPago4 = ""
                            monto_pago4 = ""
                            
                    fechasPagoCreditoTotal.append([fechaPago1,monto_pago1,fechaPago2,monto_pago2,fechaPago3,monto_pago3,fechaPago4,monto_pago4])  
                
                venta = credito.venta_id
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
                        consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
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
                
                
               
                productosCreditoTotal.append(miniProductos)
                serviciosCorporalesTotal.append(miniSC)
                serviciosFacialesTotal.append(miniSF)
                
                
            
            
            
            listaCreditosTotales = zip(creditosCliente,productosCreditoTotal,serviciosCorporalesTotal,serviciosFacialesTotal,boolEstatusCreditoTotal,fechasPagoCreditoTotal,realizadoPorCreditoTotal,sucursalPorCreditoTotal)
                
            

            
            

        #Todas las rentas del cliente
            rentasCliente = Rentas.objects.filter(cliente_id__id_cliente =idCliente)
            numeroRentas = 0
            for renta in rentasCliente:
                numeroRentas = numeroRentas + 1

        #Tipo de cliente
            tipoCliente = ""
            sumaCantidades = int(cantidadCompras) + int(numeroCreditos) + int(numeroRentas)
            if sumaCantidades <= 3:
                tipoCliente = "POSIBLE CONSUMIDOR"
            elif sumaCantidades > 3 and sumaCantidades <=6:
                tipoCliente = "CLIENTE POTENCIAL"
            elif sumaCantidades > 6 and sumaCantidades <=9:
                tipoCliente = "CLIENTE FRECUENTE"
            elif sumaCantidades > 9:
                tipoCliente = "SUPER CLIENTE"
                
        #Todas las rentas totales del cliente
        
            
            rentasTotalesDelCliente = Rentas.objects.filter(cliente_id__id_cliente =idCliente)
            if rentasTotalesDelCliente:    
                datosProductosRentasTotalesCliente=[]
                encargadosRentasTotalesCliente = []
            
                sucursalesRentasTotalesCliente = []
        
                for rentasTotales in rentasTotalesDelCliente:
                    
                    
                    idsProductosRentasTotales = rentasTotales.codigos_productos_renta
                    encargado_rentas_totales = rentasTotales.realizado_por_id
                        
                        
                        
                        
                        
                    datosEncargadoRentasTotales = Empleados.objects.filter(id_empleado = encargado_rentas_totales)
                    for datoEncargadoRentas in datosEncargadoRentasTotales:
                        nombresEncargado = datoEncargadoRentas.nombres
                        apellidoPaternoEncargado = datoEncargadoRentas.apellido_paterno
                        apellidoMaternoEncargado = datoEncargadoRentas.apellido_materno
                    datosCompletoEncargadoRentas = nombresEncargado + " " + apellidoPaternoEncargado + " " + apellidoMaternoEncargado
                    encargadosRentasTotalesCliente.append(datosCompletoEncargadoRentas)
                        
                    datosProductosRentasTotales = []
                    arregloCodigosRentasTotalesProductos = idsProductosRentasTotales.split(",")
                    
                    
                    for codigo in arregloCodigosRentasTotalesProductos:
                        codigoProductoRentasTotales = str(codigo)
                        
                        consultaProductoRentasTotales = ProductosRenta.objects.filter(codigo_producto = codigoProductoRentasTotales)
                        for datoProducto in consultaProductoRentasTotales:
                            nombreProRentasTotales = datoProducto.nombre_producto
                            idSucursalRentasTotales = datoProducto.sucursal_id
                            
                            
                                
                        datosProductosRentasTotales.append([codigoProductoRentasTotales,nombreProRentasTotales])
                    datosProductosRentasTotalesCliente.append(datosProductosRentasTotales)
                        
                    sucursalRentasTotales = Sucursales.objects.filter(id_sucursal = idSucursalRentasTotales)
                    for dato in sucursalRentasTotales:
                        nombreSucursalRentasTotales = dato.nombre
                    sucursalesRentasTotalesCliente.append(nombreSucursalRentasTotales)
                        
                listaRentasTotalesCliente = zip (rentasTotalesDelCliente,datosProductosRentasTotalesCliente,encargadosRentasTotalesCliente,sucursalesRentasTotalesCliente)
                        
            else:
                listaRentasTotalesCliente = None
                
            sucursalesTotales = Sucursales.objects.all()
            limitesCreditos = []
            for sucursalTotal in sucursalesTotales:
                idSucursalTotal = sucursalTotal.id_sucursal
                nombreSucursalTotal = sucursalTotal.nombre
                
                configuracionCreditoCliente = ConfiguracionCredito.objects.filter(sucursal_id__id_sucursal = idSucursalTotal,activo = "S")
                if configuracionCreditoCliente:
                    for confCredito in configuracionCreditoCliente:
                        limiteCreditoSucursal = confCredito.limite_credito
                        
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
                    
                    creditoLibre = limiteCreditoSucursal - creditoFaltantePorPagar
                    
                    limitesCreditos.append([idSucursalTotal,nombreSucursalTotal,limiteCreditoSucursal,creditoLibre])
                


            #Citas del cliente
            listaCitaCliente = []
            consultaCitasCliente = Citas.objects.filter(cliente_id__id_cliente = idCliente) 

            for citaCliente in consultaCitasCliente:
                idCita = citaCliente.id_cita
                #empleadoRealizo
                idEmpleadoRealizo = citaCliente.empleado_realizo_id
                consultaEmpleadoRealizo = Empleados.objects.filter(id_empleado = idEmpleadoRealizo)
                for datoEmpleadoRealizo in consultaEmpleadoRealizo:
                    nombreEmpleadoRealizo = datoEmpleadoRealizo.nombres
                    apellidoPaternoRealizo = datoEmpleadoRealizo.apellido_paterno
                nombreCompletoEmpleadoRealizo = nombreEmpleadoRealizo + " "+ apellidoPaternoRealizo

                #sucursal
                idSucursal = citaCliente.sucursal_id
                consultaSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
                if consultaSucursal:
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                else:
                    nombreSucursal = "Sin sucursal"
                

                    
                    
                
            
                      
                      

        
                

            return render(request, "5 Clientes/InfoCliente/infoCliente.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado, "idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"clienteInfo":clienteInfo,"idC":idC, "idClienteEstatus":idClienteEstatus, "estado2":estado2, "telefonoParaActualizar":telefonoParaActualizar, "idClienteTelefono":idClienteTelefono,"correo2":correo2, "clienteCompleto":clienteCompleto, "letrasCliente":letrasCliente,
            "cantidadCompras":cantidadCompras, "totalComprado":totalComprado, "listaVentasCliente":listaVentasCliente,"listaCreditosPendientesCliente":listaCreditosPendientesCliente,"listaRentasPendientesCliente":listaRentasPendientesCliente, "numeroCreditos":numeroCreditos, "totalCredito":totalCredito, "numeroRentas":numeroRentas, "tipoCliente":tipoCliente, "cantiadCreditosPendientes":cantiadCreditosPendientes, "cantidadRentasPendientes":cantidadRentasPendientes, "listaCreditosTotales":listaCreditosTotales,
            "listaRentasTotalesCliente":listaRentasTotalesCliente,"limitesCreditos":limitesCreditos,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})

        return redirect('/verClientes/')
    else:
        return render(request,"1 Login/login.html")

def actTelCliente(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idClienteTelefono = request.POST['idClienteTelefono']
            telefonoClienteActualizado = request.POST['telefonoClienteActualizado']

            consultaCliente = Clientes.objects.filter(id_cliente = idClienteTelefono)

            for dato in consultaCliente:
                nombre = dato.nombre_cliente


            actualizacionCliente = Clientes.objects.filter(id_cliente = idClienteTelefono).update(telefono=telefonoClienteActualizado)
            
            if actualizacionCliente:    
                request.session['clienteActualizado'] = "El teléfono del cliente " + nombre + " se ha actualizado satisfactoriamente!"
                return redirect('/verClientes/')      
