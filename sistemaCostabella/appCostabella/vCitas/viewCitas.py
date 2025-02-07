
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

from datetime import date, datetime, time, timedelta

#Para mandar telegram
import telepot
#Plugin impresora termica
from appCostabella import Conector, keysBotCostabella
# Importacion de modelos
from appCostabella.models import (CertificadosProgramados, Citas, Clientes, ConfiguracionCredito,Creditos, Descuentos,
                                  Empleados, HistorialTratamientosClientes,
                                  MovimientosCaja, PagosCreditos,
                                  PaquetesPromocionTratamientos, Permisos,
                                  ProductosGasto,Servicios,
                                  ServiciosCertificados,
                                  ServiciosProductosGasto, Sucursales,
                                  Tratamientos, TratamientosClientes,
                                  TratamientosProductosGasto, Ventas,
                                  citasTratamientos, pagosPaquetesTratamientos)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)
from dateutil.relativedelta import relativedelta

def agendarCita(request):

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
            sucursalCita = request.POST["sucursalCita"]
            datosSucursal = Sucursales.objects.filter(id_sucursal = sucursalCita)
            for dato in datosSucursal:
                nombreSucursal = dato.nombre
            clientes = Clientes.objects.filter(estado = "A")

            serviciosSucursal = Servicios.objects.filter(sucursal_id__id_sucursal = sucursalCita)
            serviciosSucursalJS = Servicios.objects.filter(sucursal_id__id_sucursal = sucursalCita)
            tratamientosSucursal = Tratamientos.objects.filter(sucursal_id__id_sucursal = sucursalCita)
            tratamientosSucursalJS = Tratamientos.objects.filter(sucursal_id__id_sucursal = sucursalCita)
            
            todasLasPromocionesTratamientos = PaquetesPromocionTratamientos.objects.filter(promocion_activa = "A")

            promocionesSucursal = []
            promocionesSucursalJS = []
            sucursalCitaInt = int(sucursalCita)
            for promo in todasLasPromocionesTratamientos:
                idTratamiento = promo.tratamiento_id
                consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)
                for datoTratamiento in consultaTratamiento:
                    idSucursalTratamiento = datoTratamiento.sucursal_id
                    

                if idSucursalTratamiento == sucursalCitaInt:
                    idPromo = promo.id_paquete_tratamiento
                    numeroSesiones = promo.numero_sesiones
                    descuento = promo.descuento
                    if descuento == None:
                        boolDescuento = "Sin descuento"
                    else:
                        boolDescuento = "Con descuento"
                    precioPromo = promo.precio_por_paquete
                    nombrePromo = promo.nombre_paquete

                    datosTratamiento = []
                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)
                    for datoTratamiento in consultaTratamiento:
                        codigoTratamiento = datoTratamiento.codigo_tratamiento
                        nombreTratamiento = datoTratamiento.nombre_tratamiento
                        precioUnitarioTratamiento = datoTratamiento.costo_venta_tratamiento

                    datosTratamiento.append([idTratamiento, codigoTratamiento, nombreTratamiento, precioUnitarioTratamiento])

                    promocionesSucursal.append([idPromo, numeroSesiones, descuento, boolDescuento, precioPromo, nombrePromo,datosTratamiento])
                    promocionesSucursalJS.append([idPromo, numeroSesiones, descuento, boolDescuento, precioPromo, nombrePromo,datosTratamiento])
                
            
            #Fecha limite para agendar 45 dias despues del día de hoy
            today = date.today()
            fechaLimite = today + timedelta(days=45)
            fechaLimite = fechaLimite.strftime("%Y-%m-%d")

            #citas entre el dia de hoy y la fecha limite
            arregloHoras45Posiciones = []
            arreglo45Fechas = []
            
            contador = 0
            for x in range(45):
                contador = contador + 1
                sinCitasPendientes = True
                if contador == 1:
                    
                    consultaCitasDelDia = Citas.objects.filter(fecha_pactada = today, estado_cita = "sinCanjear")
                    if consultaCitasDelDia:
                            sinCitasPendientes = False
                    else:
                        sinCitasPendientes = True
                    fechaHoy = today.strftime("%Y-%m-%d")
                    arreglo45Fechas.append(fechaHoy)
                else:
                    nuevoContador = contador - 1
                    fechita = today + timedelta(days=nuevoContador)
                    consultaCitasDelDia = Citas.objects.filter(fecha_pactada = fechita, estado_cita = "sinCanjear")
                    fechaOtroDia = fechita.strftime("%Y-%m-%d")
                    arreglo45Fechas.append(fechaOtroDia)
                
                arregloHoras = ["09:00 AM","10:00 AM","11:00 AM","12:00 PM","13:00 PM","14:00 PM","15:00 PM","16:00 PM","17:00 PM","18:00 PM"]
                
                for cita in consultaCitasDelDia:
                    horaProgramada = cita.hora_pctada

                    if horaProgramada in arregloHoras:
                        duracion = cita.duracionCitaMinutos
                        if duracion > 60:
                            indiceAQuitar = arregloHoras.index(horaProgramada)
                            indiceAQuitarTambien = indiceAQuitar+1

                            if  indiceAQuitarTambien == 10: #Despues de las 6.. solo quita las 6
                                #arregloHoras.remove(horaProgramada)
                                arregloHoras[indiceAQuitar] = horaProgramada + " - Con cita" #No se quita del arreglo, solo se pone que ya hay una cita programada ahi
                            else:
                                horaTambienAQuitar = arregloHoras[indiceAQuitarTambien]
                                arregloHoras[indiceAQuitar] = horaProgramada + " - Con cita" #No se quita del arreglo, solo se pone que ya hay una cita programada ahi
                                arregloHoras[indiceAQuitarTambien] = horaTambienAQuitar + " - Con cita" #No se quita del arreglo, solo se pone que ya hay una cita programada ahi
                                #arregloHoras.remove(horaProgramada) #Quita la hora
                                #arregloHoras.remove(horaTambienAQuitar) #Quita la siguiente hora
                        else:
                            indiceAQuitar = arregloHoras.index(horaProgramada)
                            #arregloHoras.remove(horaProgramada) 
                            arregloHoras[indiceAQuitar] = horaProgramada + " - Con cita"
                        
                #Si no hay citas ese dia, no entra al for y el arreglo se queda igual.
                
                arregloHoras45Posiciones.append(arregloHoras)
                
                arregloHorasDiaActual = ["09:00 AM","10:00 AM","11:00 AM","12:00 PM","13:00 PM","14:00 PM","15:00 PM","16:00 PM","17:00 PM","18:00 PM"]
                
                consultaCitasDelDiaActual = Citas.objects.filter(fecha_pactada = today, estado_cita = "sinCanjear")
                if consultaCitasDelDia:
                    sinCitasPendientes = False
                else:
                    for cita in consultaCitasDelDiaActual:
                        horaProgramada = cita.hora_pctada

                        if horaProgramada in arregloHorasDiaActual:
                            duracion = cita.duracionCitaMinutos
                            if duracion > 60:
                                indiceAQuitar = arregloHorasDiaActual.index(horaProgramada)
                                indiceAQuitarTambien = indiceAQuitar+1

                                if  indiceAQuitarTambien == 10: #Despues de las 6.. solo quita las 6
                                    #arregloHoras.remove(horaProgramada)
                                    arregloHorasDiaActual[indiceAQuitar] = horaProgramada + " - Con cita" #No se quita del arreglo, solo se pone que ya hay una cita programada ahi
                                else:
                                    horaTambienAQuitar = arregloHorasDiaActual[indiceAQuitarTambien]
                                    arregloHorasDiaActual[indiceAQuitar] = horaProgramada + " - Con cita" #No se quita del arreglo, solo se pone que ya hay una cita programada ahi
                                    arregloHorasDiaActual[indiceAQuitarTambien] = horaTambienAQuitar + " - Con cita" #No se quita del arreglo, solo se pone que ya hay una cita programada ahi
                                    #arregloHoras.remove(horaProgramada) #Quita la hora
                                    #arregloHoras.remove(horaTambienAQuitar) #Quita la siguiente hora
                            else:
                                #arregloHoras.remove(horaProgramada) 
                                arregloHorasDiaActual[indiceAQuitar] = horaProgramada + " - Con cita"
                                
            

            

            listaZipFechaHora = zip(arreglo45Fechas,arregloHoras45Posiciones)



            #Certificados
            consultaCertificadosSucursal = CertificadosProgramados.objects.all()

            certificadosPendientes = []
            certificadosPendientesJS = []
            certificadosPendientesJSDos = []
            certificadosPendientesJSTres = []

            for certificado in consultaCertificadosSucursal:
                venta = certificado.venta_id
                consultaVenta = Ventas.objects.filter(id_venta = venta)
                for dato in consultaVenta:
                    idSucursalVenta = dato.sucursal_id

                    
                intSucursalMandada = int(sucursalCita)
                sucursalVenta = int(idSucursalVenta)
                if sucursalVenta == intSucursalMandada:
                    idCertificado = certificado.id_certificado
                    codigoCertificado = certificado.codigo_certificado
                    fechaAlta = certificado.fecha_alta
                    vigencia = certificado.vigencia

                    servicios = []
                    pendientesCanjeados = []

                    #Info de cada servicio
                    listaServiciosCertificados = certificado.lista_servicios_certificados
                    arregloServicios = listaServiciosCertificados.split(",")
                    for servicio in arregloServicios:
                        idServicio = int(servicio)
                        consultaServicioCertificado = ServiciosCertificados.objects.filter(id_servicio_certificado = idServicio)
                        for datoServicio in consultaServicioCertificado:
                            nombreServicio = datoServicio.nombre
                            tiempoMinimo = datoServicio.tiempo_minimo
                            tiempoMaximo = datoServicio.tiempo_maximo

                        
                        servicios.append([nombreServicio,idServicio,tiempoMinimo, tiempoMaximo])


                    listaPendientesCanjeados = certificado.lista_servicios_efectuados
                    arregloPendientesCanjeados = listaPendientesCanjeados.split(",")
                    for uno in arregloPendientesCanjeados:
                        pendienteCanjeado = uno
                        pendientesCanjeados.append(pendienteCanjeado)

                    clienteCompro = certificado.cliente_compro_id
                    if clienteCompro == "Momentaneo":
                        nombreCliente = "Momentanteo"
                    else:
                        consultaCliente = Clientes.objects.filter(id_cliente = clienteCompro)
                        for datoCliente in consultaCliente:
                            nombreClientex = datoCliente.nombre_cliente
                            apellidoCliente = datoCliente.apellidoPaterno_cliente

                        nombreCliente = nombreClientex + " "+apellidoCliente
                    nombreBeneficiaria = certificado.nombre_beneficiaria
                    montoTotalAPagar = certificado.monto_total_pagar

                    estatusCertificado = certificado.estatus_certificado

                    listaZipeada = zip(servicios,pendientesCanjeados)

                    if estatusCertificado == "P":
                        estaVigente = ""
                        fechaActual = datetime.now()
                        fechaActualFormato = fechaActual.strftime('%Y-%m-%d')
                        hoy = date.today()


                        if vigencia < hoy:
                            estaVigente = "yaNoEstaVigente"
                        else:
                            estaVigente = "aunEstaVigente"
                            certificadosPendientes.append([idCertificado,codigoCertificado,fechaAlta, vigencia, listaZipeada, nombreCliente, nombreBeneficiaria, montoTotalAPagar, estaVigente])
                            certificadosPendientesJS.append([idCertificado,codigoCertificado,fechaAlta, vigencia, listaZipeada, nombreCliente, nombreBeneficiaria, montoTotalAPagar, estaVigente])
                            certificadosPendientesJSDos.append([idCertificado,codigoCertificado,fechaAlta, vigencia, servicios, nombreCliente, nombreBeneficiaria, montoTotalAPagar, estaVigente])
                            certificadosPendientesJSTres.append([idCertificado,codigoCertificado,fechaAlta, vigencia, servicios, nombreCliente, nombreBeneficiaria, montoTotalAPagar, estaVigente])


            return render(request, "22 Citas/agendarCita.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta,"tipoUsuario":tipoUsuario, "sucursalCita":sucursalCita, "nombreSucursal":nombreSucursal, 
                "clientes":clientes, "serviciosSucursal":serviciosSucursal, "tratamientosSucursal":tratamientosSucursal, "promocionesSucursal":promocionesSucursal, "fechaLimite":fechaLimite, "sinCitasPendientes":sinCitasPendientes, "arregloHoras45Posiciones":arregloHoras45Posiciones,
                "listaZipFechaHora":listaZipFechaHora, "serviciosSucursalJS":serviciosSucursalJS, "tratamientosSucursalJS":tratamientosSucursalJS, "promocionesSucursalJS":promocionesSucursalJS, "notificacionCita":notificacionCita, "certificadosPendientes":certificadosPendientes,
                "certificadosPendientesJS":certificadosPendientesJS, "certificadosPendientesJSDos":certificadosPendientesJSDos, "certificadosPendientesJSTres":certificadosPendientesJSTres, "arregloHorasDiaActual":arregloHorasDiaActual})


        else:           
            if tipoUsuario == "esAdmin":
                sucursales = Sucursales.objects.all()
                
                if "citaGuardada" in request.session:
                    citaGuardada = request.session["citaGuardada"]
                    del request.session["citaGuardada"]
                    return render(request, "22 Citas/seleccionarSucursalCita.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "citaGuardada":citaGuardada, "notificacionCita":notificacionCita})

                if "citaNoGuardada" in request.session:
                    citaNoGuardada = request.session["citaNoGuardada"]
                    del request.session["citaNoGuardada"]
                    return render(request, "22 Citas/seleccionarSucursalCita.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "citaNoGuardada":citaNoGuardada, "notificacionCita":notificacionCita})

                return render(request, "22 Citas/seleccionarSucursalCita.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})
            else:
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    sucursalEmpleado = datoEmpleado.id_sucursal_id
                sucursales = Sucursales.objects.filter(id_sucursal = sucursalEmpleado)
                
                if "citaGuardada" in request.session:
                    citaGuardada = request.session["citaGuardada"]
                    del request.session["citaGuardada"]
                    return render(request, "22 Citas/seleccionarSucursalCita.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "citaGuardada":citaGuardada, "notificacionCita":notificacionCita})

                if "citaNoGuardada" in request.session:
                    citaNoGuardada = request.session["citaNoGuardada"]
                    del request.session["citaNoGuardada"]
                    return render(request, "22 Citas/seleccionarSucursalCita.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "citaNoGuardada":citaNoGuardada, "notificacionCita":notificacionCita})

                

                return render(request, "22 Citas/seleccionarSucursalCita.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})
        
    else:
        return render(request,"1 Login/login.html")

def guardarCita(request):

    if "idSesion" in request.session:


        if request.method == "POST":
            cliente = request.POST['clienteCita']
            sucursal = request.POST['sucursalCita']
            empleadoRealizo = request.POST['idEmpleado']

            #seleccion
            servicioSeleccionado = request.POST['servicioSeleccionado']
            tratamientoSeleccionado = request.POST['tratamientoSeleccionado']
            paqueteTratamientoSeleccionado = request.POST['paqueteTratamientoSeleccionado']
            servicioCertificadoSeleccionado = request.POST['servicioCertificadoSeleccionado']

            tipoDeCita = ""
            idServTratPaq = 0
            duracion = 0

            if servicioSeleccionado == "nada":
                sinServicioSeleccionado = True
            else:
                tipoDeCita = "Servicio"
                idServTratPaq = int(servicioSeleccionado)

                consultaServicio = Servicios.objects.filter(id_servicio = idServTratPaq)
                for datoServicio in consultaServicio:
                    duracionMaxima = datoServicio.tiempo_maximo
                    nombreServicioTratamiento = datoServicio.nombre_servicio
                duracion = float(duracionMaxima)

                fechaPactada = request.POST['fechaAgendar']
                horaCitaJunta = request.POST['horarioCita'] #Este puede ser normal o que incluya " - Con cita"
                horaCitaSeparada =horaCitaJunta.split(' ') #Se hace arreglo, solo se va a tomar la primera y segunda posicion
                horaCita = horaCitaSeparada[0] + ' ' + horaCitaSeparada[1]
                estadoCita = "sinCanjear"
                citaVendida = "No"

                comentarios = request.POST['comentarios']

                registroCita = Citas(cliente = Clientes.objects.get(id_cliente = cliente),
                sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                empleado_realizo = Empleados.objects.get(id_empleado = empleadoRealizo),
                tipo_cita = tipoDeCita,
                id_serv_trat_paq = idServTratPaq,
                fecha_pactada = fechaPactada,
                hora_pctada = horaCita,
                estado_cita = estadoCita,
                cita_vendida = citaVendida,
                comentarios = comentarios,
                duracionCitaMinutos = duracion)


            if tratamientoSeleccionado == "nada":
                sinTratamientoSeleccionado = True
            else:
                tipoDeCita = "SesionTratamiento"
                idServTratPaq = int(tratamientoSeleccionado)

                consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idServTratPaq)
                for datoTratamiento in consultaTratamiento:
                    duracionMaxima = datoTratamiento.tiempo_maximo
                    nombreServicioTratamiento = datoTratamiento.nombre_tratamiento
                duracion = float(duracionMaxima)

                fechaPactada = request.POST['fechaAgendar']
                horaCita = request.POST['horarioCita']
                estadoCita = "sinCanjear"
                citaVendida = "No"

                comentarios = request.POST['comentarios']

                registroCita = Citas(cliente = Clientes.objects.get(id_cliente = cliente),
                sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                empleado_realizo = Empleados.objects.get(id_empleado = empleadoRealizo),
                tipo_cita = tipoDeCita,
                id_serv_trat_paq = idServTratPaq,
                fecha_pactada = fechaPactada,
                hora_pctada = horaCita,
                estado_cita = estadoCita,
                cita_vendida = citaVendida,
                comentarios = comentarios,
                duracionCitaMinutos = duracion)

            if paqueteTratamientoSeleccionado == "nada":
                sinPaqueteTratamientoSeleccionado = True
            else:
                tipoDeCita = "PaqueteTratamiento"
                idServTratPaq = int(paqueteTratamientoSeleccionado)

                consultaPaquete = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)
                for datoPaquete in consultaPaquete:
                    idTratamiento = datoPaquete.tratamiento_id
                    nombreServicioTratamiento = datoPaquete.nombre_paquete
                    
                    precioPagar = datoPaquete.precio_por_paquete
                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)
                    for datoTratamiento in consultaTratamiento:
                        duracionMaxima = datoTratamiento.tiempo_maximo
                    duracion = float(duracionMaxima)
                    precioPagar = float(precioPagar)
                paqueteTratamiento = True
                fechaPactada = request.POST['fechaAgendar']
                horaCita = request.POST['horarioCita']
                estadoCita = "sinCanjear"
                citaVendida = "No"

                comentarios = request.POST['comentarios']

                registroCita = Citas(cliente = Clientes.objects.get(id_cliente = cliente),
                sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                empleado_realizo = Empleados.objects.get(id_empleado = empleadoRealizo),
                tipo_cita = tipoDeCita,
                id_serv_trat_paq = idServTratPaq,
                fecha_pactada = fechaPactada,
                hora_pctada = horaCita,
                estado_cita = estadoCita,
                cita_vendida = citaVendida,
                comentarios = comentarios,
                duracionCitaMinutos = duracion)

            if servicioCertificadoSeleccionado == "nada":
                sinServicioCertificadoSeleccionado = True
            else:
                tipoDeCita = "ServicioCertificado"

                #Duracion, certificado y nombre de servicio
                certificadoServicioSeparado = servicioCertificadoSeleccionado.split("-")
                idCertificado = certificadoServicioSeparado[0]
                idCertificadoInt = int(idCertificado)
                idServicioCertificado = certificadoServicioSeparado[1]
                idServicioCertificadoInt = int(idServicioCertificado)

                #Consulta de certificado
                consultaCertificado = CertificadosProgramados.objects.filter(id_certificado = idCertificadoInt)
                for datoCertificado in consultaCertificado:
                    codigoCertificado = datoCertificado.codigo_certificado

                #Consulta de servicio certificado
                consultaServicioCertificado = ServiciosCertificados.objects.filter(id_servicio_certificado = idServicioCertificadoInt)
                for datoServicio in consultaServicioCertificado:
                    nombreServicioCertificado = datoServicio.nombre
                    duracionMaxima = datoServicio.tiempo_maximo
                duracion = float(duracionMaxima)

                fechaPactada = request.POST['fechaAgendar']
                horaCita = request.POST['horarioCita']
                estadoCita = "sinCanjear"
                citaVendida = "No"

                comentarios = request.POST['comentarios']

                registroCita = Citas(cliente = Clientes.objects.get(id_cliente = cliente),
                sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                empleado_realizo = Empleados.objects.get(id_empleado = empleadoRealizo),
                tipo_cita = tipoDeCita,
                certificado_servicio = servicioCertificadoSeleccionado,
                fecha_pactada = fechaPactada,
                hora_pctada = horaCita,
                estado_cita = estadoCita,
                cita_vendida = citaVendida,
                comentarios = comentarios,
                duracionCitaMinutos = duracion)
                

            

            registroCita.save()

            #Datos del cliente
            datosCliente = Clientes.objects.filter(id_cliente = cliente)
            for datoCliente in datosCliente:
                nombreCliente = datoCliente.nombre_cliente
                apellidoCliente = datoCliente.apellidoPaterno_cliente

            nombreCompletoCliente = nombreCliente + " "+apellidoCliente

            #Datos sucursal
            datosSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
            for datoSucursal in datosSucursal:
                nombreSucursalCita = datoSucursal.nombre

            if registroCita:
                if tipoDeCita == "PaqueteTratamiento":
                    #Guardar tratamiento de cliente que es por paquete.. 
                    consultaPaquete = PaquetesPromocionTratamientos.objects.all()
                    for datoPaquete in consultaPaquete:
                        sesionesPromo = datoPaquete.numero_sesiones
                    
                    registroTratamientoCliente = TratamientosClientes(cliente = Clientes.objects.get(id_cliente = cliente), paquete_tratamiento = PaquetesPromocionTratamientos.objects.get(id_paquete_tratamiento = idServTratPaq),
                    num_sesiones = sesionesPromo, sesionesPendientes = sesionesPromo, sesionesCanjeadas = 0)
                    registroTratamientoCliente.save()

                    #Consulta de tratamiento
                    consultaTratamientoPaquete = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)
                    for datoPaqueteTratamiento in consultaTratamientoPaquete:
                        nombrePaquete = datoPaqueteTratamiento.nombre_paquete



                    if registroTratamientoCliente:
                        
                        consultaTratamientosClientes = TratamientosClientes.objects.all()
                        for trat in consultaTratamientosClientes:
                            ultimoRegistroTratamientoCliente = trat.id_tratamiento_cliente
                        
                        consultaCitas = Citas.objects.all()
                        for cita in consultaCitas:
                            ultimoRegistroCita = cita.id_cita

                        #Guardar cita y tratamiento juntos
                        guardarCitaConTratamiento = citasTratamientos(cita = Citas.objects.get(id_cita = ultimoRegistroCita), 
                        idTratamientoCliente = TratamientosClientes.objects.get(id_tratamiento_cliente = ultimoRegistroTratamientoCliente))
                        
                        guardarCitaConTratamiento.save()

                        #Guardar registro de historial de pago tratamiento.
                        registroPago = pagosPaquetesTratamientos(id_tratamiento_cliente = TratamientosClientes.objects.get(id_tratamiento_cliente = ultimoRegistroTratamientoCliente),
                        total_pagar = precioPagar,
                        total_abonado = 0,
                        total_restante = precioPagar,
                        estatus_pago = "Pendiente")

                        registroPago.save()

                        #Mandar notificación con telegram
                        try:
                            tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                            botCostabella = telepot.Bot(tokenTelegram)

                            idGrupoTelegram = keysBotCostabella.idGrupo
                            
                            mensaje = "\U0001F4C6 CITA AGENDADA \U0001F4C6 \n El cliente "+nombreCompletoCliente+" ha agendado una cita para el día "+fechaPactada+" a las "+str(horaCita)+" hrs en la sucursal "+nombreSucursalCita+"\n Tratamiento:\n"+nombreServicioTratamiento
                            botCostabella.sendMessage(idGrupoTelegram,"\U0001F4C6 *CITA AGENDADA*\U0001F4C6 \n",mensaje, parse_mode= 'Markdown')
                        except:
                            print("An exception occurred")

                        request.session["citaGuardada"] = "La cita se ha guardado correctamente!"
                        return redirect("/agendarCita/")
                    
                elif tipoDeCita == "ServicioCertificado":
                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo
                        
                        mensaje = "\U0001F381 CITA AGENDADA CERTIFICADO \U0001F381 \n El cliente "+nombreCompletoCliente+" ha agendado una cita para el día "+fechaPactada+" a las "+str(horaCita)+" hrs en la sucursal "+nombreSucursalCita+"\n Certificado a canjear: "+codigoCertificado+"\n Servicio: "+nombreServicioCertificado
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")
                    request.session["citaGuardada"] = "La cita se ha guardado correctamente!"
                    return redirect("/agendarCita/")

                else:
                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo
                        
                        mensaje = "\U0001F4C6 CITA AGENDADA \U0001F4C6 \n El cliente "+nombreCompletoCliente+" ha agendado una cita para el día "+fechaPactada+" a las "+str(horaCita)+" hrs en la sucursal "+nombreSucursalCita+"\n Servicio/Tratamiento:\n"+nombreServicioTratamiento
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")
                    request.session["citaGuardada"] = "La cita se ha guardado correctamente!"
                    return redirect("/agendarCita/")

            
        
    else:
        return render(request,"1 Login/login.html")

def citas(request):

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

            sucursal = request.POST['sucursalCita']
            consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
            for datoSucursal in consultaSucursal:
                nombreSucursalView = datoSucursal.nombre

            consultaCitasPendientesSucursal = Citas.objects.filter(estado_cita = "sinCanjear", sucursal_id__id_sucursal = sucursal)
            
            citasPendientes = []
            citasPendientesReagendar = []
            citasPendientesReagendar2 = []
            citasPendientesReagendar3 = []
            citasPendientesReagendar4 = []
            citasPendientesReagendar5 = []

            idCertificadosPendientesCitas = []

            sinCitasPendientes = True
            arregloHoras2 = []
            listaZipFechaHora = ""
            listaZipFechaHora2 = ""
            fechaLimite = ""
            for citaPendiente in consultaCitasPendientesSucursal:
                #idCita
                idCita = citaPendiente.id_cita
                #cliente
                idCliente = citaPendiente.cliente_id
                consultaCliente = Clientes.objects.filter(id_cliente = idCliente)
                for datoCliente in consultaCliente:
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoPaterno = datoCliente.apellidoPaterno_cliente
                nombreCompletoCliente = nombreCliente + " " + apellidoPaterno

                #Empleado que realizo
                idEmpleado = citaPendiente.empleado_realizo_id
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    nombreEmpleado = datoEmpleado.nombres
                    apellidoEmpleado = datoEmpleado.apellido_paterno
                nombreCompletoEmpleado = nombreEmpleado +" "+apellidoEmpleado

                tipoCita = citaPendiente.tipo_cita
                idServTratPaq = citaPendiente.id_serv_trat_paq
                nombreServTratPaq = ""
                precioServTratPaq = 0
                if tipoCita == "Servicio":
                    consultaServicio = Servicios.objects.filter(id_servicio = idServTratPaq)
                    for datoServicio in consultaServicio:
                        nombreServTratPaq = datoServicio.nombre_servicio
                        precioServTratPaq = datoServicio.precio_venta
                    idCertificadosPendientesCitas.append("x")
                elif tipoCita == "SesionTratamiento":
                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idServTratPaq)
                    for datoTratamiento in consultaTratamiento:
                        nombreServTratPaq = datoTratamiento.nombre_tratamiento
                        precioServTratPaq = datoTratamiento.costo_venta_tratamiento
                    idCertificadosPendientesCitas.append("x")
                elif tipoCita == "PaqueteTratamiento":
                    consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)
                    for datoPaquete in consultaPaqueteTratamiento:
                        nombreServTratPaq = datoPaquete.nombre_paquete
                        precioServTratPaq = datoPaquete.precio_por_paquete
                    idCertificadosPendientesCitas.append("x")

                elif tipoCita == "ServicioCertificado":
                    certificadoServicio = citaPendiente.certificado_servicio
                    servCertSeparado = certificadoServicio.split("-")
                    idCertificado = servCertSeparado[0]
                    idServicioCertificado = servCertSeparado[1]
                    idCertificadoInt = int(idCertificado)
                    idServicioCertificadoInt = int(idCertificadoInt)
                    idCertificadosPendientesCitas.append(idCertificadoInt)
                    #Consulta de certificado
                    consultaCertificado = CertificadosProgramados.objects.filter(id_certificado = idCertificadoInt)
                    for datoCertificado in consultaCertificado:
                        codigoCertificado = datoCertificado.codigo_certificado

                    #Consulta de servicio certificado
                    consultaServicioCertificado = ServiciosCertificados.objects.filter(id_servicio_certificado = idServicioCertificadoInt)
                    for datoServicio in consultaServicioCertificado:
                        nombreServicioCertificado = datoServicio.nombre
                        nombreServTratPaq = codigoCertificado + " - "+nombreServicioCertificado
                        
                
                fechaPactada = citaPendiente.fecha_pactada
                horaPactada = citaPendiente.hora_pctada
                duracionCita = citaPendiente.duracionCitaMinutos
                duracionCita = int(duracionCita)
                comentarios = citaPendiente.comentarios

                today = date.today()


                diasParaLaCita = (fechaPactada - today).days
                
                if diasParaLaCita > 1:
                    sePuedeCambiar = "sePuedeCambiar"
                elif diasParaLaCita == 1:
                    #Aqui ya se que es un día antes de la cita
                    #Validar las horas..
                    horaActual = datetime.now().time()
                    horaActual = horaActual.strftime("%H") 

                    print("La hora actual es:"+str(horaActual))

                    arregloHora = horaPactada.split(" ")
                    horita = arregloHora[0]
                    intHoraActual = int(horaActual)

                    horitaSplit = horita.split(":")
                    horitaHorita = horitaSplit[0]

                    intHoraCita = int(horitaHorita)

                    if intHoraActual < intHoraCita:  #La hora de hoy es menor a la hora de la cita..
                        sePuedeCambiar = "sePuedeCambiar"

                    else: #Ya no se puede
                        sePuedeCambiar = "noSePuedeCambiar"
                else:
                    sePuedeCambiar = "noSePuedeCambiar"

                #Fecha limite para agendar 45 dias despues del día de hoy
                today = date.today()
                fechaLimite = today + timedelta(days=45)
                fechaLimite = fechaLimite.strftime("%Y-%m-%d")

                #citas entre el dia de hoy y la fecha limite
                arregloHoras45Posiciones = []
                arreglo45Fechas = []
                
                contador = 0
                for x in range(45):
                    
                    contador = contador + 1
                    sinCitasPendientes = True
                    if contador == 1:
                        consultaCitasDelDia = Citas.objects.filter(fecha_pactada = today, estado_cita = "sinCanjear")
                        if consultaCitasDelDia:
                            sinCitasPendientes = False
                            print("Hay citas pendientes!!")
                        else:
                            sinCitasPendientes = True
                        fechaHoy = today.strftime("%Y-%m-%d")
                        arreglo45Fechas.append(fechaHoy)
                    else:
                        nuevoContador = contador - 1
                        fechita = today + timedelta(days=nuevoContador)
                        consultaCitasDelDia = Citas.objects.filter(fecha_pactada = fechita, estado_cita = "sinCanjear")
                        fechaOtroDia = fechita.strftime("%Y-%m-%d")
                        arreglo45Fechas.append(fechaOtroDia)
                    
                    arregloHoras = ["09:00 AM","10:00 AM","11:00 AM","12:00 PM","13:00 PM","14:00 PM","15:00 PM","16:00 PM","17:00 PM","18:00 PM"]
                    for cita in consultaCitasDelDia:
                        
                        horaProgramada = cita.hora_pctada


                        if horaProgramada in arregloHoras:
                            duracion = cita.duracionCitaMinutos
                            if duracion > 60:
                                indiceAQuitar = arregloHoras.index(horaProgramada)
                                indiceAQuitarTambien = indiceAQuitar+1
                                if  indiceAQuitarTambien == 10:
                                    arregloHoras.remove(horaProgramada)
                                else:
                                    horaTambienAQuitar = arregloHoras[indiceAQuitarTambien]
                                    arregloHoras.remove(horaProgramada) 
                                    arregloHoras.remove(horaTambienAQuitar) 
                            else:
                                arregloHoras.remove(horaProgramada) 
                        
                    arregloHoras45Posiciones.append(arregloHoras)
                

                
                consultaPrimerDia = Citas.objects.filter(fecha_pactada = today, estado_cita = "sinCanjear")
                arregloHoras2 = ["09:00 AM","10:00 AM","11:00 AM","12:00 PM","13:00 PM","14:00 PM","15:00 PM","16:00 PM","17:00 PM","18:00 PM"]
                for cita in consultaPrimerDia:
                    horaProgramada = cita.hora_pctada

                    if horaProgramada in arregloHoras2:
                        duracion = cita.duracionCitaMinutos
                        if duracion > 60:
                            indiceAQuitar = arregloHoras2.index(horaProgramada)
                            indiceAQuitarTambien = indiceAQuitar+1
                            if  indiceAQuitarTambien == 10:
                                arregloHoras2.remove(horaProgramada)
                            else:
                                horaTambienAQuitar = arregloHoras2[indiceAQuitarTambien]
                                arregloHoras2.remove(horaProgramada) 
                                arregloHoras2.remove(horaTambienAQuitar) 
                        else:
                            arregloHoras2.remove(horaProgramada) 


                listaZipFechaHora = zip(arreglo45Fechas,arregloHoras45Posiciones)
                listaZipFechaHora2 = zip(arreglo45Fechas,arregloHoras45Posiciones)



                citasPendientes.append([idCita, nombreCompletoCliente, nombreCompletoEmpleado, tipoCita, nombreServTratPaq, precioServTratPaq,
                fechaPactada, horaPactada,duracionCita, comentarios, sePuedeCambiar])
                

                citasPendientesReagendar.append([idCita, nombreCompletoCliente, nombreCompletoEmpleado, tipoCita, nombreServTratPaq, precioServTratPaq,
                fechaPactada, horaPactada,duracionCita, comentarios, sePuedeCambiar])

                citasPendientesReagendar2.append([idCita, nombreCompletoCliente, nombreCompletoEmpleado, tipoCita, nombreServTratPaq, precioServTratPaq,
                fechaPactada, horaPactada,duracionCita, comentarios, sePuedeCambiar])

                citasPendientesReagendar3.append([idCita, nombreCompletoCliente, nombreCompletoEmpleado, tipoCita, nombreServTratPaq, precioServTratPaq,
                fechaPactada, horaPactada,duracionCita, comentarios, sePuedeCambiar])

                citasPendientesReagendar4.append([idCita, nombreCompletoCliente, nombreCompletoEmpleado, tipoCita, nombreServTratPaq, precioServTratPaq,
                fechaPactada, horaPactada,duracionCita, comentarios, sePuedeCambiar])

                citasPendientesReagendar5.append([idCita, nombreCompletoCliente, nombreCompletoEmpleado, tipoCita, nombreServTratPaq, precioServTratPaq,
                fechaPactada, horaPactada,duracionCita, comentarios, sePuedeCambiar])

            cistasPendientesZipeada = zip(citasPendientes, idCertificadosPendientesCitas)
            consultaCitasEfectuadasSucursal = Citas.objects.filter(estado_cita = "efectuada", sucursal_id__id_sucursal = sucursal)
            
            citasEfectuadas = []
            for citaEfectuada in consultaCitasEfectuadasSucursal:
                #idCita
                idCita = citaEfectuada.id_cita
                #cliente
                idCliente = citaEfectuada.cliente_id
                consultaCliente = Clientes.objects.filter(id_cliente = idCliente)
                for datoCliente in consultaCliente:
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoPaterno = datoCliente.apellidoPaterno_cliente
                nombreCompletoCliente = nombreCliente + " " + apellidoPaterno

                #Empleado que realizo
                idEmpleado = citaEfectuada.empleado_realizo_id
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    nombreEmpleado = datoEmpleado.nombres
                    apellidoEmpleado = datoEmpleado.apellido_paterno
                nombreCompletoEmpleado = nombreEmpleado +" "+apellidoEmpleado

                tipoCita = citaEfectuada.tipo_cita
                idServTratPaq = citaEfectuada.id_serv_trat_paq
                nombreServTratPaq = ""
                precioServTratPaq = 0
                if tipoCita == "Servicio":
                    consultaServicio = Servicios.objects.filter(id_servicio = idServTratPaq)
                    for datoServicio in consultaServicio:
                        nombreServTratPaq = datoServicio.nombre_servicio
                        precioServTratPaq = datoServicio.precio_venta
                elif tipoCita == "SesionTratamiento":
                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idServTratPaq)
                    for datoTratamiento in consultaTratamiento:
                        nombreServTratPaq = datoTratamiento.nombre_tratamiento
                        precioServTratPaq = datoTratamiento.costo_venta_tratamiento
                elif tipoCita == "PaqueteTratamiento":
                    consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)
                    for datoPaquete in consultaPaqueteTratamiento:
                        nombreServTratPaq = datoPaquete.nombre_paquete
                        precioServTratPaq = datoPaquete.precio_por_paquete
                elif tipoCita == "ServicioCertificado":
                    certificadoServicio = citaEfectuada.certificado_servicio
                    servCertSeparado = certificadoServicio.split("-")
                    idCertificado = servCertSeparado[0]
                    idServicioCertificado = servCertSeparado[1]
                    idCertificadoInt = int(idCertificado)
                    idServicioCertificadoInt = int(idCertificadoInt)
                    idCertificadosPendientesCitas.append(idCertificadoInt)
                    #Consulta de certificado
                    consultaCertificado = CertificadosProgramados.objects.filter(id_certificado = idCertificadoInt)
                    for datoCertificado in consultaCertificado:
                        codigoCertificado = datoCertificado.codigo_certificado

                    #Consulta de servicio certificado
                    consultaServicioCertificado = ServiciosCertificados.objects.filter(id_servicio_certificado = idServicioCertificadoInt)
                    for datoServicio in consultaServicioCertificado:
                        nombreServicioCertificado = datoServicio.nombre
                    nombreServTratPaq = codigoCertificado + " - "+nombreServicioCertificado
                        
                
                fechaPactada = citaEfectuada.fecha_pactada
                horaPactada = citaEfectuada.hora_pctada
                duracionCita = citaEfectuada.duracionCitaMinutos
                duracionCita = int(duracionCita)
                comentarios = citaEfectuada.comentarios

                idVenta = citaEfectuada.venta_id



                citasEfectuadas.append([idCita, nombreCompletoCliente, nombreCompletoEmpleado, tipoCita, nombreServTratPaq, precioServTratPaq,
                fechaPactada, horaPactada,duracionCita, comentarios,idVenta])


            
            return render(request, "22 Citas/verCitas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta,"tipoUsuario":tipoUsuario, "nombreSucursalView":nombreSucursalView,
                "citasPendientes":citasPendientes, "citasEfectuadas":citasEfectuadas, "notificacionCita":notificacionCita, "citasPendientesReagendar":citasPendientesReagendar, "sinCitasPendientes":sinCitasPendientes, "arregloHoras2":arregloHoras2,
                "listaZipFechaHora":listaZipFechaHora, "fechaLimite":fechaLimite, "citasPendientesReagendar2":citasPendientesReagendar2, "citasPendientesReagendar3":citasPendientesReagendar3, "citasPendientesReagendar4":citasPendientesReagendar4, "listaZipFechaHora2":listaZipFechaHora2,
                "citasPendientesReagendar5":citasPendientesReagendar5, "cistasPendientesZipeada":cistasPendientesZipeada})


        else:           
            if tipoUsuario == "esAdmin":
                sucursales = Sucursales.objects.all()
                
                if "citasEnviadas" in request.session:
                    citasEnviadas = request.session["citasEnviadas"]
                    del request.session["citasEnviadas"]
                    return render(request, "22 Citas/seleccionarSucursalCitaVer.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "citasEnviadas":citasEnviadas, "notificacionCita":notificacionCita})
                    
                if "citaReagendada" in request.session:
                    citaReagendada = request.session["citaReagendada"]
                    del request.session["citaReagendada"]
                    return render(request, "22 Citas/seleccionarSucursalCitaVer.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita, "citaReagendada":citaReagendada})

                return render(request, "22 Citas/seleccionarSucursalCitaVer.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})
            else:
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    sucursalEmpleado = datoEmpleado.id_sucursal_id
                sucursales = Sucursales.objects.filter(id_sucursal = sucursalEmpleado)
                
                if "citasEnviadas" in request.session:
                    citasEnviadas = request.session["citasEnviadas"]
                    del request.session["citasEnviadas"]
                    return render(request, "22 Citas/seleccionarSucursalCitaVer.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "citasEnviadas":citasEnviadas, "notificacionCita":notificacionCita})

                if "citaReagendada" in request.session:
                    citaReagendada = request.session["citaReagendada"]
                    del request.session["citaReagendada"]
                    return render(request, "22 Citas/seleccionarSucursalCitaVer.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                    "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita, "citaReagendada":citaReagendada})


                return render(request, "22 Citas/seleccionarSucursalCitaVer.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})
        
    else:
        return render(request,"1 Login/login.html")

def calendarioCitas(request):

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

        print(notificacionCita)

        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)

        if request.method == "POST":
            sucursalCita = request.POST['sucursalCita']
            consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalCita)
            for datoSucursal in consultaSucursal:
                nombreSucursal = datoSucursal.nombre

            #Calendario citas

            #Fecha mes anterior
            fechaMesAnterior = datetime.now()-relativedelta(months=1)
            añoAnterior = fechaMesAnterior.strftime("%Y")
            mesAnterior = fechaMesAnterior.strftime("%m")
            fechaMesAnterior = añoAnterior + "-"+mesAnterior+"-01"

            #Fecha mes despues
            fechaMesDespues = datetime.now()+relativedelta(months=1)
            añoDespues = fechaMesDespues.strftime("%Y")
            mesDespues = fechaMesDespues.strftime("%m")
            fechaMesDespues = añoDespues + "-"+mesDespues+"-15"

            citasPendientes = Citas.objects.filter(fecha_pactada__range = [fechaMesAnterior, fechaMesDespues], estado_cita = "sinCanjear")

            arrayCitasPendientes = []

            for citaPendiente in citasPendientes:
                
                #Datos de la cita
                idCita = citaPendiente.id_cita
                cliente = citaPendiente.cliente_id
                empleadoRealizo = citaPendiente.empleado_realizo_id
                tipoCita = citaPendiente.tipo_cita
                idServTratPaq = citaPendiente.id_serv_trat_paq
                fechaPactada = citaPendiente.fecha_pactada
                horaPactada = citaPendiente.hora_pctada
                comentarios = citaPendiente.comentarios
                duracionMinutos = citaPendiente.duracionCitaMinutos
                duracionMinutos = int(duracionMinutos)

                fechaPactadaTipoDate = datetime.strftime(fechaPactada, '%Y-%m-%d')
                #Fecha en texto
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

                mesPactado = datetime.strftime(fechaPactada, '%m')
                diaPactado = datetime.strftime(fechaPactada, '%d')
                añoPactado = datetime.strftime(fechaPactada, '%Y')

                mesEnTexto = mesesDic[str(mesPactado)]
                fechaPactadaMensaje = diaPactado + " de "+mesEnTexto+ " del " + añoPactado

                #Datos del cliente
                consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                for datoCliente in consultaCliente:
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoPaterno = datoCliente.apellidoPaterno_cliente

                nombreCompletoCliente = nombreCliente + " "+apellidoPaterno

                #Datos del empleado que realizo la cita
                consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoRealizo)
                for datoEmpleado in consultaEmpleado:
                    nombreEmpleado = datoEmpleado.nombres
                    apellidoEmpleado = datoEmpleado.apellido_paterno
                
                nombreCompletoEmpleado = nombreEmpleado +" "+apellidoEmpleado

                tipoCitaTexto = ""
                if tipoCita == "Servicio":
                    tipoCitaTexto = "Servicio"
                    consultaServicio = Servicios.objects.filter(id_servicio = idServTratPaq)
                    for datoServicio in consultaServicio:
                        nombreServTratPaq = datoServicio.nombre_servicio
                        precioServTraPaq = datoServicio.precio_venta
                elif tipoCita == "SesionTratamiento":
                    tipoCitaTexto = "Sesion de tratamiento"
                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idServTratPaq)
                    for datoTratamiento in consultaTratamiento:
                        nombreServTratPaq = datoTratamiento.nombre_tratamiento
                        precioServTraPaq = datoTratamiento.costo_venta_tratamiento
                elif tipoCita == "PaqueteTratamiento":
                    tipoCitaTexto = "Paquete/Promoción de tratamiento"
                    consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)
                    for datoPaquete in consultaPaqueteTratamiento:
                        nombreServTratPaq = datoPaquete.nombre_paquete
                        precioServTraPaq = datoPaquete.precio_por_paquete

                arrayCitasPendientes.append([fechaPactadaMensaje, idCita, nombreCompletoCliente, tipoCitaTexto,nombreServTratPaq, precioServTraPaq, horaPactada, duracionMinutos,fechaPactadaTipoDate])
            
            citasEfectuadas = Citas.objects.filter(fecha_pactada__range = [fechaMesAnterior, fechaMesDespues], estado_cita = "efectuada")

            arrayCitasEfectuadas = []

            for citaEfectuada in citasEfectuadas:
                
                #Datos de la cita
                idCita = citaEfectuada.id_cita
                cliente = citaEfectuada.cliente_id
                empleadoRealizo = citaEfectuada.empleado_realizo_id
                tipoCita = citaEfectuada.tipo_cita
                idServTratPaq = citaEfectuada.id_serv_trat_paq
                fechaPactada = citaEfectuada.fecha_pactada
                horaPactada = citaEfectuada.hora_pctada
                comentarios = citaEfectuada.comentarios
                duracionMinutos = citaEfectuada.duracionCitaMinutos
                duracionMinutos = int(duracionMinutos)

                fechaPactadaTipoDate = datetime.strftime(fechaPactada, '%Y-%m-%d')
                #Fecha en texto
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

                mesPactado = datetime.strftime(fechaPactada, '%m')
                diaPactado = datetime.strftime(fechaPactada, '%d')
                añoPactado = datetime.strftime(fechaPactada, '%Y')

                mesEnTexto = mesesDic[str(mesPactado)]
                fechaPactadaMensaje = diaPactado + " de "+mesEnTexto+ " del " + añoPactado

                #Datos del cliente
                consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                for datoCliente in consultaCliente:
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoPaterno = datoCliente.apellidoPaterno_cliente

                nombreCompletoCliente = nombreCliente + " "+apellidoPaterno

                #Datos del empleado que realizo la cita
                consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoRealizo)
                for datoEmpleado in consultaEmpleado:
                    nombreEmpleado = datoEmpleado.nombres
                    apellidoEmpleado = datoEmpleado.apellido_paterno
                
                nombreCompletoEmpleado = nombreEmpleado +" "+apellidoEmpleado

                tipoCitaTexto = ""
                if tipoCita == "Servicio":
                    tipoCitaTexto = "Servicio"
                    consultaServicio = Servicios.objects.filter(id_servicio = idServTratPaq)
                    for datoServicio in consultaServicio:
                        nombreServTratPaq = datoServicio.nombre_servicio
                        precioServTraPaq = datoServicio.precio_venta
                elif tipoCita == "SesionTratamiento":
                    tipoCitaTexto = "Sesion de tratamiento"
                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idServTratPaq)
                    for datoTratamiento in consultaTratamiento:
                        nombreServTratPaq = datoTratamiento.nombre_tratamiento
                        precioServTraPaq = datoTratamiento.costo_venta_tratamiento
                elif tipoCita == "PaqueteTratamiento":
                    tipoCitaTexto = "Paquete/Promoción de tratamiento"
                    consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)
                    for datoPaquete in consultaPaqueteTratamiento:
                        nombreServTratPaq = datoPaquete.nombre_paquete
                        precioServTraPaq = datoPaquete.precio_por_paquete

                arrayCitasEfectuadas.append([fechaPactadaMensaje, idCita, nombreCompletoCliente, tipoCitaTexto,nombreServTratPaq, precioServTraPaq, horaPactada, duracionMinutos,fechaPactadaTipoDate])



                

                    


            


            return render(request, "22 Citas/calendarioCitas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
            "notificacionRenta":notificacionRenta,"notificacionCita":notificacionCita, "nombreSucursal":nombreSucursal, "arrayCitasPendientes":arrayCitasPendientes, 
            "arrayCitasEfectuadas":arrayCitasEfectuadas})


        else:
            if tipoUsuario == "esAdmin":
                sucursales = Sucursales.objects.all()
                
                return render(request, "22 Citas/seleccionarSucursalCitaCalendarioCitas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta,"notificacionCita":notificacionCita, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "sucursales":sucursales})
            else:
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    sucursalEmpleado = datoEmpleado.id_sucursal_id
                sucursales = Sucursales.objects.filter(id_sucursal = sucursalEmpleado)
                return render(request, "22 Citas/seleccionarSucursalCitaCalendarioCitas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta,"notificacionCita":notificacionCita, "sucursales":sucursales})
        
    else:
        return render(request,"1 Login/login.html")


def vistaVenderCita(request):

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

            idCita = request.POST["idCita"]
            #Datos de cita
            consultaCita = Citas.objects.filter(id_cita = idCita)
            for datoCita in consultaCita:
                idSucursal = datoCita.sucursal_id
                horaPactada = datoCita.hora_pctada
                cliente = datoCita.cliente_id
                tipoCita = datoCita.tipo_cita
                duracion = datoCita.duracionCitaMinutos
                duracion = int(duracion)
                idServTratPaq = datoCita.id_serv_trat_paq
                idCita = datoCita.id_cita
                estadoCita = datoCita.estado_cita
            
            #Datos de cliente
            consultaCliente = Clientes.objects.filter(id_cliente = cliente)
            for datoCliente in consultaCliente:
                nombreCliente = datoCliente.nombre_cliente
                apellidoPaternoCliente = datoCliente.apellidoPaterno_cliente
                idCliente = datoCliente.id_cliente
                nombreCompletoCliente = nombreCliente + " "+apellidoPaternoCliente

            #Datos de sucursal
            consultaSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
            for datoSucursal in consultaSucursal:
                nombreSucursal = datoSucursal.nombre

            #Datos del vendedor
            consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = idEmpleado)

            #Datos de servicio/tratamiento/paquete a vender
            tipoDeCita = ""
            datosTipoCita = []
            
            if tipoCita == "Servicio":
                tipoDeCita = "SERVICIO"
                consultaServicio = Servicios.objects.filter(id_servicio =idServTratPaq) 
                for datoServicio in consultaServicio:
                    idServicio = datoServicio.id_servicio
                    nombreServicio = datoServicio.nombre_servicio
                    precioServicio = datoServicio.precio_venta
                    descripcionServicio = datoServicio.descripcion_servicio
                    complementosServicio = datoServicio.complementos_servicio
                    precioCita = precioServicio
                
                datosTipoCita.append([idServicio,nombreServicio,precioServicio,descripcionServicio, complementosServicio])
            elif tipoCita == "SesionTratamiento":
                tipoDeCita = "SESIÓN DE TRATAMIENTO"
                consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idServTratPaq)
                for datoTratamiento in consultaTratamiento:
                    nombreTratamiento = datoTratamiento.nombre_tratamiento
                    codigoTratamiento = datoTratamiento.codigo_tratamiento
                    tipoTratamiento = datoTratamiento.tipo_tratamiento
                    descripcionTratamiento = datoTratamiento.descripcion_tratamiento
                    complementosTratamiento = datoTratamiento.complementos_tratamiento
                    precioTratamiento = datoTratamiento.costo_venta_tratamiento
                    precioCita = precioTratamiento
                datosTipoCita.append([codigoTratamiento,nombreTratamiento,precioTratamiento,tipoTratamiento,descripcionTratamiento, complementosTratamiento])
            elif tipoCita == "PaqueteTratamiento":
                tipoDeCita = "PAQUETE/PROMOCIÓN TRATAMIENTO"
                consultaPromocion = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)
                for datoPromo in consultaPromocion:
                    nombrePaquete = datoPromo.nombre_paquete
                    numero_sesiones = datoPromo.numero_sesiones
                    descuento = datoPromo.descuento
                    if descuento == None:
                        boolDescuento = "Con descuento"
                    else:
                        boolDescuento = "Sin descuento"
                    precioPaquete = datoPromo.precio_por_paquete
                    precioCita = precioPaquete

                    #Datos de tratamiento
                    idTratamiento = datoPromo.tratamiento_id
                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)
                    for datoTratamiento in consultaTratamiento:
                        nombreTratamiento = datoTratamiento.nombre_tratamiento
                        codigoTratamiento = datoTratamiento.codigo_tratamiento
                        tipoTratamiento = datoTratamiento.tipo_tratamiento
                datosTipoCita.append([nombrePaquete,numero_sesiones,boolDescuento,descuento,precioPaquete, nombreTratamiento, codigoTratamiento, tipoTratamiento])

                
            #Límites de creditos de cliente
            limiteCreditoSucursal = ConfiguracionCredito.objects.filter(sucursal_id__id_sucursal = idSucursal)
            
            for limite in limiteCreditoSucursal:
                if limite.activo == "S":
                    montoLimite = float(limite.limite_credito)
        
            consultaCreditosPendientesClientes = Creditos.objects.filter(cliente_id__id_cliente = idCliente, estatus ="Pendiente")
            creditoFaltantePorPagar= 0
            creditoLibreCliente = 0
            creditoSolicitado =0
            creditoPagado = 0
            for credito in consultaCreditosPendientesClientes:
                montoTotal = credito.monto_pagar
                montoPagado = credito.monto_pagado
                montoRestante = credito.monto_restante
                
                creditoSolicitado = creditoSolicitado + montoTotal
                creditoPagado = creditoPagado + montoPagado
                creditoFaltantePorPagar = creditoFaltantePorPagar + montoRestante
            
            creditoLibreCliente = montoLimite - creditoFaltantePorPagar
            
            boolCreditoLibreCliente = False

            if creditoLibreCliente > precioCita:
                boolCreditoLibreCliente = True
            else:
                boolCreditoLibreCliente = False

            #Descuentos
            descuentos = Descuentos.objects.all()

            #Fechas Abonos
            fechaInicioDePago = datetime.now()+relativedelta(days=15)
            fechaInicioDePago = datetime.strftime(fechaInicioDePago, '%Y-%m-%d')
            print(str(fechaInicioDePago));
            fechaFinalDePago = datetime.now()+relativedelta(days=75)
            fechaFinalDePago = datetime.strftime(fechaFinalDePago, '%Y-%m-%d')
            print(str(fechaFinalDePago));



            if tipoCita == "PaqueteTratamiento":
                consultaCitasTratamientos = citasTratamientos.objects.filter(cita_id__id_cita = idCita)

                for datoCitaTratamiento in consultaCitasTratamientos:
                    idTratamientoCliente = datoCitaTratamiento.idTratamientoCliente_id
                
                consultaPagosTratamiento = pagosPaquetesTratamientos.objects.filter(id_tratamiento_cliente_id__id_tratamiento_cliente = idTratamientoCliente)
                for datoPago in consultaPagosTratamiento:
                    totalAbonado = datoPago.total_abonado
                    totalRestante = datoPago.total_restante
                    estatusPago = datoPago.estatus_pago
                
                mitad = totalRestante/2

                primerPago = False
                if totalAbonado == 0:
                    primerPago = True
                else:
                    primerPago = False

                return render(request, "22 Citas/vistaVenderCita.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "idSucursal":idSucursal, "nombreSucursal":nombreSucursal, "consultaEmpleadoVendedor":consultaEmpleadoVendedor, "horaPactada":horaPactada,
                "nombreCompletoCliente":nombreCompletoCliente, "idCliente":idCliente, "tipoDeCita":tipoDeCita, "duracion":duracion, "datosTipoCita":datosTipoCita,"boolCreditoLibreCliente":boolCreditoLibreCliente,
                "creditoLibreCliente":creditoLibreCliente, "montoLimite":montoLimite, "creditoFaltantePorPagar":creditoFaltantePorPagar, "descuentos":descuentos, "precioCita":precioCita, "fechaInicioDePago":fechaInicioDePago,
                "fechaFinalDePago":fechaFinalDePago, "idServTratPaq":idServTratPaq, "idCita":idCita, "totalAbonado":totalAbonado, "totalRestante":totalRestante, 
                "estatusPago":estatusPago, "mitad":mitad, "primerPago":primerPago, "tipoCita":tipoCita, "notificacionCita":notificacionCita})
            
            if estadoCita == "sinCanjear":

                estatusPago = estadoCita
            else:
                estatusPago = "Efectuado"
            return render(request, "22 Citas/vistaVenderCita.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "idSucursal":idSucursal, "nombreSucursal":nombreSucursal, "consultaEmpleadoVendedor":consultaEmpleadoVendedor, "horaPactada":horaPactada,
                "nombreCompletoCliente":nombreCompletoCliente, "idCliente":idCliente, "tipoDeCita":tipoDeCita, "duracion":duracion, "datosTipoCita":datosTipoCita,"boolCreditoLibreCliente":boolCreditoLibreCliente,
                "creditoLibreCliente":creditoLibreCliente, "montoLimite":montoLimite, "creditoFaltantePorPagar":creditoFaltantePorPagar, "descuentos":descuentos, "precioCita":precioCita, "fechaInicioDePago":fechaInicioDePago,
                "fechaFinalDePago":fechaFinalDePago, "idServTratPaq":idServTratPaq, "idCita":idCita, "tipoCita":tipoCita, "notificacionCita":notificacionCita, "estatusPago":estatusPago})



        
        
    else:
        return render(request,"1 Login/login.html")

def guardarVentaCita(request):

    if "idSesion" in request.session:

        idEmpleado = request.session['idSesion']
        if request.method == "POST":

            tipoCita = request.POST['tipoCita']
            if tipoCita == "PaqueteTratamiento":   #Es paquete..
                totalRestante = request.POST['totalRestante']
                totalRestante = float(totalRestante)

                if totalRestante == 0:
                    #Se guarda la cita pero no la venta pporque ya se pago..
                    request.session['ventaAgregada'] = "La cita se ha guardado satisfactoriamente!"
                    idCita = request.POST['idCita']
                    tipoCita = request.POST['tipoCita']
                    idServTratPaq = request.POST['idServTratPaq']

                    #Actualizar Cita
                    idUltimaVenta = 0
                    consultaVentas = Ventas.objects.all()
                    for venta in consultaVentas:
                        idUltimaVenta = venta.id_venta
                    actualizacionCita = Citas.objects.get(id_cita = idCita)
                    actualizacionCita.estado_cita = "efectuada"
                    actualizacionCita.venta_id = Ventas.objects.get(id_venta = idUltimaVenta)
                    actualizacionCita.save()

                    

                    consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)

                    for datoPromo in consultaPaqueteTratamiento:
                        idTratamiento = datoPromo.tratamiento_id
                        nombreTratamientoPaquete = datoPromo.nombre_paquete
                        precioPaquete = datoPromo.precio_por_paquete
                        consultaTratamientoProductos = TratamientosProductosGasto.objects.filter(tratamiento_id__id_tratamiento = idTratamiento)

                        if consultaTratamientoProductos:
                            sinProductos = False
                            for producto in consultaTratamientoProductos:
                                idProducto = producto.producto_gasto_id
                                cantidadUtilizada = producto.cantidad

                                consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                                for dato in consultaProducto:
                                    cantidadActualEnExistencia = dato.cantidad
                                    cuantificable = dato.contenido_cuantificable

                                if cuantificable == "S":
                                    actualizacionCantidad = cantidadActualEnExistencia - cantidadUtilizada

                                    actualizarProducto = ProductosGasto.objects.filter(id_producto = idProducto).update(cantidad = actualizacionCantidad)

                        else:
                            sinProductos = True

                    #Actualización de cita-tratamiento en caso de que haya
                    consultaCitaEnTablaTratamientoCliente = citasTratamientos.objects.filter(cita_id__id_cita = idCita)
                    if consultaCitaEnTablaTratamientoCliente:
                        for cita in consultaCitaEnTablaTratamientoCliente:
                            idTratamientoCliente = cita.idTratamientoCliente_id
                        
                        consultaTratamientoCliente = TratamientosClientes.objects.filter(id_tratamiento_cliente = idTratamientoCliente)

                        for datoTratamientoCliente in consultaTratamientoCliente:
                            sesionesPendientesActuales = datoTratamientoCliente.sesionesPendientes
                            sesionesCanjeadas = datoTratamientoCliente.sesionesCanjeadas
                            cliente= datoTratamientoCliente.cliente_id
                        
                        nuevasSesionesPendientes = sesionesPendientesActuales - 1
                        nuevasSesionesCanjeadas = sesionesCanjeadas + 1

                        actualizacionTratamientoCliente = TratamientosClientes.objects.filter(id_tratamiento_cliente = idTratamientoCliente).update(sesionesPendientes = nuevasSesionesPendientes,
                        sesionesCanjeadas = nuevasSesionesCanjeadas)

                        if actualizacionTratamientoCliente:
                            fechaMovimiento = datetime.now()
                            #Registro de historial
                            registroEnHistorialDeTratamiento = HistorialTratamientosClientes(tratamiento_cliente = TratamientosClientes.objects.get(id_tratamiento_cliente = idTratamientoCliente),
                            sesion_efectuada = nuevasSesionesCanjeadas, fecha_efectuado = fechaMovimiento)

                            registroEnHistorialDeTratamiento.save()

                    #IMPRESION DE TICKEEETSSSS
                    
                    consultaCita = Citas.objects.filter(id_cita = idCita)
                    for datoCita in consultaCita:
                        empleadoVendedor = datoCita.empleado_realizo_id
                        sucursal = datoCita.sucursal_id
                        cliente = datoCita.cliente_id

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
                    horaVenta = datetime.now().time()
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
                        c.EscribirTexto("SESIÓN #"+str(nuevasSesionesCanjeadas)+"\n")
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto(str(nuevasSesionesPendientes)+" SESIONES PENDIENTES\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")

                        #Listado de productos 
                        
                        
                        costototalProductoDosDecimales = round(precioPaquete, 2)
                        costototalProductoDosDecimales = str(costototalProductoDosDecimales)

                        costoTotalProductoDivididoEnElPunto = costototalProductoDosDecimales.split(".")
                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                        longitudCostoTotal = int(longitudCostoTotal)

                        
                        caracteresProducto = len(nombreTratamientoPaquete)

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
                        c.EscribirTexto("1 x "+nombreTratamientoPaquete+espaciosTicket+str(costototalProductoDosDecimales)+"\n")


                        c.EscribirTexto("\n")
                        
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("====== LIQUIDADA ======\n")
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        
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


                        try:
                            tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                            botCostabella = telepot.Bot(tokenTelegram)

                            idGrupoTelegram = keysBotCostabella.idGrupo
                            
                            mensaje = "\U0001F4C6 CITA VENDIDA \U0001F4C6 \n El cliente "+nombreClienteTicket+" acudió por sesión de la cita #"+str(idCita)+" previamente pagada, sesión #"+str(nuevasSesionesCanjeadas)+" de "+str(nuevasSesionesPendientes)+", el día "+hoyFormato+" a las "+str(horaVenta)+" hrs en la sucursal "+nombreSucursal+"\n Paquete:\n"+nombreTratamientoPromo
                            botCostabella.sendMessage(idGrupoTelegram,mensaje)
                        except:
                            print("An exception occurred")

                    return redirect("/ventas/")
                else:

                    #Se guarda la venta sin credito

                    ventaEnCredito = False
                    fechaVenta = datetime.now()
                    horaVenta = datetime.now().time()


                    sucursal = request.POST['idSucursal']
                    comentariosExtras = request.POST['comentarios']
                    if comentariosExtras == "":
                        comentarios = "Sin comentarios"
                    else:
                        comentarios = comentariosExtras

                    #Empleado vendedor
                    empleadoVendedor = idEmpleado

                    #cliente
                    clienteMandado = request.POST['clienteSeleccionado']

                    #Tipo de cita y id servicio trata paquete
                    tipoCita = request.POST['tipoDeCita']
                    idServTratPaq = request.POST['idServTratPaq']
                    esServicio = False
                    esTratamiento = False
                    esPaquete = False
                    idCita = request.POST['idCita']

                    if tipoCita == "SERVICIO":
                        esServicio = True

                        servicioCorporal = False
                        consultaServicio = Servicios.objects.filter(id_servicio = idServTratPaq)
                        for datoServicio in consultaServicio:
                            tipoServicio = datoServicio.tipo_servicio
                        
                        if tipoServicio == "Corporal":
                            servicioCorporal = True
                    elif tipoCita == "SESIÓN DE TRATAMIENTO":
                        esTratamiento = True
                    elif tipoCita == "PAQUETE/PROMOCIÓN TRATAMIENTO":
                        esPaquete = True

                    #COSTO TOTAL A PAGAR
                    abonoCliente = request.POST['abonoCliente']
                    


                    esConEfectivo = False
                    esConTarjeta = False
                    esConTransferencia = False

                    stridServTratPaq = str(idServTratPaq)
                    cantidad = "1"
                    descuento = "SinDescuento"
                    if ventaEnCredito == False: #Venta normal sin credito
                        formaPago = request.POST['tipoPago']
                        
                        #datos de pago.
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
                            if descuento == "SinDescuento":
                                if esPaquete: #Venta en efectivo, sin descuento y paquete tratamiento
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                        tipo_pago = formaPago, 
                                        empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                        ids_productos = "", cantidades_productos = "",
                                        ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                        ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                        id_paquete_promo_vendido = PaquetesPromocionTratamientos.objects.get(id_paquete_tratamiento = idServTratPaq),
                                        monto_pagar = abonoCliente, credito = "N",
                                        comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                        cliente = Clientes.objects.get(id_cliente = clienteMandado))

                           

                        if esConTarjeta: 
                            if descuento == "SinDescuento":
                                if esPaquete: #Venta con tarjeta, sin descuento y paquete
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                        tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta, 
                                        empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                        ids_productos = "", cantidades_productos = "",
                                        ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                        ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                        id_paquete_promo_vendido = PaquetesPromocionTratamientos.objects.get(id_paquete_tratamiento = idServTratPaq),
                                        monto_pagar = abonoCliente, credito = "N",
                                        comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                        cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            
                            
                        if esConTransferencia:
                            if descuento == "SinDescuento":
                                if esPaquete: #Venta con transferencia, sin descuento y paquete
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                        tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                                        empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                        ids_productos = "", cantidades_productos = "",
                                        ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                        ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                        id_paquete_promo_vendido = PaquetesPromocionTratamientos.objects.get(id_paquete_tratamiento = idServTratPaq),
                                        monto_pagar = abonoCliente, credito = "N",
                                        comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                        cliente = Clientes.objects.get(id_cliente = clienteMandado))

                            
                    
                        registroVenta.save()

                    if registroVenta and esConEfectivo: #Venta guardada y con efectivo.. genera un movimiento
                        
                        ultimoId = 0
                        ventasTotalesEfectivo = Ventas.objects.filter(tipo_pago = "Efectivo")
                        for venta in ventasTotalesEfectivo:
                            ultimoId = venta.id_venta
                        tipoMovimiento = "IN"
                        montoMovimiento = float(abonoCliente)
                        descripcionMovimiento = "Movimiento por venta "+str(ultimoId)
                        fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                        horaMovimiento = datetime.now().time()

                        ingresarCantidadEfectivoACaja = MovimientosCaja(fecha = fechaMovimiento, hora = horaMovimiento, tipo = tipoMovimiento, monto = montoMovimiento, descripcion = descripcionMovimiento, 
                        sucursal = Sucursales.objects.get(id_sucursal = sucursal), realizado_por = Empleados.objects.get(id_empleado = empleadoVendedor))
                        ingresarCantidadEfectivoACaja.save()

                        request.session['ventaAgregada'] = "La venta ha sido agregada satisfactoriamente!"

                        #Actualizar Cita
                        idUltimaVenta = 0
                        consultaVentas = Ventas.objects.all()
                        for venta in consultaVentas:
                            idUltimaVenta = venta.id_venta
                        actualizacionCita = Citas.objects.get(id_cita = idCita)
                        actualizacionCita.estado_cita = "efectuada"
                        actualizacionCita.venta_id = Ventas.objects.get(id_venta = idUltimaVenta)
                        actualizacionCita.save()


                        
                        if esPaquete:
                            consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)

                            for datoPromo in consultaPaqueteTratamiento:
                                idTratamiento = datoPromo.tratamiento_id
                                nombreTratamientoPromo = datoPromo.nombre_paquete
                                precioPromo = datoPromo.precio_por_paquete
                                consultaTratamientoProductos = TratamientosProductosGasto.objects.filter(tratamiento_id__id_tratamiento = idTratamiento)

                                if consultaTratamientoProductos:
                                    sinProductos = False
                                    for producto in consultaTratamientoProductos:
                                        idProducto = producto.producto_gasto_id
                                        cantidadUtilizada = producto.cantidad

                                        consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                                        for dato in consultaProducto:
                                            cantidadActualEnExistencia = dato.cantidad
                                            cuantificable = dato.contenido_cuantificable

                                        if cuantificable == "S":
                                            actualizacionCantidad = cantidadActualEnExistencia - cantidadUtilizada

                                            actualizarProducto = ProductosGasto.objects.filter(id_producto = idProducto).update(cantidad = actualizacionCantidad)

                                else:
                                    sinProductos = True
                        
                        #Actualización de cita-tratamiento en caso de que haya
                        consultaCitaEnTablaTratamientoCliente = citasTratamientos.objects.filter(cita_id__id_cita = idCita)
                        if consultaCitaEnTablaTratamientoCliente:
                            for cita in consultaCitaEnTablaTratamientoCliente:
                                idTratamientoCliente = cita.idTratamientoCliente_id
                            
                            consultaTratamientoCliente = TratamientosClientes.objects.filter(id_tratamiento_cliente = idTratamientoCliente)

                            for datoTratamientoCliente in consultaTratamientoCliente:
                                sesionesPendientesActuales = datoTratamientoCliente.sesionesPendientes
                                sesionesCanjeadas = datoTratamientoCliente.sesionesCanjeadas
                            
                            nuevasSesionesPendientes = sesionesPendientesActuales - 1
                            nuevasSesionesCanjeadas = sesionesCanjeadas + 1

                            actualizacionTratamientoCliente = TratamientosClientes.objects.filter(id_tratamiento_cliente = idTratamientoCliente).update(sesionesPendientes = nuevasSesionesPendientes,
                            sesionesCanjeadas = nuevasSesionesCanjeadas)

                            if actualizacionTratamientoCliente:

                                #Registro de historial
                                registroEnHistorialDeTratamiento = HistorialTratamientosClientes(tratamiento_cliente = TratamientosClientes.objects.get(id_tratamiento_cliente = idTratamientoCliente),
                                sesion_efectuada = nuevasSesionesCanjeadas, fecha_efectuado = fechaMovimiento)

                                registroEnHistorialDeTratamiento.save()
                        
                        #Actualizar pago
                        consultaPagosTratamiento = pagosPaquetesTratamientos.objects.filter(id_tratamiento_cliente_id__id_tratamiento_cliente = idTratamientoCliente)

                        for datosPagoTratamiento in consultaPagosTratamiento:
                            totalAbonado = datosPagoTratamiento.total_abonado
                            totalRestante = datosPagoTratamiento.total_restante
                            totalAPagar = datosPagoTratamiento.total_pagar

                        abono = float(totalAbonado) + float(abonoCliente)
                        restante = float(totalAPagar) - abono

                        pagadoTotalmenteTratamiento = False

                        if restante == 0:
                            pagadoTotalmenteTratamiento = True

                        if pagadoTotalmenteTratamiento:
                            actualizarPagoRegistro = pagosPaquetesTratamientos.objects.filter(id_tratamiento_cliente_id__id_tratamiento_cliente = idTratamientoCliente).update(
                                total_abonado = abono, total_restante = restante, estatus_pago = "Efectuado"
                            )
                        else:
                            actualizarPagoRegistro = pagosPaquetesTratamientos.objects.filter(id_tratamiento_cliente_id__id_tratamiento_cliente = idTratamientoCliente).update(
                                total_abonado = abono, total_restante = restante
                            )
                        

                        #IMPRESION DE TICKEEETSSSS
                        #Ultimo id de venta
                        consultaVentas = Ventas.objects.all()
                        ultimoIdVenta = 0
                        for venta in consultaVentas:
                            ultimoIdVenta = venta.id_venta
                            cliente = venta.cliente_id
                            sucursal = venta.sucursal_id
                            descuento = venta.descuento_id

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
                        if cliente == None:
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
                            c.EscribirTexto("CITA "+str(idCita)+"- VENTA #"+str(ultimoIdVenta)+"\n")
                            c.EscribirTexto("SESIÓN #"+str(nuevasSesionesCanjeadas)+"\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto(str(nuevasSesionesPendientes)+" SESIONES PENDIENTES\n")
                            c.EstablecerEnfatizado(False)
                            c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("\n")
                            c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                            c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                            c.EscribirTexto("\n")
                            
                            
                            
                                    
                            
                            costototalDecimales = round(float(precioPromo), 2)
                            costototalDecimales = str(precioPromo)

                            costoTotalProductoDivididoEnElPunto = costototalDecimales.split(".")
                            longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                            longitudCostoTotal = int(longitudCostoTotal)

                                
                            caracteresProducto = len(nombreTratamientoPromo)

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
                            c.EscribirTexto("1 x "+nombreTratamientoPromo+espaciosTicket+str(costototalDecimales)+"\n")


                            
                            c.EscribirTexto("\n")
                            c.EscribirTexto("\n")
                            
                            if descuento == None:
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("TOTAL:  $"+str(precioPromo)+"\n")
                                restantePorPagar = float(restante) - float(abonoCliente)
                                c.EscribirTexto("ABONADO:  $"+str(abono)+"\n")
                                c.EscribirTexto("RESTANTE:  $"+str(restante)+"\n")
                            else:
                                intDescuento = int(descuento)
                                consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                                for datoDescuento in consultaDescuentos:
                                    nombreDescuento = datoDescuento.nombre_descuento
                                    porcentajeDescuento = datoDescuento.porcentaje

                                porcentajePagado = 100 - porcentajeDescuento #85
                                totalSinDescuento1 = 100 * float(precioPromo)
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
                                restantePorPagar = float(restante) - float(abonoCliente)
                                c.EscribirTexto("ABONADO:  $"+str(abono)+"\n")
                                c.EscribirTexto("RESTANTE:  $"+str(restante)+"\n")

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

                        try:
                            tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                            botCostabella = telepot.Bot(tokenTelegram)

                            idGrupoTelegram = keysBotCostabella.idGrupo
                            
                            mensaje = "\U0001F4C6 CITA VENDIDA \U0001F4C6 \n El cliente "+nombreClienteTicket+" acudió y pago la cita #"+str(idCita)+", sesión #"+str(nuevasSesionesCanjeadas)+" de "+str(nuevasSesionesPendientes)+", el día "+hoyFormato+" a las "+str(horaVenta)+" hrs en la sucursal "+nombreSucursal+"\n Paquete:\n"+nombreTratamientoPromo
                            botCostabella.sendMessage(idGrupoTelegram,mensaje)
                        except:
                            print("An exception occurred")


                        return redirect("/ventas/")

                    if registroVenta:
                        request.session['ventaAgregada'] = "La venta ha sido agregada satisfactoriamente!"

                        #Actualizar Cita
                        idUltimaVenta = 0
                        consultaVentas = Ventas.objects.all()
                        for venta in consultaVentas:
                            idUltimaVenta = venta.id_venta
                        actualizacionCita = Citas.objects.get(id_cita = idCita)
                        actualizacionCita.estado_cita = "efectuada"
                        actualizacionCita.venta_id = Ventas.objects.get(id_venta = idUltimaVenta)
                        actualizacionCita.save()

                        consultaCitaEnTablaTratamientoCliente = citasTratamientos.objects.filter(cita_id__id_cita = idCita)
                        if consultaCitaEnTablaTratamientoCliente:
                            for cita in consultaCitaEnTablaTratamientoCliente:
                                idTratamientoCliente = cita.idTratamientoCliente_id

                        if esPaquete:
                            consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)

                            for datoPromo in consultaPaqueteTratamiento:
                                idTratamiento = datoPromo.tratamiento_id
                                precioPromo = datoPromo.precio_por_paquete
                                nombreTratamientoPromo = datoPromo.nombre_paquete
                                consultaTratamientoProductos = TratamientosProductosGasto.objects.filter(tratamiento_id__id_tratamiento = idTratamiento)

                                if consultaTratamientoProductos:
                                    sinProductos = False
                                    for producto in consultaTratamientoProductos:
                                        idProducto = producto.producto_gasto_id
                                        cantidadUtilizada = producto.cantidad

                                        consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                                        for dato in consultaProducto:
                                            cantidadActualEnExistencia = dato.cantidad
                                            cuantificable = dato.contenido_cuantificable

                                        if cuantificable == "S":
                                            actualizacionCantidad = cantidadActualEnExistencia - cantidadUtilizada

                                            actualizarProducto = ProductosGasto.objects.filter(id_producto = idProducto).update(cantidad = actualizacionCantidad)

                                else:
                                    sinProductos = True
                            
                            #Actualización de cita-tratamiento en caso de que haya
                            fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                            consultaCitaEnTablaTratamientoCliente = citasTratamientos.objects.filter(cita_id__id_cita = idCita)
                            if consultaCitaEnTablaTratamientoCliente:
                                for cita in consultaCitaEnTablaTratamientoCliente:
                                    idTratamientoCliente = cita.idTratamientoCliente_id
                                
                                consultaTratamientoCliente = TratamientosClientes.objects.filter(id_tratamiento_cliente = idTratamientoCliente)

                                for datoTratamientoCliente in consultaTratamientoCliente:
                                    sesionesPendientesActuales = datoTratamientoCliente.sesionesPendientes
                                    sesionesCanjeadas = datoTratamientoCliente.sesionesCanjeadas
                                
                                nuevasSesionesPendientes = sesionesPendientesActuales - 1
                                nuevasSesionesCanjeadas = sesionesCanjeadas + 1

                                actualizacionTratamientoCliente = TratamientosClientes.objects.filter(id_tratamiento_cliente = idTratamientoCliente).update(sesionesPendientes = nuevasSesionesPendientes,
                                sesionesCanjeadas = nuevasSesionesCanjeadas)

                                if actualizacionTratamientoCliente:

                                    #Registro de historial
                                    registroEnHistorialDeTratamiento = HistorialTratamientosClientes(tratamiento_cliente = TratamientosClientes.objects.get(id_tratamiento_cliente = idTratamientoCliente),
                                    sesion_efectuada = nuevasSesionesCanjeadas, fecha_efectuado = fechaMovimiento)

                                    registroEnHistorialDeTratamiento.save()

                            #Actualizar pago
                            consultaPagosTratamiento = pagosPaquetesTratamientos.objects.filter(id_tratamiento_cliente_id__id_tratamiento_cliente = idTratamientoCliente)

                            for datosPagoTratamiento in consultaPagosTratamiento:
                                totalAbonado = datosPagoTratamiento.total_abonado
                                totalRestante = datosPagoTratamiento.total_restante
                                totalAPagar = datosPagoTratamiento.total_pagar

                            abono = float(totalAbonado) + float(abonoCliente)
                            restante = float(totalAPagar) - abono
                            
                            pagadoTotalmenteTratamiento = False
                            if restante == 0:
                                pagadoTotalmenteTratamiento = True

                            if pagadoTotalmenteTratamiento:
                                actualizarPagoRegistro = pagosPaquetesTratamientos.objects.filter(id_tratamiento_cliente_id__id_tratamiento_cliente = idTratamientoCliente).update(
                                    total_abonado = abono, total_restante = restante, estatus_pago = "Efectuado"
                                )
                            else:
                                actualizarPagoRegistro = pagosPaquetesTratamientos.objects.filter(id_tratamiento_cliente_id__id_tratamiento_cliente = idTratamientoCliente).update(
                                    total_abonado = abono, total_restante = restante
                                )

                        #IMPRESION DE TICKEEETSSSS
                        #Ultimo id de venta
                        consultaVentas = Ventas.objects.all()
                        ultimoIdVenta = 0
                        for venta in consultaVentas:
                            ultimoIdVenta = venta.id_venta
                            cliente = venta.cliente_id
                            sucursal = venta.sucursal_id
                            descuento = venta.descuento_id

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
                        if cliente == None:
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
                            c.EscribirTexto("CITA "+str(idCita)+" - VENTA #"+str(ultimoIdVenta)+"\n")
                            c.EscribirTexto("SESIÓN #"+str(nuevasSesionesCanjeadas)+"\n")
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto(str(nuevasSesionesPendientes)+" SESIONES PENDIENTES\n")
                            c.EstablecerEnfatizado(False)
                            c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("\n")
                            c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                            c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                            c.EscribirTexto("\n")
                            
                            
                            
                                    
                            
                            costototalDecimales = round(float(precioPromo), 2)
                            costototalDecimales = str(precioPromo)

                            costoTotalProductoDivididoEnElPunto = costototalDecimales.split(".")
                            longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                            longitudCostoTotal = int(longitudCostoTotal)

                                
                            caracteresProducto = len(nombreTratamientoPromo)

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
                            c.EscribirTexto("1 x "+nombreTratamientoPromo+espaciosTicket+str(costototalDecimales)+"\n")


                            
                            c.EscribirTexto("\n")
                            c.EscribirTexto("\n")
                            
                            if descuento == None:
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("TOTAL:  $"+str(precioPromo)+"\n")
                                restantePorPagar = float(restante) - float(abonoCliente)
                                c.EscribirTexto("ABONADO:  $"+str(abono)+"\n")
                                c.EscribirTexto("RESTANTE:  $"+str(restante)+"\n")
                            else:
                                intDescuento = int(descuento)
                                consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                                for datoDescuento in consultaDescuentos:
                                    nombreDescuento = datoDescuento.nombre_descuento
                                    porcentajeDescuento = datoDescuento.porcentaje

                                porcentajePagado = 100 - porcentajeDescuento #85
                                totalSinDescuento1 = 100 * float(precioPromo)
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
                                restantePorPagar = float(restante) - float(abonoCliente)
                                c.EscribirTexto("ABONADO:  $"+str(abono)+"\n")
                                c.EscribirTexto("RESTANTE:  $"+str(restante)+"\n")

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
                        
                        try:
                            tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                            botCostabella = telepot.Bot(tokenTelegram)

                            idGrupoTelegram = keysBotCostabella.idGrupo
                            
                            mensaje = "\U0001F4C6 CITA VENDIDA \U0001F4C6 \n El cliente "+nombreClienteTicket+" acudió y pago la cita #"+str(idCita)+", sesión #"+str(nuevasSesionesCanjeadas)+" de "+str(nuevasSesionesPendientes)+", el día "+hoyFormato+" a las "+str(horaVenta)+" hrs en la sucursal "+nombreSucursal+"\n Paquete:\n"+nombreTratamientoPromo
                            botCostabella.sendMessage(idGrupoTelegram,mensaje)
                        except:
                            print("An exception occurred")


                        return redirect("/ventas/")

            else: #No es paquete..
                
                fechaVenta = datetime.now()
                horaVenta = datetime.now().time()

                esACredito = False

                nameInput = "checkboxCredito"
                ventaEnCredito = False
                if request.POST.get(nameInput, False): #Credito Checkeado
                    ventaEnCredito = True
                elif request.POST.get(nameInput, True): #Credito No checkeado
                    ventaEnCredito = False

                sucursal = request.POST['idSucursal']
                comentariosExtras = request.POST['comentarios']
                if comentariosExtras == "":
                    comentarios = "Sin comentarios"
                else:
                    comentarios = comentariosExtras

                #Empleado vendedor
                empleadoVendedor = idEmpleado

                #cliente
                clienteMandado = request.POST['clienteSeleccionado']

                #Tipo de cita y id servicio trata paquete
                tipoCita = request.POST['tipoCita']
                idServTratPaq = request.POST['idServTratPaq']
                esServicio = False
                esTratamiento = False
                esPaquete = False
                idCita = request.POST['idCita']

                if tipoCita == "Servicio":
                    esServicio = True
                    servicioCorporal = False
                    consultaServicio = Servicios.objects.filter(id_servicio = idServTratPaq)
                    for datoServicio in consultaServicio:
                        tipoServicio = datoServicio.tipo_servicio

                        nombreServicioTratamiento = datoServicio.nombre_servicio
                    
                    if tipoServicio == "Corporal":
                        servicioCorporal = True
                elif tipoCita == "SesionTratamiento":
                    esTratamiento = True
                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idServTratPaq)
                    for datoTratamiento in consultaTratamiento:
                        nombreServicioTratamiento = datoTratamiento.nombre_tratamiento
                    
                elif tipoCita == "PaqueteTratamiento":
                    esPaquete = True
                
                    

                #COSTO TOTAL A PAGAR
                costoTotalAPagar = request.POST['costoTotalAPagar']

                #Descuento
                descuento = request.POST['descuento'] 

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


                esConEfectivo = False
                esConTarjeta = False
                esConTransferencia = False

                stridServTratPaq = str(idServTratPaq)
                cantidad = "1"

                if ventaEnCredito == False: #Venta normal sin credito
                    formaPago = request.POST['tipoPago']

                    
                    #datos de pago.
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
                        if descuento == "SinDescuento":
                            if esServicio:
                                
                                if servicioCorporal: #Venta en efectivo, sin descuento y servicio corporal
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales =stridServTratPaq, cantidades_servicios_corporales =cantidad,
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado)) 
                                else: #Venta en efectivo, sin descuento y servicio facial
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales =stridServTratPaq, cantidades_servicios_faciales =cantidad,
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            
                            elif esTratamiento: #Venta en efectivo, sin descuento y tratamiento
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    id_tratamiento_vendido = Tratamientos.objects.get(id_tratamiento = idServTratPaq),
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))

                            elif esPaquete: #Venta en efectivo, sin descuento y paquete tratamiento
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    id_paquete_promo_vendido = PaquetesPromocionTratamientos.objects.get(id_paquete_tratamiento = idServTratPaq),
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))

                        else:
                            if esServicio:
                                if servicioCorporal: #Venta en efectivo, con descuento y servicio corporal
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales =stridServTratPaq, cantidades_servicios_corporales =cantidad,
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    descuento = Descuentos.objects.get(id_descuento = descuento),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado)) 
                                else: #Venta en efectivo, con descuento y servicio facial
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales =stridServTratPaq, cantidades_servicios_faciales =cantidad,
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    descuento = Descuentos.objects.get(id_descuento = descuento),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            
                            elif esTratamiento: #Venta en efectivo, con descuento y tratamiento
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    id_tratamiento_vendido = Tratamientos.objects.get(id_tratamiento = idServTratPaq),
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal,
                                    descuento = Descuentos.objects.get(id_descuento = descuento)),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))

                            elif esPaquete: #Venta en efectivo, con descuento y paquete tratamiento
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    id_paquete_promo_vendido = PaquetesPromocionTratamientos.objects.get(id_paquete_tratamiento = idServTratPaq),
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    descuento = Descuentos.objects.get(id_descuento = descuento),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado)) 

                    if esConTarjeta: 
                        if descuento == "SinDescuento":
                            if esServicio:
                                if servicioCorporal: #Vente con tarjeta, sin descuento y corporal
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta,
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales =stridServTratPaq, cantidades_servicios_corporales =cantidad,
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                                else: #Venta con tarjeta, sin descuento y facial
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta,
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales =stridServTratPaq, cantidades_servicios_faciales =cantidad,
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            
                            elif esTratamiento: #Venta con tarjeta, sin descuento y tratamiento
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    id_tratamiento_vendido = Tratamientos.objects.get(id_tratamiento = idServTratPaq),
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            elif esPaquete: #Venta con tarjeta, sin descuento y paquete
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    id_paquete_promo_vendido = PaquetesPromocionTratamientos.objects.get(id_paquete_tratamiento = idServTratPaq),
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                        
                        else:
                            if esServicio: 
                                if servicioCorporal:#Venta con tarjeta, con descuento y corporal
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales =stridServTratPaq, cantidades_servicios_corporales =cantidad,
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    descuento = Descuentos.objects.get(id_descuento = descuento),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado)) 
                                else: #Venta con tarjeta, con descuento y facial
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta,
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales =stridServTratPaq, cantidades_servicios_faciales =cantidad,
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    descuento = Descuentos.objects.get(id_descuento = descuento),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            
                            elif esTratamiento: #Venta con tarjeta, con descuento y tratamiento
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    id_tratamiento_vendido = Tratamientos.objects.get(id_tratamiento = idServTratPaq),
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    descuento = Descuentos.objects.get(id_descuento = descuento),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))

                            elif esPaquete: #Venta con tarjeta, con descuento y paquete 
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, tipo_tarjeta = tipo_tarjeta, referencia_pago_tarjeta = referencia_tarjeta, 
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    id_paquete_promo_vendido = PaquetesPromocionTratamientos.objects.get(id_paquete_tratamiento = idServTratPaq),
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    descuento = Descuentos.objects.get(id_descuento = descuento),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado)) 
                    
                    if esConTransferencia:
                        if descuento == "SinDescuento":
                            if esServicio:
                                if servicioCorporal: #Venta con transferencia, sin descuento y corporal
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales =stridServTratPaq, cantidades_servicios_corporales =cantidad,
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                                else: #Venta con transferencia, sin descuento y facial
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales =stridServTratPaq, cantidades_servicios_faciales =cantidad,
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            elif esTratamiento: #Venta con transferencia, sin descuento y tratamiento
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    id_tratamiento_vendido = Tratamientos.objects.get(id_tratamiento = idServTratPaq),
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            elif esPaquete: #Venta con transferencia, sin descuento y paquete
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    id_paquete_promo_vendido = PaquetesPromocionTratamientos.objects.get(id_paquete_tratamiento = idServTratPaq),
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))

                        else:
                            if esServicio:
                                if servicioCorporal: #Venta con transferencia, con descuento y corporal
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales =stridServTratPaq, cantidades_servicios_corporales =cantidad,
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    descuento = Descuentos.objects.get(id_descuento = descuento),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado)) 
                                else: #Venta con transferencia, con descuento y facial
                                    registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales =stridServTratPaq, cantidades_servicios_faciales =cantidad,
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    descuento = Descuentos.objects.get(id_descuento = descuento),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            elif esTratamiento: #Venta con transferencia, con descuento y tratamiento
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    id_tratamiento_vendido = Tratamientos.objects.get(id_tratamiento = idServTratPaq),
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    descuento = Descuentos.objects.get(id_descuento = descuento),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            elif esPaquete: #Venta con transferencia, con descuento y paquete
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                    tipo_pago = formaPago, clave_rastreo_transferencia = clave_transferencia,
                                    empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                    ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                    id_paquete_promo_vendido = PaquetesPromocionTratamientos.objects.get(id_paquete_tratamiento = idServTratPaq),
                                    monto_pagar = costoTotalAPagar, credito = "N",
                                    comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                    descuento = Descuentos.objects.get(id_descuento = descuento),
                                    cliente = Clientes.objects.get(id_cliente = clienteMandado))
                
                else: #Venta a credito
                    
                   
                    
                    
                    

                    if descuento == "SinDescuento":
                        if esServicio:
                            
                            if servicioCorporal: #Venta en efectivo, sin descuento y servicio corporal
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                ids_productos = "", cantidades_productos = "",
                                ids_servicios_corporales =stridServTratPaq, cantidades_servicios_corporales =cantidad,
                                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                monto_pagar = costoTotalAPagar, credito = "S",
                                comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                cliente = Clientes.objects.get(id_cliente = clienteMandado)) 
                                esACredito = True
                                
                            else: #Venta en efectivo, sin descuento y servicio facial
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                ids_productos = "", cantidades_productos = "",
                                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                ids_servicios_faciales =stridServTratPaq, cantidades_servicios_faciales =cantidad,
                                monto_pagar = costoTotalAPagar, credito = "S",
                                comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                cliente = Clientes.objects.get(id_cliente = clienteMandado))
                                print("AQUI SE GUARDA LA VENTA POR EL SERVICIO CORPOPRAL")
                                esACredito = True
                            
                        
                        elif esTratamiento: #Venta en efectivo, sin descuento y tratamiento
                            registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                ids_productos = "", cantidades_productos = "",
                                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                id_tratamiento_vendido = Tratamientos.objects.get(id_tratamiento = idServTratPaq),
                                monto_pagar = costoTotalAPagar, credito = "S",
                                comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            esACredito = True

                        elif esPaquete: #Venta en efectivo, sin descuento y paquete tratamiento
                            registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                ids_productos = "", cantidades_productos = "",
                                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                id_paquete_promo_vendido = PaquetesPromocionTratamientos.objects.get(id_paquete_tratamiento = idServTratPaq),
                                monto_pagar = costoTotalAPagar, credito = "S",
                                comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            esACredito = True

                    else:
                        if esServicio:
                            if servicioCorporal: #Venta en efectivo, sin descuento y servicio corporal
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                ids_productos = "", cantidades_productos = "",
                                ids_servicios_corporales =stridServTratPaq, cantidades_servicios_corporales =cantidad,
                                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                monto_pagar = costoTotalAPagar, credito = "S",
                                comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                descuento = Descuentos.objects.get(id_descuento = descuento),
                                cliente = Clientes.objects.get(id_cliente = clienteMandado)) 
                                esACredito = True
                            else: #Venta en efectivo, sin descuento y servicio facial
                                registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                ids_productos = "", cantidades_productos = "",
                                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                ids_servicios_faciales =stridServTratPaq, cantidades_servicios_faciales =cantidad,
                                monto_pagar = costoTotalAPagar, credito = "S",
                                comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                descuento = Descuentos.objects.get(id_descuento = descuento),
                                cliente = Clientes.objects.get(id_cliente = clienteMandado))
                                esACredito = True
                        
                        elif esTratamiento: #Venta en efectivo, sin descuento y tratamiento
                            registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                ids_productos = "", cantidades_productos = "",
                                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                id_tratamiento_vendido = Tratamientos.objects.get(id_tratamiento = idServTratPaq),
                                monto_pagar = costoTotalAPagar, credito = "S",
                                comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                descuento = Descuentos.objects.get(id_descuento = descuento),
                                cliente = Clientes.objects.get(id_cliente = clienteMandado))
                            esACredito = True

                        elif esPaquete: #Venta en efectivo, sin descuento y paquete tratamiento
                            registroVenta = Ventas(fecha_venta = fechaVenta, hora_venta =horaVenta,
                                empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                                ids_productos = "", cantidades_productos = "",
                                ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                ids_servicios_faciales ="", cantidades_servicios_faciales ="",
                                id_paquete_promo_vendido = PaquetesPromocionTratamientos.objects.get(id_paquete_tratamiento = idServTratPaq),
                                monto_pagar = costoTotalAPagar, credito = "S",
                                comentariosVenta = comentarios, sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                                descuento = Descuentos.objects.get(id_descuento = descuento),
                                cliente = Clientes.objects.get(id_cliente = clienteMandado))

                            esACredito = True

                registroVenta.save()



                if registroVenta and esConEfectivo: #Venta guardada y con efectivo.. genera un movimiento
                    
                    ultimoId = 0
                    ventasTotalesEfectivo = Ventas.objects.filter(tipo_pago = "Efectivo")
                    for venta in ventasTotalesEfectivo:
                        ultimoId = venta.id_venta
                    tipoMovimiento = "IN"
                    montoMovimiento = float(costoTotalAPagar)
                    descripcionMovimiento = "Movimiento por venta "+str(ultimoId)
                    fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                    horaMovimiento = datetime.now().time()

                    ingresarCantidadEfectivoACaja = MovimientosCaja(fecha = fechaMovimiento, hora = horaMovimiento, tipo = tipoMovimiento, monto = montoMovimiento, descripcion = descripcionMovimiento, 
                    sucursal = Sucursales.objects.get(id_sucursal = sucursal), realizado_por = Empleados.objects.get(id_empleado = empleadoVendedor))
                    ingresarCantidadEfectivoACaja.save()

                    request.session['ventaAgregada'] = "La venta ha sido agregada satisfactoriamente!"

                    #Actualizar Cita
                    idUltimaVenta = 0
                    consultaVentas = Ventas.objects.all()
                    for venta in consultaVentas:
                        idUltimaVenta = venta.id_venta
                    actualizacionCita = Citas.objects.get(id_cita = idCita)
                    actualizacionCita.estado_cita = "efectuada"
                    actualizacionCita.venta_id = Ventas.objects.get(id_venta = idUltimaVenta)
                    actualizacionCita.save()


                    if esServicio:
                        consultaServiciosProductos = ServiciosProductosGasto.objects.filter(servicio_id__id_servicio =idServTratPaq)
                        if consultaServiciosProductos:
                            sinProductos = False

                            for producto in consultaServiciosProductos:
                                idProducto = producto.producto_gasto_id
                                cantidadUtilizada = producto.cantidad

                                consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                                for dato in consultaProducto:
                                    cantidadActualEnExistencia = dato.cantidad
                                    cuantificable = dato.contenido_cuantificable

                                if cuantificable == "S":
                                    actualizacionCantidad = cantidadActualEnExistencia - cantidadUtilizada

                                    actualizarProducto = ProductosGasto.objects.filter(id_producto = idProducto).update(cantidad = actualizacionCantidad)
                        else:
                            sinProductos = True
                    elif esTratamiento:
                        consultaTratamientoProductos = TratamientosProductosGasto.objects.filter(tratamiento_id__id_tratamiento = idServTratPaq)

                        if consultaTratamientoProductos:
                            sinProductos = False
                            for producto in consultaTratamientoProductos:
                                idProducto = producto.producto_gasto_id
                                cantidadUtilizada = producto.cantidad

                                consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                                for dato in consultaProducto:
                                    cantidadActualEnExistencia = dato.cantidad
                                    cuantificable = dato.contenido_cuantificable

                                if cuantificable == "S":
                                    actualizacionCantidad = cantidadActualEnExistencia - cantidadUtilizada

                                    actualizarProducto = ProductosGasto.objects.filter(id_producto = idProducto).update(cantidad = actualizacionCantidad)

                        else:
                            sinProductos = True

                    elif esPaquete:
                        consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)

                        for datoPromo in consultaPaqueteTratamiento:
                            idTratamiento = datoPromo.tratamiento_id
                            consultaTratamientoProductos = TratamientosProductosGasto.objects.filter(tratamiento_id__id_tratamiento = idTratamiento)

                            if consultaTratamientoProductos:
                                sinProductos = False
                                for producto in consultaTratamientoProductos:
                                    idProducto = producto.producto_gasto_id
                                    cantidadUtilizada = producto.cantidad

                                    consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                                    for dato in consultaProducto:
                                        cantidadActualEnExistencia = dato.cantidad
                                        cuantificable = dato.contenido_cuantificable

                                    if cuantificable == "S":
                                        actualizacionCantidad = cantidadActualEnExistencia - cantidadUtilizada

                                        actualizarProducto = ProductosGasto.objects.filter(id_producto = idProducto).update(cantidad = actualizacionCantidad)

                            else:
                                sinProductos = True
                    
                    #Actualización de cita-tratamiento en caso de que haya
                    consultaCitaEnTablaTratamientoCliente = citasTratamientos.objects.filter(cita_id__id_cita = idCita)
                    if consultaCitaEnTablaTratamientoCliente:
                        for cita in consultaCitaEnTablaTratamientoCliente:
                            idTratamientoCliente = cita.idTratamientoCliente_id
                        
                        consultaTratamientoCliente = TratamientosClientes.objects.filter(id_tratamiento_cliente = idTratamientoCliente)

                        for datoTratamientoCliente in consultaTratamientoCliente:
                            sesionesPendientesActuales = datoTratamientoCliente.sesionesPendientes
                            sesionesCanjeadas = datoTratamientoCliente.sesionesCanjeadas
                        
                        nuevasSesionesPendientes = sesionesPendientesActuales - 1
                        nuevasSesionesCanjeadas = sesionesCanjeadas + 1

                        actualizacionTratamientoCliente = TratamientosClientes.objects.filter(id_tratamiento_cliente = idTratamientoCliente).update(sesionesPendientes = nuevasSesionesPendientes,
                        sesionesCanjeadas = nuevasSesionesCanjeadas)

                        if actualizacionTratamientoCliente:

                            #Registro de historial
                            registroEnHistorialDeTratamiento = HistorialTratamientosClientes(tratamiento_cliente = TratamientosClientes.objects.get(id_tratamiento_cliente = idTratamientoCliente),
                            sesion_efectuada = nuevasSesionesCanjeadas, fecha_efectuado = fechaMovimiento)

                            registroEnHistorialDeTratamiento.save()




                    #IMPRESION DE TICKEEETSSSS
                    #Ultimo id de venta
                    consultaVentas = Ventas.objects.all()
                    ultimoIdVenta = 0
                    for venta in consultaVentas:
                        ultimoIdVenta = venta.id_venta
                        cliente = venta.cliente_id
                        sucursal = venta.sucursal_id

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
                    if cliente == None:
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
                        c.EscribirTexto("CITA #"+str(idCita)+" - VENTA #"+str(ultimoIdVenta)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                        c.EscribirTexto("\n")
                        
                        
                        #Listado de productos 
                        if esServicio:
                            consultaServicio = Servicios.objects.filter(id_servicio =idServTratPaq)
                            for datoServicio in consultaServicio:
                                nombreTratamiento = datoServicio.nombre_servicio
                            
                        elif esTratamiento:
                            consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idServTratPaq)
                            for datoTratamiento in consultaTratamiento:
                                nombreTratamiento = datoTratamiento.nombre_tratamiento

                        elif esPaquete:
                            consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)

                            for datoPromo in consultaPaqueteTratamiento:
                                nombreTratamiento = datoTratamiento.nombre_paquete
                                
                        
                        costototalDecimales = round(float(costoTotalAPagar), 2)
                        costototalDecimales = str(costoTotalAPagar)

                        costoTotalProductoDivididoEnElPunto = costototalDecimales.split(".")
                        longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                        longitudCostoTotal = int(longitudCostoTotal)

                            
                        caracteresProducto = len(nombreTratamiento)

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
                        c.EscribirTexto("1 x "+nombreTratamiento+espaciosTicket+str(costototalDecimales)+"\n")


                        
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
                            totalSinDescuento1 = 100 * float(costoTotalAPagar)
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



                   

                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo
                        
                        mensaje = "\U0001F4C6 CITA VENDIDA \U0001F4C6 \n El cliente "+nombreClienteTicket+" acudió y pago la cita #"+str(idCita)+" el día "+hoyFormato+" a las "+str(horaVenta)+" hrs en la sucursal "+nombreSucursal+"\n Servicio/Tratamiento:\n"+nombreTratamiento
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")

                    return redirect("/ventas/")

                if registroVenta:
                    print("Venta guardada xddd")
                    request.session['ventaAgregada'] = "La venta ha sido agregada satisfactoriamente!"

                    #Actualizar Cita
                    idUltimaVenta = 0
                    consultaVentas = Ventas.objects.all()
                    for venta in consultaVentas:
                        idUltimaVenta = venta.id_venta
                    actualizacionCita = Citas.objects.get(id_cita = idCita)
                    actualizacionCita.estado_cita = "efectuada"
                    actualizacionCita.venta_id = Ventas.objects.get(id_venta = idUltimaVenta)
                    actualizacionCita.save()

                    if esServicio:
                        consultaServiciosProductos = ServiciosProductosGasto.objects.filter(servicio_id__id_servicio =idServTratPaq)
                        if consultaServiciosProductos:
                            sinProductos = False

                            for producto in consultaServiciosProductos:
                                idProducto = producto.producto_gasto_id
                                cantidadUtilizada = producto.cantidad

                                consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                                for dato in consultaProducto:
                                    cantidadActualEnExistencia = dato.cantidad
                                    cuantificable = dato.contenido_cuantificable

                                if cuantificable == "S":
                                    actualizacionCantidad = cantidadActualEnExistencia - cantidadUtilizada

                                    actualizarProducto = ProductosGasto.objects.filter(id_producto = idProducto).update(cantidad = actualizacionCantidad)
                        else:
                            sinProductos = True
                    elif esTratamiento:
                        consultaTratamientoProductos = TratamientosProductosGasto.objects.filter(tratamiento_id__id_tratamiento = idServTratPaq)

                        if consultaTratamientoProductos:
                            sinProductos = False
                            for producto in consultaTratamientoProductos:
                                idProducto = producto.producto_gasto_id
                                cantidadUtilizada = producto.cantidad

                                consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                                for dato in consultaProducto:
                                    cantidadActualEnExistencia = dato.cantidad
                                    cuantificable = dato.contenido_cuantificable

                                if cuantificable == "S":
                                    actualizacionCantidad = cantidadActualEnExistencia - cantidadUtilizada

                                    actualizarProducto = ProductosGasto.objects.filter(id_producto = idProducto).update(cantidad = actualizacionCantidad)

                        else:
                            sinProductos = True

                    elif esPaquete:
                        consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)

                        for datoPromo in consultaPaqueteTratamiento:
                            idTratamiento = datoPromo.tratamiento_id
                            consultaTratamientoProductos = TratamientosProductosGasto.objects.filter(tratamiento_id__id_tratamiento = idTratamiento)

                            if consultaTratamientoProductos:
                                sinProductos = False
                                for producto in consultaTratamientoProductos:
                                    idProducto = producto.producto_gasto_id
                                    cantidadUtilizada = producto.cantidad

                                    consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                                    for dato in consultaProducto:
                                        cantidadActualEnExistencia = dato.cantidad
                                        cuantificable = dato.contenido_cuantificable

                                    if cuantificable == "S":
                                        actualizacionCantidad = cantidadActualEnExistencia - cantidadUtilizada

                                        actualizarProducto = ProductosGasto.objects.filter(id_producto = idProducto).update(cantidad = actualizacionCantidad)

                            else:
                                sinProductos = True
                    
                    if esACredito: #Guardar el registro del crédito

                     
                        ultimoidVenta = 0
                        totalesVentas = Ventas.objects.all()
                        for venta in totalesVentas:
                            ultimoidVenta = venta.id_venta

                        registroCredito = Creditos(fecha_venta_credito = fechaVenta,
                        empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                        cliente = Clientes.objects.get(id_cliente = clienteMandado),
                        concepto_credito = "Venta",
                        descripcion_credito = comentarios,
                        monto_pagar = costoTotalAPagar,
                        monto_pagado = 0,
                        monto_restante = costoTotalAPagar,
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
                        if clienteMandado == "clienteMomentaneo":
                            nombreClienteTicket = "Momentaneo"

                        else:
                            consultaCliente = Clientes.objects.filter(id_cliente = clienteMandado)
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
                            if esServicio:
                                consultaServicio = Servicios.objects.filter(id_servicio =idServTratPaq)
                                for datoServicio in consultaServicio:
                                    nombreTratamiento = datoServicio.nombre_servicio
                                
                            elif esTratamiento:
                                consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idServTratPaq)
                                for datoTratamiento in consultaTratamiento:
                                    nombreTratamiento = datoTratamiento.nombre_tratamiento

                            elif esPaquete:
                                consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)

                                for datoPromo in consultaPaqueteTratamiento:
                                    nombreTratamiento = datoTratamiento.nombre_paquete
                                    
                            
                            costototalDecimales = round(float(costoTotalAPagar), 2)
                            costototalDecimales = str(costoTotalAPagar)

                            costoTotalProductoDivididoEnElPunto = costototalDecimales.split(".")
                            longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                            longitudCostoTotal = int(longitudCostoTotal)

                                
                            caracteresProducto = len(nombreTratamiento)

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
                            c.EscribirTexto("1 x "+nombreTratamiento+espaciosTicket+str(costototalDecimales)+"\n")



                            
                            c.EscribirTexto("\n")
                            c.EscribirTexto("\n")

                            if descuento == "SinDescuento":
                                c.EstablecerTamañoFuente(2, 2)
                                c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                                c.EscribirTexto("TOTAL:  $"+str(costoTotalAPagar)+"\n")
                                costoTotalPagarCredito = costoTotalAPagar
                            else:
                                intDescuento = int(descuento)
                                consultaDescuentos = Descuentos.objects.filter(porcentaje = intDescuento)
                                for datoDescuento in consultaDescuentos:
                                    nombreDescuento = datoDescuento.nombre_descuento
                                    porcentajeDescuento = datoDescuento.porcentaje

                                porcentajePagado = 100 - porcentajeDescuento #85
                                totalSinDescuento1 = 100 * float(costoTotalAPagar)
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
                        try:
                            tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                            botCostabella = telepot.Bot(tokenTelegram)

                            idGrupoTelegram = keysBotCostabella.idGrupo
                            
                            mensaje = "\U0001F4C6 CITA VENDIDA \U0001F4C6 \n El cliente "+nombreClienteTicket+" acudió y pago a crédito la cita #"+str(idCita)+" el día "+hoyFormato+" a las "+str(horaVenta)+" hrs en la sucursal "+nombreSucursal+"\n Servicio/Tratamiento:\n"+nombreTratamiento
                            botCostabella.sendMessage(idGrupoTelegram,mensaje)
                        except:
                            print("An exception occurred")
                    else:
                        #IMPRESION DE TICKEEETSSSS
                        #Ultimo id de venta
                        consultaVentas = Ventas.objects.all()
                        ultimoIdVenta = 0
                        for venta in consultaVentas:
                            ultimoIdVenta = venta.id_venta
                            cliente = venta.cliente_id
                            sucursal = venta.sucursal_id

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
                        if cliente == None:
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
                            c.EscribirTexto("CITA #"+str(idCita)+" - VENTA #"+str(ultimoIdVenta)+"\n")
                            c.EstablecerEnfatizado(False)
                            c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                            c.EstablecerTamañoFuente(1, 1)
                            c.EscribirTexto("\n")
                            c.EscribirTexto(" "+str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                            c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                            c.EscribirTexto("\n")
                            
                            
                            #Listado de productos 
                            if esServicio:
                                consultaServicio = Servicios.objects.filter(id_servicio =idServTratPaq)
                                for datoServicio in consultaServicio:
                                    nombreTratamiento = datoServicio.nombre_servicio
                                
                            elif esTratamiento:
                                consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idServTratPaq)
                                for datoTratamiento in consultaTratamiento:
                                    nombreTratamiento = datoTratamiento.nombre_tratamiento

                            elif esPaquete:
                                consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)

                                for datoPromo in consultaPaqueteTratamiento:
                                    nombreTratamiento = datoTratamiento.nombre_paquete
                                    
                            
                            costototalDecimales = round(float(costoTotalAPagar), 2)
                            costototalDecimales = str(costoTotalAPagar)

                            costoTotalProductoDivididoEnElPunto = costototalDecimales.split(".")
                            longitudCostoTotal = len(str(costoTotalProductoDivididoEnElPunto[0]))
                            longitudCostoTotal = int(longitudCostoTotal)

                                
                            caracteresProducto = len(nombreTratamiento)

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
                            c.EscribirTexto("1 x "+nombreTratamiento+espaciosTicket+str(costototalDecimales)+"\n")


                            
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
                                totalSinDescuento1 = 100 * float(costoTotalAPagar)
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

                        try:
                            tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                            botCostabella = telepot.Bot(tokenTelegram)

                            idGrupoTelegram = keysBotCostabella.idGrupo
                            
                            mensaje = "\U0001F4C6 CITA VENDIDA \U0001F4C6 \n El cliente "+nombreClienteTicket+" acudió y pago la cita #"+str(idCita)+" el día "+hoyFormato+" a las "+str(horaVenta)+" hrs en la sucursal "+nombreSucursal+"\n Servicio/Tratamiento:\n"+nombreTratamiento
                            botCostabella.sendMessage(idGrupoTelegram,mensaje)
                        except:
                            print("An exception occurred")

                        return redirect("/ventas/")

                        

                

                
                


            


        
        
    else:
        return render(request,"1 Login/login.html")


def paquetesPorCliente(request):

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
            sucursalPromos = request.POST["sucursalPromos"]
            datosSucursal = Sucursales.objects.filter(id_sucursal = sucursalPromos)
            for dato in datosSucursal:
                nombreSucursal = dato.nombre

            paquetesActivos = []
            paquetesEfectuados = []

            consultaTratamientos = TratamientosClientes.objects.all()

            for tratamiento in consultaTratamientos:
                
                idTratamientoCliente = tratamiento.id_tratamiento_cliente
                sesiones = tratamiento.num_sesiones
                sesionesPendientes = tratamiento.sesionesPendientes
                sesionesCanjeadas = tratamiento.sesionesCanjeadas
                idCliente = tratamiento.cliente_id
                paqueteTratamiento = tratamiento.paquete_tratamiento_id

                consultaCliente = Clientes.objects.filter(id_cliente = idCliente)
                for datoCliente in consultaCliente:
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoCliente = datoCliente.apellidoPaterno_cliente

                nombreCompletoCliente = nombreCliente + " " + apellidoCliente
                
                consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = paqueteTratamiento)
                for datoPaquete in consultaPaqueteTratamiento:
                    idTratamiento = datoPaquete.tratamiento_id
                    nombrePromo = datoPaquete.nombre_paquete

                    consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)
                    for datoTratamiento in consultaTratamiento:
                        idSucursal = datoTratamiento.sucursal_id
                        codigoTratamiento = datoTratamiento.codigo_tratamiento
                        tipoTratamiento = datoTratamiento.tipo_tratamiento
                        nombreTratamiento = datoTratamiento.nombre_tratamiento
                        costoTratamiento = datoTratamiento.costo_venta_tratamiento

                intIdSucursal = int(idSucursal)
                intSucursalPromos = int(sucursalPromos)


                #ConsultarPagos
                consultaPagoTratamiento = pagosPaquetesTratamientos.objects.filter(id_tratamiento_cliente_id__id_tratamiento_cliente = idTratamientoCliente)
                for datoPago in consultaPagoTratamiento:
                    totalAPagar = datoPago.total_pagar
                    totalAbonado = datoPago.total_abonado
                    totalRestante = datoPago.total_restante
                    estatusPago = datoPago.estatus_pago

                if intIdSucursal == intSucursalPromos:
                    

                    if sesiones == sesionesCanjeadas: #Paquete promoción efectuado
                        paquetesEfectuados.append([idTratamientoCliente, nombrePromo, codigoTratamiento, tipoTratamiento, nombreTratamiento, costoTratamiento,
                        sesiones, sesionesPendientes, sesionesCanjeadas, nombreCompletoCliente, totalAPagar, totalAbonado, totalRestante, estatusPago])
                    else:  #Activo
                        paquetesActivos.append([idTratamientoCliente, nombrePromo, codigoTratamiento, tipoTratamiento, nombreTratamiento, costoTratamiento,
                        sesiones, sesionesPendientes, sesionesCanjeadas, nombreCompletoCliente, totalAPagar, totalAbonado, totalRestante, estatusPago])
                
                
            
                

            return render(request, "22 Citas/paquetesPorCliente/verPaquetesClientes.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta,"tipoUsuario":tipoUsuario, "sucursalPromos":sucursalPromos, "nombreSucursal":nombreSucursal, "paquetesActivos":paquetesActivos, "paquetesEfectuados":paquetesEfectuados, "notificacionCita":notificacionCita})


        else:           
            if tipoUsuario == "esAdmin":
                sucursales = Sucursales.objects.all()
                
                

                return render(request, "22 Citas/paquetesPorCliente/seleccionarSucursalPaqCliente.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})
            else:
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    sucursalEmpleado = datoEmpleado.id_sucursal_id
                sucursales = Sucursales.objects.filter(id_sucursal = sucursalEmpleado)
                
                

                

                return render(request, "22 Citas/paquetesPorCliente/seleccionarSucursalPaqCliente.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta, "sucursales":sucursales,"tipoUsuario":tipoUsuario, "notificacionCita":notificacionCita})
        
    else:
        return render(request,"1 Login/login.html")

def historialTratamientoCliente(request):

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

            idTratamientoCliente = request.POST["idTratamientoCliente"]

            datosView = []

            consultaTratamiento = TratamientosClientes.objects.filter(id_tratamiento_cliente = idTratamientoCliente)

            for datoTratamientoCliente in consultaTratamiento:
                idTratamientoCliente = datoTratamientoCliente.id_tratamiento_cliente
                sesionesPendientes = datoTratamientoCliente.sesionesPendientes
                sesionesCanjeadas = datoTratamientoCliente.sesionesCanjeadas
                idCliente = datoTratamientoCliente.cliente_id
                paqueteTratamiento = datoTratamientoCliente.paquete_tratamiento_id

            #Datos del cliente
            consultaCliente = Clientes.objects.filter(id_cliente = idCliente)
            for datoCliente in consultaCliente:
                nombreCliente = datoCliente.nombre_cliente
                apellidoCliente = datoCliente.apellidoPaterno_cliente

            nombreCompletoCliente = nombreCliente + " "+apellidoCliente

            #Datos de paquete
            consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = paqueteTratamiento)
            for datoPaqueteTratamiento in consultaPaqueteTratamiento:
                sesionesTotales = datoPaqueteTratamiento.numero_sesiones
                nombrePaquete = datoPaqueteTratamiento.nombre_paquete
                precioPaquete = datoPaqueteTratamiento.precio_por_paquete

                idTratamiento = datoPaqueteTratamiento.tratamiento_id

            #Datos de tratamiento
            consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)
            for datoTratamiento in consultaTratamiento:
                codigoTratamiento = datoTratamiento.codigo_tratamiento
                nombreTratamiento = datoTratamiento.nombre_tratamiento
                costoVentaTratamiento = datoTratamiento.costo_venta_tratamiento
                tiempoMaximoTratamiento = datoTratamiento.tiempo_maximo

            #Datos de historial
            consultaHistorialDeCitasTratamientoCliente = HistorialTratamientosClientes.objects.filter(tratamiento_cliente_id__id_tratamiento_cliente = idTratamientoCliente)
            
            arrayHistorial = []
            for cita in consultaHistorialDeCitasTratamientoCliente:
                idHistorial = cita.id_historial_tratamiento
                sesionEfectuada = cita.sesion_efectuada
                fechaEfectuada = cita.fecha_efectuado

                arrayHistorial.append([idHistorial,sesionEfectuada,fechaEfectuada])


            if sesionesPendientes == 0:
                noEfectuada = "efectuada"
            else:
                noEfectuada = "noEfectuada"

            #Datos de pago
            consultaPagoTratamiento = pagosPaquetesTratamientos.objects.filter(id_tratamiento_cliente__id_tratamiento_cliente = idTratamientoCliente)
            for datoPago in consultaPagoTratamiento:
                totalAbonado = datoPago.total_abonado
                totalPendiente = datoPago.total_restante
                estatusPago = datoPago.estatus_pago


            datosView.append([nombrePaquete, sesionesTotales, precioPaquete,nombreCompletoCliente, sesionesPendientes, sesionesCanjeadas,codigoTratamiento,
            nombreTratamiento, costoVentaTratamiento, tiempoMaximoTratamiento, arrayHistorial, noEfectuada, idTratamientoCliente, totalAbonado, totalPendiente, estatusPago])
                


            #Fecha limite para agendar 45 dias despues del día de hoy
            today = date.today()
            fechaLimite = today + timedelta(days=45)
            fechaLimite = fechaLimite.strftime("%Y-%m-%d")

            #citas entre el dia de hoy y la fecha limite
            arregloHoras45Posiciones = []
            arreglo45Fechas = []
            
            contador = 0
            for x in range(45):
                contador = contador + 1
                sinCitasPendientes = True
                if contador == 1:
                    sinCitasPendientes = False
                    consultaCitasDelDia = Citas.objects.filter(fecha_pactada = today, estado_cita = "sinCanjear")
                    fechaHoy = today.strftime("%Y-%m-%d")
                    arreglo45Fechas.append(fechaHoy)
                else:
                    sinCitasPendientes = False
                    nuevoContador = contador - 1
                    fechita = today + timedelta(days=nuevoContador)
                    consultaCitasDelDia = Citas.objects.filter(fecha_pactada = fechita, estado_cita = "sinCanjear")
                    fechaOtroDia = fechita.strftime("%Y-%m-%d")
                    arreglo45Fechas.append(fechaOtroDia)
                
                arregloHoras = ["09:00 AM","10:00 AM","11:00 AM","12:00 PM","13:00 PM","14:00 PM","15:00 PM","16:00 PM","17:00 PM","18:00 PM"]
                for cita in consultaCitasDelDia:
                    horaProgramada = cita.hora_pctada

                    if horaProgramada in arregloHoras:
                        duracion = cita.duracionCitaMinutos
                        if duracion > 60:
                            indiceAQuitar = arregloHoras.index(horaProgramada)
                            indiceAQuitarTambien = indiceAQuitar+1
                            if  indiceAQuitarTambien == 10:
                                arregloHoras.remove(horaProgramada)
                            else:
                                horaTambienAQuitar = arregloHoras[indiceAQuitarTambien]
                                arregloHoras.remove(horaProgramada) 
                                arregloHoras.remove(horaTambienAQuitar) 
                        else:
                            arregloHoras.remove(horaProgramada) 
                    
                arregloHoras45Posiciones.append(arregloHoras)
            

            
            consultaPrimerDia = Citas.objects.filter(fecha_pactada = today, estado_cita = "sinCanjear")
            arregloHoras2 = ["09:00 AM","10:00 AM","11:00 AM","12:00 PM","13:00 PM","14:00 PM","15:00 PM","16:00 PM","17:00 PM","18:00 PM"]
            for cita in consultaPrimerDia:
                horaProgramada = cita.hora_pctada

                if horaProgramada in arregloHoras2:
                    duracion = cita.duracionCitaMinutos

                    if duracion > 60:
                        indiceAQuitar = arregloHoras2.index(horaProgramada)
                        indiceAQuitarTambien = indiceAQuitar+1

                        if  indiceAQuitarTambien == 10:
                            arregloHoras2.remove(horaProgramada)
                        else:

                            horaTambienAQuitar = arregloHoras2[indiceAQuitarTambien]
                            arregloHoras2.remove(horaProgramada) 
                            arregloHoras2.remove(horaTambienAQuitar) 
                    else:
                        arregloHoras2.remove(horaProgramada) 


            listaZipFechaHora = zip(arreglo45Fechas,arregloHoras45Posiciones)


            return render(request, "22 Citas/paquetesPorCliente/historialTratamientoCliente.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                "notificacionRenta":notificacionRenta,"tipoUsuario":tipoUsuario, "datosView":datosView, "listaZipFechaHora":listaZipFechaHora, "fechaLimite":fechaLimite, "sinCitasPendientes":sinCitasPendientes, "arregloHoras2":arregloHoras2, "notificacionCita":notificacionCita})


        
        
    else:
        return render(request,"1 Login/login.html")

def guardarCitaSesion(request):

    if "idSesion" in request.session:

        idEmpleado = request.session['idSesion']

        if request.method == "POST":
            idTratamientoCliente = request.POST['idTratamientoCliente']

            consultaTratamientoCliente = TratamientosClientes.objects.filter(id_tratamiento_cliente = idTratamientoCliente)

            for datoTratamientoCliente in consultaTratamientoCliente:
                cliente = datoTratamientoCliente.cliente_id
                paqueteTratamiento = datoTratamientoCliente.paquete_tratamiento_id
                sesionesCanjeadas = datoTratamientoCliente.sesionesCanjeadas

            proximaCita = int(sesionesCanjeadas) + 1
           

            #Sacar sucursal de tratamiento
            consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = paqueteTratamiento)
            for datoPaqueteTratamiento in consultaPaqueteTratamiento:
                idTratamiento = datoPaqueteTratamiento.tratamiento_id
            
            consultaTratamiento = Tratamientos.objects.filter(id_tratamiento = idTratamiento)
            for datoTratamiento in consultaTratamiento:
                sucursal = datoTratamiento.sucursal_id
                duracionMaxima = datoTratamiento.tiempo_maximo



            empleadoRealizo = idEmpleado

            #seleccion
            paqueteTratamientoSeleccionado = paqueteTratamiento

            tipoDeCita = ""
            idServTratPaq = 0
            duracion = 0


            tipoDeCita = "PaqueteTratamiento"
            idServTratPaq = int(paqueteTratamientoSeleccionado)

            duracion = float(duracionMaxima)
            paqueteTratamiento = True


            fechaPactada = request.POST['fechaAgendar']
            horaCita = request.POST['horarioCita']
            estadoCita = "sinCanjear"
            citaVendida = "No"

            comentarios = "Sesión #"+str(proximaCita)+ " del tratamiento."

            registroCita = Citas(cliente = Clientes.objects.get(id_cliente = cliente),
            sucursal = Sucursales.objects.get(id_sucursal = sucursal),
            empleado_realizo = Empleados.objects.get(id_empleado = empleadoRealizo),
            tipo_cita = tipoDeCita,
            id_serv_trat_paq = idServTratPaq,
            fecha_pactada = fechaPactada,
            hora_pctada = horaCita,
            estado_cita = estadoCita,
            cita_vendida = citaVendida,
            comentarios = comentarios,
            duracionCitaMinutos = duracion)

            registroCita.save()

            if registroCita:
                consultaTratamientosClientes = TratamientosClientes.objects.all()
                for trat in consultaTratamientosClientes:
                    ultimoRegistroTratamientoCliente = trat.id_tratamiento_cliente
                
                consultaCitas = Citas.objects.all()
                for cita in consultaCitas:
                    ultimoRegistroCita = cita.id_cita

                #Guardar cita y tratamiento juntos
                guardarCitaConTratamiento = citasTratamientos(cita = Citas.objects.get(id_cita = ultimoRegistroCita), 
                idTratamientoCliente = TratamientosClientes.objects.get(id_tratamiento_cliente = idTratamientoCliente))
                
                guardarCitaConTratamiento.save()

            
                request.session["citaGuardada"] = "La cita se ha guardado correctamente!"
                return redirect("/agendarCita/")
                        
                        
            else:
                request.session["citaNoGuardada"] = "La cita se ha guardado correctamente!"
                return redirect("/agendarCita/")

            
        
    else:
        return render(request,"1 Login/login.html")

def notificacionCitasDeHoy(request):
    
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
        citas = Citas.objects.filter(fecha_pactada = fechaHoy, estado_cita = "sinCanjear")

        citasNotificacion =[]
        mensajeCitas = ""
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
            elif tipoCita == "Tratamiento":
                consultaTratamiento = Servicios.objects.filter(id_tratamiento = idServTratPaq)
                for datoTratamiento in consultaTratamiento:
                    tipoTratamiento = datoTratamiento.tipo_tratamiento
                    nombreTratamiento = datoTratamiento.nombre_tratamiento
                nombreServicioTratamientoPaqueteCita = tipoTratamiento +" "+nombreTratamiento
            elif tipoCita == "PaqueteTratamiento":
                consultaPaqueteTratamiento = PaquetesPromocionTratamientos.objects.filter(id_paquete_tratamiento = idServTratPaq)
                for datoPromo in consultaPaqueteTratamiento:
                    nombrePaquete = datoPromo.nombre_paquete
                    sesionesPaquete = datoPromo.numero_sesiones
                nombreServicioTratamientoPaqueteCita = nombrePaquete + " "+str(sesionesPaquete)+" sesiones"

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
            

            
            
            horaPactada = cita.hora_pctada
            duracion = cita.duracionCitaMinutos
            duracion = int(duracion)
    
            
            citasNotificacion.append([idCita,nombreSucursal,horaPactada,nombreCompletoCliente,nombreServicioTratamientoPaqueteCita,duracion])  

            contador = 0
            for cita in citasNotificacion:
                idCita = cita[0]
                nombreSucursal = cita[1]
                horaPactada = cita[2]
                nombreCompletoCliente = cita[3]
                nombreServicioTratamientoPaqueteCita = cita[4]
                duracion = cita[5]

                contador = contador + 1
                if contador == 1:
                    mensajeCitas = "\U0001F4C5 Cita #"+str(idCita)+" en "+str(nombreSucursal)+" a "+(nombreCompletoCliente) +" a las "+str(horaPactada)+" - "+str(nombreServicioTratamientoPaqueteCita)+" de "+str(duracion)+" min"
                else:
                    mensajeCitas = mensajeCitas + ", \n"+"\U0001F4C5 Cita #"+str(idCita)+" en "+str(nombreSucursal)+" a "+(nombreCompletoCliente) +" a las "+str(horaPactada)+" - "+str(nombreServicioTratamientoPaqueteCita)+" de "+str(duracion)+" min"
        
        try:
            tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
            botCostabella = telepot.Bot(tokenTelegram)

            idGrupoTelegram = keysBotCostabella.idGrupo
            
            mensaje = "Hola \U0001F44B! \nLa empleada "+nombreEmpleado+" ha generado un aviso de citas del día!.\nEste es el itinerario de hoy:\n"+mensajeCitas
            botCostabella.sendMessage(idGrupoTelegram,mensaje)
        except:
            print("An exception occurred")

        request.session["citasEnviadas"] = "Se ha notificado a los administradores sobre las citas del día!"
        return redirect("/citas/")
        
        
        
              
        
    # Si no hay una sesion iniciada..
    else:
        return render(request, "1 Login/login.html")

def reAgendarCita(request):

    if "idSesion" in request.session:

        if request.method == "POST":

            idCitaReagendar = request.POST["idCitaReagendar"]

            nameFecha = "fechaReagendar"+str(idCitaReagendar)
            fechaReagendar = request.POST[nameFecha]
            nameHorario = "horarioCitaReagendada"+str(idCitaReagendar)
            horarioCitaReagendada = request.POST[nameHorario]

            actualizacionCita = Citas.objects.filter(id_cita = idCitaReagendar).update(fecha_pactada = fechaReagendar, hora_pctada =  horarioCitaReagendada)

            if actualizacionCita:
                request.session["citaReagendada"] = "La cita ha sido reagendada satisfactoriamente!"
                
                consultaCita = Citas.objects.filter(id_cita = idCitaReagendar)
                for datoCita in consultaCita:
                    idCliente = datoCita.cliente_id
                    sucursalCita = datoCita.sucursal_id

                consultaCliente = Clientes.objects.filter(id_cliente = idCliente)
                for datoCliente in consultaCliente:
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoCliente = datoCliente.apellidoPaterno_cliente

                nombreCompletoCliente = nombreCliente + " "+apellidoCliente

                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalCita)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
                try:
                    tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                    botCostabella = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCostabella.idGrupo
                    
                    mensaje = "\U0001F4C6 CITA REAGENDADA \U0001F4C6 \n El cliente "+nombreCompletoCliente+" ha reagendado la cita #"+str(idCitaReagendar)+" al día "+fechaReagendar+" a las "+str(horarioCitaReagendada)+" hrs en la sucursal "+nombreSucursal
                    botCostabella.sendMessage(idGrupoTelegram,mensaje)
                except:
                    print("An exception occurred")


                return redirect("/citas/")

        
    else:
        return render(request,"1 Login/login.html")

def reAgendarCancelarCita(request):

    if "idSesion" in request.session:

        idEmpleado = request.session['idSesion']
        if request.method == "POST":

            idCitaReagendarCancelar = request.POST["idCitaReagendarCancelar"]

            nameJunto = "checkBoxCancelacion"+str(idCitaReagendarCancelar)
            
            if request.POST.get(nameJunto,False): #checkbox chequeado
                quiereCancelar = "Si"
            elif request.POST.get(nameJunto,True): #checkbox deschequeado
                quiereCancelar = "No"
            
            #Comentario venta
            consultaCita = Citas.objects.filter(id_cita = idCitaReagendarCancelar)
            for datoCita in consultaCita:
                idClienteCita = datoCita.cliente_id
                sucursalCita = datoCita.sucursal_id
                
                consultaCliente = Clientes.objects.filter(id_cliente = idClienteCita)
                for datoCliente in consultaCliente:
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoCliente = datoCliente.apellidoPaterno_cliente

            #El comentario cambiaaaaa
            nombreCompletoCliente = nombreCliente +" "+apellidoCliente


            if quiereCancelar == "Si":

                #Cancelar cita.
                cita = Citas.objects.get(id_cita = idCitaReagendarCancelar)
                cita.delete()
                

            elif quiereCancelar == "No":
               #Agendar nueva cita.
                nameFecha = "fechaReagendar"+str(idCitaReagendarCancelar)
                fechaReagendar = request.POST[nameFecha]
                horaReagendada = request.POST["horarioCitaCancelada"]

                actualizacionCita = Citas.objects.filter(id_cita = idCitaReagendarCancelar).update(fecha_pactada = fechaReagendar, hora_pctada =  horaReagendada)
               
            


            #Recibir pago.
            formaDePago = request.POST["tipoPago"]

            esEnEfectivo = False
            esConTarjeta = False
            esConTransferencia = False

            if formaDePago == "Efectivo":
                esEnEfectivo = True
            elif formaDePago == "Tarjeta":
                esConTarjeta = True
                tipoTarjeta = request.POST["tipoTarjeta"]
                referenciaBancaria = request.POST["referenciaBancaria"]
            elif formaDePago == "Transferencia":
                esConTransferencia = True
                claveRastreo = request.POST["claveRastreoTransferencia"]

            
            if quiereCancelar == "Si":

                comentarioVenta = "Pago por cancelación de cita #"+str(idCitaReagendarCancelar)+" para el cliente "+nombreCompletoCliente

            elif quiereCancelar == "No":
                
                comentarioVenta = "Pago por reagendación de cita #"+str(idCitaReagendarCancelar)+" para el cliente "+nombreCompletoCliente

            #Guardar la venta
            fechaVenta = datetime.now() #La fecha con hora
            horaVenta= datetime.now().time()
            vendedor = idEmpleado
            intPago = 200
            floatPago = float(intPago)
            if esEnEfectivo:
                registroVenta = Ventas(fecha_venta = fechaVenta,
                hora_venta = horaVenta, tipo_pago = formaDePago, empleado_vendedor = Empleados.objects.get(id_empleado = vendedor), ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="", cliente = Clientes.objects.get(id_cliente = idClienteCita), monto_pagar = floatPago, credito = "N", comentariosVenta = comentarioVenta, sucursal = Sucursales.objects.get(id_sucursal = sucursalCita))
                registroVenta.save()
                
                #Generar movimiento en Caja
                ultimoIdVenta = 0
                ventasTotalesEfectivo = Ventas.objects.filter(tipo_pago ="Efectivo")
                for venta in ventasTotalesEfectivo:
                    ultimoIdVenta = venta.id_venta
                tipoMovimiento ="IN"
                montoMovimiento = float(200)
                descripcionMovimiento ="Movimiento por venta " + str(ultimoIdVenta) + " ,por cancelación de cita."
                fechaMovimiento = datetime.today().strftime('%Y-%m-%d')
                horaMovimiento = datetime.now().time()
                ingresarCantidadEfectivoAcaja =MovimientosCaja(fecha =fechaMovimiento,hora = horaMovimiento,tipo=tipoMovimiento,monto =montoMovimiento, descripcion=descripcionMovimiento,sucursal =  Sucursales.objects.get(id_sucursal = sucursalCita),
                                                                    realizado_por = Empleados.objects.get(id_empleado = vendedor))
                ingresarCantidadEfectivoAcaja.save()
                

            if esConTarjeta:
                registroVenta = Ventas(fecha_venta = fechaVenta,
                hora_venta = horaVenta, tipo_pago = formaDePago,
                tipo_tarjeta = tipoTarjeta, referencia_pago_tarjeta = referenciaBancaria
                , empleado_vendedor = Empleados.objects.get(id_empleado = vendedor), ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="", cliente = Clientes.objects.get(id_cliente = idClienteCita), monto_pagar = floatPago, credito = "N", comentariosVenta = comentarioVenta, sucursal = Sucursales.objects.get(id_sucursal = sucursalCita))
                registroVenta.save()

            if esConTransferencia:
                registroVenta = Ventas(fecha_venta = fechaVenta,
                hora_venta = horaVenta, tipo_pago = formaDePago,
                clave_rastreo_transferencia = claveRastreo,
                empleado_vendedor = Empleados.objects.get(id_empleado = vendedor), ids_productos = "", cantidades_productos = "",
                                    ids_servicios_corporales ="", cantidades_servicios_corporales ="",
                                    ids_servicios_faciales ="", cantidades_servicios_faciales ="", cliente = Clientes.objects.get(id_cliente = idClienteCita), monto_pagar = floatPago, credito = "N", comentariosVenta = comentarioVenta, sucursal = Sucursales.objects.get(id_sucursal = sucursalCita))
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
                horaVenta = horaVenta.strftime("%H:%M:%S")

                #Empleado vendedor
                consultaEmpleadoVendedor = Empleados.objects.filter(id_empleado = vendedor)
                for datoVendedor in consultaEmpleadoVendedor:
                    nombreEmpleado = datoVendedor.nombres
                    apellidoPatEmpleado = datoVendedor.apellido_paterno

                nombreCompletoEmpleadoVendedor = nombreEmpleado + " "+ apellidoPatEmpleado

                #Datos sucurssal
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalCita)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
                    telefonoSucursal = datoSucursal.telefono
                    direccionSucursal = datoSucursal.direccion

                #DatosCliente
                consultaCliente = Clientes.objects.filter(id_cliente = idClienteCita)
                for datoCliente in consultaCliente:
                    idCienteTicket = datoCliente.id_cliente
                    nombreCliente = datoCliente.nombre_cliente
                    apellidoCliente = datoCliente.apellidoPaterno_cliente

                nombreClienteTicket = nombreCliente + " " + apellidoCliente
                

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
                    c.EscribirTexto(str(hoyFormato)+" - "+str(horaVenta)+" hrs.\n")
                    c.EscribirTexto("Atendida por: "+nombreCompletoEmpleadoVendedor+".\n")
                    c.EscribirTexto("\n")

                    #Listado de productos 
                    #Productos venta
                    
                    longitudCostoTotal = len("200.00")
                    longitudCostoTotal = int(longitudCostoTotal)

                    if quiereCancelar == "Si":
                        nombreProducto = "Cancelación cita" 
                        caracteresProducto = len(nombreProducto)

                    elif quiereCancelar == "No":
                        nombreProducto = "Reagendación cita"

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
                    c.EscribirTexto("1 x "+nombreProducto+espaciosTicket+str("200.00")+"\n")


                    

                    
                    c.EscribirTexto("\n")
                    c.EscribirTexto("\n")
                    
                   
                    c.EscribirTexto("TOTAL PAGADO:  $200.00\n")
                    c.EscribirTexto("\n")
                    c.EstablecerTamañoFuente(2, 2)
                    c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                    if quiereCancelar == "Si":
                        c.EscribirTexto("CITA CANCELADA!\n")

                    elif quiereCancelar == "No":
                        c.EscribirTexto("CITA REAGENDADA!\n")
                    
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("El día: "+str(fechaReagendar)+" a las "+str(horaReagendada)+" hrs. \n")
                    c.EstablecerEnfatizado(True)
                    c.EstablecerTamañoFuente(1, 1)
                    c.EscribirTexto("========== IVA incluido en el precio ==========\n")
                    c.EscribirTexto("\n")
                    c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                    c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                    c.EstablecerEnfatizado(False)
                    c.EscribirTexto("\n")
                    if esEnEfectivo:
                        c.EscribirTexto("Pago en efectivo.\n")
                    elif esConTarjeta:
                        c.EscribirTexto("Pago con "+str(tipoTarjeta)+".\n")
                        c.EscribirTexto("Referencia: "+referenciaBancaria+".\n")
                    elif esConTransferencia:
                        c.EscribirTexto("Transferencia.\n")
                        c.EscribirTexto("Clave de rastreo: "+str(claveRastreo)+".\n")
                    c.EscribirTexto("\n")
                    c.EstablecerEnfatizado(True)
                    c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                    c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACIÓN DE CLIENTE.\n")

                    
                    c.EstablecerEnfatizado(False)
                    c.EscribirTexto("ID:"+str(idCienteTicket)+" - "+nombreClienteTicket+".\n")
                    c.EscribirTexto("=========== Gracias por su pago!! ===========\n")
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
                    print("Imprimiendo...")
                    # Recuerda cambiar por el nombre de tu impresora
                    respuesta = c.imprimirEn("POS80 Printer")
                    if respuesta == True:
                        print("Impresión correcta")
                    else:
                        print(f"Error. El mensaje es: {respuesta}")

                if quiereCancelar == "Si":
                    
                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo
                        
                        mensaje = "\U0001F4C6 CITA CANCELADA \U0001F4C6 \n El cliente "+nombreClienteTicket+" ha cancelado la cita #"+str(idCitaReagendarCancelar)+" en la sucursal "+nombreSucursal
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")

                elif quiereCancelar == "No":
                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo
                        
                        mensaje = "\U0001F4C6 CITA REAGENDADA CON CUOTA \U0001F4C6 \n El cliente "+nombreClienteTicket+" ha reagendado con cuota la cita #"+str(idCitaReagendarCancelar)+" en la sucursal "+nombreSucursal
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")


                request.session['ventaCancelacionCita'] = "La venta por $200 ha sido agregada satisfactoriamente!"

                return redirect("/ventas/")



        
    else:
        return render(request,"1 Login/login.html")
