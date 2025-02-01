
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

import json
# Librerías de fecha
from datetime import date, datetime

#Para mandar telegram
import telepot
#Plugin impresora termica
from appCostabella import Conector, keysBotCostabella
# Importacion de modelos
from appCostabella.models import (CertificadosProgramados, Citas, Clientes, Empleados, Permisos,ProductosGasto, ProductosServiciosCertificados, Servicios,ServiciosCertificados, Sucursales, Ventas)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)
from dateutil.relativedelta import relativedelta
# Archivo configuración de django
from django.conf import settings
#Correo electrónico
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def agregarCertificado(request):
    if "idSesion" in request.session:
     
        #Variables de sesión
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

        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)

        if request.method == "POST":
            sucursalCertificado = request.POST["sucursalCertificado"]
            consultaSucursalCertificado = Sucursales.objects.filter(id_sucursal = sucursalCertificado)
            for datoSucursal in consultaSucursalCertificado:
                nombreSucursal = datoSucursal.nombre
            #CERTIFICADOS
            #Folio certificado
            consultaCertificados = CertificadosProgramados.objects.all()

            nuevoCodigoCertificado = ""
            if consultaCertificados:
                for certificado in consultaCertificados:
                    certificadoActual = certificado.codigo_certificado

                    splitCertificadoActual = certificadoActual.split("-")
                    posicionNumero = splitCertificadoActual[1]
                    posicionNumeroInt = int(posicionNumero)
                    nuevaPosicionNumero = posicionNumeroInt+1
                    nuevoCodigoCertificado = "CERT-"+str(nuevaPosicionNumero)
            else:
                nuevoCodigoCertificado = "CERT-1000"

            #Fechas
            fechaHoy = datetime.now()
            fechaVigencia = fechaHoy + relativedelta(months=1)

            #Clientes
            clientes = Clientes.objects.all()

            #Servicios de esa sucursal
            consultaServicios = ServiciosCertificados.objects.filter(sucursal_id__id_sucursal = sucursalCertificado)
            consultaServiciosJava = ServiciosCertificados.objects.filter(sucursal_id__id_sucursal = sucursalCertificado)

            sucursalCertificado = str(sucursalCertificado)
            data = [i.json() for i in ServiciosCertificados.objects.filter(sucursal_id__id_sucursal = sucursalCertificado)]



            return render(request,"19 Certificados/agregarCertificado.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                         "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita,
                                                                         "nuevoCodigoCertificado":nuevoCodigoCertificado, "nombreSucursal":nombreSucursal, "fechaHoy":fechaHoy, 
                                                                         "fechaVigencia":fechaVigencia, "clientes":clientes, "consultaServicios":consultaServicios, "serviciosTotales":json.dumps(data),
                                                                         "consultaServiciosJava":consultaServiciosJava, "sucursalCertificado":sucursalCertificado})
        
        else:
            if tipoUsuario == "esAdmin":
                sucursales = Sucursales.objects.all()
            else:
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    sucursalEmpleado = datoEmpleado.sucursal_id
                
                sucursales = Sucursales.objects.filter(id_sucursal = sucursalEmpleado)
            return render(request,"19 Certificados/seleccionarAgregarCertificado.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                         "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita,
                                                                         "sucursales":sucursales})
        
       
    
    
    else:
        return render(request,"1 Login/login.html")  
    
def agregarServicioCertificado(request):
    if "idSesion" in request.session:
     
        #Variables de sesión
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

        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)

        #CERTIFICADOS
        ultimoCodigoCertificado = ""
        consultaServiciosCertificados =ServiciosCertificados.objects.all()

        if consultaServiciosCertificados:
            for servicio in consultaServiciosCertificados:
                ultimoCodigoCertificado = servicio.codigo_servocio
                ultimoCodigoCertificado = str(ultimoCodigoCertificado)
                splitCodigo = ultimoCodigoCertificado.split("-")
                intCodigo = int(splitCodigo[1])
                inCodigoNuevo = intCodigo+1
                ultimoCodigoCertificado = "SERV-"+str(inCodigoNuevo)
        else:
            ultimoCodigoCertificado = "SERV-1000"

        #Sucursales
        sucursales = Sucursales.objects.all()

        if request.method == "POST": #Si clic al botón..
            codigoServicioNuevo = request.POST['codigoServicioNuevo']
            nombreServicio = request.POST['nombreServicio']
            costoServicio = request.POST['costoServicio']
            descripcion = request.POST['descripcion']
            tiempo_minimo = request.POST['tiempoMinimo']  #Requerido
            tiempo_maximo= request.POST['tiempoMaximo'] 
            listaSucursales = request.POST.getlist('sucursales')

            costoServicio = float(costoServicio)

            if "Todas" in listaSucursales:
                #El servicio se dara de alta en todas las sucursales
                sucursales = Sucursales.objects.all()
                contador = 0
                for sucursal in sucursales:
                    idSucursal = sucursal.id_sucursal
                    contador = contador+1
                    if contador == 1:
                        codigoServicioFormado = codigoServicioNuevo
                    else:
                        splitCodigoAnterior = codigoServicioNuevo.split("-")
                        intCodigoNuevo = int(splitCodigoAnterior[1])
                        inCodigoNuevo = intCodigoNuevo+1
                        codigoServicioFormado = "SERV-"+str(inCodigoNuevo)
                    registroServicio = ServiciosCertificados(codigo_servocio = codigoServicioFormado,
                    sucursal = Sucursales.objects.get(id_sucursal = idSucursal), nombre = nombreServicio,
                    precio = costoServicio, descripcion = descripcion,
                    tiempo_minimo = tiempo_minimo, 
                    tiempo_maximo = tiempo_maximo)

                    registroServicio.save()
            else:
                contador = 0
                for sucursal in listaSucursales:
                    idSucursal = int(sucursal)
                    contador = contador+1
                    if contador == 1:
                        codigoServicioFormado = codigoServicioNuevo
                    else:
                        splitCodigoAnterior = codigoServicioNuevo.split("-")
                        intCodigoNuevo = int(splitCodigoAnterior[1])
                        inCodigoNuevo = intCodigoNuevo+1
                        codigoServicioFormado = "SERV-"+str(inCodigoNuevo)

                    registroServicio = ServiciosCertificados(codigo_servocio = codigoServicioFormado,
                    sucursal = Sucursales.objects.get(id_sucursal = idSucursal), nombre = nombreServicio,
                    precio = costoServicio, descripcion = descripcion,
                    tiempo_minimo = tiempo_minimo, 
                    tiempo_maximo = tiempo_maximo)
                    registroServicio.save()

            if registroServicio:
                request.session["ServicioCertificadoRegistrado"] = "El servicio ha sido dado de alta en las sucursales correspondientes!"
                return redirect("/agregarServicioCertificado/")

        if "ServicioCertificadoRegistrado" in request.session:
            ServicioCertificadoRegistrado = request.session["ServicioCertificadoRegistrado"]
            del request.session["ServicioCertificadoRegistrado"]
            return render(request,"19 Certificados/agregarServicioCertificado.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                         "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, "ultimoCodigoCertificado":ultimoCodigoCertificado,
                                                                         "sucursales":sucursales, "ServicioCertificadoRegistrado":ServicioCertificadoRegistrado})
        return render(request,"19 Certificados/agregarServicioCertificado.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                         "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, "ultimoCodigoCertificado":ultimoCodigoCertificado,
                                                                         "sucursales":sucursales})
    
    
    else:
        return render(request,"1 Login/login.html")  

def verServiciosCertificado(request):
    if "idSesion" in request.session:
     
        #Variables de sesión
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

        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)

        if request.method == "POST":
            sucursalServicio = request.POST["sucursalServicio"]

            #Info sucursal
            consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalServicio)
            for datoSucursal in consultaSucursal:
                nombreSucursal = datoSucursal.nombre

            yaTienePaquete = []
            consultaServicios = ServiciosCertificados.objects.filter(sucursal_id__id_sucursal = sucursalServicio)
            consultaServicios2 = ServiciosCertificados.objects.filter(sucursal_id__id_sucursal = sucursalServicio)
            
            productosPorServicio = []
            for servicio in consultaServicios:
                idServicio = servicio.id_servicio_certificado

                consultaProductosServicio = ProductosServiciosCertificados.objects.filter(servicio_certificado_id__id_servicio_certificado = idServicio)
                if consultaProductosServicio:
                    conPaquete = "Con paquete"
                    yaTienePaquete.append("Con paquete")

                    productosServicio = []
                    for productoUtilizado in consultaProductosServicio:
                        #Ya tiene productos asignados... Sacar todos los productos y mandarlos a un arreglo de ese servicio.
                        idProductoGastoUtilizado = productoUtilizado.producto_gasto_id
                        cantidadUtilizada = productoUtilizado.cantidad_utilizada
                        datosProducto = ProductosGasto.objects.filter(id_producto = idProductoGastoUtilizado)
                        for dato in datosProducto:
                            codigo = dato.codigo_producto
                            idProducto = dato.id_producto
                            sku = dato.sku_producto
                            nombre = dato.nombre_producto
                            cantidad_existencias = dato.cantidad
                            
                        productosServicio.append([idProducto,codigo,sku,nombre,cantidadUtilizada,cantidad_existencias])
                    
                else:
                    conPaquete = "Sin paquete"
                    yaTienePaquete.append("Sin paquete")

                if conPaquete == "Con paquete":
                    productosPorServicio.append(productosServicio)

                if conPaquete == "Con paquete":
                    productosPorServicio.append("nada")

            listaZipTabla = zip(consultaServicios, yaTienePaquete)
            listaZipTabla2 = zip(consultaServicios, yaTienePaquete, productosPorServicio)

            return render(request,"19 Certificados/verServiciosCertificado.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "nombreSucursal":nombreSucursal, "listaZipTabla":listaZipTabla, "consultaServicios2":consultaServicios2, "listaZipTabla2":listaZipTabla2})

        else:

            if tipoUsuario == "esAdmin":
                sucursales = Sucursales.objects.all()
            else:
                infoEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in infoEmpleado:
                    idSucursal = datoEmpleado.sucursal_id

                sucursales = Sucursales.objects.filter(id_sucursal = idSucursal)

            if "servicioCertificadoActualizado" in request.session:
                servicioCertificadoActualizado = request.session["servicioCertificadoActualizado"]
                del request.session["servicioCertificadoActualizado"]
                return render(request,"19 Certificados/seleccionarSucursalServiciosCertificados.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "sucursales":sucursales, "servicioCertificadoActualizado":servicioCertificadoActualizado})
            if "registroPaquete" in request.session:
                registroPaquete = request.session["registroPaquete"]
                del request.session["registroPaquete"]
                return render(request,"19 Certificados/seleccionarSucursalServiciosCertificados.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "sucursales":sucursales, "registroPaquete":registroPaquete})

            
            if "paqueteProductoActualizado" in request.session:
                paqueteProductoActualizado = request.session["paqueteProductoActualizado"]
                del request.session["paqueteProductoActualizado"] 

                return render(request,"19 Certificados/seleccionarSucursalServiciosCertificados.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "sucursales":sucursales, "paqueteProductoActualizado":paqueteProductoActualizado})

            return render(request,"19 Certificados/seleccionarSucursalServiciosCertificados.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "sucursales":sucursales})
    
    
    else:
        return render(request,"1 Login/login.html")

def actualizarServicioCertificado(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idServicioCertificadoEditar = request.POST["idServicioCertificadoEditar"]
            nombreActualizado = request.POST['nombreActualizado']
            precioActualizado = request.POST['precioActualizado']
            

            actualizacionServicioCertificado = ServiciosCertificados.objects.filter(id_servicio_certificado = idServicioCertificadoEditar).update(nombre = nombreActualizado, precio = precioActualizado)
            

            if actualizacionServicioCertificado: 
               
             
                request.session['servicioCertificadoActualizado'] = "El servicio para certificado #" + idServicioCertificadoEditar  +", "+  nombreActualizado + ", ha sido actualizado correctamente!"
            return redirect('/verServiciosCertificado/')

def crearPaqueteServicioCertificado(request):

    
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
            
            idServicioCertificado= request.POST['idServicioCertificado'] 
            intServicio = int(idServicioCertificado)
            datosServicio = ServiciosCertificados.objects.filter(id_servicio_certificado = intServicio)
            infoServicio = []
         
            for dato in datosServicio:
                codigo = dato.codigo_servocio
                nombre = dato.nombre
                descripcion = dato.descripcion
                precio = dato.precio
                
                idSucursal = dato.sucursal_id
                
                datosSucursal = Sucursales.objects.filter(id_sucursal = idSucursal)
                for suc in datosSucursal:
                    nombreSucursal = suc.nombre
            
                infoServicio.append([codigo,nombre,descripcion,precio,nombreSucursal])
            
            
            data = [i.json() for i in ProductosGasto.objects.filter(sucursal_id__id_sucursal = idSucursal)]
            
            
            #----------------
            productos_totales = ProductosGasto.objects.filter(sucursal_id__id_sucursal = idSucursal)
            productos_ids = []
                
            for prod in productos_totales:
                productos_ids.append(prod.id_producto)
            
            productosServicios = ProductosServiciosCertificados.objects.filter(servicio_certificado_id__id_servicio_certificado = intServicio)
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
            
            
            productosVenta = ProductosGasto.objects.filter(sucursal_id__id_sucursal = idSucursal)
            productosVentaJavaScript = ProductosGasto.objects.filter(sucursal_id__id_sucursal = idSucursal)
            
        
            return render(request, "19 Certificados/crearPaqueteServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,
                                                                                       "infoServicio":infoServicio,"idServicioCertificado":idServicioCertificado,"productosVenta":productosVenta,"productosVentaJson":json.dumps(data),"productosVentaJavaScript":productosVentaJavaScript,
                                                                                       "datos_productos_no_paquete":datos_productos_no_paquete,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
            
            
         

       

            
            
        return render(request, "19 Certificados/crearPaqueteServicios.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita
                                                                                   
                                                                                 
                                                                                   
        })
    
    else:
        return render(request,"1 Login/login.html")

def guardarPaqueteServicioCertificado(request):

    
    if "idSesion" in request.session:
     

      
        
        if request.method == "POST":
            
            idServicioCertificado = request.POST['idServicioCertificado']
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
                
                registroProducto = ProductosServiciosCertificados(servicio_certificado = ServiciosCertificados.objects.get(id_servicio_certificado=idServicioCertificado),producto_gasto=ProductosGasto.objects.get(id_producto =idProductoBD),cantidad_utilizada=cantidadProductoBD)
                
                registroProducto.save()
                
            if registroProducto:
                
                consultaServicio = ServiciosCertificados.objects.filter(id_servicio_certificado = idServicioCertificado)
                for datoServicio in consultaServicio:
                    nombreServicio = datoServicio.nombre
                request.session['registroPaquete'] = "El paquete del servicio "+str(nombreServicio)+" ha sido gregado satisfactoriamente!"
                return redirect('/verServiciosCertificado/')
                
                
            
            
            
            
            
            
            
            
    
    
    else:
        return render(request,"1 Login/login.html")

def verProductoDePaqueteServicioCertificadoEditar(request):

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
            
            idServicioCertificadoEditar = request.POST['idServicioCertificadoEditar']
            consultaDatosServicios = ServiciosCertificados.objects.filter(id_servicio_certificado = idServicioCertificadoEditar)
            consultaDeProductos = ProductosServiciosCertificados.objects.filter(servicio_certificado_id__id_servicio_certificado = idServicioCertificadoEditar)
            
            productosElegidos = []
            
            for producto in consultaDeProductos:
                idProducto = producto.producto_gasto_id
                cantidadUtilizadaDeProducto = producto.cantidad_utilizada
                
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
            
            
            consultaProductosUtilizados = ProductosServiciosCertificados.objects.filter(servicio_certificado_id__id_servicio_certificado = idServicioCertificadoEditar)
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
            
        
        
            return render(request, "19 Certificados/actualizarPaquete.html", {"consultaPermisos":consultaPermisos,"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"notificacionRenta":notificacionRenta, "consultaDatosServicios":consultaDatosServicios, "productosElegidos":productosElegidos, "nombreSucursal":nombreSucursal, "arrayProductosGastoNoEnServicio":arrayProductosGastoNoEnServicio, "productosVentaJson":json.dumps(data),
                                                                                   "todosLosProductosGasto":todosLosProductosGasto, "notificacionCita":notificacionCita})
            

            
        return render(request, "19 Certificados/actualizarPaquete.html", {"consultaPermisos":consultaPermisos,"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"notificacionRenta":notificacionRenta, "consultaDatosServicios":consultaDatosServicios, "productosElegidos":productosElegidos, "nombreSucursal":nombreSucursal, "notificacionCita":notificacionCita})
    
    else:
        return render(request,"1 Login/login.html")


def actualizarPaqueteCertificados(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idProductoPaqueteEditar = request.POST['idServicioEditar']
            
            #Nombre de servicio
            consultaServicio = ServiciosCertificados.objects.filter(id_servicio_certificado = idProductoPaqueteEditar)
            for datoServicio in consultaServicio:
                nombreServicio = datoServicio.nombre
            
            nameInputEliminar = "eliminarProducto"
            nameInputCantidad = "cantidadProducto"
            
            consultaProductosServicio = ProductosServiciosCertificados.objects.filter(servicio_certificado_id__id_servicio_certificado = idProductoPaqueteEditar)
            
            for producto in consultaProductosServicio:
                idProductoUtilizado = producto.producto_gasto_id
                
                nameInputPorProductoEliminar = nameInputEliminar+str(idProductoUtilizado)
                nameInputCantidadProductoEditar = nameInputCantidad+str(idProductoUtilizado)
                
                
            
                if request.POST.get(nameInputPorProductoEliminar, False): #Checkeado Eliminar producto
                    borrado = ProductosServiciosCertificados.objects.get(producto_gasto_id = idProductoUtilizado, servicio_certificado_id__id_servicio_certificado = idProductoPaqueteEditar)
                    borrado.delete()
                    actualizacionProductoPaquete = True
                    
                elif request.POST.get(nameInputPorProductoEliminar, True): #No checkeado, actualizar producto
                    cantidadProductoActualizar = request.POST[nameInputCantidadProductoEditar]
                    actualizacionProductoPaquete = ProductosServiciosCertificados.objects.filter(producto_gasto_id = idProductoUtilizado).update(cantidad_utilizada = cantidadProductoActualizar)
                
                
            #Agregar más productos.
            masProductos = request.POST['masProductos']
            if masProductos == "noMasProductos":
                
                if actualizacionProductoPaquete or borrado: 
                    request.session['paqueteProductoActualizado'] = "El paquete del servicio "+nombreServicio+" ha sido actualizado correctamente!"
                    return redirect('/verServiciosCertificado/')
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
                    
                    registroProducto = ProductosServiciosCertificados(servicio = Servicios.objects.get(id_servicio=idProductoPaqueteEditar),producto_gasto=ProductosGasto.objects.get(id_producto =idProductoBD),cantidad=cantidadProductoBD)
                    registroProducto.save()
                
                if actualizacionProductoPaquete or borrado or registroProducto: 
                    request.session['paqueteProductoActualizado'] = "El paquete del servicio "+nombreServicio+" ha sido actualizado correctamente!"
                    return redirect('/verServiciosCertificado/')

def guardarVenderCertificado(request):
    if "idSesion" in request.session:
        idEmpleado = request.session['idSesion']

        if request.method == "POST":
            
            #Datos para la venta
            
            tipoPago = request.POST["tipoPago"]

            if tipoPago == "Efectivo":
                esEnEfectivo = True
            elif tipoPago == "Tarjeta":
                esConTarjeta = True
                tipoTarjeta = request.POST["tipoTarjeta"]
                referencia = request.POST["referencia"]
            elif tipoPago == "Transferencia":
                esConTransferencia = True
                claveRastreo = request.POST["claveRastreo"]

            empleadoVendedor = idEmpleado

            clienteSeleccionado = request.POST["clienteSeleccionado"] #Puede ser clienteMomentaneo o tener el id del cliente.
            nombreBeneficiaria = request.POST["nombreBeneficiaria"]
            correoBeneficiaria = request.POST["correoBeneficiaria"]
            if correoBeneficiaria == "":
                conCorreo=False
            else:
                conCorreo=True


                
            #Datos para certificado
            codigoCertificadoNuevo = request.POST["codigoCertificadoNuevo"] #Codigo de nuevo certificado.
            fechaActual = datetime.now()
            fechaVigencia = fechaActual + relativedelta(months=1)

            sucursalCertificado = request.POST["sucursalCertificado"]

            consultaServiciosCertificado = ServiciosCertificados.objects.filter(sucursal_id__id_sucursal = sucursalCertificado)
            
            stringServiciosAVender = ""
            stringCantidadesAVender = ""
            stringPreciosAVender = ""
            stringEstatusAVender = ""
            contadorServiciosEnCarrito = 0

            montoTotalAPagar = 0
            datosServicios = []
            listaServiciosSeleccionados = []
            for servicio in consultaServiciosCertificado:
                print("Entro al if principal")

                idDelServicio = servicio.id_servicio_certificado
                nombreServicio = servicio.nombre
                precioServicio = servicio.precio
                datosServicios.append([nombreServicio,precioServicio])
                name = "checkboxServicio"+str(idDelServicio)
            
                # Inicializar servicioVendido como False
                servicioVendido = False

                if request.POST.get(name):  # Servicio checkeado
                    servicioVendido = True
                else:  # Servicio no checkeado
                    servicioVendido = False    

                if servicioVendido:
                    print("entre al if!!  servicioVendido")
                    contadorServiciosEnCarrito = contadorServiciosEnCarrito + 1

                    if contadorServiciosEnCarrito == 1:
                        print("Entre al if contadorServiciosEnCarrito")
                        stringServiciosAVender = str(idDelServicio)
                        stringCantidadesAVender = "1"
                        stringPreciosAVender = str([nombreServicio,precioServicio])
                        stringEstatusAVender = "P"
                        
                    else:
                        print("Entre al else")
                        stringServiciosAVender = stringServiciosAVender+ ","+str(idDelServicio)
                        stringCantidadesAVender = stringCantidadesAVender+ ",1"
                        stringPreciosAVender = stringPreciosAVender+ ","+str(precioServicio)
                        stringEstatusAVender = stringEstatusAVender+ ",P"
                        
                    montoTotalAPagar = montoTotalAPagar + precioServicio

                    listaServiciosSeleccionados.append([nombreServicio,precioServicio])
                else:
                    print("entro al else pendejo")
                
                print(montoTotalAPagar)

            
            #Guardar la venta
            horaVenta= datetime.now().time()
            if tipoPago == "Efectivo":
                if clienteSeleccionado == "clienteMomentaneo":
                    registroVenta = Ventas(fecha_venta = fechaActual, hora_venta = horaVenta, tipo_pago = tipoPago, empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                    ids_productos = "",cantidades_productos = "",ids_servicios_corporales = "",cantidades_servicios_corporales = "", ids_servicios_faciales = "", cantidades_servicios_faciales = "",
                    monto_pagar = montoTotalAPagar, credito = "N", sucursal = Sucursales.objects.get(id_sucursal = sucursalCertificado) )
                else:
                    registroVenta = Ventas(fecha_venta = fechaActual, hora_venta = horaVenta, tipo_pago = tipoPago, empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor), cliente = Clientes.objects.get(id_cliente = clienteSeleccionado),
                    monto_pagar = montoTotalAPagar, credito = "N", sucursal = Sucursales.objects.get(id_sucursal = sucursalCertificado) )

            elif tipoPago == "Tarjeta":
                if clienteSeleccionado == "clienteMomentaneo":
                    registroVenta = Ventas(fecha_venta = fechaActual, hora_venta = horaVenta, tipo_pago = tipoPago, empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                    ids_productos = "",cantidades_productos = "",ids_servicios_corporales = "",cantidades_servicios_corporales = "", ids_servicios_faciales = "", cantidades_servicios_faciales = "",
                    monto_pagar = montoTotalAPagar, credito = "N", sucursal = Sucursales.objects.get(id_sucursal = sucursalCertificado), tipo_tarjeta =  tipoTarjeta, referencia_pago_tarjeta = referencia)
                else:
                    registroVenta = Ventas(fecha_venta = fechaActual, hora_venta = horaVenta, tipo_pago = tipoPago, empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor), cliente = Clientes.objects.get(id_cliente = clienteSeleccionado),
                    ids_productos = "",cantidades_productos = "",ids_servicios_corporales = "",cantidades_servicios_corporales = "", ids_servicios_faciales = "", cantidades_servicios_faciales = "",
                    monto_pagar = montoTotalAPagar, credito = "N", sucursal = Sucursales.objects.get(id_sucursal = sucursalCertificado), tipo_tarjeta =  tipoTarjeta, referencia_pago_tarjeta = referencia)


            elif tipoPago == "Transferencia":
                if clienteSeleccionado == "clienteMomentaneo":
                    registroVenta = Ventas(fecha_venta = fechaActual, hora_venta = horaVenta, tipo_pago = tipoPago, empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor),
                    ids_productos = "",cantidades_productos = "",ids_servicios_corporales = "",cantidades_servicios_corporales = "", ids_servicios_faciales = "", cantidades_servicios_faciales = "",
                    monto_pagar = montoTotalAPagar, credito = "N", sucursal = Sucursales.objects.get(id_sucursal = sucursalCertificado), clave_rastreo_transferencia = claveRastreo)
                else:
                    registroVenta = Ventas(fecha_venta = fechaActual, hora_venta = horaVenta, tipo_pago = tipoPago, empleado_vendedor = Empleados.objects.get(id_empleado = empleadoVendedor), cliente = Clientes.objects.get(id_cliente = clienteSeleccionado),
                    ids_productos = "",cantidades_productos = "",ids_servicios_corporales = "",cantidades_servicios_corporales = "", ids_servicios_faciales = "", cantidades_servicios_faciales = "",
                    monto_pagar = montoTotalAPagar, credito = "N", sucursal = Sucursales.objects.get(id_sucursal = sucursalCertificado), clave_rastreo_transferencia = claveRastreo)
            registroVenta.save()
            #If venta guardada.. Guardar certificado e imprimir ticket\
            if registroVenta:
                ultimoIdVenta = 0 
                consultaTodasLasVentas = Ventas.objects.all()
                for venta in consultaTodasLasVentas:
                    ultimoIdVenta = venta.id_venta
                if clienteSeleccionado == "clienteMomentaneo":
                    if conCorreo:
                        registroCertificado = CertificadosProgramados(codigo_certificado= codigoCertificadoNuevo, fecha_alta= fechaActual, vigencia = fechaVigencia, lista_servicios_certificados = stringServiciosAVender, lista_cantidades_servicios = stringCantidadesAVender, lista_precios =stringPreciosAVender, lista_servicios_efectuados = stringEstatusAVender,
                        nombre_beneficiaria = nombreBeneficiaria, monto_total_pagar = montoTotalAPagar, monto_total_canjeado = 0, estatus_certificado = "P", venta = Ventas.objects.get(id_venta = ultimoIdVenta),correo_beneficiaria = correoBeneficiaria)
                    else:

                        registroCertificado = CertificadosProgramados(codigo_certificado= codigoCertificadoNuevo, fecha_alta= fechaActual, vigencia = fechaVigencia, lista_servicios_certificados = stringServiciosAVender, lista_cantidades_servicios = stringCantidadesAVender, lista_precios =stringPreciosAVender, lista_servicios_efectuados = stringEstatusAVender,
                        nombre_beneficiaria = nombreBeneficiaria, monto_total_pagar = montoTotalAPagar, monto_total_canjeado = 0, estatus_certificado = "P", venta = Ventas.objects.get(id_venta = ultimoIdVenta)  )
                else:
                    if conCorreo:
                        registroCertificado = CertificadosProgramados(codigo_certificado= codigoCertificadoNuevo, fecha_alta= fechaActual, vigencia = fechaVigencia, lista_servicios_certificados = stringServiciosAVender, lista_cantidades_servicios = stringCantidadesAVender, lista_precios =stringPreciosAVender, lista_servicios_efectuados = stringEstatusAVender, cliente_compro = Clientes.objects.get(id_cliente = clienteSeleccionado),
                        nombre_beneficiaria = nombreBeneficiaria, monto_total_pagar = montoTotalAPagar, monto_total_canjeado = 0, estatus_certificado = "P", venta = Ventas.objects.get(id_venta = ultimoIdVenta),correo_beneficiaria = correoBeneficiaria)
                    else:
                        registroCertificado = CertificadosProgramados(codigo_certificado= codigoCertificadoNuevo, fecha_alta= fechaActual, vigencia = fechaVigencia, lista_servicios_certificados = stringServiciosAVender, lista_cantidades_servicios = stringCantidadesAVender, lista_precios =stringPreciosAVender, lista_servicios_efectuados = stringEstatusAVender, cliente_compro = Clientes.objects.get(id_cliente = clienteSeleccionado),
                        nombre_beneficiaria = nombreBeneficiaria, monto_total_pagar = montoTotalAPagar, monto_total_canjeado = 0, estatus_certificado = "P", venta = Ventas.objects.get(id_venta = ultimoIdVenta)  )
                registroCertificado.save()
                if registroCertificado:
                    #Imprimir Ticket
                    fechaActualConFormato = fechaActual.strftime('%Y/%m/%d')
                    #Empleado Vendedor
                    empleadoVendedor = Empleados.objects.filter(id_empleado = empleadoVendedor)
                    for datoEmpleado in empleadoVendedor:
                        nombreEmpleado = datoEmpleado.nombres
                        apellidoPaternoEmpleado= datoEmpleado.apellido_paterno
                    nombreCompletoEmpleadoVendedor = nombreEmpleado + " " + apellidoPaternoEmpleado

                    #Datos Sucursal
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalCertificado)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        telefonoSucursal = datoSucursal.telefono
                        direccionSucursal = datoSucursal.direccion 

                    #Datos Cliente
                    if clienteSeleccionado == "clienteMomentaneo":
                        clienteTicket = "Momentaneo"
                    else:
                        consultaCliente = Clientes.objects.filter(id_cliente = clienteSeleccionado)
                        for datoCliente in consultaCliente:
                            idClienteticket = datoCliente.id_cliente
                            nombreCliente = datoCliente.nombre_cliente
                            apellidoCliente = datoCliente.apellidoPaterno_cliente
                        clienteTicket= nombreCliente + " " + apellidoCliente

                    #Hora Venta
                    horaVenta = horaVenta.strftime("%H:%M:%S")
                    #Obtener las impresoras
                    impresoras = Conector.ConectorV3.obtenerImpresoras()
                    
                    contadorDeTickets=0
                    for x in range (2):
                        contadorDeTickets = contadorDeTickets+1
                        c = Conector.ConectorV3()
                        c.Corte(1)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.CargarImagenLocalEImprimir("C:\\COSTABELLA\\sistemaCostabella\\static\\images\\anegragrande.png", 0, 216)
                        c.EscribirTexto("\n")
                        c.EstablecerTamañoFuente(1,1)
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("Sucursal:"+nombreSucursal+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("TEL:"+telefonoSucursal+"\n")
                        c.TextoSegunPaginaDeCodigos(2, "cp850", direccionSucursal+"\n")
                        
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("================================================\n")
                        c.EstablecerTamañoFuente(2,2)
                        c.EscribirTexto("VENTAS #"+str(ultimoIdVenta)+"\n")
                        c.EscribirTexto(codigoCertificadoNuevo+"\n")
                        c.EstablecerEnfatizado(False)
                        c.EstablecerAlineacion(Conector.ALINEACION_IZQUIERDA)
                        c.EstablecerTamañoFuente(1,1)
                        c.EscribirTexto("\n")
                        c.EscribirTexto(str(fechaActualConFormato)+" - "+str(horaVenta)+" hrs.\n")
                        c.EscribirTexto("Atendida por:"+nombreCompletoEmpleadoVendedor+"\n")
                        c.EscribirTexto("\n")
                      
                        #Listado de servicios
                        for servicio in listaServiciosSeleccionados:
                            nombreServicioTicket = servicio[0]
                            precioServicioTicket = servicio[1]
                            precioServicioTicketRedondeado = round(precioServicioTicket,2)
                            precioServicioTicketRedondeadoStr = str(precioServicioTicketRedondeado)
                            precioServicioDivididoEnElPunto = precioServicioTicketRedondeadoStr.split(".")
                            longitudPrecioServicio = len(str(precioServicioDivididoEnElPunto[0]))
                            longitudPrecioServicioEntero = int(longitudPrecioServicio)
                            caracteresServicio = len(nombreServicioTicket)

                            if longitudPrecioServicioEntero == 1:
                                espacio = 38
                            elif longitudPrecioServicioEntero == 2:
                                espacio = 37
                            elif longitudPrecioServicioEntero == 3:
                                espacio = 36
                            elif longitudPrecioServicioEntero == 4:
                                espacio = 35
                            elif longitudPrecioServicioEntero == 5:
                                espacio = 34
                            elif longitudPrecioServicioEntero == 6:
                                espacio = 33
                            numeroEspacios = espacio - int(caracteresServicio)
                            espaciosTicket = ""
                            for x in range(numeroEspacios):
                                espacioMini = " "
                                espaciosTicket = espaciosTicket + espacioMini
                            c.EscribirTexto("1 x "+ nombreServicioTicket + espaciosTicket + str(precioServicioTicketRedondeadoStr)+"\n") 

                        c.EscribirTexto("\n")
                        c.EscribirTexto("\n")

                        c.EstablecerTamañoFuente(2,2)
                        c.EstablecerAlineacion(Conector.ALINEACION_DERECHA)
                        c.EscribirTexto("TOTAL: $"+str(montoTotalAPagar)+"\n")
                        c.EscribirTexto("\n")

                        c.EstablecerEnfatizado(True)
                        c.EstablecerTamañoFuente(1,1)
                        
                        c.EscribirTexto("========= IVA incluido en el precio =========\n")
                        c.EscribirTexto("\n")
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.TextoSegunPaginaDeCodigos(2, "cp850", "INFORMACION DE PAGO.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto("\n")
                        if tipoPago == "Efectivo":
                            c.EscribirTexto("Pago en Efectivo \n")
                        elif tipoPago == "Tarjeta":
                            c.EscribirTexto("Pago con Tarjeta de "+str(tipoTarjeta)+"\n")
                            c.EscribirTexto("Referencia: "+referencia+"\n")
                        elif tipoPago == "Transferencia":
                            c.EscribirTexto("Pago con Transferencia\n")
                            c.EscribirTexto("Clave de Rastreo: "+claveRastreo+"\n")
                        c.EscribirTexto("\n")
                        
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        c.EscribirTexto("INFORMACION DEL CLIENTE.\n")
                        if clienteTicket == "Momentaneo":
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("Cliente Momentaneo\n")
                        else:
                            c.EstablecerEnfatizado(False)
                            c.EscribirTexto("ID: "+str(idClienteticket)+" - "+clienteTicket+"\n")
                        c.EscribirTexto("\n")
                        c.EstablecerEnfatizado(True)
                        c.EscribirTexto("INFORMACION DE LA BENEFICIARIA.\n")
                        c.EstablecerEnfatizado(False)
                        c.EscribirTexto(nombreBeneficiaria+"\n")
                        if conCorreo:
                            c.EscribirTexto(correoBeneficiaria+"\n")


                        c.EscribirTexto("=========== Gracias por su compra!! ===========\n")
                        c.EstablecerTamañoFuente(2, 2)
                        c.EstablecerEnfatizado(True)
                        c.EstablecerAlineacion(Conector.ALINEACION_CENTRO)
                        if contadorDeTickets == 1:
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

                            

                    if conCorreo:
                        try:
                            #Mandar correo.
                            correo = correoBeneficiaria
                            asunto = "Costabella | Nuevo certificado de regalo!!"
                            plantilla = "19 Certificados/correoCertificado.html"
                            html_mensaje = render_to_string(plantilla,{"nombreSucursal":nombreSucursal, "fechaActualConFormato":fechaActualConFormato, "nombreCompletoEmpleadoVendedor":nombreCompletoEmpleadoVendedor,
                            "codigoCertificadoNuevo":codigoCertificadoNuevo,"montoTotalAPagar":montoTotalAPagar, "datosServicios":datosServicios, "telefonoSucursal":telefonoSucursal, "direccionSucursal":direccionSucursal,
                            "nombreBeneficiaria":nombreBeneficiaria, "clienteTicket":clienteTicket,"fechaVigencia":fechaVigencia}) #Aqui va el diccionario de datos.
                            email_remitente = settings.EMAIL_HOST_USER
                            email_destino = [correo]
                            mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                            mensaje.content_subtype = 'html'
                            #Mandar excel en el correo.
                            mensaje.send()
                            
                        except:
                            print("Error al mandar correo")
                            

                            



                        


                    #Variable para notificaciones
                    request.session["certificadoGuardado"] = "El certificado se ha guardado correctamente."
                    
                    return redirect("/verCertificadosProgramados/")

            
       
    
    
    else:
        return render(request,"1 Login/login.html")  

def verCertificadosProgramados(request):
    if "idSesion" in request.session:
     
        #Variables de sesión
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

        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)

        if request.method == "POST":
            
            sucursalCertificados = request.POST["sucursalCertificados"]


            consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalCertificados)
            for datoSucursal in consultaSucursal:
                nombreSucursalCertificados = datoSucursal.nombre
            
            consultaCertificadosSucursal = CertificadosProgramados.objects.all()

            certificadosPendientes = []
            certificadosCanjeados = []

            for certificado in consultaCertificadosSucursal:
                venta = certificado.venta_id
                consultaVenta = Ventas.objects.filter(id_venta = venta)
                for dato in consultaVenta:
                    idSucursalVenta = dato.sucursal_id

                    
                intSucursalMandada = int(sucursalCertificados)
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
                        
                        servicios.append(nombreServicio)


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
                    elif estatusCertificado == "C":
                        certificadosCanjeados.append([idCertificado,codigoCertificado,fechaAlta, vigencia, listaZipeada, nombreCliente, nombreBeneficiaria, montoTotalAPagar])
            
            return render(request,"19 Certificados/verCertificados.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "nombreSucursalCertificados":nombreSucursalCertificados, "certificadosPendientes":certificadosPendientes, "certificadosCanjeados":certificadosCanjeados})
                
        else:

            if tipoUsuario == "esAdmin":
                sucursales = Sucursales.objects.all()
            else:
                infoEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in infoEmpleado:
                    idSucursal = datoEmpleado.sucursal_id

                sucursales = Sucursales.objects.filter(id_sucursal = idSucursal)

            if "certificadoGuardado" in request.session:
                certificadoGuardado = request.session["certificadoGuardado"]
                del request.session["certificadoGuardado"]
                return render(request,"19 Certificados/seleccionarSucursalVerCertificados.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "sucursales":sucursales, "certificadoGuardado":certificadoGuardado})
            
            if "certificadoCanjeado" in request.session:
                certificadoCanjeado = request.session["certificadoCanjeado"]
                del request.session["certificadoCanjeado"]
                return render(request,"19 Certificados/seleccionarSucursalVerCertificados.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "sucursales":sucursales, "certificadoCanjeado":certificadoCanjeado})
            return render(request,"19 Certificados/seleccionarSucursalVerCertificados.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "sucursales":sucursales})
    
    
    else:
        return render(request,"1 Login/login.html")

def verServiciosParaCanjear(request):
    if "idSesion" in request.session:
     
        #Variables de sesión
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

        consultaPermisos = Permisos.objects.filter(id_empleado_id__id_empleado = idEmpleado)

        if request.method == "POST": #Si le apreto al boton del boletito
            
            idCertificado = request.POST["idCertificado"]

            consultaCertificado = CertificadosProgramados.objects.filter(id_certificado = idCertificado)

            for datoCertificado in consultaCertificado:
                idClienteQueCompro = datoCertificado.cliente_compro_id

                listaDeIdsDeServiciosACanjear = datoCertificado.lista_servicios_certificados
                listaEstatusServiciosCanjeados = datoCertificado.lista_servicios_efectuados

            #datos del cliente
            consultaCliente = Clientes.objects.filter(id_cliente = idClienteQueCompro)

            for datoCliente in consultaCliente:
                nombreCliente = datoCliente.nombre_cliente
                apellidoCliente = datoCliente.apellidoPaterno_cliente

            nombreCompletoCliente = nombreCliente + " " + apellidoCliente

            #Datos de los servicios

            #Separar cada servicio y meterlo a un arreglo
            arregloIdsServiciosACanjear = listaDeIdsDeServiciosACanjear.split(",")
            arregloEstatusServicios = listaEstatusServiciosCanjeados.split(",")

            zipServicios = zip(arregloIdsServiciosACanjear, arregloEstatusServicios)

            arregloServiciosTabla = []
            arregloServiciosTablaCanjeados = []
            for servicio, estatus in zipServicios:
                intServicio = int(servicio)
                consultaServicio = ServiciosCertificados.objects.filter(id_servicio_certificado = intServicio)

                for datoServicio in consultaServicio:
                    codigoServicio = datoServicio.codigo_servocio
                    nombreServicio = datoServicio.nombre
                    precioServicio = datoServicio.precio
                    descripcionServicio = datoServicio.descripcion

                if estatus == "P":

                    arregloServiciosTabla.append([intServicio,codigoServicio,nombreServicio,precioServicio,descripcionServicio])

                else:
                    arregloServiciosTablaCanjeados.append([intServicio,codigoServicio,nombreServicio,precioServicio,descripcionServicio])

            
            #Separar arreglo de estados
            

            listaZipeadaServicios = zip(arregloServiciosTabla,arregloEstatusServicios )
            listaZipeadaServiciosCanjeados = zip(arregloServiciosTablaCanjeados,arregloEstatusServicios )
                
               
           
            if "viendeDeCita" in request.POST:
                idDeCita = request.POST["viendeDeCita"]
                vieneDeCita = True
                consultaCita = Citas.objects.filter(id_cita=idDeCita)
                for datoCertificado in consultaCita:

                    certificadoServicio = datoCertificado.certificado_servicio
                certificadoServicioSeparado = certificadoServicio.split("-")
                idServicioCita = certificadoServicioSeparado[1]
                idServicioCitaEntero = int(idServicioCita)
                
                arregloServiciosTablaCita = []

                for servicioDisponible in arregloServiciosTabla:
                    idServicioDisponible = servicioDisponible[0]
                    idServicioDisponibleEntero = int(idServicioDisponible)
                    
                    if idServicioCitaEntero == idServicioDisponibleEntero:
                        disponibleCita = "si"
                    else:
                        disponibleCita = "no"

                    arregloServiciosTablaCita.append(disponibleCita)

                listaZipeadaServicios = zip(arregloServiciosTabla,arregloEstatusServicios, arregloServiciosTablaCita )



                return render(request,"19 Certificados/verServiciosParaCanjear.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "idCertificado":idCertificado, "consultaCertificado":consultaCertificado, "nombreCompletoCliente":nombreCompletoCliente, "listaZipeadaServicios":listaZipeadaServicios,
                                                                            "arregloServiciosTabla":arregloServiciosTabla, "listaZipeadaServiciosCanjeados":listaZipeadaServiciosCanjeados, "idDeCita":idDeCita, "vieneDeCita":vieneDeCita})

            return render(request,"19 Certificados/verServiciosParaCanjear.html",{"nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "puestoEmpleado":puestoEmpleado, "letra":letra,
                                                                            "notificacionRenta":notificacionRenta,"consultaPermisos":consultaPermisos,"notificacionCita":notificacionCita, 
                                                                            "idCertificado":idCertificado, "consultaCertificado":consultaCertificado, "nombreCompletoCliente":nombreCompletoCliente, "listaZipeadaServicios":listaZipeadaServicios,
                                                                            "arregloServiciosTabla":arregloServiciosTabla, "listaZipeadaServiciosCanjeados":listaZipeadaServiciosCanjeados})
                
        
    
    
    else:
        return render(request,"1 Login/login.html")

def canjearCertificado(request):
    if "idSesion" in request.session:
     
        if request.method == "POST": #Si se dio clic al botón de canjear certificado
            
            idCertificadoACanjear = request.POST["idCertificadoACanjear"]
            

            consultaCertificado = CertificadosProgramados.objects.filter(id_certificado = idCertificadoACanjear)

            for datoCertificado in consultaCertificado:
                listaServicios = datoCertificado.lista_servicios_certificados
                codigoCertificado = datoCertificado.codigo_certificado
                listaEstatus = datoCertificado.lista_servicios_efectuados
                correoBeneficiaria = datoCertificado.correo_beneficiaria
                nombreBeneficiaria = datoCertificado.nombre_beneficiaria
                fechaAlta = datoCertificado.fecha_alta
                fechaVigencia = datoCertificado.vigencia
                idVenta = datoCertificado.venta_id

            #Consulta de id de usucrsal
            consultaVenta = Ventas.objects.filter(id_venta = idVenta)
            for datoVenta in consultaVenta:
                idSucursalCertificado = datoVenta.sucursal_id

            consultaDatosSucursal = Sucursales.objects.filter(id_sucursal = idSucursalCertificado)
            for datoSucursal in consultaDatosSucursal:
                nombreSucursalCertificado = datoSucursal.nombre
                telefonoSucursal = datoSucursal.telefono
                direccionSucursal = datoSucursal.direccion

            arregloServicios = listaServicios.split(",")
            arregloEstatus = listaEstatus.split(",")

            listazipeada = zip(arregloServicios,arregloEstatus)


            serviciosCanjeadosCorreo = []
            serviciosNoCanjeadosCorreo = []

            stringEstatusServicios = ""
            contadorServicios = 0
            for servicio, estatus in listazipeada:
                
                contadorServicios = contadorServicios + 1
                idDelServicio = servicio
                name = "checkboxServicio"+str(idDelServicio)

                #Consulta del servicio
                consultaServicio = ServiciosCertificados.objects.filter(id_servicio_certificado = idDelServicio)
                for datoServicio in consultaServicio:
                    nombreServicio = datoServicio.nombre


                if estatus == "P":
                
                    if request.POST.get(name, False): #Servicio Checkeado
                        servicioCanjeado = True
                    elif request.POST.get(name, True): #Servicio No checkeado
                        servicioCanjeado = False


                    if servicioCanjeado: #El servicio tiene chequeado el checkbox..
                        
                        if contadorServicios == 1:
                            stringEstatusServicios = "C"
                        else:
                            stringEstatusServicios = stringEstatusServicios + ",C"

                        #Dar de baja los productos gasto que utiliza
                        idDelServicioInt = int(idDelServicio)
                        consultaTratamientoProductos = ProductosServiciosCertificados.objects.filter(servicio_certificado_id__id_servicio_certificado = idDelServicioInt)
                        if consultaTratamientoProductos:
                            sinProductos = False

                            idsProductosQueUtilizaElTratamiento = []
                            for producto in consultaTratamientoProductos:
                                idProducto = producto.producto_gasto_id
                                cantidadUtilizada = producto.cantidad_utilizada

                                idsProductosQueUtilizaElTratamiento.append([idProducto, cantidadUtilizada])

                            for producto in idsProductosQueUtilizaElTratamiento:
                                idProductoSF = int(producto[0])
                                cantidadPSF = int(producto[1])

                                consultaProducto = ProductosGasto.objects.filter(id_producto = idProductoSF)
                                for dato in consultaProducto:
                                    cantidadActualEnExistencia = dato.cantidad
                                    cuantificable = dato.contenido_cuantificable  #N O S
                                
                                if cuantificable == "S":
                                    cantidadARestar = 1 * cantidadPSF
                                    actualizacionCantidad = cantidadActualEnExistencia - cantidadARestar

                                    actualizarProducto = ProductosGasto.objects.filter(id_producto = idProductoSF).update(cantidad = actualizacionCantidad)
                        else:
                            sinProductos = True

                        serviciosCanjeadosCorreo.append(nombreServicio)

                        

                    else: #El servicio aun está sin canjear.
                        print("nochequeado")
                        if contadorServicios == 1:
                            stringEstatusServicios = "P"
                        else:
                            stringEstatusServicios = stringEstatusServicios + ",P"

                        serviciosNoCanjeadosCorreo.append(nombreServicio)
                else:
                    if contadorServicios == 1:
                        stringEstatusServicios = "C"
                    else:
                        stringEstatusServicios = stringEstatusServicios + ",C"
                    
                    serviciosCanjeadosCorreo.append(nombreServicio)

            arregloNuevosEstatus = stringEstatusServicios.split(",")

            certificadoSinCanjearAlCien = False


            for estatus in arregloNuevosEstatus:
                estatusNuevo = estatus
                if estatusNuevo == "P":
                    certificadoSinCanjearAlCien = True

            
            if certificadoSinCanjearAlCien:
            #Actualizacion
                #Servicios pendientes por canjear

                #Mandar correo electrónico

                fechaActual = datetime.now()
                fechaActualConFormato = fechaActual.strftime('%Y/%m/%d')

                try:
                    #Mandar correo.
                    correo = correoBeneficiaria
                    asunto = "Costabella | Servicios canjeados!!"
                    plantilla = "19 Certificados/correoCertificadoPendiente.html"
                    html_mensaje = render_to_string(plantilla,{"nombreSucursalCertificado":nombreSucursalCertificado, "fechaActualConFormato":fechaActualConFormato, "fechaAlta":fechaAlta, "fechaVigencia":fechaVigencia,
                    "codigoCertificado":codigoCertificado, "serviciosCanjeadosCorreo":serviciosCanjeadosCorreo, "serviciosNoCanjeadosCorreo":serviciosNoCanjeadosCorreo,"telefonoSucursal":telefonoSucursal, "direccionSucursal":direccionSucursal,
                    "nombreBeneficiaria":nombreBeneficiaria}) #Aqui va el diccionario de datos.
                    email_remitente = settings.EMAIL_HOST_USER
                    email_destino = [correo]
                    mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                    mensaje.content_subtype = 'html'
                    #Mandar excel en el correo.
                    mensaje.send()
                    
                except:
                    print("Error al mandar correo")
                actualizacionCertificado = CertificadosProgramados.objects.filter(id_certificado = idCertificadoACanjear).update(lista_servicios_efectuados = stringEstatusServicios)
            else:
                #Canjeado al 100%

                fechaActual = datetime.now()
                fechaActualConFormato = fechaActual.strftime('%Y/%m/%d')
                #Mandar correo electrónico
                try:
                    #Mandar correo.
                    correo = correoBeneficiaria
                    asunto = "Costabella | Certificado canjeado completamente!!"
                    plantilla = "19 Certificados/correoCertificadoCanjeado.html"
                    html_mensaje = render_to_string(plantilla,{"nombreSucursalCertificado":nombreSucursalCertificado, "fechaActualConFormato":fechaActualConFormato, "fechaAlta":fechaAlta, "fechaVigencia":fechaVigencia,
                    "codigoCertificado":codigoCertificado, "serviciosCanjeadosCorreo":serviciosCanjeadosCorreo, "serviciosNoCanjeadosCorreo":serviciosNoCanjeadosCorreo,"telefonoSucursal":telefonoSucursal, "direccionSucursal":direccionSucursal,
                    "nombreBeneficiaria":nombreBeneficiaria}) #Aqui va el diccionario de datos.
                    email_remitente = settings.EMAIL_HOST_USER
                    email_destino = [correo]
                    mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                    mensaje.content_subtype = 'html'
                    #Mandar excel en el correo.
                    mensaje.send()
                    
                except:
                    print("Error al mandar correo")

                actualizacionCertificado = CertificadosProgramados.objects.filter(id_certificado = idCertificadoACanjear).update(lista_servicios_efectuados = stringEstatusServicios, estatus_certificado = "C")
            
            if "vieneDeCita" in request.POST:
                idDeCita = request.POST["vieneDeCita"]
                actualizacionCita = Citas.objects.get(id_cita = idDeCita)
                actualizacionCita.estado_cita = "efectuada"
                actualizacionCita.save()

                try:
                    tokenTelegram = keysBotCostabella.tokenBotCostabellaCitas
                    botCostabella = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCostabella.idGrupo
                    
                    mensaje = "\U0001F381 CITA VENDIDA CERTIFICADO \U0001F381 \n El cliente "+nombreBeneficiaria+" acudió y efectuo la cita #"+str(idDeCita)+", correspondiente al certificado "+codigoCertificado
                    botCostabella.sendMessage(idGrupoTelegram,mensaje)
                except:
                    print("An exception occurred")
                
            request.session["certificadoCanjeado"] = "Se han canjeado uno o varios servicios del certificado "+str(codigoCertificado)

            return redirect("/verCertificadosProgramados/")

                
        
    
    
    else:
        return render(request,"1 Login/login.html")

