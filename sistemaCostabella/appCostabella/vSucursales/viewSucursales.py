
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent



# Importacion de modelos
from appCostabella.models import Empleados, Permisos, Sucursales
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)


def altaSucursal(request):

    if "idSesion" in request.session:

        # Variables de sesión
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        idPerfil = idEmpleado
        idConfig = idEmpleado
    
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']

        # Variable para Menu
        estaEnAltaSucursal = True

        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]
        
        #notificacionRentas
        notificacionRenta = notificacionRentas(request)

        #notificacionCitas
        notificacionCita = notificacionCitas(request)

        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)


        # retornar sucrusales
        sucursales = Sucursales.objects.all()
        if request.method == "POST":
            nombreSucursal = request.POST['nombreSucursal']
            telefono = request.POST['telefonoSucursal']
            direccion = request.POST['direccionSucursal']
            latitud = request.POST['latitud']
            longitud = request.POST['longitud']
       

      

            # Si usuario administrador..
     
            altaSucursal = Sucursales(nombre= nombreSucursal,
                direccion=direccion,
                telefono=telefono,
                latitud = latitud,
                longitud = longitud
                ) #Sin sucursal porque Admin
            altaSucursal.save()

            if altaSucursal:
                sucursalAgregado = "La sucursal "+nombreSucursal + " ha sido agregado satisfactoriamente!"
                return render(request, "4 Sucursales/altaSucursal.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaSucursal":estaEnAltaSucursal, "sucursales":sucursales, "sucursalAgregado":sucursalAgregado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
            else:
                sucursalNoAgregada = "Error en la base de datos, intentelo más tarde.."
                return render(request, "4 Sucursales/altaSucursal.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaSucursal":estaEnAltaSucursal, "sucursales":sucursales, "sucursalNoAgregada":sucursalNoAgregada,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})

        return render(request, "4 Sucursales/altaSucursal.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaSucursal":estaEnAltaSucursal, "sucursales":sucursales,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")

def verSucursales(request):

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


        empleadosPorSucursal = []
        
        empleadosTotalesPorSucursal =[]
   
        listaSucursales = Sucursales.objects.all()
        cantidadSucursales = 0
        
       
        
        for sucursal in listaSucursales:
            cantidadSucursales +=1
            id_sucursal_una = sucursal.id_sucursal
            sucursalInt = int(id_sucursal_una)
            
            empleadosEnSucursal = Empleados.objects.filter(id_sucursal_id__id_sucursal = sucursalInt)#filtro de los empleados que esten dentro de un area especifica
            if empleadosEnSucursal:
                empleadosDatos = []
                for datosEmpleado in empleadosEnSucursal:
                    idEmpleadoSucursal = datosEmpleado.id_empleado
                    nombreEmpleadoSucursal = datosEmpleado.nombres
                    apellidoPEmpleadoSucursal = datosEmpleado.apellido_paterno
                    apellidoMEmpleadoSucursal = datosEmpleado.apellido_materno
                    empleadosDatos.append([idEmpleadoSucursal,nombreEmpleadoSucursal,apellidoPEmpleadoSucursal,apellidoMEmpleadoSucursal])
                empleadosTotalesPorSucursal.append(empleadosDatos)
                
                numero_empleados = 0
                for empleado in empleadosEnSucursal:
                    numero_empleados+=1
                
                empleadosPorSucursal.append(numero_empleados)
            else:
                empleadosTotalesPorSucursal.append("Sin empleados")
                empleadosPorSucursal.append(0)

                
                    
        
            
        lista = zip(listaSucursales,empleadosTotalesPorSucursal)
                
                  
       
            
            
        
        
        
        


        return render(request, "4 Sucursales/verSucursales.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "lista":lista, "cantidadSucursales":cantidadSucursales,"notificacionRenta":notificacionRenta,"notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")
