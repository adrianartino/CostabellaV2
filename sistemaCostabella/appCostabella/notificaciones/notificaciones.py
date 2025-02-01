# Renderizado
from django.shortcuts import render
from django.shortcuts import redirect

# Importacion de modelos
from appCostabella.models import Sucursales, Empleados, Clientes,ProductosRenta,Rentas,Servicios,Permisos, Tratamientos, PaquetesPromocionTratamientos, Citas, ServiciosCertificados, CertificadosProgramados

# Librerías de fecha
from datetime import date, datetime, time,timedelta

from django.db.models import Q

#Notificaciones
def notificacionRentas(request):
    #Si ya existe una sesion al teclear login...
    if "idSesion" in request.session:
        idEmpleado = request.session['idSesion']
        datosEmpleado = Empleados.objects.filter(id_empleado =idEmpleado)
        for empleado in datosEmpleado:
            sucursal = empleado.id_sucursal_id
        if sucursal == None:
            
            fechaHoy = date.today()
            rentas = Rentas.objects.exclude(estado_devolucion = "F").filter(Q(fecha_entrega_renta =  fechaHoy) | Q(fecha_limite_devolucion = fechaHoy))
            rentasNotificacion =[]
            for renta in rentas:
                idrenta = renta.id_renta
                vestido = renta.codigos_productos_renta
                estatusRenta = renta.estado_devolucion
                cliente = renta.cliente_id
                vestidos = []
                arregloVestidos = vestido.split(',')
                
                for vestidoRenta in arregloVestidos:
                    consultaVestido = ProductosRenta.objects.filter(codigo_producto= vestidoRenta)
                    for dato in consultaVestido:
                        codigoVestido= dato.codigo_producto
                        nombreVestido = dato.nombre_producto
                        sucursalVestido = dato.sucursal_id
                        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalVestido)
                        for datoSucursal in consultaSucursal:
                            nombreSucursal = datoSucursal.nombre
                    vestidos.append([codigoVestido,nombreVestido])
                
                clienteRenta = Clientes.objects.filter(id_cliente = cliente)
                for datoCliente in clienteRenta:
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoPaterno = datoCliente.apellidoPaterno_cliente
                nombreCompletoCliente = nombreCliente + " " + apellidoPaterno
                
                rentasNotificacion.append([idrenta,estatusRenta,vestidos,nombreCompletoCliente,nombreSucursal])   
        else:
            
            fechaHoy = date.today()
            rentas = Rentas.objects.exclude(estado_devolucion = "F").filter(Q(fecha_entrega_renta = fechaHoy ) | Q(fecha_limite_devolucion =  fechaHoy))
            rentasNotificacion =[]
            for renta in rentas:
                idVendedor = renta.realizado_por_id
                datosVendedor = Empleados.objects.filter(id_empleado = idVendedor)
                for datoVendedor in datosVendedor:
                    sucursalVendedor = datoVendedor.id_sucursal_id
                if sucursalVendedor == sucursal:
                    idrenta = renta.id_renta
                    vestido = renta.codigos_productos_renta
                    estatusRenta = renta.estado_devolucion
                    cliente = renta.cliente_id
                    vestidos = []
                    arregloVestidos = vestido.split(',')
                    
                    for vestidoRenta in arregloVestidos:
                        consultaVestido = ProductosRenta.objects.filter(codigo_producto= vestidoRenta)
                        for dato in consultaVestido:
                            codigoVestido= dato.codigo_producto
                            nombreVestido = dato.nombre_producto
                            consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalVestido)
                            for datoSucursal in consultaSucursal:
                                nombreSucursal = datoSucursal.nombre
                        vestidos.append([codigoVestido,nombreVestido])
                    
                    clienteRenta = Clientes.objects.filter(id_cliente = cliente)
                    for datoCliente in clienteRenta:
                        nombreCliente = datoCliente.nombre_cliente
                        apellidoPaterno = datoCliente.apellidoPaterno_cliente
                    nombreCompletoCliente = nombreCliente + " " + apellidoPaterno
                    
                    rentasNotificacion.append([idrenta,estatusRenta,vestidos,nombreCompletoCliente,nombreSucursal]) 
        
        return rentasNotificacion
        
    # Si no hay una sesion iniciada..
    else:
        return render(request, "1 Login/login.html")

def notificacionCitas(request):
    #Si ya existe una sesion al teclear login...
    if "idSesion" in request.session:
        idEmpleado = request.session['idSesion']
        datosEmpleado = Empleados.objects.filter(id_empleado =idEmpleado)
        for empleado in datosEmpleado:
            sucursal = empleado.id_sucursal_id

        
        fechaHoy = date.today()
        if sucursal == None: #Todas las citas
            citas = Citas.objects.filter(fecha_pactada = fechaHoy, estado_cita = "sinCanjear")
        else:
            citas = Citas.objects.filter(fecha_pactada = fechaHoy, estado_cita = "sinCanjear", sucursal_id__id_sucursal = sucursal)

        citasNotificacion =[]
        for cita in citas:
            idCita = cita.id_cita
            #cliente
            cliente = cita.cliente_id
            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
            for datoCliente in consultaCliente:
                nombreCliente = datoCliente.nombre_cliente
                apellidoCliente = datoCliente.apellidoPaterno_cliente
            nombreCompletoCliente = nombreCliente+" "+apellidoCliente
            #sucursal
            sucursal = cita.sucursal_id
            consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
            for datoSucursal in consultaSucursal:
                nombreSucursal = datoSucursal.nombre

            

            tipoCita = cita.tipo_cita   #Tratamiento, PaqueteTratamiento, Servicio
            idServTratPaq = cita.id_serv_trat_paq
            certificadoServicio = cita.certificado_servicio
            if tipoCita == "Servicio":
                consultaServicio = Servicios.objects.filter(id_servicio = idServTratPaq)
                for datoServicio in consultaServicio:
                    tipoServicio = datoServicio.tipo_servicio
                    nombreServicio = datoServicio.nombre_servicio
                
                nombreServicioTratamientoPaqueteCita = tipoServicio +" "+nombreServicio
                esCertificado = "No"
                idCertificado = "No"
            elif tipoCita == "SesionTratamiento":
                consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idServTratPaq)
                for datoTratamiento in consultaTratamiento:
                    tipoTratamiento = datoTratamiento.tipo_tratamiento
                    nombreTratamiento = datoTratamiento.nombre_tratamiento
                nombreServicioTratamientoPaqueteCita = tipoTratamiento +" "+nombreTratamiento
                esCertificado = "No"
                idCertificado = "No"
            elif tipoCita == "PaqueteTratamiento":
                consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)
                for datoPromo in consultaPaqueteTratamiento:
                    nombrePaquete = datoPromo.nombre_paquete
                    sesionesPaquete = datoPromo.numero_sesiones
                nombreServicioTratamientoPaqueteCita = nombrePaquete + " "+str(sesionesPaquete)+" sesiones"
                esCertificado = "No"
                idCertificado = "No"
            elif tipoCita == "ServicioCertificado":
                servCertSeparado = certificadoServicio.split("-")
                idCertificado = servCertSeparado[0]
                idServicioCertificado = servCertSeparado[1]
                idCertificadoInt = int(idCertificado)
                idServicioCertificadoInt = int(idServicioCertificado)

                #Consulta de certificado
                consultaCertificado = CertificadosProgramados.objects.filter(id_certificado = idCertificadoInt)
                for datoCertificado in consultaCertificado:
                    codigoCertificado = datoCertificado.codigo_certificado

                #Consulta de servicio certificado
                consultaServicioCertificado = ServiciosCertificados.objects.filter(id_servicio_certificado = idServicioCertificadoInt)
                for datoServicio in consultaServicioCertificado:
                    nombreServicioCertificado = datoServicio.nombre
                nombreServicioTratamientoPaqueteCita = codigoCertificado + " - "+nombreServicioCertificado
                esCertificado = "Si"
                idCertificado = idCertificadoInt
            

            
            
            horaPactada = cita.hora_pctada
            duracion = cita.duracionCitaMinutos
            duracion = int(duracion)
    
            
            citasNotificacion.append([idCita,nombreSucursal,horaPactada,nombreCompletoCliente,nombreServicioTratamientoPaqueteCita,duracion, esCertificado, idCertificado])  
        
        return citasNotificacion
        
    # Si no hay una sesion iniciada..
    else:
        return render(request, "1 Login/login.html")
