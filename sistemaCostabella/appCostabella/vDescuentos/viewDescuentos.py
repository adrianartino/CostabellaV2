
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

# Librerías de fecha
from datetime import date, datetime, time, timedelta

# Importacion de modelos
from appCostabella.models import (Descuentos, Permisos,)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)


def descuentos(request):

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
        

        descuentos_totales = Descuentos.objects.all()
        descuentos_totales_modal_editar = Descuentos.objects.all()
        
        if "porcentajeActualizado" in request.session:
            porcentajeActualizado = request.session['porcentajeActualizado']
            del request.session['porcentajeActualizado']
          
            return render(request, "12 Descuentos/descuentos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"descuentos_totales":descuentos_totales,"descuentos_totales_modal_editar":descuentos_totales_modal_editar,
                                                                     "porcentajeActualizado":porcentajeActualizado,"notificacionRenta":notificacionRenta,"notificacionCita":notificacionCita
                                                                        
        })

        if "descuentoAgregado" in request.session:
            descuentoAgregado = request.session['descuentoAgregado']
            del request.session['descuentoAgregado']
          
            return render(request, "12 Descuentos/descuentos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"descuentos_totales":descuentos_totales,"descuentos_totales_modal_editar":descuentos_totales_modal_editar,
                                                                     "descuentoAgregado":descuentoAgregado,"notificacionRenta":notificacionRenta,"notificacionCita":notificacionCita
                                                                        
        })
    


            
        return render(request, "12 Descuentos/descuentos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"descuentos_totales":descuentos_totales,"descuentos_totales_modal_editar":descuentos_totales_modal_editar,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
                                                                        
        })
    
    else:
        return render(request,"1 Login/login.html")


def altaDescuentos(request):

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


        if request.method == "POST":
            nombre_descuento = request.POST['nombreDescuento']  #Requerido
            porcentaje = request.POST['porcentajeDescuento']  #Requerido
            descripcion_descuento= request.POST['descripcion']  #Requerido
            fechaAlta = datetime.today().strftime('%Y-%m-%d') #Requerido
            #fechaAlta = datetime.now()
            
    
                
             

            registroDescuento = Descuentos(nombre_descuento = nombre_descuento,
                    porcentaje = porcentaje,
                    fecha_agregado = fechaAlta,
                    descripcion_descuento = descripcion_descuento)
      
   
            registroDescuento.save()
           

            if registroDescuento:
                request.session["descuentoAgregado"] = "El descuento "+nombre_descuento + "ha sido gregado satisfactoriamente!"
                return redirect("/descuentos/")


                    
           
                    

        return render(request, "12 Descuentos/altaDescuentos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")

def actualizarDescuentos(request):

    if "idSesion" in request.session:

        
       

        if request.method == "POST":
            idDescuentoActualizado = request.POST['idDescuentoEditar']
            porcentaje_actualizado = request.POST['porcentajeDescuentoEditar']
            descripcion_actualizado = request.POST['descripcion']
            
            if descripcion_actualizado == "":
                
                actualizarDescuento = Descuentos.objects.filter(id_descuento = idDescuentoActualizado).update(porcentaje=porcentaje_actualizado)
                
                if actualizarDescuento:
                
                    request.session['porcentajeActualizado'] = "El descuento ha sido actualizado con el porcentaje " + porcentaje_actualizado + "%" + " " + "de manera satisfactoria."
                    return redirect('/descuentos/')
                
            else:
                actualizarDescuento = Descuentos.objects.filter(id_descuento = idDescuentoActualizado).update(porcentaje=porcentaje_actualizado,descripcion_descuento=descripcion_actualizado)
                
                if actualizarDescuento:
                
                    request.session['porcentajeActualizado'] = "El descuento ha sido actualizado de manera satisfactoria."
                    return redirect('/descuentos/')
            
        return redirect('/descuentos/')
    else:
        return render(request,"1 Login/login.html")
    
