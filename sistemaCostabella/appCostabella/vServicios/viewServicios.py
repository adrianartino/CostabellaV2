
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

import json

# Importacion de modelos
from appCostabella.models import (Empleados,  Permisos,
                                  ProductosGasto,
                                  ProductosVenta, Servicios,
                                  ServiciosProductosGasto, Sucursales)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)

def altaServicios(request):

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
        

        # retornar sucrusales
        sucursales = Sucursales.objects.all()
        if request.method == "POST":
            
            tipo_Servicio = request.POST['tipoServicio']  #Requerido
            nombre_Servicio = request.POST['nombreServicio']  #Requerido
            
            
            descripcion_servicio = request.POST['descripcion']  #Requerido
            costo_servicio = request.POST['costoServicio']  #Requerido
            tiempo_minimo = request.POST['tiempoMinimo']  #Requerido
            tiempo_maximo= request.POST['tiempoMaximo']  #Requerido
            complementos= request.POST['complementos']  #Requerido
            
            listaSucursales = request.POST.getlist('sucursales')
            #fechaAlta = datetime.now()
            if tipo_Servicio == "Corporal":
                tipo = "Corporales"
            elif tipo_Servicio == "Facial":
                tipo= "Faciales"
         
            
            if "Todas" in listaSucursales:
                #El servicio se dara de alta en todas las sucursales
                sucursales = Sucursales.objects.all()
                for sucursal in sucursales:
                    idSucursal = sucursal.id_sucursal
                    registroServicio = Servicios(tipo_servicio = tipo_Servicio,
                    nombre_servicio = nombre_Servicio,
                    descripcion_servicio = descripcion_servicio, 
                    tiempo_minimo = tiempo_minimo, 
                    tiempo_maximo = tiempo_maximo, 
                    precio_venta = costo_servicio, 
                    complementos_servicio=complementos,
                    sucursal = Sucursales.objects.get(id_sucursal = idSucursal))

                    registroServicio.save()
            else:
                for sucursal in listaSucursales:
                    idSucursal = int(sucursal)
                    registroServicio = Servicios(tipo_servicio = tipo_Servicio,
                    nombre_servicio = nombre_Servicio,
                    descripcion_servicio = descripcion_servicio, 
                    tiempo_minimo = tiempo_minimo, 
                    tiempo_maximo = tiempo_maximo, 
                    precio_venta = costo_servicio, 
                    complementos_servicio=complementos,
                    sucursal = Sucursales.objects.get(id_sucursal = idSucursal))
                    registroServicio.save()


            if registroServicio:
                    servicioAgregado = "El servicio " + nombre_Servicio +  "  de tipo " + tipo  + "  ha sido gregado satisfactoriamente!"
                    return render(request, "10 Servicios/altaServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado, "idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "sucursales":sucursales, "servicioAgregado":servicioAgregado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
            else:
                    servicioNoAgregado = "Error en la base de datos, intentelo más tarde.."
                    return render(request, "10 Servicios/altaServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "sucursales":sucursales, "servicioNoAgregado":servicioNoAgregado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})

            
        return render(request, "10 Servicios/altaServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "sucursales":sucursales,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })
    
    else:
        return render(request,"1 Login/login.html")
    
def inventarioServicios(request):

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

            sucursalServicios = request.POST['sucursalServicios']

            

            # Arreglo para tabla y modal editar
            sucursales = []
            sucursalesE = []

            if sucursalServicios == "todasLasSucursales":
                nombreSucursalServicios = "Todas las sucursales"
                
            else:
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalServicios)

                for datoSucursal in consultaSucursal:
                    nombreSucursalServicios = datoSucursal.nombre
                



            #------------servicios tipo corporales -------------
            productosVentasSucursalCoorporal = []
            productosGastoSucursalCoorporal = []

            yaTienePaqueteCorporal = []
            paqueteDeProductosServiciosCorporales = []
            if sucursalServicios == "todasLasSucursales":
                serviciosCorporales = Servicios.objects.filter(tipo_servicio ="Corporal")
            else:
                serviciosCorporales = Servicios.objects.filter(tipo_servicio ="Corporal", sucursal_id__id_sucursal = sucursalServicios)

                

            for servicio in serviciosCorporales:
                
                arregloProductosVentaSucursal = []
                arregloProductosGastoSucursal = []

                id_sucursal = servicio.sucursal_id
                
                sucursal = Sucursales.objects.filter(id_sucursal = id_sucursal)
                for dato in sucursal:
                    idSucursal = dato.id_sucursal
                    nombreSucursal = dato.nombre
                sucursales.append(nombreSucursal)
                sucursalesE.append([idSucursal,nombreSucursal])
                
                #Verificar si ya tiene un paquete
                idServicio = servicio.id_servicio
                servicioCorporalYaTienePaquete = False
                paquetesServicios = ServiciosProductosGasto.objects.all()
                productosServicio = []
                for productoUtilizado in paquetesServicios:
                    servicioUtilizado = productoUtilizado.servicio_id
                    
                    if servicioUtilizado == idServicio:
                        servicioCorporalYaTienePaquete = True
                        
                        #Ya tiene productos asignados... Sacar todos los productos y mandarlos a un arreglo de ese servicio.
                        idProductoGastoUtilizado = productoUtilizado.producto_gasto_id
                        cantidadUtilizada = productoUtilizado.cantidad
                        datosProducto = ProductosGasto.objects.filter(id_producto = idProductoGastoUtilizado)
                        for dato in datosProducto:
                            codigo = dato.codigo_producto
                            idProducto = dato.id_producto
                            sku = dato.sku_producto
                            nombre = dato.nombre_producto
                            cantidad_existencias = dato.cantidad
                            
                        productosServicio.append([idProducto,codigo,sku,nombre,cantidadUtilizada,cantidad_existencias])
                    
                if servicioCorporalYaTienePaquete:
                    paqueteDeProductosServiciosCorporales.append(productosServicio)
                else:
                    paqueteDeProductosServiciosCorporales.append("nada")
                
                    
                
                        
                        
                        
                    
                yaTienePaqueteCorporal.append(servicioCorporalYaTienePaquete)

                #Productos para venta sucursal
                productosVentas = ProductosVenta.objects.filter(sucursal = idSucursal)
                for productoV in productosVentas:
                    idPventa = productoV.id_producto
                    codigoPventa = productoV.codigo_producto
                    nombrePventa = productoV.nombre_producto
                    arregloProductosVentaSucursal.append([idPventa,codigoPventa,nombrePventa])

                productosVentasSucursalCoorporal.append(arregloProductosVentaSucursal)

                #Productos gasto sucursal
                productosGastos = ProductosGasto.objects.filter(sucursal = idSucursal)
                for productoG in productosGastos:
                    idPgasto = productoG.id_producto
                    codigoPgasto = productoG.codigo_producto
                    nombrePgasto = productoG.nombre_producto
                    arregloProductosGastoSucursal.append([idPgasto,codigoPgasto,nombrePgasto]) 
                productosGastoSucursalCoorporal.append(arregloProductosGastoSucursal)
                
                
                
                
            listaCorporales = zip(serviciosCorporales, sucursales, yaTienePaqueteCorporal, paqueteDeProductosServiciosCorporales)
            listaCorporales2 = zip(serviciosCorporales, sucursales, yaTienePaqueteCorporal, paqueteDeProductosServiciosCorporales)
            listaCorporalesEditar = zip(serviciosCorporales, sucursalesE)
            listaCorporalesProductosVenta = zip(serviciosCorporales, productosVentasSucursalCoorporal,productosGastoSucursalCoorporal)
            
            sucursalesTotalesEditat=[]
            sucursalesTotales = Sucursales.objects.all()
            for suc in sucursalesTotales:
                idSucTotal = suc.id_sucursal
                nombreSucTotal = suc.nombre
                sucursalesTotalesEditat.append([idSucTotal,nombreSucTotal])
            
            #sucursalesTotalesEditat.pop(idSucursal -1)
            
            
            
            
            #---paquetes de servicio
            
            
            
            
        
            
        
            
        
            
            
            
            
            #------------servicios tipo faciales -------------
            yaTienePaqueteFacial = []
            paqueteDeProductosServiciosFaciales = []
            if sucursalServicios == "todasLasSucursales":
                serviciosFaciales = Servicios.objects.filter(tipo_servicio ="Facial")
            else:
                serviciosFaciales = Servicios.objects.filter(tipo_servicio ="Facial", sucursal_id__id_sucursal = sucursalServicios)
            for servicio in serviciosFaciales:
                id_sucursal = servicio.sucursal_id
                
                sucursal = Sucursales.objects.filter(id_sucursal = id_sucursal)
                for dato in sucursal:
                    idSucursalF = dato.id_sucursal
                    nombreSucursalF = dato.nombre
                sucursales.append(nombreSucursalF)
                sucursalesE.append([idSucursalF,nombreSucursalF])
                
                #Verificar si ya tiene un paquete
                idServicio = servicio.id_servicio
                servicioFacialYaTienePaquete = False
                paquetesServicios = ServiciosProductosGasto.objects.all()
                
                productosServicioFacial = []
                for productoUtilizado in paquetesServicios:
                    servicioUtilizado = productoUtilizado.servicio_id
                    
                    if servicioUtilizado == idServicio:
                        servicioFacialYaTienePaquete = True
                        #Ya tiene productos asignados... Sacar todos los productos y mandarlos a un arreglo de ese servicio.asdfasdfasdfasdfadsfasdf
                        idProductoGastoUtilizado = productoUtilizado.producto_gasto_id
                        cantidadUtilizada = productoUtilizado.cantidad
                        datosProducto = ProductosGasto.objects.filter(id_producto = idProductoGastoUtilizado)
                        for dato in datosProducto:
                            codigo = dato.codigo_producto
                            idProducto = dato.id_producto
                            sku = dato.sku_producto
                            nombre = dato.nombre_producto
                            cantidad_existencias = dato.cantidad
                            
                        productosServicioFacial.append([idProducto,codigo,sku,nombre,cantidadUtilizada,cantidad_existencias])
                    
                if servicioFacialYaTienePaquete:
                    paqueteDeProductosServiciosFaciales.append(productosServicioFacial)
                else:
                    paqueteDeProductosServiciosFaciales.append("nada")
                    
                #alsdkfjnlaksdjfkljaslkdfjlajsdklfkajsdfklalfjdlajfdlkj
                
                        
                yaTienePaqueteFacial.append(servicioFacialYaTienePaquete)
                
                
            listaFaciales = zip(serviciosFaciales, sucursales, yaTienePaqueteFacial, paqueteDeProductosServiciosFaciales)
            listaFaciales2 = zip(serviciosFaciales, sucursales, yaTienePaqueteFacial, paqueteDeProductosServiciosFaciales)
            listaFacialesEditar = zip(serviciosFaciales, sucursalesE)
            
            return render(request, "10 Servicios/inventarioServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                         "listaCorporales":listaCorporales,"listaFaciales":listaFaciales,"listaCorporalesEditar":listaCorporalesEditar,
                                                                         "listaFacialesEditar":listaFacialesEditar,"serviciosCorporales":serviciosCorporales,
                                                                        "listaCorporalesProductosVenta":listaCorporalesProductosVenta,"notificacionRenta":notificacionRenta, "listaCorporales2":listaCorporales2, "listaFaciales2":listaFaciales2, "notificacionCita":notificacionCita, "nombreSucursalServicios":nombreSucursalServicios
            })
        #Else seleccionar sucursal
        else:
            if tipoUsuario == "esAdmin":
                sucursales = Sucursales.objects.all()

                if "servicioCorporalActualizado" in request.session:
                    servicioCorporalActualizado = request.session['servicioCorporalActualizado']
                    del request.session['servicioCorporalActualizado']
                
                    return render(request, "10 Servicios/seleccionarSucursalServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                                 "notificacionCita":notificacionCita, "notificacionRenta":notificacionRenta, "servicioCorporalActualizado":servicioCorporalActualizado, "sucursales":sucursales})
                    
                if "servicioFacialActualizado" in request.session:
                
                    servicioFacialActualizado = request.session['servicioFacialActualizado']
                    del request.session['servicioFacialActualizado']
                    return render(request, "10 Servicios/seleccionarSucursalServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                                 "notificacionCita":notificacionCita, "notificacionRenta":notificacionRenta, "servicioFacialActualizado":servicioFacialActualizado, "sucursales":sucursales})

                if "registroPaquete" in request.session:
                
                    paquetecreado = request.session['registroPaquete']
                    del request.session['registroPaquete']
                    return render(request, "10 Servicios/seleccionarSucursalServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                                 "notificacionCita":notificacionCita, "notificacionRenta":notificacionRenta, "paquetecreado":paquetecreado, "sucursales":sucursales})
                
                if "paqueteProductoActualizado" in request.session:
                    paqueteProductoActualizado = request.session["paqueteProductoActualizado"]
                    del request.session["paqueteProductoActualizado"]
                    return render(request, "10 Servicios/seleccionarSucursalServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                                 "notificacionCita":notificacionCita, "notificacionRenta":notificacionRenta, "paqueteProductoActualizado":paqueteProductoActualizado, "sucursales":sucursales})
                
                return render(request, "10 Servicios/seleccionarSucursalServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                                 "notificacionCita":notificacionCita, "notificacionRenta":notificacionRenta,"sucursales":sucursales})


            else:
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    sucursalEmpleado = datoEmpleado.id_sucursal_id
                sucursales = Sucursales.objects.filter(id_sucursal = sucursalEmpleado)

                if "servicioCorporalActualizado" in request.session:
                    servicioCorporalActualizado = request.session['servicioCorporalActualizado']
                    del request.session['servicioCorporalActualizado']
                
                    return render(request, "10 Servicios/seleccionarSucursalServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                                 "notificacionCita":notificacionCita, "notificacionRenta":notificacionRenta, "servicioCorporalActualizado":servicioCorporalActualizado, "sucursales":sucursales})
                    
                if "servicioFacialActualizado" in request.session:
                
                    servicioFacialActualizado = request.session['servicioFacialActualizado']
                    del request.session['servicioFacialActualizado']
                    return render(request, "10 Servicios/seleccionarSucursalServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                                 "notificacionCita":notificacionCita, "notificacionRenta":notificacionRenta, "servicioFacialActualizado":servicioFacialActualizado, "sucursales":sucursales})

                if "registroPaquete" in request.session:
                
                    paquetecreado = request.session['registroPaquete']
                    del request.session['registroPaquete']
                    return render(request, "10 Servicios/seleccionarSucursalServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                                 "notificacionCita":notificacionCita, "notificacionRenta":notificacionRenta, "paquetecreado":paquetecreado, "sucursales":sucursales})
                
                if "paqueteProductoActualizado" in request.session:
                    paqueteProductoActualizado = request.session["paqueteProductoActualizado"]
                    del request.session["paqueteProductoActualizado"]
                    return render(request, "10 Servicios/seleccionarSucursalServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                                 "notificacionCita":notificacionCita, "notificacionRenta":notificacionRenta, "paqueteProductoActualizado":paqueteProductoActualizado, "sucursales":sucursales})

                return render(request, "10 Servicios/seleccionarSucursalServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                                 "notificacionCita":notificacionCita, "notificacionRenta":notificacionRenta, "sucursales":sucursales})
    
        
        
        
        
        
        
            
            
        
    else:
        return render(request,"1 Login/login.html")

def actualizarServiciosCoporales(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idServicioCEditar = request.POST['idServicioCorporalEditar']
            nombreEditar = request.POST['nombreActualizado']
            descripcion = request.POST['descripcionActualizado']
            precio_ventaEditar = request.POST['precioActualizado']
            minimo_Editar = request.POST['minimoActualizado']
            maximo_Editar = request.POST['maximoActualizado']
            sucursal_Editar = request.POST['idSucursal']
            
            
            
            
           
            actualizacionServicioCorporal = Servicios.objects.filter(id_servicio = idServicioCEditar).update(nombre_servicio = nombreEditar,descripcion_servicio = descripcion,tiempo_minimo = minimo_Editar,tiempo_maximo =maximo_Editar,
                                                                                                             precio_venta=precio_ventaEditar,sucursal=sucursal_Editar)
            

            if actualizacionServicioCorporal: 
               
             
                request.session['servicioCorporalActualizado'] = "El servicio corporal " + idServicioCEditar  +" "+  nombreEditar + " ha sido actualizado correctamente!"
            return redirect('/inventarioServicios/')
    
def actualizarServiciosFaciales(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idServicioFEditar = request.POST['idServicioFacialEditar']
            nombreEditar = request.POST['nombreActualizado']
            descripcion = request.POST['descripcionActualizado']
            precio_ventaEditar = request.POST['precioActualizado']
            minimo_Editar = request.POST['minimoActualizado']
            maximo_Editar = request.POST['maximoActualizado']
            sucursal_Editar = request.POST['idSucursal']
            
            
            
            
           
            actualizacionServicioFacial = Servicios.objects.filter(id_servicio = idServicioFEditar).update(nombre_servicio = nombreEditar,descripcion_servicio = descripcion,tiempo_minimo = minimo_Editar,tiempo_maximo =maximo_Editar,
                                                                                                             precio_venta=precio_ventaEditar,sucursal=sucursal_Editar)
            

            if actualizacionServicioFacial: 
               
             
                request.session['servicioFacialActualizado'] = "El servicio facial " + idServicioFEditar  +" "+  nombreEditar + " ha sido actualizado correctamente!"
            return redirect('/inventarioServicios/')
        
def crearPaqueteServicios(request):

    
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
            
            idServicio= request.POST['idServicioPaquete'] 
            intServicio = int(idServicio)
            datosServicios = Servicios.objects.filter(id_servicio = intServicio)
            infoServicio = []
         
            for dato in datosServicios:
                nombre = dato.nombre_servicio
                descripcion = dato.descripcion_servicio
                if dato.complementos_servicio == None:
                    complementos = "Ninguno"
                else:
                    complementos = dato.complementos_servicio
                tiempo_min = dato.tiempo_minimo
                tiempo_max = dato.tiempo_maximo
                precio = dato.precio_venta
                
                idSucursal = dato.sucursal_id
                
                datosSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
                for suc in datosSucursal:
                    nombreSucursal = suc.nombre
            
                infoServicio.append([nombre,descripcion,complementos,tiempo_min,tiempo_max,precio,nombreSucursal])
            data = [i.json() for i in ProductosGasto.objects.filter(sucursal_id__id_sucursal = idSucursal)]
            
            
            #----------------
            productos_totales = ProductosGasto.objects.filter(sucursal_id__id_sucursal = idSucursal)
            productos_ids = []
                
            for prod in productos_totales:
                productos_ids.append(prod.id_producto)
            
            productosServicios = ServiciosProductosGasto.objects.filter(servicio_id__id_servicio = idServicio)
            productosServicio = []
            for productoServicio in productosServicios:
                ids_producto_gasto = productoServicio.producto_gasto_id
            
                for dato in productos_ids:
                    if dato  == ids_producto_gasto:
                        productos_ids.remove(dato)
                
                  
                  
            datos_productos_no_paquete = []
                
            for id in productos_ids:
                datos = ProductosGasto.objects.filter(id_producto = id)
                for dato in datos:
                    id_producto = dato.id_producto
                    codigo_producto = dato.codigo_producto
                    sku = dato.sku_producto
                    nombreProd = dato.nombre_producto
                    existencias = dato.cantidad
                    descripcionP = dato.descripcion
                    imagen = dato.imagen_producto
                    fecha_alta = dato.fecha_alta
                    
                datos_productos_no_paquete.append([id_producto,codigo_producto,sku,nombreProd,existencias,descripcionP,imagen,fecha_alta])   
            
            
            
            
        #----------------------
            
      
                
       
           
                    
            
            
            
            
            
            productosVenta = ProductosGasto.objects.filter(sucursal_id__id_sucursal = idSucursal)
            productosVentaJavaScript = ProductosGasto.objects.filter(sucursal_id__id_sucursal = idSucursal)
            
        
            return render(request, "11 PaquetesServicios/crearPaqueteServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,
                                                                                       "infoServicio":infoServicio,"idServicio":idServicio,"productosVenta":productosVenta,"productosVentaJson":json.dumps(data),"productosVentaJavaScript":productosVentaJavaScript,
                                                                                       "datos_productos_no_paquete":datos_productos_no_paquete,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
            
            
         

       

            
            
        return render(request, "11 PaquetesServicios/crearPaqueteServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
                                                                                   
                                                                                 
                                                                                   
        })
    
    else:
        return render(request,"1 Login/login.html")
        
def crearPaqueteServicioConProductosVenta(request):

    
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
        

        
        if request.method == "POST":
            
            idServicio= request.POST['idServicioPaqueteConProductosVenta'] 
            intServicio = int(idServicio)
            datosServicios = Servicios.objects.filter(id_servicio = intServicio)
            infoServicio = []
         
            for dato in datosServicios:
                nombreServicio = dato.nombre_servicio
                descripcion = dato.descripcion_servicio
                if dato.complementos_servicio == None:
                    complementos = "Ninguno"
                else:
                    complementos = dato.complementos_servicio
                tiempo_min = dato.tiempo_minimo
                tiempo_max = dato.tiempo_maximo
                precio = dato.precio_venta
                
                idSucursal = dato.sucursal_id
                
                datosSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
                for suc in datosSucursal:
                    nombreSucursal = suc.nombre
                    
            
                productosServicios = ServiciosProductosGasto.objects.filter(servicio_id__id_servicio = intServicio)
                productosServicio = []
                for productoServicio in productosServicios:
                    ids_producto_gasto = productoServicio.producto_gasto_id
                    
                    cantidad = productoServicio.cantidad
                    datosProducto = ProductosGasto.objects.filter(id_producto = ids_producto_gasto)
                    for dato in datosProducto:
                        codigo = dato.codigo_producto
                        idProducto = dato.id_producto
                        sku = dato.sku_producto
                        nombre = dato.nombre_producto
                        imagen = dato.imagen_producto
                        cantidad_existencia = dato.cantidad
                        productosServicio.append([idProducto,codigo,sku,nombre,imagen,cantidad,cantidad_existencia])
                    
                
                    
                    
                    
                    
                    
                    
                    
            
                infoServicio.append([nombreServicio,descripcion,complementos,tiempo_min,tiempo_max,precio,nombreSucursal])
            
            data = [i.json() for i in ProductosVenta.objects.filter(sucursal_id__id_sucursal = idSucursal)]
            productosVenta = ProductosVenta.objects.filter(sucursal_id__id_sucursal = idSucursal)
            productosVentaJavaScript = ProductosVenta.objects.filter(sucursal_id__id_sucursal = idSucursal)
            
        
            return render(request, "11 PaquetesServicios/editarPaqueteServicio.html", {"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,
                                                                                       "infoServicio":infoServicio,"idServicio":idServicio,"productosVenta":productosVenta,"productosVentaJson":json.dumps(data),"productosVentaJavaScript":productosVentaJavaScript,
                                                                                       "productosServicio":productosServicio,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
            
            
         

       

            
            
        return render(request, "11 PaquetesServicios/editarPaqueteServicio.html", {"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
                                                                                
                                                                                   
                                                                                 
                                                                                   
        })
    
    else:
        return render(request,"1 Login/login.html")

def guardarPaquete(request):

    
    if "idSesion" in request.session:
     

      
        
        if request.method == "POST":
            
            idServicio = request.POST['idServicio']
            productosSolicitados = request.POST['cantidadesProductosVenta']
            listaProductosSolicitados = productosSolicitados.split(",")
  
            listaCantidadesSolicitadas = []
           
            for idProducto in listaProductosSolicitados:
               
                nameCantidadProducto = "cantidadUsar" + str(idProducto)
                cantidadSolicitadaMandada = request.POST[nameCantidadProducto]
                listaCantidadesSolicitadas.append(cantidadSolicitadaMandada)
            
            lista = zip(listaProductosSolicitados,listaCantidadesSolicitadas)
            
            for producto, cantidad in lista:
                idProductoBD = producto
                cantidadProductoBD = cantidad
                
                registroProducto = ServiciosProductosGasto(servicio = Servicios.objects.get(id_servicio=idServicio),producto_gasto=ProductosGasto.objects.get(id_producto =idProductoBD),cantidad=cantidadProductoBD)
                
                registroProducto.save()
                
            if registroProducto:
                    
                request.session['registroPaquete'] = "El paquete ha sido gregado satisfactoriamente!"
                return redirect('/inventarioServicios/')
                
                
            else:
                request.session['registroPaquete'] = "Error en la base de datos, intentelo más tarde.."
                return redirect('/inventarioServicios/')

            
            
            
            
            
            
            
    
    
    else:
        return render(request,"1 Login/login.html")
        
def guardarPaqueteEditadoProductosVenta(request):

    if "idSesion" in request.session:

        
        
       
        if request.method == "POST":
            
            idServicio = request.POST['idServicio']
            productosSolicitados = request.POST['cantidadesProductosVenta']
            listaProductosSolicitados = productosSolicitados.split(",")
  
            listaCantidadesSolicitadas = []
           
            for idProducto in listaProductosSolicitados:
               
                nameCantidadProducto = "cantidadUsar" + str(idProducto)
                cantidadSolicitadaMandada = request.POST[nameCantidadProducto]
                listaCantidadesSolicitadas.append(cantidadSolicitadaMandada)
            
            lista = zip(listaProductosSolicitados,listaCantidadesSolicitadas)
            
            for producto, cantidad in lista:
                idProductoBD = producto
                cantidadProductoBD = cantidad
                
                registroProducto = ServiciosProductosGasto(servicio = Servicios.objects.get(id_servicio=idServicio),producto_gasto=ProductosGasto.objects.get(id_producto =idProductoBD),cantidad=cantidadProductoBD)
                
                registroProducto.save()
                
            if registroProducto:
                    
                request.session['registroPaquete'] = "El paquete ha sido gregado satisfactoriamente!"
                return redirect('/inventarioServicios/')
                
                
            else:
                request.session['registroPaquete'] = "Error en la base de datos, intentelo más tarde.."
                return redirect('/inventarioServicios/')


    
    else:
        return render(request,"1 Login/login.html")
        
def actualizarPaquete(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idProductoPaqueteEditar = request.POST['idServicioEditar']
            
            #Nombre de servicio
            consultaServicio = Servicios.objects.filter(id_servicio = idProductoPaqueteEditar)
            for datoServicio in consultaServicio:
                nombreServicio = datoServicio.nombre_servicio
            
            nameInputEliminar = "eliminarProducto"
            nameInputCantidad = "cantidadProducto"
            
            consultaProductosServicio = ServiciosProductosGasto.objects.filter(servicio_id__id_servicio = idProductoPaqueteEditar)
            
            for producto in consultaProductosServicio:
                idProductoUtilizado = producto.producto_gasto_id
                
                nameInputPorProductoEliminar = nameInputEliminar+str(idProductoUtilizado)
                nameInputCantidadProductoEditar = nameInputCantidad+str(idProductoUtilizado)
                
                
            
                if request.POST.get(nameInputPorProductoEliminar, False): #Checkeado Eliminar producto
                    borrado = ServiciosProductosGasto.objects.get(producto_gasto_id = idProductoUtilizado, servicio_id__id_servicio = idProductoPaqueteEditar)
                    borrado.delete()
                    
                elif request.POST.get(nameInputPorProductoEliminar, True): #No checkeado, actualizar producto
                    cantidadProductoActualizar = request.POST[nameInputCantidadProductoEditar]
                    actualizacionProductoPaquete = ServiciosProductosGasto.objects.filter(producto_gasto_id = idProductoUtilizado).update(cantidad = cantidadProductoActualizar)
                
                
            #Agregar más productos.
            
            
            masProductos = request.POST['masProductos']
            if masProductos == "noMasProductos":
                
                if actualizacionProductoPaquete or borrado: 
                    request.session['paqueteProductoActualizado'] = "El paquete del servicio "+nombreServicio+" ha sido actualizado correctamente!"
                    return redirect('/inventarioServicios/')
            elif masProductos == "masProductos":
                productosAgregar = request.POST['idsProductosGastoServicio']
                listaProductosAgregar = productosAgregar.split(",")
                
                listaCantidadesSolicitadas = []
                
                for idProducto in listaProductosAgregar:
                    nameCantidadProducto = "cantidadUsar"+str(idProducto)
                    cantidadSolicitadaMandada = request.POST[nameCantidadProducto]
                    listaCantidadesSolicitadas.append(cantidadSolicitadaMandada)
                lista = zip(listaProductosAgregar,listaCantidadesSolicitadas)
                
                
                for producto, cantidad in lista:
                    idProductoBD = producto
                    cantidadProductoBD = cantidad
                    
                    registroProducto = ServiciosProductosGasto(servicio = Servicios.objects.get(id_servicio=idProductoPaqueteEditar),producto_gasto=ProductosGasto.objects.get(id_producto =idProductoBD),cantidad=cantidadProductoBD)
                    registroProducto.save()
                
                if actualizacionProductoPaquete or borrado or registroProducto: 
                    request.session['paqueteProductoActualizado'] = "El paquete del servicio "+nombreServicio+" ha sido actualizado correctamente!"
                    return redirect('/inventarioServicios/')
                
def actualizarPaqueteFacial(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idProductoPaqueteEditar = request.POST['idProducto']
            cantidadProductoEditar = request.POST['idProductoPaqueteEditar']
            nameInput = "eliminarProducto"
            
            if request.POST.get(nameInput, True): #Checkeado
                eliminarProducto = True
                borrado = ServiciosProductosGasto.objects.get(producto_gasto_id = idProductoPaqueteEditar)
                borrado.delete()
                
                return redirect('/inventarioPaqueteServicios/')
                      
            elif request.POST.get(nameInput, False): #No checkeado
                eliminarProducto = False
           
                actualizacionProductoPaquete = ServiciosProductosGasto.objects.filter(producto_gasto_id = idProductoPaqueteEditar).update(cantidad = cantidadProductoEditar)
                

                if actualizacionProductoPaquete: 
                    request.session['paqueteProductoActualizado'] = "El producto del paquete ha sido actualizado correctamente!"
                
                
               
           
                
                return redirect('/inventarioPaqueteServicios/')       
           
def verProductoDePaqueteCorporalEditar(request):

    if "idSesion" in request.session:
        idEmpleado = request.session['idSesion']
        nombresEmpleado = request.session['nombresSesion']
        tipoUsuario = request.session['tipoUsuario']
        puestoEmpleado = request.session['puestoSesion']
        #INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]
        #notificacionRentas
        notificacionRenta = notificacionRentas(request)
        #notificacionCitas
        notificacionCita = notificacionCitas(request)
         #permisosEmpleado
        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)
        
        if request.method == "POST":
            
            idServicioCorporalEditar = request.POST['idServicioCorporalEditar']
            consultaDatosServicios = Servicios.objects.filter(id_servicio = idServicioCorporalEditar)
            consultaDeProductos = ServiciosProductosGasto.objects.filter(servicio__id_servicio = idServicioCorporalEditar)
            
            productosElegidos = []
            
            for producto in consultaDeProductos:
                idProducto = producto.producto_gasto_id
                cantidadUtilizadaDeProducto = producto.cantidad
                
                consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                for dato in consultaProducto:
                    codigoProducto = dato.codigo_producto
                    nombreProducto = dato.nombre_producto
                    imagenProducto = dato.imagen_producto
                    skuProducto = dato.sku_producto
                    
                productosElegidos.append([idProducto,cantidadUtilizadaDeProducto,
                                          codigoProducto,
                                          nombreProducto,
                                          imagenProducto,
                                          skuProducto])
                
                
            #Sucursal de servicio
            for datoServicio in consultaDatosServicios:
                sucursal = datoServicio.sucursal_id
                
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
             
            #Lista de productos a elegir para agregar más al servicio.
            todosLosProductosGasto = ProductosGasto.objects.filter(sucursal_id__id_sucursal = sucursal)
            arrayProductosGastoNoEnServicio = []
            
            
            consultaProductosUtilizados = ServiciosProductosGasto.objects.filter(servicio__id_servicio = idServicioCorporalEditar)
            idsProductosYaUtilizados = []
            
            for productoServ in consultaProductosUtilizados:
                idProducto = productoServ.producto_gasto_id
                idsProductosYaUtilizados.append(idProducto)
                
            for producto in todosLosProductosGasto:
                idProducto = producto.id_producto
                productoYaEstaEnServicio = False
                for productoEnServicio in idsProductosYaUtilizados:
                    idProductoEnServicio = productoEnServicio
                    
                    if idProducto == idProductoEnServicio:
                        productoYaEstaEnServicio = True
                
                if productoYaEstaEnServicio == False:
                    consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                    for dato in consultaProducto:
                        codigoProducto = dato.codigo_producto
                        skuProducto = dato.sku_producto
                        nombreProducto = dato.nombre_producto
                        existenciasProducto = dato.cantidad
                        descripcionProducto = dato.descripcion
                        imagenProducto = dato.imagen_producto
                        fechaAgregadoProducto = dato.fecha_alta
                    
                    arrayProductosGastoNoEnServicio.append([idProducto,codigoProducto, skuProducto, nombreProducto,
                                                     existenciasProducto, descripcionProducto, imagenProducto, fechaAgregadoProducto])
                    
                    
            
            
            #Lista de productos en formato JSON.
            data = [i.json() for i in ProductosGasto.objects.filter(sucursal_id__id_sucursal = sucursal)]
            
        
        
            return render(request, "11 PaquetesServicios/actualizarPaquete.html", {"consultaPermisos":consultaPermisos,"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"notificacionRenta":notificacionRenta, "consultaDatosServicios":consultaDatosServicios, "productosElegidos":productosElegidos, "nombreSucursal":nombreSucursal, "arrayProductosGastoNoEnServicio":arrayProductosGastoNoEnServicio, "productosVentaJson":json.dumps(data),
                                                                                   "todosLosProductosGasto":todosLosProductosGasto, "notificacionCita":notificacionCita})
            

            
        return render(request, "11 PaquetesServicios/actualizarPaquete.html", {"consultaPermisos":consultaPermisos,"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"notificacionRenta":notificacionRenta, "consultaDatosServicios":consultaDatosServicios, "productosElegidos":productosElegidos, "nombreSucursal":nombreSucursal, "notificacionCita":notificacionCita})
    
    else:
        return render(request,"1 Login/login.html")
    
def verProductoDePaqueteFacialEditar(request):

    if "idSesion" in request.session:


   #notificacionRentas
        notificacionRenta = notificacionRentas(request)
        if request.method == "POST":
            
            
            idProducto= request.POST['idProductoEditarPaqueteFacial'] 
            cantidadEnPaquete = request.POST['cantidadEnPaqueteFacial']
            datos = ProductosGasto.objects.filter(id_producto = idProducto)
            for x in datos :
                idP = x.id_producto
             

        
            return render(request, "11 PaquetesServicios/actualizarPaquete.html", {"idP":idP,"datos":datos,"cantidadEnPaquete":cantidadEnPaquete,"notificacionRenta":notificacionRenta})
            

            
        return render(request, "11 PaquetesServicios/actualizarPaquete.html", {"idP":idP,"datos":datos,"cantidadEnPaquete":cantidadEnPaquete,"notificacionRenta":notificacionRenta
                                                                                   
                                                                                 
                                                                                   
        })
    
    else:
        return render(request,"1 Login/login.html")
    
def inventarioPaqueteServicios(request):

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
      
        #------------servicios tipo corporales -------------
        
        productosPorServicio = []
        sucursalesPorServicio = []
        serviciosCorporales = Servicios.objects.filter(tipo_servicio="Corporal")
        for servicioCorporal in serviciosCorporales:
            idservicio_corporal = servicioCorporal.id_servicio
            id_sucursal = servicioCorporal.sucursal_id
            sucursales = Sucursales.objects.filter(id_sucursal = id_sucursal)
          
            for sucursal in sucursales:
                nombreSucursal = sucursal.nombre
            
                
            productosServicios = ServiciosProductosGasto.objects.filter(servicio_id__id_servicio = idservicio_corporal)
            productosServicio = []
            for productoServicio in productosServicios:
                ids_producto_gasto = productoServicio.producto_gasto_id
                ids_servicios = productoServicio.servicio_id
                cantidad = productoServicio.cantidad
                datosProducto = ProductosGasto.objects.filter(id_producto = ids_producto_gasto)
                for dato in datosProducto:
                    codigo = dato.codigo_producto
                    idProducto = dato.id_producto
                    sku = dato.sku_producto
                    nombre = dato.nombre_producto
                    cantidad_existencias = dato.cantidad
                productosServicio.append([idProducto,codigo,sku,nombre,cantidad,cantidad_existencias])
            
            productosPorServicio.append(productosServicio)
            sucursalesPorServicio.append(nombreSucursal)
            
                
       
      
            
        
  
        lista = zip(serviciosCorporales,productosPorServicio,sucursalesPorServicio)
        listaModal = zip(serviciosCorporales,productosPorServicio,sucursalesPorServicio)
        
        listaModalEditarCorporal = zip(serviciosCorporales,productosPorServicio,sucursalesPorServicio)
        
        listaModalJavaScript = zip(serviciosCorporales,productosPorServicio,sucursalesPorServicio)
            

        
        #------------servicios tipo faciales -------------
        
        productosPorServicio = []
        sucursalesPorServicio = []
        serviciosFaciales = Servicios.objects.filter(tipo_servicio="Facial")
        for servicioFacial in serviciosFaciales:
            idservicio_facial = servicioFacial.id_servicio
            id_sucursal = servicioFacial.sucursal_id
            sucursales = Sucursales.objects.filter(id_sucursal = id_sucursal)
          
            for sucursal in sucursales:
                nombreSucursal = sucursal.nombre
            
                
            productosServicios = ServiciosProductosGasto.objects.filter(servicio_id__id_servicio = idservicio_facial)
            productosServicio = []
            productosServicioJS =[]
            for productoServicio in productosServicios:
                ids_producto_gasto = productoServicio.producto_gasto_id
               
                cantidad = productoServicio.cantidad
                datosProducto = ProductosGasto.objects.filter(id_producto = ids_producto_gasto)
                for dato in datosProducto:
                    codigo = dato.codigo_producto
                    idProducto = dato.id_producto
                    sku = dato.sku_producto
                    nombre = dato.nombre_producto
                productosServicio.append([idProducto,codigo,sku,nombre,cantidad])
                productosServicioJS.append([idProducto,codigo,sku,nombre,cantidad])
            
            productosPorServicio.append(productosServicio)
            sucursalesPorServicio.append(nombreSucursal)
            
                
       
      
            
        
  
        listaFaciales = zip(serviciosFaciales,productosPorServicio,sucursalesPorServicio)
        listaModalFaciales = zip(serviciosFaciales,productosPorServicio,sucursalesPorServicio)
        
    
        if "paqueteProductoActualizado" in request.session:
            paqueteProductoActualizado = request.session['paqueteProductoActualizado']
            del request.session['paqueteProductoActualizado']
          
            return render(request, "11 PaquetesServicios/inventarioPaqueteServicios.html",  {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                         
                                                                    "productosPorServicio":productosPorServicio,"lista":lista,"serviciosCorporales":serviciosCorporales,"productosServicio":productosServicio,"listaModal":listaModal,"listaFaciales":listaFaciales,
                                                                    "listaModalFaciales":listaModalFaciales,"listaModalEditarCorporal":listaModalEditarCorporal,"listaModalJavaScript":listaModalJavaScript,"productosServicioJS":productosServicioJS,
                                                                    "paqueteProductoActualizado":paqueteProductoActualizado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })

        if "productoBorrado" in request.session:
            paqueteProductoBorrado = request.session['productoBorrado']
            del request.session['productoBorrado']
          
            return render(request, "11 PaquetesServicios/inventarioPaqueteServicios.html",  {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                         
                                                                    "productosPorServicio":productosPorServicio,"lista":lista,"serviciosCorporales":serviciosCorporales,"productosServicio":productosServicio,"listaModal":listaModal,"listaFaciales":listaFaciales,
                                                                    "listaModalFaciales":listaModalFaciales,"listaModalEditarCorporal":listaModalEditarCorporal,"listaModalJavaScript":listaModalJavaScript,"productosServicioJS":productosServicioJS,
                                                                    "paqueteProductoBorrado":paqueteProductoBorrado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })

        
        
        
        
       
        
        
            
        return render(request, "11 PaquetesServicios/inventarioPaqueteServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
                                                                         
                                                                    "productosPorServicio":productosPorServicio,"lista":lista,"serviciosCorporales":serviciosCorporales,"productosServicio":productosServicio,"listaModal":listaModal,"listaFaciales":listaFaciales,
                                                                    "listaModalFaciales":listaModalFaciales,"listaModalEditarCorporal":listaModalEditarCorporal,"listaModalJavaScript":listaModalJavaScript,"productosServicioJS":productosServicioJS,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
        })
    
    else:
        return render(request,"1 Login/login.html")
    
