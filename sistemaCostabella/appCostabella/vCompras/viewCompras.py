
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent


# Importacion de modelos
from appCostabella.models import (ComprasGastos, ComprasRentas, ComprasVentas, Permisos,
                                  ProductosGasto, ProductosRenta,
                                  ProductosVenta, Sucursales)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)


def inventarioCompras(request):

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
        
        
        
        # contadores
        contadorComprasVentas = 0
        contadorComprasRentas = 0
        contadorComprasGastos = 0
        comprasParaVenta = ComprasVentas.objects.all()
        comprasParaRenta = ComprasRentas.objects.all()
        comprasParaGasto = ComprasGastos.objects.all()
        
        for compraVentac in comprasParaVenta:
            contadorComprasVentas = contadorComprasVentas + 1

        for compraRentac in comprasParaRenta:
            contadorComprasRentas = contadorComprasRentas + 1

        for compraGastoc in comprasParaGasto:
            contadorComprasGastos = contadorComprasGastos + 1
        
        # compras para ventas
        productosComprasVentas = []
        sucursalesComprasVentas = []
       
        for comprasVenta in comprasParaVenta:
            id_producto_comprado = comprasVenta.id_productoComprado_id
            

            datosProducto = ProductosVenta.objects.filter(id_producto = id_producto_comprado)
            for dato in datosProducto:
                codigo = dato.codigo_producto
                nombre = dato.nombre_producto
                id_sucursal = dato.sucursal_id
            nombreCompletoProductoCompra = codigo + " " + nombre

            datosSucursal = Sucursales.objects.filter(id_sucursal = id_sucursal)
            for datoSucursal in datosSucursal:
                nombreSucursal = datoSucursal.nombre

            productosComprasVentas.append(nombreCompletoProductoCompra)
            sucursalesComprasVentas.append(nombreSucursal)
           
            
        listaComprasProductosVenta = zip(comprasParaVenta, productosComprasVentas, sucursalesComprasVentas)
     
     

        # compras para rentas
        productosComprasRentas = []
        sucursalesComprasRentas = []
        for comprasRenta in comprasParaRenta:
            id_producto_comprado = comprasRenta.id_productoComprado_id
            

            datosProducto = ProductosRenta.objects.filter(id_producto = id_producto_comprado)
            for dato in datosProducto:
                codigo = dato.codigo_producto
                nombre = dato.nombre_producto
                id_sucursal = dato.sucursal_id
            nombreCompletoProductoCompra = codigo + " " + nombre

            datosSucursal = Sucursales.objects.filter(id_sucursal = id_sucursal)
            for datoSucursal in datosSucursal:
                nombreSucursal = datoSucursal.nombre

            productosComprasRentas.append(nombreCompletoProductoCompra)
            sucursalesComprasRentas.append(nombreSucursal)
           
            
        listaComprasProductosRenta = zip(comprasParaRenta, productosComprasRentas, sucursalesComprasRentas)
        

        # compras para gasto
        productosComprasGastos = []
        sucursalesComprasGastos = []
        for comprasGasto in comprasParaGasto:
            id_producto_comprado = comprasGasto.id_productoComprado_id
            

            datosProducto = ProductosGasto.objects.filter(id_producto = id_producto_comprado)
            for dato in datosProducto:
                codigo = dato.codigo_producto
                nombre = dato.nombre_producto
                id_sucursal = dato.sucursal_id
            nombreCompletoProductoCompra = codigo + " " + nombre

            datosSucursal = Sucursales.objects.filter(id_sucursal = id_sucursal)
            for datoSucursal in datosSucursal:
                nombreSucursal = datoSucursal.nombre

            productosComprasGastos.append(nombreCompletoProductoCompra)
            sucursalesComprasGastos.append(nombreSucursal)
           
            
        listaComprasProductosGasto = zip(comprasParaGasto, productosComprasGastos, sucursalesComprasGastos)
        
       
        
       
        
        return render(request, "7 Compras/inventarioCompras.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
        "contadorComprasVentas":contadorComprasVentas,
        "contadorComprasRentas":contadorComprasRentas,
        "contadorComprasGastos":contadorComprasGastos,
        "listaComprasProductosVenta":listaComprasProductosVenta,
        "listaComprasProductosRenta":listaComprasProductosRenta,
        "listaComprasProductosGasto":listaComprasProductosGasto,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")
    