
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent


# Importacion de modelos
from appCostabella.models import (Empleados, Permisos, Sucursales,)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)


def verPanelAdministrativo(request):

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

        #permisos
        tablas_modulos =["Panel administrativo","Empleados","Clientes","Sucursales","Ventas","Descuentos","Configuracion caja", "Movimientos","Movimiento semanal","Rentas","Calendario rentas","Productos",
                                     "Servicios","Paquetes","Creditos","Configuracion credito","Pagos creditos","Compras","Citas","Calendario citas","Codigos de barras", "Tratamientos", "Certificado"]
                    
        
        
        modulos = []
        modulosIconosJS = []
        contadorEmpleados1 = []
        contadorEmpleadosJS = []
        for tabla in tablas_modulos:
            
            consultaPermisosTabla = Permisos.objects.filter(tabla_modulo = tabla)
            
            registrosTabla = []
            contadorEmpleadosEnTabla = 0
            for permiso in consultaPermisosTabla:
                idPermiso = permiso.id_permiso
                idEmpleado = permiso.id_empleado_id
                nombreTabla = permiso.tabla_modulo
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    nombre = datoEmpleado.nombres
                    apellidoPaterno = datoEmpleado.apellido_paterno

                    nombreCompletoEmpleado = nombre + " "+ apellidoPaterno

                    id_sucursal = datoEmpleado.id_sucursal_id

                    if id_sucursal == None:
                        nombreSucursal = "Sin sucursal"
                    else:
                        consultaSucursal = Sucursales.objects.filter(id_sucursal = id_sucursal)
                        for datoSucursal in consultaSucursal:
                            nombreSucursal = datoSucursal.nombre
                    
                ver = permiso.ver
                if ver == "Si":
                    contadorEmpleadosEnTabla = contadorEmpleadosEnTabla + 1
                agregar = permiso.agregar
                editar = permiso.editar
                bloquear = permiso.bloquear
                ver_detalles = permiso.ver_detalles
                activar = permiso.activar
                comprar = permiso.comprar
                recibir_pago = permiso.recibir_pagos

                registrosTabla.append([idPermiso,idEmpleado,nombreCompletoEmpleado,nombreSucursal,ver,agregar,editar,bloquear,ver_detalles,activar,comprar,recibir_pago])

            modulos.append([nombreTabla,registrosTabla])
            modulosIconosJS.append([nombreTabla,registrosTabla])
            contadorEmpleados1.append(contadorEmpleadosEnTabla)
            contadorEmpleadosJS.append(contadorEmpleadosEnTabla)
            
            
        if 'PermisosPanelAdminActualizados' in request.session:
            permisoPanelAdministracion = True
            mensaje =  request.session['PermisosPanelAdminActualizados'] 
            del  request.session['PermisosPanelAdminActualizados'] 
                
            return render(request, "16 Panel administrativo/verPanelAdministrativo.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,
        "notificacionRenta":notificacionRenta, "modulos":modulos, "modulosIconosJS":modulosIconosJS,"permisoPanelAdministracion":permisoPanelAdministracion,"mensaje":mensaje,"consultaPermisos":consultaPermisos, "contadorEmpleados1":contadorEmpleados1,"contadorEmpleadosJS":contadorEmpleadosJS,"notificacionCita":notificacionCita})
        
        if "permisoPanelAdministracionNo" in request.session:
            permisoPanelAdministracionNo = True
            mensaje =  request.session['PermisosPanelAdminActualizados'] 
            del  request.session['permisoPanelAdministracionNo'] 
            return render(request, "16 Panel administrativo/verPanelAdministrativo.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,
        "notificacionRenta":notificacionRenta, "modulos":modulos, "modulosIconosJS":modulosIconosJS,"permisoPanelAdministracionNo":permisoPanelAdministracionNo,"mensaje":mensaje,"consultaPermisos":consultaPermisos, "contadorEmpleados1":contadorEmpleados1,"contadorEmpleadosJS":contadorEmpleadosJS,"notificacionCita":notificacionCita})
               

        
       
        return render(request, "16 Panel administrativo/verPanelAdministrativo.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig,"consultaPermisos":consultaPermisos, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,
        "notificacionRenta":notificacionRenta, "modulos":modulos, "modulosIconosJS":modulosIconosJS, "contadorEmpleados1":contadorEmpleados1, "contadorEmpleadosJS":contadorEmpleadosJS, "notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")
  

def actualizarPermisosPanelAdministraativo(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Panel administrativo")
            for permiso in permisos:
                name = "ver"
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = name + stringIdPermido
                permiso = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permiso = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permiso = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permiso)
            if actualizacionPermiso:
                
                
                
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del panel de administracion satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
            
    else:
        return render(request,"1 Login/login.html")     


def actualizarPermisosEmpleados(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Empleados")
            for permiso in permisos:
                nameVer = "ver"
                nameEditar = "editar"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                nameJuntoEditar = nameEditar + stringIdPermido
                nameJuntoAgregar = nameAgregar + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
                permisoEditar = ""
                if request.POST.get(nameJuntoEditar,False): #checkbox chequeado
                    permisoEditar = "Si"
                elif request.POST.get(nameJuntoEditar,True): #checkbox deschequeado
                    permisoEditar = "No"
                
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, editar = permisoEditar,  agregar= permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Empleados satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")
          
          

def actualizarPermisosClientes(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Clientes")
            for permiso in permisos:
                nameVer = "ver"
                nameEditar = "editar"
                nameAgregar = "agregar"
                nameBloquear = "bloquear"
                nameVerDetalles = "verDetalles"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                nameJuntoEditar = nameEditar + stringIdPermido
                nameJuntoAgregar = nameAgregar + stringIdPermido
                nameJuntoBloquear = nameBloquear + stringIdPermido
                nameJuntoVerDetalles = nameVerDetalles + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
                permisoEditar = ""
                if request.POST.get(nameJuntoEditar,False): #checkbox chequeado
                    permisoEditar = "Si"
                elif request.POST.get(nameJuntoEditar,True): #checkbox deschequeado
                    permisoEditar = "No"
                
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                    
                permisoBloquear = ""
                if request.POST.get(nameJuntoBloquear,False): #checkbox chequeado
                    permisoBloquear = "Si"
                elif request.POST.get(nameJuntoBloquear,True): #checkbox deschequeado
                    permisoBloquear = "No"
                    
                permisoVerDetalles = ""
                if request.POST.get(nameJuntoVerDetalles,False): #checkbox chequeado
                    permisoVerDetalles = "Si"
                elif request.POST.get(nameJuntoVerDetalles,True): #checkbox deschequeado
                    permisoVerDetalles = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, editar = permisoEditar,  agregar= permisoAgregar, bloquear = permisoBloquear, ver_detalles = permisoVerDetalles)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Clientes satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")


def actualizarPermisosSucursales(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Sucursales")
            for permiso in permisos:
                nameVer = "ver"
                nameAgregar = "agregar"
                nameVerDetalles = "verDetalles"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                nameJuntoAgregar = nameAgregar + stringIdPermido
                nameJuntoVerDetalles = nameVerDetalles + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
               
                
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                    
                
                    
                permisoVerDetalles = ""
                if request.POST.get(nameJuntoVerDetalles,False): #checkbox chequeado
                    permisoVerDetalles = "Si"
                elif request.POST.get(nameJuntoVerDetalles,True): #checkbox deschequeado
                    permisoVerDetalles = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, agregar= permisoAgregar, ver_detalles = permisoVerDetalles)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Sucursales satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")

def actualizarPermisosVentas(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Ventas")
            for permiso in permisos:
                nameVer = "ver"
                nameAgregar = "agregar"
                
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                nameJuntoAgregar = nameAgregar + stringIdPermido
               
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
               
                
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                    
                
                    
                
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, agregar= permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Ventas satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")
         
         

def actualizarPermisosDescuentos(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Descuentos")
            for permiso in permisos:
                nameVer = "ver"
                nameEditar = "editar"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                nameJuntoEditar = nameEditar + stringIdPermido
                nameJuntoAgregar = nameAgregar + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
                permisoEditar = ""
                if request.POST.get(nameJuntoEditar,False): #checkbox chequeado
                    permisoEditar = "Si"
                elif request.POST.get(nameJuntoEditar,True): #checkbox deschequeado
                    permisoEditar = "No"
                
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, editar = permisoEditar,  agregar= permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Descuentos satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")

def actualizarPermisosCaja(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Configuracion caja")
            for permiso in permisos:
                nameVer = "ver"
                nameActivar = "activar"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                nameJuntoActivar = nameActivar + stringIdPermido
                nameJuntoAgregar = nameAgregar + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
                permisoActivar = ""
                if request.POST.get(nameJuntoActivar,False): #checkbox chequeado
                    permisoActivar = "Si"
                elif request.POST.get(nameJuntoActivar,True): #checkbox deschequeado
                    permisoActivar = "No"
                
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, activar = permisoActivar,  agregar= permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Configuración Caja satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")
    
def actualizarPermisosMovimientosTotalesCaja(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Movimientos")
            for permiso in permisos:
                nameVer = "ver"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                nameJuntoAgregar = nameAgregar + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
               
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer,  agregar= permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Movimientos de Caja satidfactoriamente"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html") 

def actualizarPermisosMovimientosSemanalCaja(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Movimiento semanal")
            for permiso in permisos:
                nameVer = "ver"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                nameJuntoAgregar = nameAgregar + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
               
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer,  agregar= permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Movimientos Semanales de Caja satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html") 

def actualizarPermisosRentas(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Rentas")
            for permiso in permisos:
                nameVer = "ver"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                nameJuntoAgregar = nameAgregar + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
               
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer,  agregar= permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Rentas satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html") 
          
          
def actualizarPermisosCalendarioRentas(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Calendario rentas")
            for permiso in permisos:
                nameVer = "ver"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
               
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Calendario Rentas satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")   


def actualizarPermisosProductos(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Productos")
            for permiso in permisos:
                nameVer = "ver"
                nameAgregar = "agregar"
                nameEditar = "editar"
                nameComprar = "comprar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                nameJuntoAgregar = nameAgregar + stringIdPermido
                nameJuntoEditar = nameEditar + stringIdPermido
                nameJuntoComprar = nameComprar + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
               
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                    
                permisoEditar = ""
                if request.POST.get(nameJuntoEditar,False): #checkbox chequeado
                    permisoEditar = "Si"
                elif request.POST.get(nameJuntoEditar,True): #checkbox deschequeado
                    permisoEditar = "No"
                    
                    
                permisoComprar = ""
                if request.POST.get(nameJuntoComprar,False): #checkbox chequeado
                    permisoComprar = "Si"
                elif request.POST.get(nameJuntoComprar,True): #checkbox deschequeado
                    permisoComprar = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer,  agregar= permisoAgregar, editar = permisoEditar, comprar = permisoComprar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Productos satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")       
                   

def actualizarPermisosServicios(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Servicios")
            for permiso in permisos:
                nameVer = "ver"
                nameEditar = "editar"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                nameJuntoEditar = nameEditar + stringIdPermido
                nameJuntoAgregar = nameAgregar + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
                permisoEditar = ""
                if request.POST.get(nameJuntoEditar,False): #checkbox chequeado
                    permisoEditar = "Si"
                elif request.POST.get(nameJuntoEditar,True): #checkbox deschequeado
                    permisoEditar = "No"
                
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, editar = permisoEditar,  agregar= permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Servicios satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")   
         
         

def actualizarPermisosPaquetesServicios(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Paquetes")
            for permiso in permisos:
                nameVer = "ver"
                nameEditar = "editar"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                nameJuntoEditar = nameEditar + stringIdPermido
                nameJuntoAgregar = nameAgregar + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
                permisoEditar = ""
                if request.POST.get(nameJuntoEditar,False): #checkbox chequeado
                    permisoEditar = "Si"
                elif request.POST.get(nameJuntoEditar,True): #checkbox deschequeado
                    permisoEditar = "No"
                
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, editar = permisoEditar,  agregar= permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Paquetes de servicios satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")     

def actualizarPermisosCreditos(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Creditos")
            for permiso in permisos:
                nameVer = "ver"
                nameEditar = "editar"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
               
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Créditos satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")     
       
       
       

def actualizarPermisosConfiguracionCreditos(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Configuracion credito")
            for permiso in permisos:
                nameVer = "ver"
                nameActivar = "activar"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                nameJuntoActivar = nameActivar + stringIdPermido
                nameJuntoAgregar = nameAgregar + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
                permisoActivar = ""
                if request.POST.get(nameJuntoActivar,False): #checkbox chequeado
                    permisoActivar = "Si"
                elif request.POST.get(nameJuntoActivar,True): #checkbox deschequeado
                    permisoActivar = "No"
                
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, activar = permisoActivar,  agregar= permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Configuración de Crédito satisfactoriamente!s"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")
          
          
def actualizarPermisosPagosCreditos(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Pagos creditos")
            for permiso in permisos:
                nameVer = "ver"
                nameRecibirPagos = "recibirPagos"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                nameJuntoRecibirPagos = nameRecibirPagos + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
                permisoRecibirPagos = ""
                if request.POST.get(nameJuntoRecibirPagos,False): #checkbox chequeado
                    permisoRecibirPagos = "Si"
                elif request.POST.get(nameJuntoRecibirPagos,True): #checkbox deschequeado
                    permisoRecibirPagos = "No"
                
               
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, recibir_pagos = permisoRecibirPagos)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Pagos de Crédito satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")
    
def actualizarPermisosCompras(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Compras")
            for permiso in permisos:
                nameVer = "ver"
                nameRecibirPagos = "recibirPagos"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
                
               
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Compras satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html") 

def actualizarPermisosCitas(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Citas")
            for permiso in permisos:
                nameVer = "ver"
                nameEditar = "editar"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
                nameJuntoEditar = nameEditar + stringIdPermido
                nameJuntoAgregar = nameAgregar + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
                permisoEditar = ""
                if request.POST.get(nameJuntoEditar,False): #checkbox chequeado
                    permisoEditar = "Si"
                elif request.POST.get(nameJuntoEditar,True): #checkbox deschequeado
                    permisoEditar = "No"
                
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, editar = permisoEditar,  agregar= permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Citas satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")    

def actualizarPermisosCalendarioCitas(request):
    
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Calendario citas")
            for permiso in permisos:
                nameVer = "ver"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
               
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
               
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Calendario Citas satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")  
    
#Listo!!    
def actualizarPermisosCodigoBarras(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Codigos de barras")
            for permiso in permisos:
                nameVer = "ver"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                
               
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
               
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Código de barras satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")  
    
def actualizarPermisosTratamientos(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Tratamientos")
            for permiso in permisos:
                nameVer = "ver"
                nameEditar = "editar"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                
                
                nameJunto = nameVer + stringIdPermido
                nameJuntoEditar = nameEditar + stringIdPermido
                nameJuntoAgregar = nameAgregar + stringIdPermido
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
                permisoEditar = ""
                if request.POST.get(nameJuntoEditar,False): #checkbox chequeado
                    permisoEditar = "Si"
                elif request.POST.get(nameJuntoEditar,True): #checkbox deschequeado
                    permisoEditar = "No"
                
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, editar = permisoEditar,  agregar= permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo Tratamientos satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")  

def actualizarPermisosCertificados(request):
    if "idSesion" in request.session:
     
        if request.method == "POST":
            
            
            permisos = Permisos.objects.filter(tabla_modulo = "Certificado")
            for permiso in permisos:
                nameVer = "ver"
                nameAgregar = "agregar"
                
                idPermiso = permiso.id_permiso
                stringIdPermido = str(idPermiso)
                nameJunto = nameVer + stringIdPermido
                nameJuntoAgregar = nameAgregar + stringIdPermido
                
               
                
                
                permisoVer = ""
                if request.POST.get(nameJunto,False): #checkbox chequeado
                    permisoVer = "Si"
                elif request.POST.get(nameJunto,True): #checkbox deschequeado
                    permisoVer = "No"
                    
                    
                permisoAgregar = ""
                if request.POST.get(nameJuntoAgregar,False): #checkbox chequeado
                    permisoAgregar = "Si"
                elif request.POST.get(nameJuntoAgregar,True): #checkbox deschequeado
                    permisoAgregar = "No"
                    
               
                
                actualizacionPermiso = Permisos.objects.filter(id_permiso = idPermiso).update(ver = permisoVer, agregar = permisoAgregar)
            if actualizacionPermiso:
                request.session['PermisosPanelAdminActualizados'] = "Se han actualizado los permisos del módulo de Certificados de regalos satisfactoriamente!"
                return redirect('/verPanelAdministrativo/')
            else:
                request.session['permisoPanelAdministracionNo'] = "Error en la base de datos! Intente más tarde!"
                return redirect('/verPanelAdministrativo/')
    
    
    else:
        return render(request,"1 Login/login.html")  
