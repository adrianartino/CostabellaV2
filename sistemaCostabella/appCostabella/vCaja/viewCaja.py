
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
from appCostabella.models import (ConfiguracionCaja, CortesDeCaja, Empleados, MovimientosCaja, Permisos, Sucursales)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)


def configuracionCaja(request):

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
        
        configuracionesTotales = ConfiguracionCaja.objects.all()
        for configuracion in configuracionesTotales:
            id_sucursal = configuracion.sucursal_id
            
            sucursal = Sucursales.objects.filter(id_sucursal = id_sucursal)
            for dato in sucursal:
                nombreSucursal = dato.nombre
            sucursales.append(nombreSucursal)
            
        lista = zip(configuracionesTotales, sucursales)
        
        if 'configuracionAgregada' in request.session:
            configuracionAgregada = request.session['configuracionAgregada']
            del request.session['configuracionAgregada']
            return render(request, "8 Caja/configuracionCaja.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "lista":lista, "configuracionAgregada":configuracionAgregada,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
            })
        
        if 'configuracionNoAgregado' in request.session:
            configuracionNoAgregado = request.session['configuracionNoAgregado']
            del request.session['configuracionNoAgregado']
            return render(request, "8 Caja/configuracionCaja.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "lista":lista, "configuracionNoAgregado":configuracionNoAgregado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
            })

        if 'configuracionActivada' in request.session:
            configuracionActivada = request.session['configuracionActivada']
            del request.session['configuracionActivada']
            return render(request, "8 Caja/configuracionCaja.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "lista":lista, "configuracionActivada":configuracionActivada,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
            })
            
        return render(request, "8 Caja/configuracionCaja.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "lista":lista,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })
    
    else:
        return render(request,"1 Login/login.html")

def agregarConfiguracionCaja(request):

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


        

        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]

        # retornar sucrusales
        sucursales = Sucursales.objects.all()
        if request.method == "POST":
            fondo_caja = request.POST['fondoCaja']  #Requerido
            corte_caja_monto = request.POST['corteCaja']  #Requerido
            fecha_config_caja = datetime.today().strftime('%Y-%m-%d') #Requerido
            sucursal =  request.POST['sucursal']  #Requerido
            #fechaAlta = datetime.now()
            
         
            

            registroConfiguracionCaja = ConfiguracionCaja(fondo = fondo_caja,
                    minimo_corte_caja = corte_caja_monto,
                
                    fecha = fecha_config_caja, 
                   
                    sucursal = Sucursales.objects.get(id_sucursal = sucursal), activo = "N")
               
       

            registroConfiguracionCaja.save()
            
            if registroConfiguracionCaja:
                    request.session['configuracionAgregada'] = "La configuracion de caja de fondo " + fondo_caja +  "con mínimo de corte de caja de " + corte_caja_monto  + " ha sido gregado satisfactoriamente!"

                    return redirect('/configuracionCaja/')
                    
            else:
                    request.session['configuracionNoAgregado'] = "Error en la base de datos, intentelo más tarde!"

                    return redirect('/configuracionCaja/')

            
        return render(request, "8 Caja/agregarConfiguracionCaja.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "sucursales":sucursales,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })
    
    else:
        return render(request,"1 Login/login.html")

def movimientosCaja(request):

    if "idSesion" in request.session:

       # Variables de sesión
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']
        idPerfil = idEmpleado
        idConfig = idEmpleado
       

        
        agregados = []
        sucursalesMovimientos =[]
        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]
        
           #notificacionRentas
        notificacionRenta = notificacionRentas(request)

        #notificacionCitas
        notificacionCita = notificacionCitas(request)

        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)

        
        totalMovimientos= MovimientosCaja.objects.all()
        for movimiento in totalMovimientos:
            id_persona_realizo = movimiento.realizado_por_id
            id_sucursal  = movimiento.sucursal_id
            
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
                sucursalesMovimientos.append(nombreSucursal)
            
        lista = zip(totalMovimientos,agregados,sucursalesMovimientos)
            
            
            
        
            
        return render(request, "8 Caja/movimientosCaja.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "lista":lista,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })
    
    else:
        return render(request,"1 Login/login.html")

def agregarMovimientoCaja(request):

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

        
        
        # Variable para Menu
        estaEnAltaMovimiento = True

        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]

        # retornar sucrusales
        empleados = Empleados.objects.all()
        sucursales = Sucursales.objects.all()
        if request.method == "POST":
            tipo_movimiento = request.POST['tipoMovimiento']  #Requerido
            monto_movimiento = request.POST['montoMovimiento']  #Requerido
            descripcion_movimiento = request.POST['descripcionMov']  #Requerid    
            sucursal = request.POST['sucursal']  #Requerid 
            fecha_movimiento = datetime.today().strftime('%Y-%m-%d') #Requerido
            hora_movimiento =datetime.now().time()
            #fechaAlta = datetime.now()
            
            if tipo_movimiento == "IN":
                movimiento = "Ingreso"
                tipoMovimiento = "Ingreso"
            elif tipo_movimiento == "RE":
                movimiento = "Retiro"
                tipoMovimiento = "Retiro"
            

            registroMovimiento = MovimientosCaja(fecha = fecha_movimiento, hora= hora_movimiento,
                    tipo = tipo_movimiento,
                    monto = monto_movimiento,
                    descripcion = descripcion_movimiento, 
                    sucursal = Sucursales.objects.get(id_sucursal = sucursal),
                   
                    realizado_por = Empleados.objects.get(id_empleado = idEmpleado))
               
       

            registroMovimiento.save()
            
            if registroMovimiento:
                if movimiento == "Retiro":
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                    date = datetime.now()
                    hora = date.time().strftime("%H:%M")
                    
                    idUltimoMovimiento = 0
                    movimientos = MovimientosCaja.objects.all()
                    for movimiento in movimientos:
                        idUltimoMovimiento = movimiento.id_movimiento

                    #Empleado vendedor
                    consultaEmpleadoRetiro = Empleados.objects.filter(id_empleado = idEmpleado)
                    for datoVendedor in consultaEmpleadoRetiro:
                        nombreEmpleado = datoVendedor.nombres
                        apellidoPatEmpleado = datoVendedor.apellido_paterno

                    nombreCompletoEmpleadoRetiro = nombreEmpleado + " "+ apellidoPatEmpleado

                    #Fecha
                    hoy = datetime.now()
                    hoyFormato = hoy.strftime('%Y/%m/%d')

                    

                    #Datos sucurssal
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        telefonoSucursal = datoSucursal.telefono
                        direccionSucursal = datoSucursal.direccion

                #Mensaje por telegram
                    
                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabella
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo
                        
                        mensaje = "Hola \U0001F44B! \nLa empleada "+nombreCompletoEmpleadoRetiro+" ha generado un retiro de efectivo, por un monto de $ "+str(monto_movimiento)+" MXN, en la sucursal de "+nombreSucursal+" a las "+str(hora)+" hrs \U0001F4B5!\nDescripción: "+str(descripcion_movimiento)+"."
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")
                #Impresion de tickets
                    

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
                        c.EscribirTexto("MOVIMIENTO #"+str(idUltimoMovimiento)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(hora)+" hrs.\n")
                        c.EscribirTexto("Realizado por: "+nombreCompletoEmpleadoRetiro+".\n")
                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.EscribirTexto("Retiro de caja por $ "+str(monto_movimiento)+" MXN.\n")
                        c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                        c.EstablecerEnfatizado(False)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "Descripción: "+descripcion_movimiento+"\n")
                        



                        
                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")
                        
                        

                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.EscribirTexto("========= Movimiento realizado =========\n")
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
                        ##c.abrirCajon()
                        c.Pulso(48, 60, 120)
                        print("Imprimiendo...")
                        # Recuerda cambiar por el nombre de tu impresora
                        respuesta = c.imprimirEn("POS80 Printer")
                        if respuesta == True:
                            print("Impresión correcta")
                        else:
                            print(f"Error. El mensaje es: {respuesta}")
                        
                    movimientoAgregado = "El movimiento de tipo  " + str(tipoMovimiento) +  " de monto " + str(monto_movimiento) + " ha sido gregado satisfactoriamente!"

                   

                    



                if movimiento == "Ingreso":
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                    date = datetime.now()
                    hora = date.time().strftime("%H:%M")

                #Impresion de tickets
                    #Fecha
                    hoy = datetime.now()
                    hoyFormato = hoy.strftime('%Y/%m/%d')

                    idUltimoMovimiento = 0
                    movimientos = MovimientosCaja.objects.all()
                    for movimiento in movimientos:
                        idUltimoMovimiento = movimiento.id_movimiento

                    #Empleado vendedor
                    consultaEmpleadoRetiro = Empleados.objects.filter(id_empleado = idEmpleado)
                    for datoVendedor in consultaEmpleadoRetiro:
                        nombreEmpleado = datoVendedor.nombres
                        apellidoPatEmpleado = datoVendedor.apellido_paterno

                    nombreCompletoEmpleadoIngreso = nombreEmpleado + " "+ apellidoPatEmpleado

                    #Datos sucurssal
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        telefonoSucursal = datoSucursal.telefono
                        direccionSucursal = datoSucursal.direccion

                    #Mensaje por telegram
                    
                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabella
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo
                        
                        mensaje = "Hola \U0001F44B! \nLa empleada "+nombreCompletoEmpleadoIngreso+" ha generado un ingreso de efectivo, por un monto de $ "+str(monto_movimiento)+" MXN, en la sucursal de "+nombreSucursal+" a las "+str(hora)+" hrs \U0001F4B5!\nDescripción: "+str(descripcion_movimiento)+"."
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")

                    
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
                        c.EscribirTexto("MOVIMIENTO #"+str(idUltimoMovimiento)+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(" "+str(hoyFormato)+" - "+str(hora)+" hrs.\n")
                        c.EscribirTexto("Realizado por: "+nombreCompletoEmpleadoIngreso+".\n")
                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.EscribirTexto("Ingreso a caja por $ "+str(monto_movimiento)+" MXN.\n")
                        c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                        c.EstablecerEnfatizado(False)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "Descripción: "+descripcion_movimiento+"\n")



                        
                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")
                        
                        

                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1, 1)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.EscribirTexto("========= Movimiento realizado =========\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        if contadorTickets == 1:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA TIENDA.\n")
                        else:
                            c.EscribirTexto("\n")
                            c.EscribirTexto("COPIA EMPLEADO.\n")
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

                       
                    movimientoAgregado = "El movimiento de tipo  " + str(tipoMovimiento) +  " de monto " + str(monto_movimiento) + " ha sido gregado satisfactoriamente!"
                    
                    
                
                
                return render(request, "8 Caja/agregarMovimientoCaja.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado, "idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado, "sucursales":sucursales, "tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaMovimiento":estaEnAltaMovimiento, "empleados":empleados, "movimientoAgregado":movimientoAgregado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
            else:
                movimientoNoAgregado = "Error en la base de datos, intentelo más tarde.."
                return render(request, "8 Caja/agregarMovimientoCaja.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "sucursales":sucursales, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaMovimiento":estaEnAltaMovimiento, "empleados":empleados, "movimientoNoAgregado":movimientoNoAgregado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})

            
        return render(request, "8 Caja/agregarMovimientoCaja.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "empleados":empleados,"sucursales":sucursales,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })
    
    else:
        return render(request,"1 Login/login.html")
   
def activarConfiguracionCaja(request):

    if "idSesion" in request.session:

       if request.method == "POST":
            idConfiguracionCajaAActivar = request.POST['idConfiguracionCaja']

            consultaConfiguracion = ConfiguracionCaja.objects.filter(id_configuracion = idConfiguracionCajaAActivar)


            for dato in consultaConfiguracion:
                idSucursal = dato.sucursal_id

                configuracionesSucursal = ConfiguracionCaja.objects.filter(sucursal_id__id_sucursal = idSucursal)

                configuracionActivaEnSucursal = False #Variable para saber si ya hay o si aun no hay una configuracion Activa..

                for configuracion in configuracionesSucursal:
                    if configuracion.activo == "S":
                        configuracionActivaEnSucursal = True

                if configuracionActivaEnSucursal == False: #Si no hay ninguna configuracion activa actualmente en esa sucursal..
                    actualizacionConfiguracionCaja = ConfiguracionCaja.objects.filter(id_configuracion = idConfiguracionCajaAActivar).update(activo = "S")
                elif configuracionActivaEnSucursal == True:
                    for config in configuracionesSucursal:
                        idConfig = config.id_configuracion
                        ponerComoInactivoConfiguracion = ConfiguracionCaja.objects.filter(id_configuracion = idConfig).update(activo = "N")
                    actualizacionConfiguracionCaja = ConfiguracionCaja.objects.filter(id_configuracion = idConfiguracionCajaAActivar).update(activo = "S")

            if actualizacionConfiguracionCaja:
                request.session['configuracionActivada'] = "La configuración ha sido activada satisfactoriamente!"
                return redirect('/configuracionCaja/')
    else:
        return render(request,"1 Login/login.html")

def seleccionarSucursalMovimientosDia(request):

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
                direccion = dato.direccion
                sucursales.append([idSucursal,nombreSucursal, direccion])

        else:
          
            empleado = Empleados.objects.filter(id_empleado =idEmpleado)
            for sucursal in empleado:
                idSucursal =sucursal.id_sucursal_id
                
            datoSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
            for dato in datoSucursal:
                nombreSucursal = dato.nombre
                direccion = dato.direccion
            sucursales.append([idSucursal, nombreSucursal, direccion])
        
        datosVendedor = Empleados.objects.filter(id_empleado =idEmpleado )
        
        if "corteRealizado" in request.session:
            corteRealizado = request.session["corteRealizado"]
            del request.session["corteRealizado"]
            return render(request, "8 Caja/seleccionarSucursalMovimientosDia.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "sucursales":sucursales,
                                                                            "datosVendedor":datosVendedor,"notificacionRenta":notificacionRenta,"notificacionCita":notificacionCita, "corteRealizado":corteRealizado})
        if "sinConfiguracionDeCaja" in request.session:

            sinConfiguracionDeCaja = request.session["sinConfiguracionDeCaja"]
            del request.session["sinConfiguracionDeCaja"]

            return render(request, "8 Caja/seleccionarSucursalMovimientosDia.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "sucursales":sucursales,
                                                                            "datosVendedor":datosVendedor,"notificacionRenta":notificacionRenta,"notificacionCita":notificacionCita, "sinConfiguracionDeCaja":sinConfiguracionDeCaja})
        return render(request, "8 Caja/seleccionarSucursalMovimientosDia.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "sucursales":sucursales,
                                                                            "datosVendedor":datosVendedor,"notificacionRenta":notificacionRenta,"notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")
 
def verSucursalMovimientosDia(request):
    
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
        
            
            agregados = []
            
            sucursal = request.POST['sucursal'] #Requerido
            fechaActual = datetime.today().strftime('%Y-%m-%d') #Requerido
            diaActual = datetime.today().isoweekday() #4 jueves
            print(diaActual)
            print(fechaActual)
            intdiaActual = int(diaActual)
            diaLunes = intdiaActual-1 #3 dias para el lunes
            print(diaLunes)
            diaSabado = 6-intdiaActual # 2 dias para el sabado
            print(diaSabado)
            fechaLunes = datetime.now()-timedelta(days =diaLunes)
            fechaSabado = datetime.now() + timedelta(days =diaSabado)
            
            consultaCortesDeCaja = CortesDeCaja.objects.all()

            if consultaCortesDeCaja:
                for corte in consultaCortesDeCaja:
                    fechaDelUltimoCorteDeCaja = corte.fecha_corte
                
                totalMovimientosPorSucursal= MovimientosCaja.objects.filter(sucursal_id__id_sucursal = sucursal, fecha__range=[fechaDelUltimoCorteDeCaja,fechaDelUltimoCorteDeCaja]) 
            else: #No se ha hecho ningún corte de caja aún
                totalMovimientosPorSucursal= MovimientosCaja.objects.filter(sucursal_id__id_sucursal = sucursal) #, fecha__range=[fechaLunes,fechaSabado]
            totalIngresosEfectivoVenta = 0
            totalIngresosEfectivo = 0
            totalRetirosEfectivo = 0
            totalEnCaja = 0
            contadorIngresosEfectivoVenta = 0
            contadorIngresosEfectivo = 0
            contadorRetirosEfectivo = 0
            
            for movimiento in totalMovimientosPorSucursal:
                id_persona_realizo = movimiento.realizado_por_id
                monto = movimiento.monto
               
                
                empleado = Empleados.objects.filter(id_empleado = id_persona_realizo)
                for dato in empleado:
                    nombre = dato.nombres
                    apellidoPat = dato.apellido_paterno
                    apellidoMat = dato.apellido_materno
                nombreCompleto = nombre + " " + apellidoPat + " " + apellidoMat
                agregados.append(nombreCompleto)
                
                if movimiento.tipo == "IN":
                    descripcion = movimiento.descripcion
                    if "venta" in descripcion:
                        totalIngresosEfectivoVenta = totalIngresosEfectivoVenta + monto
                        contadorIngresosEfectivoVenta = contadorIngresosEfectivoVenta +1
                    else:
                        totalIngresosEfectivo = totalIngresosEfectivo + monto
                        contadorIngresosEfectivo = contadorIngresosEfectivo +1
                        
                elif movimiento.tipo== "RE":
                    totalRetirosEfectivo = totalRetirosEfectivo + monto
                    contadorRetirosEfectivo = contadorRetirosEfectivo + 1
             
            totalIngresos = totalIngresosEfectivoVenta + totalIngresosEfectivo 
            totalEnCaja = totalIngresos - totalRetirosEfectivo
            totalContadorIngresos = contadorIngresosEfectivoVenta + contadorIngresosEfectivo
            
            lista = zip(totalMovimientosPorSucursal,agregados)
            
            botonCortedeCajaBloqueado = True

            consultaConfiguracionCaja= ConfiguracionCaja.objects.filter(sucursal_id__id_sucursal = sucursal, activo="S")
            if consultaConfiguracionCaja:
                hayConfiguracion = "Si hay"
                for datoConfigCaja in consultaConfiguracionCaja:
                    fondoCaja = datoConfigCaja.fondo
                    minimoCorte = datoConfigCaja.minimo_corte_caja
                    minimoCorte = float(minimoCorte)
            else:
                hayConfiguracion = "No hay configuración de caja aún."

            
                
            corteMenorQueElMinimo = True
            
            
            horaMovimiento =datetime.now().time() #"15:49"
            print(horaMovimiento)
            strHoraMovimiento = str(horaMovimiento)
            if intdiaActual == 6:  #Aqui debe ser 6
                #Es sabado

                separacionHoraMinutos = strHoraMovimiento.split(":") #[15,49]
                hora = separacionHoraMinutos[0]  #15
                minutos = separacionHoraMinutos[1]  #49

               
                horaInt = int(hora)

                if horaInt >= 13: #Aqui debe ser 13
                    if totalEnCaja > minimoCorte:
                        corteMenorQueElMinimo = False
                        botonCortedeCajaBloqueado = False
                    else:
                        corteMenorQueElMinimo = True
                        botonCortedeCajaBloqueado = True
                    
                    
                else:
                    botonCortedeCajaBloqueado = True
                    corteMenorQueElMinimo = False

                
            else:
                botonCortedeCajaBloqueado = True
                corteMenorQueElMinimo = False


            
            
            
            
        
        
        if hayConfiguracion == "Si hay":


            return render(request, "8 Caja/verSucursalMovimientosDia.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "lista":lista,
                                                                            "totalIngresos":totalIngresos,"totalEnCaja":totalEnCaja,"totalContadorIngresos":totalContadorIngresos,"totalIngresosEfectivoVenta":totalIngresosEfectivoVenta,"totalIngresosEfectivo":totalIngresosEfectivo,
                                                                            "totalRetirosEfectivo":totalRetirosEfectivo,"contadorIngresosEfectivoVenta":contadorIngresosEfectivoVenta,"contadorIngresosEfectivo":contadorIngresosEfectivo,"contadorRetirosEfectivo":contadorRetirosEfectivo, "botonCortedeCajaBloqueado":botonCortedeCajaBloqueado,
                                                                            "fondoCaja":fondoCaja, "corteMenorQueElMinimo":corteMenorQueElMinimo, "minimoCorte":minimoCorte, "notificacionCita":notificacionCita, "sucursal":sucursal
                                                                            
                                                                            
            })
        else:
            request.session["sinConfiguracionDeCaja"] = "Aún no se ha configurado la caja chica ni el fondo de caja!!"
            return redirect("/seleccionarSucursalMovimientosDia/")

    
    else:
        return render(request,"1 Login/login.html")
    

def seleccionarSucursalCortesDeCaja(request):

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
                direccion = dato.direccion
                sucursales.append([idSucursal,nombreSucursal, direccion])

        else:
          
            empleado = Empleados.objects.filter(id_empleado =idEmpleado)
            for sucursal in empleado:
                idSucursal =sucursal.id_sucursal_id
                
            datoSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
            for dato in datoSucursal:
                nombreSucursal = dato.nombre
                direccion = dato.direccion
            sucursales.append([idSucursal, nombreSucursal, direccion])
        
        datosVendedor = Empleados.objects.filter(id_empleado =idEmpleado )
        
        if "corteRealizado" in request.session:
            corteRealizado = request.session["corteRealizado"]
            del request.session["corteRealizado"]
            return render(request, "8 Caja/seleccionarSucursalCortesDeCaja.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "sucursales":sucursales,
                                                                            "datosVendedor":datosVendedor,"notificacionRenta":notificacionRenta,"notificacionCita":notificacionCita, "corteRealizado":corteRealizado})

        return render(request, "8 Caja/seleccionarSucursalCortesDeCaja.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "sucursales":sucursales,
                                                                            "datosVendedor":datosVendedor,"notificacionRenta":notificacionRenta,"notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")
    
def cortesDeCaja(request):

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

            idSucursal = request.POST["sucursal"]


            consultaSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
            for datosSucursal in consultaSucursal:
                nombreSucursal = datosSucursal.nombre

            arregloNombresDeEmpleados = []
            consultaCortesDeCaja = CortesDeCaja.objects.filter(sucursal_id__id_sucursal = idSucursal)
            for corteCaja in consultaCortesDeCaja:
                idEmpleado = corteCaja.empleado_corte_id

                consultaEmpleadoCorteDeCaja = Empleados.objects.filter(id_empleado = idEmpleado)

                for fila in consultaEmpleadoCorteDeCaja:
                    nombresEmpleado = fila.nombres
                    apellidoPaterno = fila.apellido_paterno
                nombreCompletoEmpleado = nombresEmpleado + " " + apellidoPaterno
                arregloNombresDeEmpleados.append(nombreCompletoEmpleado)
            





            listaZipeada = zip(consultaCortesDeCaja,arregloNombresDeEmpleados)


                

            return render(request, "8 Caja/cortesDeCaja.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "notificacionRenta":notificacionRenta,"idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "notificacionCita":notificacionCita, "nombreSucursal":nombreSucursal,
            "listaZipeada":listaZipeada})
    
    else:
        return render(request,"1 Login/login.html")
    
def realizarCorteDeCaja(request):

    if "idSesion" in request.session:

       # Variables de sesión
        idEmpleado = request.session['idSesion']
        
        
        if request.method == "POST":
            
            idSucursal = request.POST["idSucursal"]
            ingresosPorVenta = request.POST["ingresosPorVenta"]
            ingresosManuales = request.POST["ingresosManuales"]
            retirosManuales = request.POST["retirosManuales"]
            montoTotalCorte = request.POST["montoTotalCorte"]

            ingresosPorVenta = float(ingresosPorVenta)
            ingresosManuales = float(ingresosManuales)
            retirosManuales = float(retirosManuales)
            montoTotalCorte = float(montoTotalCorte)
            
            fechaActual = datetime.today().strftime('%Y-%m-%d') #Requerido
            date = datetime.now()
            
            horaCorte = date.time().strftime("%H:%M") #"15:49"

            registroCorteDeCaja = CortesDeCaja(sucursal = Sucursales.objects.get(id_sucursal = idSucursal),
            fecha_corte = fechaActual, hora_corte = horaCorte, monto_ingresos_venta = ingresosPorVenta,
            monto_ingresos_manuales = ingresosManuales,
            monto_retiros_manuales = retirosManuales,
            monto_total_corte = montoTotalCorte,
            empleado_corte = Empleados.objects.get(id_empleado = idEmpleado))

            registroCorteDeCaja.save()

            if registroCorteDeCaja:
                
                #Consulta sucursal
                consultaSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
                    telefonoSucursal = datoSucursal.telefono
                    direccionSucursal = datoSucursal.direccion

                #Consulta empleado
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    nombreEmpleado = datoEmpleado.nombres
                    apellidoEmpleado = datoEmpleado.apellido_paterno

                nombreCompletoEmpleadoCorte = nombreEmpleado + " "+apellidoEmpleado
                
                #ULTIMO CORTE
                idUltimoCorte = 0
                cortesDeCajaTotales = CortesDeCaja.objects.all()
                for corte in cortesDeCajaTotales:
                    idUltimoCorte = corte.id_corte_caja

                try:
                    tokenTelegram = keysBotCostabella.tokenBotCostabella
                    botCostabella = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCostabella.idGrupo
                    
                    mensaje = "Hola \U0001F44B! \nLa empleada "+nombreCompletoEmpleadoCorte+" ha generado un corte de caja, por un monto de $ "+str(montoTotalCorte)+" MXN, en la sucursal de "+nombreSucursal+" a las "+str(horaCorte)+" hrs \U0001F9FE!\n"
                    botCostabella.sendMessage(idGrupoTelegram,mensaje)
                except:
                    print("An exception occurred")
                #Impresion de tickets
                    

                    

                    

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
                    c.EscribirTexto("CORTE DE CAJA #"+str(idUltimoCorte)+"\n")
                    c.EstablecerEnfatizado(False)
                    c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                    c.EstablecerTamañoFuente(1, 1)
                    c.EscribirTexto("\n")
                    c.EscribirTexto(" "+str(fechaActual)+" - "+str(horaCorte)+" hrs.\n")
                    c.EscribirTexto("Realizado por: "+nombreCompletoEmpleadoCorte+".\n")
                    c.EscribirTexto("\n")
                    c.EscribirTexto("\n")
                    c.EstablecerEnfatizado(True)
                    c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                    c.EscribirTexto("Total ingresos por ventas $ "+str(ingresosPorVenta)+" MXN.\n")
                    c.EscribirTexto("\n")
                    c.EscribirTexto("Total ingresos manuales $ "+str(ingresosManuales)+" MXN.\n")
                    c.EscribirTexto("\n")
                    c.EscribirTexto("Total retiros manuales $ "+str(retirosManuales)+" MXN.\n")
                    c.EscribirTexto("\n")
                    c.EscribirTexto("Total en caja $ "+str(montoTotalCorte)+" MXN.\n")
                    c.EscribirTexto("\n")
                    c.EscribirTexto("Sucursal: "+nombreSucursal+"\n")
                    c.EstablecerEnfatizado(False)
                    



                    
                    c.EscribirTexto("\n")
                    c.EscribirTexto("\n")
                    
                    

                    c.EscribirTexto("\n")
                    c.EstablecerEnfatizado(True)
                    c.EstablecerTamañoFuente(1, 1)
                    c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                    c.EscribirTexto("======== Corte de caja realizado =======\n")
                    c.EstablecerTamañoFuente(2, 2)
                    c.EstablecerEnfatizado(True)
                    c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                    if contadorTickets == 1:
                        c.EscribirTexto("\n")
                        c.EscribirTexto("COPIA TIENDA.\n")
                    else:
                        c.EscribirTexto("\n")
                        c.EscribirTexto("COPIA TRABAJADOR.\n")
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








                request.session["corteRealizado"] = "El corte de caja se afectuado adecuadamente!!"
                return redirect("/seleccionarSucursalMovimientosDia/")
    else:
        return render(request,"1 Login/login.html")
