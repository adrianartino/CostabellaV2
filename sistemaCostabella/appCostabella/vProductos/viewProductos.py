#Para ruta
from pathlib import Path
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

BASE_DIR = Path(__file__).resolve().parent.parent

from django.http.response import HttpResponse

# Archivo configuración de django
from django.conf import settings

#Libreria excel.
import xlwt
import numpy as np
#Para leer exceles.
import pandas as pd

# Librerías de fecha
from datetime import date, datetime

#Para mandar telegram
import telepot
#Plugin impresora termica
from appCostabella import keysBotCostabella

# Importacion de modelos
from appCostabella.models import (Clientes, ComprasGastos, ComprasRentas, ComprasVentas, Empleados, Permisos, ProductosGasto, ProductosRenta, ProductosVenta, Rentas, Sucursales)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)

#Correo electrónico
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from zebra import Zebra

def altaProductos(request):

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

        # retornar sucrusales
        sucursales = Sucursales.objects.all()
        if request.method == "POST":
            tipo_producto = request.POST['tipoProducto']  #Requerido
            nombre_producto = request.POST['nombreProducto']  #Requerido
            descripcion_producto = request.POST['descripcion']  #Requerido
            imagen_producto = request.FILES.get('imagenProducto') #No requerido
            
                
            sucursal = request.POST['sucursal'] #Requerido
            fechaAlta = datetime.today().strftime('%Y-%m-%d') #Requerido
            #fechaAlta = datetime.now()
            
            if tipo_producto == "venta":
                
                
            
                costo_compraVenta = request.POST['costoCompra']
                sku_producto = request.POST['skuProducto']  #Requerido
                nameInput = "checkboxMargen"
                if request.POST.get(nameInput, False): #Checkeado
                    margen = request.POST['margenManual']
                elif request.POST.get(nameInput, True): #No checkeado
                    margen = request.POST['margen']
                
                cantidad_altaProducto = request.POST['cantidadAltaProducto']
                cantidad_productoStock = request.POST['cantidadStock']

                margenstr = str(margen)
                if margen == "100":
                    porcentajeUtilidad = 1.00
                else:
                    
                    porcentajeUtilidad = "0." + str(margen)   #"0.20"
                procentajeUtilidadNeta = 1.00 + float(porcentajeUtilidad) 
                costoVenta = float(costo_compraVenta) * procentajeUtilidadNeta
                costoVenta = round(costoVenta, 2)
                
                productosVentas = ProductosVenta.objects.all()
                if productosVentas :
                    hayRegistros = True
                    ultimoCodigo =""
                    for venta in productosVentas:
                        ultimoCodigo= venta.codigo_producto
                        
                    primerDigito = ultimoCodigo[2]
                    segundoDigito = ultimoCodigo[3]
                    tercerDigito = ultimoCodigo[4]
                    cuartoDigito = ultimoCodigo[5]
                    
                    numeroCompleto = primerDigito + segundoDigito + tercerDigito + cuartoDigito
                    codigoCompleto = int(numeroCompleto)
                    codigoCompleto = codigoCompleto +1
                    codigo = "PV"+str(codigoCompleto)
             
                else:
                    codigo= "PV1000"

                #Calculo de costo a credito de producto
                costoVentaCredito = float(costoVenta) * 1.20
                costoVentaCredito = round(costoVentaCredito,2)

                #alta de producto para venta
                if imagen_producto == "":

                    registroProducto = ProductosVenta(codigo_producto = codigo,
                    codigo_barras = codigo,
                    tipo_producto = tipo_producto,
                    nombre_producto = nombre_producto, 
                    costo_compra = costo_compraVenta,
                    margen_ganancia_producto = margen,
                    costo_venta = costoVenta, 
                    costo_venta_a_credito = costoVentaCredito,
                    cantidad = cantidad_altaProducto, 
                    stock = cantidad_productoStock, 
                    descripcion = descripcion_producto,
                    fecha_alta = fechaAlta, 
                    sku_producto =sku_producto,
                    creado_por = Empleados.objects.get(id_empleado = idEmpleado),
                    sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                else:
                    registroProducto = ProductosVenta(codigo_producto = codigo,
                    codigo_barras = codigo,
                    tipo_producto = tipo_producto,
                    nombre_producto = nombre_producto, 
                    costo_compra = costo_compraVenta,
                    margen_ganancia_producto = margen,
                    costo_venta = costoVenta, 
                    costo_venta_a_credito = costoVentaCredito,
                    cantidad = cantidad_altaProducto, 
                    stock = cantidad_productoStock, 
                    descripcion = descripcion_producto,
                    imagen_producto = imagen_producto,
                    fecha_alta = fechaAlta, 
                    sku_producto =sku_producto,
                    creado_por = Empleados.objects.get(id_empleado = idEmpleado),
                    sucursal = Sucursales.objects.get(id_sucursal = sucursal))

                registroProducto.save()
                
                # Agregar compra en tabla de compras
                if registroProducto:
                    consultaProductoRecienAgregado = ProductosVenta.objects.filter(codigo_producto = codigo)
                    for dato in consultaProductoRecienAgregado:
                        idProductoRecienAgregado = dato.id_producto
                        nombreVenta = dato.nombre_producto
                        
                    totalCostoCompra = float(costo_compraVenta) * float(cantidad_altaProducto) 
                    totalCostoCompra = round(totalCostoCompra,2)
                        
                    registroCompra = ComprasVentas(id_productoComprado = ProductosVenta.objects.get(id_producto = idProductoRecienAgregado),
                                                   costo_unitario = costo_compraVenta,
                                                   cantidad_comprada = cantidad_altaProducto,
                                                   total_costoCompra = totalCostoCompra,
                                                   fecha_compra = fechaAlta)
                    registroCompra.save()

                    #ImprimirEtiquetas
                    fechaHoy = date.today()
                    cantidadEtiquetas = int(cantidad_altaProducto)
                    
                    primerDigitoCodigo = codigo[2]
                    segundoDigitoCodigo = codigo[3]
                    tercerDigitoCodigo = codigo[4]
                    cuartoDigitoCodigo = codigo[5]
                    
                    numeroCompletoCodigo = primerDigitoCodigo + segundoDigitoCodigo + tercerDigitoCodigo + cuartoDigitoCodigo
                    print(numeroCompletoCodigo)
                    codigoCompletoImprimir = str(numeroCompletoCodigo)

                    for x in range(cantidadEtiquetas):
                        
                        label = ("^XA~TA000~JSN^LT0^MNW^MTD^PON^PMN^LH0,0^JMA^PR2,2~SD30^JUS^LRN^CI0^XZ^XA^MMT^PW406^LL0203^LS0^FO0,160^GFA,00768,00768,00012,:Z64:eJxjYKAnYD/i3n5/zsfzIDb/u/f3z99tf98AZLOlJd69e/d44gEgm+/d+//n/v17fACs3vf+/TvmBw+A1T/uP7//8UMQm4EtgfGADAMjmM33gPGBHQMzmM3iABLjb4CKA9l89PCXvPzH57bHIWz+/7u/J4J9xcAge/9CeeEdiDjf/d2/baFs+fufy3nPQdX3/37/E6oeCNgZGOFsZgZuOJuB8TzCPsZz1PbBSAUAlzNF0w==:6D8B^FO128,128^GFA,01920,01920,00020,:Z64:eJztkT1Lw0Ach+8uoRdDKR2rtE2wy9mpHQotCCp+gRQaOwmCq0OkVh0KnukgBPETOJx1CefiR2jtUOjuKqGCrgFB3Opd2sGXDuKiQ39wy3MP9/L7AzDPPH8dNINBaFnJqlpNfoRUmvSruj5dv4o5g1nfkc4/XZvEXSOo285LL2xhGAqSIGTIONM54yPWSbi+YKWnyttuj0ILZrOLvczgQrCcu3Kba1PE0VJZO2Wu/JFyVgnWFFqyrXR5sR/uKYIhl7A8onnP14h2x0jk4eLgVaH3di3lpPpBS3oKKnodBDj3SaFsXvnSw4nG5aMCm/XDVaeQ3uhieZ63fE494XHCzBiNmsTpRqY3hra9fRzsP2x2VcnK1wttFwmvMrzxkavLO8JnA8dw0z4yjHF4ghNRByMd6cjjohgGdF2TCA5ALL5j2zUAuwDE05HnAqSZnPjR5DQy9TAMtqoHkaA6Uw/w6b547qRuddL2D+c2y5tnnv+bd/8tZhU=:C773^FO8,97^GB391,0,2^FS^BY2,3,61^FT295,29^BCI,,Y,N^FD>:PV>5"+codigoCompletoImprimir+"^FS^FT398,178^A0I,14,14^FH\^FD"+str(fechaHoy)+"^FS^FT236,119^A0I,14,14^FH\^FD"+nombreVenta+"^FS^FT237,143^A0I,11,12^FH\^FDNombre producto:^FS^FT376,143^A0I,17,16^FH\^FDCosto de venta^FS^FT376,110^A0I,28,28^FH\^FD$ "+str(costoVenta)+" ^FS^PQ1,0,1,Y^XZ")  
                        z = Zebra('ZDesigner GC420d')
                        z.output(label)




            elif tipo_producto == "renta":
            
                costo_de_compra = request.POST['costoCompraRenta']
                costo_Renta = request.POST['costoRenta']
          

                
                productosRentas = ProductosRenta.objects.all()
                if productosRentas :
                    hayRegistros = True
                    ultimoCodigo =""
                    for renta in productosRentas:
                        ultimoCodigo= renta.codigo_producto
                        
                    primerDigito = ultimoCodigo[2]
                    segundoDigito = ultimoCodigo[3]
                    tercerDigito = ultimoCodigo[4]
                    cuartoDigito = ultimoCodigo[5]
                    
                    numeroCompleto = primerDigito + segundoDigito + tercerDigito + cuartoDigito
                    codigoCompleto = int(numeroCompleto)
                    codigoCompleto = codigoCompleto +1
                    codigo = "PR"+str(codigoCompleto)
             
                else:
                    codigo= "PR1000"

                #alta de producto para venta
                if imagen_producto == "":

                    registroProducto = ProductosRenta(codigo_producto = codigo,
                    codigo_barras = codigo,
                    tipo_producto = tipo_producto,
                    nombre_producto = nombre_producto, 
                    costo_de_compra =costo_de_compra,
                    costo_renta = costo_Renta,
                 
                    cantidad = 1, 
                    estado_renta = "Sin rentar",
                    descripcion = descripcion_producto,
                    fecha_alta = fechaAlta, 
                    creado_por = Empleados.objects.get(id_empleado = idEmpleado),
                    sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                else:
                    registroProducto = ProductosRenta(codigo_producto = codigo,
                    codigo_barras = codigo,
                    tipo_producto = tipo_producto,
                    nombre_producto = nombre_producto, 
                    costo_de_compra =costo_de_compra,
                    costo_renta = costo_Renta,
                 
                    cantidad = 1, 
                    estado_renta = "Sin rentar",
                    descripcion = descripcion_producto,
                    imagen_producto = imagen_producto,
                    fecha_alta = fechaAlta, 
                    creado_por = Empleados.objects.get(id_empleado = idEmpleado),
                    sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    
                registroProducto.save()
                
                # Agregar compra en tabla de compras
                if registroProducto:
                    consultaProductoRecienAgregado = ProductosRenta.objects.filter(codigo_producto = codigo)
                    for dato in consultaProductoRecienAgregado:
                        idProductoRecienAgregado = dato.id_producto
                        
                    totalCostoCompra = float(costo_Renta) * float(1) 
                    totalCostoCompra = round(totalCostoCompra,2)
                        
                    registroCompra = ComprasRentas(id_productoComprado = ProductosRenta.objects.get(id_producto = idProductoRecienAgregado),
                                                   costo_unitario = costo_Renta,
                                                   cantidad_comprada = 1,
                                                   total_costoCompra = totalCostoCompra,
                                                   fecha_compra = fechaAlta)
                    registroCompra.save()

                    #ImprimirEtiquetas
                    fechaHoy = date.today()
                    cantidadEtiquetas = int(1)
                    
                    primerDigitoCodigo = codigo[2]
                    segundoDigitoCodigo = codigo[3]
                    tercerDigitoCodigo = codigo[4]
                    cuartoDigitoCodigo = codigo[5]
                    
                    numeroCompletoCodigo = primerDigitoCodigo + segundoDigitoCodigo + tercerDigitoCodigo + cuartoDigitoCodigo
                    codigoCompletoImprimir = str(numeroCompletoCodigo)

                    for x in range(cantidadEtiquetas):
                        label = ("^XA~TA000~JSN^LT0^MNW^MTD^PON^PMN^LH0,0^JMA^PR2,2~SD30^JUS^LRN^CI0^XZ^XA^MMT^PW406^LL0203^LS0^FO0,160^GFA,00768,00768,00012,:Z64:eJxjYKAnYD/i3n5/zsfzIDb/u/f3z99tf98AZLOlJd69e/d44gEgm+/d+//n/v17fACs3vf+/TvmBw+A1T/uP7//8UMQm4EtgfGADAMjmM33gPGBHQMzmM3iABLjb4CKA9l89PCXvPzH57bHIWz+/7u/J4J9xcAge/9CeeEdiDjf/d2/baFs+fufy3nPQdX3/37/E6oeCNgZGOFsZgZuOJuB8TzCPsZz1PbBSAUAlzNF0w==:6D8B^FO128,128^GFA,01920,01920,00020,:Z64:eJztkT1Lw0Ach+8uoRdDKR2rtE2wy9mpHQotCCp+gRQaOwmCq0OkVh0KnukgBPETOJx1CefiR2jtUOjuKqGCrgFB3Opd2sGXDuKiQ39wy3MP9/L7AzDPPH8dNINBaFnJqlpNfoRUmvSruj5dv4o5g1nfkc4/XZvEXSOo285LL2xhGAqSIGTIONM54yPWSbi+YKWnyttuj0ILZrOLvczgQrCcu3Kba1PE0VJZO2Wu/JFyVgnWFFqyrXR5sR/uKYIhl7A8onnP14h2x0jk4eLgVaH3di3lpPpBS3oKKnodBDj3SaFsXvnSw4nG5aMCm/XDVaeQ3uhieZ63fE494XHCzBiNmsTpRqY3hra9fRzsP2x2VcnK1wttFwmvMrzxkavLO8JnA8dw0z4yjHF4ghNRByMd6cjjohgGdF2TCA5ALL5j2zUAuwDE05HnAqSZnPjR5DQy9TAMtqoHkaA6Uw/w6b547qRuddL2D+c2y5tnnv+bd/8tZhU=:C773^FO8,97^GB391,0,2^FS^BY2,3,61^FT295,29^BCI,,Y,N^FD>:PR>5"+codigoCompletoImprimir+"^FS^FT398,178^A0I,14,14^FH\^FD"+str(fechaHoy)+"^FS^FT236,119^A0I,14,14^FH\^FD"+nombre_producto+"^FS^FT237,143^A0I,11,12^FH\^FDNombre vestido:^FS^FT376,143^A0I,17,16^FH\^FDCosto de renta^FS^FT376,110^A0I,28,28^FH\^FD$ "+str(costo_Renta)+" ^FS^PQ1,0,1,Y^XZ")
                       
                        z = Zebra('ZDesigner GC420d')
                        z.output(label)

                    #Checar si ese producto renta se va a vender
                    nameCheckboxVenderVestido = "sePuedeVender"
                    if request.POST.get(nameCheckboxVenderVestido,False): #checkbox chequeado
                        sePuedeVenderVestido = "Si"
                    elif request.POST.get(nameCheckboxVenderVestido,True): #checkbox deschequeado
                        sePuedeVenderVestido = "No"

                    if sePuedeVenderVestido == "Si":

                        costoVentaVestido = request.POST["costoVentaVestido"]
                        #Calculo de costo a credito de producto
                        costoVentaCreditoVestido = float(costo_Renta) * 1.20
                        costoVentaCreditoVestido = round(costoVentaCreditoVestido,2)
                        
                        #Obtener el ultimo codigo venta
                        productosVentas = ProductosVenta.objects.all()
                        if productosVentas :
                            hayRegistros = True
                            ultimoCodigo =""
                            for venta in productosVentas:
                                ultimoCodigo= venta.codigo_producto
                                
                            primerDigito = ultimoCodigo[2]
                            segundoDigito = ultimoCodigo[3]
                            tercerDigito = ultimoCodigo[4]
                            cuartoDigito = ultimoCodigo[5]
                            
                            numeroCompleto = primerDigito + segundoDigito + tercerDigito + cuartoDigito
                            codigoCompleto = int(numeroCompleto)
                            codigoCompleto = codigoCompleto +1
                            codigoPV = "PV"+str(codigoCompleto)
                    
                        else:
                            codigoPV= "PV1000"

                        #Registrar el producto como producto Venta
                        if imagen_producto == "":

                            registroProductoVenta = ProductosVenta(codigo_producto = codigoPV,
                            codigo_barras = codigoPV,
                            tipo_producto = tipo_producto,
                            nombre_producto = nombre_producto, 
                            costo_compra = costo_de_compra,
                            margen_ganancia_producto = 0,
                            costo_venta = costoVentaVestido, 
                            costo_venta_a_credito = costoVentaCreditoVestido,
                            cantidad = 1, 
                            stock = 1, 
                            descripcion = descripcion_producto,
                            fecha_alta = fechaAlta, 
                            sku_producto =codigoPV,
                            creado_por = Empleados.objects.get(id_empleado = idEmpleado),
                            sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                        else:
                           registroProductoVenta = ProductosVenta(codigo_producto = codigoPV,
                            codigo_barras = codigoPV,
                            tipo_producto = tipo_producto,
                            nombre_producto = nombre_producto, 
                            costo_compra = costo_de_compra,
                            margen_ganancia_producto = 0,
                            costo_venta = costoVentaVestido, 
                            costo_venta_a_credito = costoVentaCreditoVestido,
                            cantidad = 1, 
                            stock = 1, 
                            descripcion = descripcion_producto,
                            imagen_producto = imagen_producto,
                            fecha_alta = fechaAlta, 
                            sku_producto =codigoPV,
                            creado_por = Empleados.objects.get(id_empleado = idEmpleado),
                            sucursal = Sucursales.objects.get(id_sucursal = sucursal))

                        registroProductoVenta.save()

                        #Imprimir el ticket

                        # Agregar compra en tabla de compras
                        if registroProducto:
                            consultaProductoRecienAgregado = ProductosVenta.objects.filter(codigo_producto = codigoPV)
                            for dato in consultaProductoRecienAgregado:
                                idProductoRecienAgregado = dato.id_producto
                                nombreVenta = dato.nombre_producto
                          

                            #ImprimirEtiquetas
                            fechaHoy = date.today()
                            cantidadEtiquetas = int(1)
                            
                            primerDigitoCodigoV = codigoPV[2]
                            segundoDigitoCodigoV = codigoPV[3]
                            tercerDigitoCodigoV = codigoPV[4]
                            cuartoDigitoCodigoV = codigoPV[5]
                            
                            numeroCompletoCodigoV = primerDigitoCodigoV + segundoDigitoCodigoV + tercerDigitoCodigoV + cuartoDigitoCodigoV
                            codigoCompletoImprimirV = str(numeroCompletoCodigoV)


                            for x in range(cantidadEtiquetas):
                                
                                label = ("^XA~TA000~JSN^LT0^MNW^MTD^PON^PMN^LH0,0^JMA^PR2,2~SD30^JUS^LRN^CI0^XZ^XA^MMT^PW406^LL0203^LS0^FO0,160^GFA,00768,00768,00012,:Z64:eJxjYKAnYD/i3n5/zsfzIDb/u/f3z99tf98AZLOlJd69e/d44gEgm+/d+//n/v17fACs3vf+/TvmBw+A1T/uP7//8UMQm4EtgfGADAMjmM33gPGBHQMzmM3iABLjb4CKA9l89PCXvPzH57bHIWz+/7u/J4J9xcAge/9CeeEdiDjf/d2/baFs+fufy3nPQdX3/37/E6oeCNgZGOFsZgZuOJuB8TzCPsZz1PbBSAUAlzNF0w==:6D8B^FO128,128^GFA,01920,01920,00020,:Z64:eJztkT1Lw0Ach+8uoRdDKR2rtE2wy9mpHQotCCp+gRQaOwmCq0OkVh0KnukgBPETOJx1CefiR2jtUOjuKqGCrgFB3Opd2sGXDuKiQ39wy3MP9/L7AzDPPH8dNINBaFnJqlpNfoRUmvSruj5dv4o5g1nfkc4/XZvEXSOo285LL2xhGAqSIGTIONM54yPWSbi+YKWnyttuj0ILZrOLvczgQrCcu3Kba1PE0VJZO2Wu/JFyVgnWFFqyrXR5sR/uKYIhl7A8onnP14h2x0jk4eLgVaH3di3lpPpBS3oKKnodBDj3SaFsXvnSw4nG5aMCm/XDVaeQ3uhieZ63fE494XHCzBiNmsTpRqY3hra9fRzsP2x2VcnK1wttFwmvMrzxkavLO8JnA8dw0z4yjHF4ghNRByMd6cjjohgGdF2TCA5ALL5j2zUAuwDE05HnAqSZnPjR5DQy9TAMtqoHkaA6Uw/w6b547qRuddL2D+c2y5tnnv+bd/8tZhU=:C773^FO8,97^GB391,0,2^FS^BY2,3,61^FT295,29^BCI,,Y,N^FD>:PV>5"+codigoCompletoImprimirV+"^FS^FT398,178^A0I,14,14^FH\^FD"+str(fechaHoy)+"^FS^FT236,119^A0I,14,14^FH\^FD"+nombreVenta+"^FS^FT237,143^A0I,11,12^FH\^FDNombre producto:^FS^FT376,143^A0I,17,16^FH\^FDCosto de venta^FS^FT376,110^A0I,28,28^FH\^FD$ "+str(costoVentaVestido)+" ^FS^PQ1,0,1,Y^XZ")  
                                z = Zebra('ZDesigner GC420d')
                                z.output(label)

                
                
            elif tipo_producto == "gasto":
            
                costo_compraGasto = request.POST['costoGasto']
                costo_compraGasto = round(float(costo_compraGasto),2)
                cantidad_altaProducto = request.POST['cantidadAltaProducto']
                cantidad_productoStock = request.POST['cantidadStock']
                sku_producto = request.POST['skuProducto']  #Requerido

                nameInput = "checkboxCuantificable"
                if request.POST.get(nameInput, False): #Checkeado
                    cuantificable = "S"
                elif request.POST.get(nameInput, True): #No checkeado
                    cuantificable = "N"
                
                
                gastos = ProductosGasto.objects.all()
                if gastos :
                    hayRegistros = True
                    ultimoCodigo =""
                    for gasto in gastos:
                        ultimoCodigo= gasto.codigo_producto
                        
                    primerDigito = ultimoCodigo[2]
                    segundoDigito = ultimoCodigo[3]
                    tercerDigito = ultimoCodigo[4]
                    cuartoDigito = ultimoCodigo[5]
                    
                    numeroCompleto = primerDigito + segundoDigito + tercerDigito + cuartoDigito
                    codigoCompleto = int(numeroCompleto)
                    codigoCompleto = codigoCompleto +1
                    codigo = "PG"+str(codigoCompleto)
              
                    
                else:
                    codigo= "PG1000"
                
                 #alta de producto para venta
                if imagen_producto == "":

                    registroProducto = ProductosGasto(codigo_producto = codigo,
                    codigo_barras = codigo,
                    tipo_producto = tipo_producto,
                    nombre_producto = nombre_producto, 
                    costo_compra = costo_compraGasto,
                 
                    cantidad = cantidad_altaProducto, 
                    stock = cantidad_productoStock,
                    contenido_cuantificable = cuantificable,
                  
                    descripcion = descripcion_producto,
                    fecha_alta = fechaAlta, 
                    sku_producto =sku_producto,
                    creado_por = Empleados.objects.get(id_empleado = idEmpleado),
                    sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                else:
                    registroProducto = ProductosGasto(codigo_producto = codigo,
                    codigo_barras = codigo,
                    tipo_producto = tipo_producto,
                    nombre_producto = nombre_producto, 
                    costo_compra = costo_compraGasto,
                 
                    cantidad = cantidad_altaProducto, 
                    stock = cantidad_productoStock,
                    contenido_cuantificable = cuantificable,
                  
                    descripcion = descripcion_producto,
                    imagen_producto = imagen_producto,
                    fecha_alta = fechaAlta, 
                      sku_producto =sku_producto,
                    creado_por = Empleados.objects.get(id_empleado = idEmpleado),
                    sucursal = Sucursales.objects.get(id_sucursal = sucursal))
                    
                registroProducto.save()
                
                # Agregar compra en tabla de compras
                if registroProducto:
                    consultaProductoRecienAgregado = ProductosGasto.objects.filter(codigo_producto = codigo)
                    for dato in consultaProductoRecienAgregado:
                        idProductoRecienAgregado = dato.id_producto
                        
                    totalCostoCompra = float(costo_compraGasto) * float(cantidad_altaProducto) 
                    totalCostoCompra = round(totalCostoCompra,2)
                        
                    registroCompra = ComprasGastos(id_productoComprado = ProductosGasto.objects.get(id_producto = idProductoRecienAgregado),
                                                   costo_unitario = costo_compraGasto,
                                                   cantidad_comprada = cantidad_altaProducto,
                                                   total_costoCompra = totalCostoCompra,
                                                   fecha_compra = fechaAlta)
                    registroCompra.save()

                    #ImprimirEtiquetas
                    fechaHoy = date.today()
                    cantidadEtiquetas = int(cantidad_altaProducto)
                    
                    primerDigitoCodigo = codigo[2]
                    segundoDigitoCodigo = codigo[3]
                    tercerDigitoCodigo = codigo[4]
                    cuartoDigitoCodigo = codigo[5]
                    
                    numeroCompletoCodigo = primerDigitoCodigo + segundoDigitoCodigo + tercerDigitoCodigo + cuartoDigitoCodigo
                    codigoCompletoImprimir = str(numeroCompletoCodigo)

                    if tipo_producto:

                        for x in range(cantidadEtiquetas):
                            label = ("^XA~TA000~JSN^LT0^MNW^MTD^PON^PMN^LH0,0^JMA^PR2,2~SD30^JUS^LRN^CI0^XZ^XA^MMT^PW406^LL0203^LS0^FO0,160^GFA,00768,00768,00012,:Z64:eJxjYKAnYD/i3n5/zsfzIDb/u/f3z99tf98AZLOlJd69e/d44gEgm+/d+//n/v17fACs3vf+/TvmBw+A1T/uP7//8UMQm4EtgfGADAMjmM33gPGBHQMzmM3iABLjb4CKA9l89PCXvPzH57bHIWz+/7u/J4J9xcAge/9CeeEdiDjf/d2/baFs+fufy3nPQdX3/37/E6oeCNgZGOFsZgZuOJuB8TzCPsZz1PbBSAUAlzNF0w==:6D8B^FO128,128^GFA,01920,01920,00020,:Z64:eJztkT1Lw0Ach+8uoRdDKR2rtE2wy9mpHQotCCp+gRQaOwmCq0OkVh0KnukgBPETOJx1CefiR2jtUOjuKqGCrgFB3Opd2sGXDuKiQ39wy3MP9/L7AzDPPH8dNINBaFnJqlpNfoRUmvSruj5dv4o5g1nfkc4/XZvEXSOo285LL2xhGAqSIGTIONM54yPWSbi+YKWnyttuj0ILZrOLvczgQrCcu3Kba1PE0VJZO2Wu/JFyVgnWFFqyrXR5sR/uKYIhl7A8onnP14h2x0jk4eLgVaH3di3lpPpBS3oKKnodBDj3SaFsXvnSw4nG5aMCm/XDVaeQ3uhieZ63fE494XHCzBiNmsTpRqY3hra9fRzsP2x2VcnK1wttFwmvMrzxkavLO8JnA8dw0z4yjHF4ghNRByMd6cjjohgGdF2TCA5ALL5j2zUAuwDE05HnAqSZnPjR5DQy9TAMtqoHkaA6Uw/w6b547qRuddL2D+c2y5tnnv+bd/8tZhU=:C773^FO8,97^GB391,0,2^FS^BY2,3,61^FT295,29^BCI,,Y,N^FD>:PG>5"+codigoCompletoImprimir+"^FS^FT398,178^A0I,14,14^FH\^FD"+str(fechaHoy)+"^FS^FT267,120^A0I,17,16^FH\^FD"+nombre_producto+"^FS^PQ1,0,1,Y^XZ")
                            
                            z = Zebra('ZDesigner GC420d')
                            z.output(label)
            

           

               

            if registroProducto:
                    productoAgregado = "El producto "+nombre_producto + "ha sido gregado satisfactoriamente!"
                    return render(request, "6 Productos/altaProductos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado, "idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "sucursales":sucursales, "productoAgregado":productoAgregado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
            else:
                    productoNoAgregado = "Error en la base de datos, intentelo más tarde.."
                    return render(request, "6 Productos/altaProductos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "sucursales":sucursales, "productoNoAgregado":productoNoAgregado,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})

        return render(request, "6 Productos/altaProductos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,"estaEnAltaEmpleado":estaEnAltaEmpleado, "sucursales":sucursales,"notificacionRenta":notificacionRenta, "notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")    

def inventarioProductos(request):

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
        contadorProductosVentas = 0
        contadorProductosRentas = 0
        contadorProductosGastos = 0
        productosParaVenta = ProductosVenta.objects.all()
        productosParaRenta = ProductosRenta.objects.all()
        productosGasto = ProductosGasto.objects.all()
        
        for productoVentac in productosParaVenta:
            contadorProductosVentas = contadorProductosVentas + 1

        for productoRentac in productosParaRenta:
            contadorProductosRentas = contadorProductosRentas + 1

        for productoGastoc in productosGasto:
            contadorProductosGastos = contadorProductosGastos + 1
        
        # Productos para ventas
        agregadosVentas = []
        sucursalesVentas = []
        stockNecesario = []
        for productoVenta in productosParaVenta:
            id_empleado_agrego = productoVenta.creado_por_id
            id_sucursal = productoVenta.sucursal_id
            stock = productoVenta.stock
            cantidadEnExistencia = productoVenta.cantidad
            
            minimoStock = stock/2
            if cantidadEnExistencia>=minimoStock:
                mensajeStock = "No se necesitan artículos"
            elif cantidadEnExistencia<minimoStock:
                mensajeStock = "Se necesita restock"

            datosEmpleado = Empleados.objects.filter(id_empleado = id_empleado_agrego)
            for dato in datosEmpleado:
                nombres_agregado = dato.nombres
                apellidoPat_agregado = dato.apellido_paterno
            nombreCompletoagregado = nombres_agregado + " " + apellidoPat_agregado

            datosSucursal = Sucursales.objects.filter(id_sucursal = id_sucursal)
            for datoSucursal in datosSucursal:
                nombreSucursal = datoSucursal.nombre

            agregadosVentas.append(nombreCompletoagregado)
            sucursalesVentas.append(nombreSucursal)
            stockNecesario.append(mensajeStock)
            
        listaProductosVenta = zip(productosParaVenta, agregadosVentas, sucursalesVentas,stockNecesario)
        listaProductosVentaEditar = zip(productosParaVenta, agregadosVentas, sucursalesVentas) # Para el modal de editar
        listaProductosVentaEditar2 = zip(productosParaVenta, agregadosVentas, sucursalesVentas) # Para el modal de editar
        
        listaProductosVentaComprar = zip(productosParaVenta, agregadosVentas, sucursalesVentas)
        listaProductosVentaComprar2 = zip(productosParaVenta, agregadosVentas, sucursalesVentas)

        # Productos para rentas
        agregadosRentas = []
        sucursalesRentas = []
        clientesRentas =[]
        for productoRenta in productosParaRenta:
            id_productoR = productoRenta.id_producto
            id_empleado_agrego = productoRenta.creado_por_id
            id_sucursal = productoRenta.sucursal_id
            codigoProductoRenta = productoRenta.codigo_producto

            datosEmpleado = Empleados.objects.filter(id_empleado = id_empleado_agrego)
            for dato in datosEmpleado:
                nombres_agregado = dato.nombres
                apellidoPat_agregado = dato.apellido_paterno
            nombreCompletoagregado = nombres_agregado + " " + apellidoPat_agregado

            datosSucursal = Sucursales.objects.filter(id_sucursal = id_sucursal)
            for datoSucursal in datosSucursal:
                nombreSucursal = datoSucursal.nombre

            agregadosRentas.append(nombreCompletoagregado)
            sucursalesRentas.append(nombreSucursal)
            
            if productoRenta.estado_renta == "En renta":
                enRenta = Rentas.objects.filter(codigos_productos_renta= codigoProductoRenta)
                for ren in enRenta:
                    idCliente = ren.cliente_id
                    
                    cliente = Clientes.objects.filter(id_cliente = idCliente)
                    for cliente_renta in cliente:
                        id = str(cliente_renta.id_cliente)
                        nombre = cliente_renta.nombre_cliente
                        apellidoP = cliente_renta.apellidoPaterno_cliente
                        apellidoM = cliente_renta.apellidoMaterno_cliente
                    completoCliente = id + " " + nombre + " " + apellidoP + " " + apellidoM
                    clientesRentas.append(completoCliente)
            else:
                completoCliente = ""
                clientesRentas.append(completoCliente)
             
        listaProductosRenta = zip(productosParaRenta, agregadosRentas, sucursalesRentas,clientesRentas)
        listaProductosRentaEditar = zip(productosParaRenta, agregadosRentas, sucursalesRentas)

        # Productos para gasto
        agregadosGasto = []
        sucursalesGasto = []
        for productoGasto in productosGasto:
            id_empleado_agrego = productoGasto.creado_por_id
            id_sucursal = productoGasto.sucursal_id

            datosEmpleado = Empleados.objects.filter(id_empleado = id_empleado_agrego)
            for dato in datosEmpleado:
                nombres_agregado = dato.nombres
                apellidoPat_agregado = dato.apellido_paterno
            nombreCompletoagregado = nombres_agregado + " " + apellidoPat_agregado

            datosSucursal = Sucursales.objects.filter(id_sucursal = id_sucursal)
            for datoSucursal in datosSucursal:
                nombreSucursal = datoSucursal.nombre

            agregadosGasto.append(nombreCompletoagregado)
            sucursalesGasto.append(nombreSucursal)
            
        listaProductosGasto = zip(productosGasto, agregadosGasto, sucursalesGasto)
        listaProductosGasto2 = zip(productosGasto, agregadosGasto, sucursalesGasto) 
        listaProductosGastoEditar = zip(productosGasto, agregadosGasto, sucursalesGasto) 
        listaProductosGastoComprar = zip(productosGasto, agregadosGasto, sucursalesGasto) 
        
        listaSucursales = Sucursales.objects.all()
        
        listaSucursalesProductosVenta = Sucursales.objects.all()
        
        #Costos Producto Ventas.
        totalesSucursalesProductosVenta = []
        costoTotalProductosVenta = 0
        for sucursal in listaSucursalesProductosVenta:
            idSucursal = sucursal.id_sucursal
            nombreSucursal = sucursal.nombre
            
            #Consulta a todos los productos
            costoTotalProductosVentaPorSucural = 0
            costoVentaTotalProductosVentaPorSucursal = 0
            numeroProductos = 0 
            consultaModalProductosVenta = ProductosVenta.objects.all()
            for productoVenta in consultaModalProductosVenta:
                idSucursalProducto = productoVenta.sucursal_id
                
                if idSucursal == idSucursalProducto:
                    costoCompra = productoVenta.costo_compra
                    costoVenta = productoVenta.costo_venta
                    existenciaProductosVenta = productoVenta.cantidad
                    
                    costoCompra = float(costoCompra)*float(existenciaProductosVenta)
                    costoVenta = float(costoVenta)*float(existenciaProductosVenta)
                    
                    costoTotalProductosVentaPorSucural = costoTotalProductosVentaPorSucural + costoCompra
                    costoVentaTotalProductosVentaPorSucursal = costoVentaTotalProductosVentaPorSucursal + costoVenta
                    numeroProductos = numeroProductos + existenciaProductosVenta
                    
            totalesSucursalesProductosVenta.append([idSucursal, nombreSucursal, numeroProductos, costoTotalProductosVentaPorSucural, costoVentaTotalProductosVentaPorSucursal])
                
            costoTotalProductosVenta = costoTotalProductosVenta + costoTotalProductosVentaPorSucural
            
        #Costos Productos Rentas
        listaSucursalesProductosRenta = Sucursales.objects.all()
        
        totalesSucursalesProductosRenta = []
        costoTotalProductosRenta = 0
        for sucursal in listaSucursalesProductosRenta:
            idSucursal = sucursal.id_sucursal
            nombreSucursal = sucursal.nombre
            
            costoTotalProductosRentaPorSucursal = 0
            costoRentaTotalProductosRentaPorSucursal = 0
            numeroProductosRenta = 0
            consultaModalProductosRenta = ProductosRenta.objects.all()
            for productoRenta in consultaModalProductosRenta:
                idSucursalProducto = productoRenta.sucursal_id
                
                if idSucursal == idSucursalProducto:
                    costoCompra = productoRenta.costo_de_compra
                    costoRenta = productoRenta.costo_renta
                    cantidad = productoRenta.cantidad
                    
                    costoCompra = float(costoCompra)*float(cantidad)
                    costoRenta = float(costoRenta)*float(cantidad)
                    costoTotalProductosRentaPorSucursal = costoTotalProductosRentaPorSucursal + costoCompra
                    costoRentaTotalProductosRentaPorSucursal = costoRentaTotalProductosRentaPorSucursal + costoRenta
                    numeroProductosRenta = numeroProductosRenta + cantidad
                    
            totalesSucursalesProductosRenta.append([idSucursal,nombreSucursal,numeroProductosRenta,costoTotalProductosRentaPorSucursal,costoRentaTotalProductosRentaPorSucursal])
            costoTotalProductosRenta = costoTotalProductosRenta + costoTotalProductosRentaPorSucursal
                    
        #Costos Productos Gasto
        listaSucursalesProductosGasto = Sucursales.objects.all()
        
        totalesSucursalesProductosGasto = []
        costoTotalProductosGasto = 0
        for sucursal in listaSucursalesProductosGasto:
            idSucursal = sucursal.id_sucursal
            nombreSucursal = sucursal.nombre
            
            costoTotalProductosGastoPorSucursal = 0
            numeroProductosGasto = 0
            consultaModalProductosGasto = ProductosGasto.objects.all()
            for productoGasto in consultaModalProductosGasto:
                idSucursalProducto = productoGasto.sucursal_id
                
                if idSucursal == idSucursalProducto:
                    costoCompra = productoGasto.costo_compra
                    cantidad = productoGasto.cantidad
                    
                    costoCompra = float(costoCompra)*float(cantidad)
                    costoTotalProductosGastoPorSucursal = costoTotalProductosGastoPorSucursal + costoCompra
                    numeroProductosGasto = numeroProductosGasto + cantidad
            
            totalesSucursalesProductosGasto.append([idSucursal,nombreSucursal,numeroProductosGasto,costoTotalProductosGastoPorSucursal])
            costoTotalProductosGasto = costoTotalProductosGasto + costoTotalProductosGastoPorSucursal
        
        
        descuentos = ["5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60", "65", "70", "75", "80", "85", "90", "95"]
        
        
        if "productoActualizado" in request.session:
            productoActualizado = request.session['productoActualizado']
            del request.session['productoActualizado']
            return render(request, "6 Productos/inventarioProductos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
            "contadorProductosVentas":contadorProductosVentas,
            "contadorProductosRentas":contadorProductosRentas,
            "contadorProductosGastos":contadorProductosGastos,
            "listaProductosVenta":listaProductosVenta, "listaProductosVentaEditar":listaProductosVentaEditar,"listaProductosVentaEditar2":listaProductosVentaEditar2, "listaProductosVentaComprar":listaProductosVentaComprar, "listaProductosVentaComprar2":listaProductosVentaComprar,
            "listaProductosRenta":listaProductosRenta,
            "listaProductosGasto":listaProductosGasto,
            "listaProductosGasto2":listaProductosGasto2, "listaProductosGastoEditar":listaProductosGastoEditar, "listaProductosGastoComprar":listaProductosGastoComprar, "productoActualizado":productoActualizado,"listaProductosRentaEditar":listaProductosRentaEditar,"notificacionRenta":notificacionRenta, "listaSucursales":listaSucursales,
            "totalesSucursalesProductosVenta":totalesSucursalesProductosVenta, "costoTotalProductosVenta":costoTotalProductosVenta,
            "totalesSucursalesProductosRenta":totalesSucursalesProductosRenta, "costoTotalProductosRenta":costoTotalProductosRenta,
            "totalesSucursalesProductosGasto":totalesSucursalesProductosGasto, "costoTotalProductosGasto":costoTotalProductosGasto, "notificacionCita":notificacionCita,
            "descuentos":descuentos})
        
        if "productosActualizados" in request.session:
            productosActualizados = request.session['productosActualizados']
            del request.session['productosActualizados']
            return render(request, "6 Productos/inventarioProductos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
            "contadorProductosVentas":contadorProductosVentas,
            "contadorProductosRentas":contadorProductosRentas,
            "contadorProductosGastos":contadorProductosGastos,
            "listaProductosVenta":listaProductosVenta, "listaProductosVentaEditar":listaProductosVentaEditar, "listaProductosVentaEditar2":listaProductosVentaEditar2, "listaProductosVentaComprar":listaProductosVentaComprar, "listaProductosVentaComprar2":listaProductosVentaComprar,
            "listaProductosRenta":listaProductosRenta,
            "listaProductosGasto":listaProductosGasto,
            "listaProductosGasto2":listaProductosGasto2, "listaProductosGastoEditar":listaProductosGastoEditar,"listaProductosGastoComprar":listaProductosGastoComprar,"listaProductosRentaEditar":listaProductosRentaEditar, "notificacionRenta":notificacionRenta, "listaSucursales":listaSucursales, "productosActualizados":productosActualizados,
            "totalesSucursalesProductosVenta":totalesSucursalesProductosVenta, "costoTotalProductosVenta":costoTotalProductosVenta,
            "totalesSucursalesProductosRenta":totalesSucursalesProductosRenta, "costoTotalProductosRenta":costoTotalProductosRenta,
            "totalesSucursalesProductosGasto":totalesSucursalesProductosGasto, "costoTotalProductosGasto":costoTotalProductosGasto, "notificacionCita":notificacionCita,
            "descuentos":descuentos})
        
        if "errorProductosActualizados" in request.session:
            errorProductosActualizados = request.session['errorProductosActualizados']
            del request.session['errorProductosActualizados']
            return render(request, "6 Productos/inventarioProductos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
            "contadorProductosVentas":contadorProductosVentas,
            "contadorProductosRentas":contadorProductosRentas,
            "contadorProductosGastos":contadorProductosGastos,
            "listaProductosVenta":listaProductosVenta, "listaProductosVentaEditar":listaProductosVentaEditar, "listaProductosVentaEditar2":listaProductosVentaEditar2, "listaProductosVentaComprar":listaProductosVentaComprar, "listaProductosVentaComprar2":listaProductosVentaComprar,
            "listaProductosRenta":listaProductosRenta,
            "listaProductosGasto":listaProductosGasto,
            "listaProductosGasto2":listaProductosGasto2, "listaProductosGastoEditar":listaProductosGastoEditar,"listaProductosGastoComprar":listaProductosGastoComprar,"listaProductosRentaEditar":listaProductosRentaEditar, "notificacionRenta":notificacionRenta, "listaSucursales":listaSucursales, "errorProductosActualizados":errorProductosActualizados,
            "totalesSucursalesProductosVenta":totalesSucursalesProductosVenta, "costoTotalProductosVenta":costoTotalProductosVenta,
            "totalesSucursalesProductosRenta":totalesSucursalesProductosRenta, "costoTotalProductosRenta":costoTotalProductosRenta,
            "totalesSucursalesProductosGasto":totalesSucursalesProductosGasto, "costoTotalProductosGasto":costoTotalProductosGasto, "notificacionCita":notificacionCita,
            "descuentos":descuentos})
        
        if "correoEnviado" in request.session:
            correoEnviado = request.session['correoEnviado']
            del request.session['correoEnviado']
            return render(request, "6 Productos/inventarioProductos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
            "contadorProductosVentas":contadorProductosVentas,
            "contadorProductosRentas":contadorProductosRentas,
            "contadorProductosGastos":contadorProductosGastos,
            "listaProductosVenta":listaProductosVenta, "listaProductosVentaEditar":listaProductosVentaEditar, "listaProductosVentaEditar2":listaProductosVentaEditar2, "listaProductosVentaComprar":listaProductosVentaComprar, "listaProductosVentaComprar2":listaProductosVentaComprar,
            "listaProductosRenta":listaProductosRenta,
            "listaProductosGasto":listaProductosGasto,
            "listaProductosGasto2":listaProductosGasto2, "listaProductosGastoEditar":listaProductosGastoEditar,"listaProductosGastoComprar":listaProductosGastoComprar,"listaProductosRentaEditar":listaProductosRentaEditar,"notificacionRenta":notificacionRenta, "listaSucursales":listaSucursales, "correoEnviado":correoEnviado,
            "totalesSucursalesProductosVenta":totalesSucursalesProductosVenta, "costoTotalProductosVenta":costoTotalProductosVenta,
            "totalesSucursalesProductosRenta":totalesSucursalesProductosRenta, "costoTotalProductosRenta":costoTotalProductosRenta,
            "totalesSucursalesProductosGasto":totalesSucursalesProductosGasto, "costoTotalProductosGasto":costoTotalProductosGasto, "notificacionCita":notificacionCita,
            "descuentos":descuentos})
        
        if "correoNoEnviado" in request.session:
            correoNoEnviado = request.session['correoNoEnviado']
            del request.session['correoNoEnviado']
            return render(request, "6 Productos/inventarioProductos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
            "contadorProductosVentas":contadorProductosVentas,
            "contadorProductosRentas":contadorProductosRentas,
            "contadorProductosGastos":contadorProductosGastos,
            "listaProductosVenta":listaProductosVenta, "listaProductosVentaEditar":listaProductosVentaEditar, "listaProductosVentaEditar2":listaProductosVentaEditar2, "listaProductosVentaComprar":listaProductosVentaComprar, "listaProductosVentaComprar2":listaProductosVentaComprar,
            "listaProductosRenta":listaProductosRenta,
            "listaProductosGasto":listaProductosGasto,
            "listaProductosGasto2":listaProductosGasto2, "listaProductosGastoEditar":listaProductosGastoEditar,"listaProductosGastoComprar":listaProductosGastoComprar,"listaProductosRentaEditar":listaProductosRentaEditar, "notificacionRenta":notificacionRenta, "listaSucursales":listaSucursales, "correoNoEnviado":correoNoEnviado,
            "totalesSucursalesProductosVenta":totalesSucursalesProductosVenta, "costoTotalProductosVenta":costoTotalProductosVenta,
            "totalesSucursalesProductosRenta":totalesSucursalesProductosRenta, "costoTotalProductosRenta":costoTotalProductosRenta,
            "totalesSucursalesProductosGasto":totalesSucursalesProductosGasto, "costoTotalProductosGasto":costoTotalProductosGasto, "notificacionCita":notificacionCita,
            "descuentos":descuentos})
        
        
        
        return render(request, "6 Productos/inventarioProductos.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, 
        "contadorProductosVentas":contadorProductosVentas,
        "contadorProductosRentas":contadorProductosRentas,
        "contadorProductosGastos":contadorProductosGastos,
        "listaProductosVenta":listaProductosVenta, "listaProductosVentaEditar":listaProductosVentaEditar, "listaProductosVentaEditar2":listaProductosVentaEditar2, "listaProductosVentaComprar":listaProductosVentaComprar, "listaProductosVentaComprar2":listaProductosVentaComprar,
        "listaProductosRenta":listaProductosRenta,
        "listaProductosGasto":listaProductosGasto,
        "listaProductosGasto2":listaProductosGasto2, "listaProductosGastoEditar":listaProductosGastoEditar,"listaProductosGastoComprar":listaProductosGastoComprar,"listaProductosRentaEditar":listaProductosRentaEditar, "notificacionRenta":notificacionRenta, "listaSucursales":listaSucursales,
        "totalesSucursalesProductosVenta":totalesSucursalesProductosVenta, "costoTotalProductosVenta":costoTotalProductosVenta,
        "totalesSucursalesProductosRenta":totalesSucursalesProductosRenta, "costoTotalProductosRenta":costoTotalProductosRenta,
            "totalesSucursalesProductosGasto":totalesSucursalesProductosGasto, "costoTotalProductosGasto":costoTotalProductosGasto, "notificacionCita":notificacionCita,
            "descuentos":descuentos})
    else:
        return render(request,"1 Login/login.html")

def actualizarProductoV(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idProductoVentaEditar = request.POST['idProductoVentaEditar']
            costoGastoActualizado = request.POST['costoGastoActualizado']
            margenActualizado = request.POST['margenActualizado']
            costoVentaActualizado = request.POST['costoVentaActualizado']
            descuentoProductoVenta = request.POST["descuentoProductoVenta"]
            
            consultaProducto = ProductosVenta.objects.filter(id_producto = idProductoVentaEditar)
            
            for dato in consultaProducto:
                nombreProducto = dato.nombre_producto
            
            actualizacionProductoVenta = ProductosVenta.objects.filter(id_producto = idProductoVentaEditar).update(costo_compra = costoGastoActualizado, margen_ganancia_producto = margenActualizado, costo_venta = costoVentaActualizado, descuento = descuentoProductoVenta)
            
            if actualizacionProductoVenta:    
                request.session['productoActualizado'] = "El producto " + nombreProducto + " ha sido actualizado correctamente!"
                return redirect('/inventarioProductos/')      

def actualizarProductoVentaCompra(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idProductoVentaComprar = request.POST['idProductoVentaComprar']
            cantidadComprarProducto = request.POST['cantidadComprarProducto']
            costoGastoActualizado = request.POST['costoGastoActualizado']
            
            consultaProducto = ProductosVenta.objects.filter(id_producto = idProductoVentaComprar)
            
            for dato in consultaProducto:
                nombreProducto = dato.nombre_producto
                cantidadActual = dato.cantidad
                codigoProducto = dato.codigo_producto
                
            cantidadActualInt = int(cantidadActual)
            cantidadActualizada = int(cantidadComprarProducto) + cantidadActualInt
            
            totalCostoDeCompra = float(cantidadComprarProducto) * float(costoGastoActualizado)
            totalCostoCompraRedondeado = round(totalCostoDeCompra,2)
            
            fechaCompra = datetime.today().strftime('%Y-%m-%d')
                
            #Actualizar costo gasto de producto y cantidades
            actualizarProducto = ProductosVenta.objects.filter(id_producto = idProductoVentaComprar).update(costo_compra = costoGastoActualizado, cantidad = cantidadActualizada)
            
            #Generar y guardar compra
            registroCompraProductoVenta = ComprasVentas(
                id_productoComprado = ProductosVenta.objects.get(id_producto = idProductoVentaComprar),
                costo_unitario = costoGastoActualizado,
                cantidad_comprada = cantidadComprarProducto,
                total_costoCompra = totalCostoCompraRedondeado,
                fecha_compra = fechaCompra
            )
            
            registroCompraProductoVenta.save()
            
            if actualizarProducto and registroCompraProductoVenta:    
                request.session['productoActualizado'] = "Se ha realizado una nueva compra del producto " + nombreProducto + " correctamente!"
                #ImprimirEtiquetas
                fechaHoy = date.today()
                letra1 = codigoProducto[0]
                letra2 = codigoProducto[1]
                primerDigitoCodigo = codigoProducto[2]
                segundoDigitoCodigo = codigoProducto[3]
                tercerDigitoCodigo = codigoProducto[4]
                cuartoDigitoCodigo = codigoProducto[5]
                
                numeroCompletoCodigo = primerDigitoCodigo + segundoDigitoCodigo + tercerDigitoCodigo + cuartoDigitoCodigo
                codigoCompletoImprimir = str(numeroCompletoCodigo)
                cantidadComprarProducto = int(cantidadComprarProducto)
                for x in range(cantidadComprarProducto):
                    label = ("^XA~TA000~JSN^LT0^MNW^MTD^PON^PMN^LH0,0^JMA^PR4,4~SD15^JUS^LRN^CI0^XZ^XA^MMT^PW406^LL0203^LS0^FO0,128^GFA,01152,01152,00012,:Z64:eJxjYBgF9AEpxjKygiwFBQVAdr2xvX3/mY4f/4DsYmNGwzlnDvawAdmPN+/fOOPNzx7mBgaGZGNDQxkXwR5msHpj+/5zM36A2C5Ac2bKFBSA2AzGDIwNPAwMTFA2AwsDAxuEDTKC4R9MDZAqoLd/DQUKWQwegNn1xhY/dxl/ALOLDQUkZxhD1CRvnv2zD8Y2FpRkh7Lr7X/MPm0M0esieaHwjAHc9UC/WMDZDIYGCAuVHyDYjAeo6pdRQCsAAK6KM48=:1B1C^FO128,128^GFA,01280,01280,00020,:Z64:eJxjYBgFAwwcGBgEHAgrYwkJEAwICUET5VDAUCggAMTkOoZJCYUryOre+Ec01L2w8ENBDVQs71jGOQ6gzec6Ol6sgordSSmIkWBlETwvy3v2IMxpWQkVEkxMjB2c3BxNUDGZmvIIAVFRRxnJ+aLMMHVrnp1Q4GBo4uBo4mCCqTtz5khBaGj4HIkwGUaomEVHR/MGLSXlGQZWFjB1snPPygPVBZfWfy48DhXj4ujjUFjR0dH0qOEBzF4GySMSKaGhIQwJDIw8MDHrBg4lJaUFDApAN8DEjBtEY0QCQcHHWIAUDg1o9CgYJgAApEY4pg==:6E1D^BY2,3,75^FT291,35^BCI,,Y,N^FD>:"+str(letra1)+str(letra2)+">5"+codigoCompletoImprimir+"^FS^FO16,118^GB373,0,3^FS^FT387,171^A0I,17,16^FH\^FD"+str(fechaHoy)+"^FS^PQ1,0,1,Y^XZ")                        
                    z = Zebra('ZDesigner GC420d')
                    z.output(label)
                return redirect('/inventarioProductos/')      

def actualizarProductoGasto(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idProductoGastoEditar = request.POST['idProductoGastoEditar']
            costoGastoActualizado = request.POST['costoGastoActualizado']
            cantidadActualizado = request.POST['cantidadActualizado']
            
            
            consultaProducto = ProductosGasto.objects.filter(id_producto = idProductoGastoEditar)
            
            for dato in consultaProducto:
                nombreProducto = dato.nombre_producto
            
            actualizacionProductoGasto = ProductosGasto.objects.filter(id_producto = idProductoGastoEditar).update(costo_compra = costoGastoActualizado,cantidad = cantidadActualizado)
            
            if actualizacionProductoGasto:    
                request.session['productoActualizado'] = "El producto " + nombreProducto + " ha sido actualizado correctamente!"
                return redirect('/inventarioProductos/')  

def actualizarProductoGastoCompra(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idProductoGastoComprar = request.POST['idProductoGastoComprar']
            cantidadComprarProducto = request.POST['cantidadComprarProducto']
            costoGastoActualizado = request.POST['costoGastoActualizado']
            
            consultaProducto = ProductosGasto.objects.filter(id_producto = idProductoGastoComprar)
            
            for dato in consultaProducto:
                nombreProducto = dato.nombre_producto
                cantidadActual = dato.cantidad
                codigoProducto = dato.codigo_producto
                
            cantidadActualInt = int(cantidadActual)
            cantidadActualizada = int(cantidadComprarProducto) + cantidadActualInt
            
            totalCostoDeCompra = float(cantidadComprarProducto) * float(costoGastoActualizado)
            totalCostoCompraRedondeado = round(totalCostoDeCompra,2)
            
            fechaCompra = datetime.today().strftime('%Y-%m-%d')
                
            #Actualizar costo gasto de producto y cantidades
            actualizarProducto = ProductosGasto.objects.filter(id_producto = idProductoGastoComprar).update(costo_compra = costoGastoActualizado, cantidad = cantidadActualizada)
            
            #Generar y guardar compra
            registroCompraProductoGasto = ComprasGastos(
                id_productoComprado = ProductosGasto.objects.get(id_producto = idProductoGastoComprar),
                costo_unitario = costoGastoActualizado,
                cantidad_comprada = cantidadComprarProducto,
                total_costoCompra = totalCostoCompraRedondeado,
                fecha_compra = fechaCompra
            )
            
            registroCompraProductoGasto.save()
            
            if actualizarProducto and registroCompraProductoGasto:    
                request.session['productoActualizado'] = "Se ha realizado una nueva compra del producto " + nombreProducto + " correctamente!"
                #ImprimirEtiquetas
                fechaHoy = date.today()
                letra1 = codigoProducto[0]
                letra2 = codigoProducto[1]
                primerDigitoCodigo = codigoProducto[2]
                segundoDigitoCodigo = codigoProducto[3]
                tercerDigitoCodigo = codigoProducto[4]
                cuartoDigitoCodigo = codigoProducto[5]
                
                numeroCompletoCodigo = primerDigitoCodigo + segundoDigitoCodigo + tercerDigitoCodigo + cuartoDigitoCodigo
                codigoCompletoImprimir = str(numeroCompletoCodigo)
                cantidadComprarProducto = int(cantidadComprarProducto)
                for x in range(cantidadComprarProducto):
                    label = ("^XA~TA000~JSN^LT0^MNW^MTD^PON^PMN^LH0,0^JMA^PR4,4~SD15^JUS^LRN^CI0^XZ^XA^MMT^PW406^LL0203^LS0^FO0,128^GFA,01152,01152,00012,:Z64:eJxjYBgF9AEpxjKygiwFBQVAdr2xvX3/mY4f/4DsYmNGwzlnDvawAdmPN+/fOOPNzx7mBgaGZGNDQxkXwR5msHpj+/5zM36A2C5Ac2bKFBSA2AzGDIwNPAwMTFA2AwsDAxuEDTKC4R9MDZAqoLd/DQUKWQwegNn1xhY/dxl/ALOLDQUkZxhD1CRvnv2zD8Y2FpRkh7Lr7X/MPm0M0esieaHwjAHc9UC/WMDZDIYGCAuVHyDYjAeo6pdRQCsAAK6KM48=:1B1C^FO128,128^GFA,01280,01280,00020,:Z64:eJxjYBgFAwwcGBgEHAgrYwkJEAwICUET5VDAUCggAMTkOoZJCYUryOre+Ec01L2w8ENBDVQs71jGOQ6gzec6Ol6sgordSSmIkWBlETwvy3v2IMxpWQkVEkxMjB2c3BxNUDGZmvIIAVFRRxnJ+aLMMHVrnp1Q4GBo4uBo4mCCqTtz5khBaGj4HIkwGUaomEVHR/MGLSXlGQZWFjB1snPPygPVBZfWfy48DhXj4ujjUFjR0dH0qOEBzF4GySMSKaGhIQwJDIw8MDHrBg4lJaUFDApAN8DEjBtEY0QCQcHHWIAUDg1o9CgYJgAApEY4pg==:6E1D^BY2,3,75^FT291,35^BCI,,Y,N^FD>:"+str(letra1)+str(letra2)+">5"+codigoCompletoImprimir+"^FS^FO16,118^GB373,0,3^FS^FT387,171^A0I,17,16^FH\^FD"+str(fechaHoy)+"^FS^PQ1,0,1,Y^XZ")                        
                    z = Zebra('ZDesigner GC420d')
                    z.output(label)
                return redirect('/inventarioProductos/')          

def actualizarProductoRenta(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idProductoRentaEditar = request.POST['idProductoRentaEditar']
            costoPrecioCompraActualizado = request.POST['costoPrecioCompraActualizado']
            costoRentaActualizado = request.POST['costoRentaActualizado']
            
            
            consultaProducto = ProductosRenta.objects.filter(id_producto = idProductoRentaEditar)
            
            for dato in consultaProducto:
                nombreProducto = dato.nombre_producto
            
            actualizacionProductoRenta = ProductosRenta.objects.filter(id_producto = idProductoRentaEditar).update(costo_de_compra = costoPrecioCompraActualizado,costo_renta = costoRentaActualizado)
            
            if actualizacionProductoRenta:    
                request.session['productoActualizado'] = "El producto " + nombreProducto + " ha sido actualizado correctamente!"
                return redirect('/inventarioProductos/')  

def imprimirCodigoBarras(request):

    #Si ya existe una sesion al teclear login...
    if "idSesion" in request.session:
        codigoProducto = request.POST['codigoProducto']
        cantidadEtiquetas = request.POST['cantidadEtiquetas']
        cantidadEtiquetas = int(cantidadEtiquetas)

        if "PV" in codigoProducto:
            #ImprimirEtiquetas
            fechaHoy = date.today()
            primerDigitoCodigo = codigoProducto[2]
            segundoDigitoCodigo = codigoProducto[3]
            tercerDigitoCodigo = codigoProducto[4]
            cuartoDigitoCodigo = codigoProducto[5]
            
            numeroCompletoCodigo = primerDigitoCodigo + segundoDigitoCodigo + tercerDigitoCodigo + cuartoDigitoCodigo
            codigoCompletoImprimir = str(numeroCompletoCodigo)

            #Consulta
            consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
            for datoProducto in consultaProducto:
                costoVenta = datoProducto.costo_venta
                costoVentaCredito = datoProducto.costo_venta_a_credito
                nombreVenta = datoProducto.nombre_producto
            
            print("El nombre del producto es"+nombreVenta)
            for x in range(cantidadEtiquetas):
                label = ("^XA~TA000~JSN^LT0^MNW^MTD^PON^PMN^LH0,0^JMA^PR2,2~SD30^JUS^LRN^CI0^XZ^XA^MMT^PW406^LL0203^LS0^FO0,160^GFA,00768,00768,00012,:Z64:eJxjYKAnYD/i3n5/zsfzIDb/u/f3z99tf98AZLOlJd69e/d44gEgm+/d+//n/v17fACs3vf+/TvmBw+A1T/uP7//8UMQm4EtgfGADAMjmM33gPGBHQMzmM3iABLjb4CKA9l89PCXvPzH57bHIWz+/7u/J4J9xcAge/9CeeEdiDjf/d2/baFs+fufy3nPQdX3/37/E6oeCNgZGOFsZgZuOJuB8TzCPsZz1PbBSAUAlzNF0w==:6D8B^FO128,128^GFA,01920,01920,00020,:Z64:eJztkT1Lw0Ach+8uoRdDKR2rtE2wy9mpHQotCCp+gRQaOwmCq0OkVh0KnukgBPETOJx1CefiR2jtUOjuKqGCrgFB3Opd2sGXDuKiQ39wy3MP9/L7AzDPPH8dNINBaFnJqlpNfoRUmvSruj5dv4o5g1nfkc4/XZvEXSOo285LL2xhGAqSIGTIONM54yPWSbi+YKWnyttuj0ILZrOLvczgQrCcu3Kba1PE0VJZO2Wu/JFyVgnWFFqyrXR5sR/uKYIhl7A8onnP14h2x0jk4eLgVaH3di3lpPpBS3oKKnodBDj3SaFsXvnSw4nG5aMCm/XDVaeQ3uhieZ63fE494XHCzBiNmsTpRqY3hra9fRzsP2x2VcnK1wttFwmvMrzxkavLO8JnA8dw0z4yjHF4ghNRByMd6cjjohgGdF2TCA5ALL5j2zUAuwDE05HnAqSZnPjR5DQy9TAMtqoHkaA6Uw/w6b547qRuddL2D+c2y5tnnv+bd/8tZhU=:C773^FO8,97^GB391,0,2^FS^BY2,3,61^FT295,29^BCI,,Y,N^FD>:PV>5"+codigoCompletoImprimir+"^FS^FT398,178^A0I,14,14^FH\^FD"+str(fechaHoy)+"^FS^FT236,119^A0I,14,14^FH\^FD"+nombreVenta+"^FS^FT237,143^A0I,11,12^FH\^FDNombre producto:^FS^FT376,143^A0I,17,16^FH\^FDCosto de venta^FS^FT376,110^A0I,28,28^FH\^FD$ "+str(costoVenta)+" ^FS^PQ1,0,1,Y^XZ")                        
                        
                z = Zebra('ZDesigner GC420d')
                z.output(label)
        
            return redirect("/inventarioProductos/")
        elif "PG" in codigoProducto:
            #ImprimirEtiquetas
            fechaHoy = date.today()
            primerDigitoCodigo = codigoProducto[2]
            segundoDigitoCodigo = codigoProducto[3]
            tercerDigitoCodigo = codigoProducto[4]
            cuartoDigitoCodigo = codigoProducto[5]
            
            numeroCompletoCodigo = primerDigitoCodigo + segundoDigitoCodigo + tercerDigitoCodigo + cuartoDigitoCodigo
            codigoCompletoImprimir = str(numeroCompletoCodigo)

            #Consulta
            consultaProducto = ProductosGasto.objects.filter(codigo_producto = codigoProducto)
            for datoProducto in consultaProducto:
                nombreProductoGasto = datoProducto.nombre_producto

            for x in range(cantidadEtiquetas):
                label = ("^XA~TA000~JSN^LT0^MNW^MTD^PON^PMN^LH0,0^JMA^PR2,2~SD30^JUS^LRN^CI0^XZ^XA^MMT^PW406^LL0203^LS0^FO0,160^GFA,00768,00768,00012,:Z64:eJxjYKAnYD/i3n5/zsfzIDb/u/f3z99tf98AZLOlJd69e/d44gEgm+/d+//n/v17fACs3vf+/TvmBw+A1T/uP7//8UMQm4EtgfGADAMjmM33gPGBHQMzmM3iABLjb4CKA9l89PCXvPzH57bHIWz+/7u/J4J9xcAge/9CeeEdiDjf/d2/baFs+fufy3nPQdX3/37/E6oeCNgZGOFsZgZuOJuB8TzCPsZz1PbBSAUAlzNF0w==:6D8B^FO128,128^GFA,01920,01920,00020,:Z64:eJztkT1Lw0Ach+8uoRdDKR2rtE2wy9mpHQotCCp+gRQaOwmCq0OkVh0KnukgBPETOJx1CefiR2jtUOjuKqGCrgFB3Opd2sGXDuKiQ39wy3MP9/L7AzDPPH8dNINBaFnJqlpNfoRUmvSruj5dv4o5g1nfkc4/XZvEXSOo285LL2xhGAqSIGTIONM54yPWSbi+YKWnyttuj0ILZrOLvczgQrCcu3Kba1PE0VJZO2Wu/JFyVgnWFFqyrXR5sR/uKYIhl7A8onnP14h2x0jk4eLgVaH3di3lpPpBS3oKKnodBDj3SaFsXvnSw4nG5aMCm/XDVaeQ3uhieZ63fE494XHCzBiNmsTpRqY3hra9fRzsP2x2VcnK1wttFwmvMrzxkavLO8JnA8dw0z4yjHF4ghNRByMd6cjjohgGdF2TCA5ALL5j2zUAuwDE05HnAqSZnPjR5DQy9TAMtqoHkaA6Uw/w6b547qRuddL2D+c2y5tnnv+bd/8tZhU=:C773^FO8,97^GB391,0,2^FS^BY2,3,61^FT295,29^BCI,,Y,N^FD>:PG>5"+codigoCompletoImprimir+"^FS^FT398,178^A0I,14,14^FH\^FD"+str(fechaHoy)+"^FS^FT267,120^A0I,17,16^FH\^FD"+nombreProductoGasto+"^FS^PQ1,0,1,Y^XZ")
                z = Zebra('ZDesigner GC420d')
                z.output(label)
        
            return redirect("/inventarioProductos/")

        elif "PR" in codigoProducto:
            #ImprimirEtiquetas
            fechaHoy = date.today()
            primerDigitoCodigo = codigoProducto[2]
            segundoDigitoCodigo = codigoProducto[3]
            tercerDigitoCodigo = codigoProducto[4]
            cuartoDigitoCodigo = codigoProducto[5]
            
            numeroCompletoCodigo = primerDigitoCodigo + segundoDigitoCodigo + tercerDigitoCodigo + cuartoDigitoCodigo
            codigoCompletoImprimir = str(numeroCompletoCodigo)

            #Consulta
            consultaProducto = ProductosRenta.objects.filter(codigo_producto = codigoProducto)
            for datoProducto in consultaProducto:
                costoRenta = datoProducto.costo_renta
                nombreRenta = datoProducto.nombre_producto

            for x in range(cantidadEtiquetas):
                label = ("^XA~TA000~JSN^LT0^MNW^MTD^PON^PMN^LH0,0^JMA^PR2,2~SD30^JUS^LRN^CI0^XZ^XA^MMT^PW406^LL0203^LS0^FO0,160^GFA,00768,00768,00012,:Z64:eJxjYKAnYD/i3n5/zsfzIDb/u/f3z99tf98AZLOlJd69e/d44gEgm+/d+//n/v17fACs3vf+/TvmBw+A1T/uP7//8UMQm4EtgfGADAMjmM33gPGBHQMzmM3iABLjb4CKA9l89PCXvPzH57bHIWz+/7u/J4J9xcAge/9CeeEdiDjf/d2/baFs+fufy3nPQdX3/37/E6oeCNgZGOFsZgZuOJuB8TzCPsZz1PbBSAUAlzNF0w==:6D8B^FO128,128^GFA,01920,01920,00020,:Z64:eJztkT1Lw0Ach+8uoRdDKR2rtE2wy9mpHQotCCp+gRQaOwmCq0OkVh0KnukgBPETOJx1CefiR2jtUOjuKqGCrgFB3Opd2sGXDuKiQ39wy3MP9/L7AzDPPH8dNINBaFnJqlpNfoRUmvSruj5dv4o5g1nfkc4/XZvEXSOo285LL2xhGAqSIGTIONM54yPWSbi+YKWnyttuj0ILZrOLvczgQrCcu3Kba1PE0VJZO2Wu/JFyVgnWFFqyrXR5sR/uKYIhl7A8onnP14h2x0jk4eLgVaH3di3lpPpBS3oKKnodBDj3SaFsXvnSw4nG5aMCm/XDVaeQ3uhieZ63fE494XHCzBiNmsTpRqY3hra9fRzsP2x2VcnK1wttFwmvMrzxkavLO8JnA8dw0z4yjHF4ghNRByMd6cjjohgGdF2TCA5ALL5j2zUAuwDE05HnAqSZnPjR5DQy9TAMtqoHkaA6Uw/w6b547qRuddL2D+c2y5tnnv+bd/8tZhU=:C773^FO8,97^GB391,0,2^FS^BY2,3,61^FT295,29^BCI,,Y,N^FD>:PR>5"+codigoCompletoImprimir+"^FS^FT398,178^A0I,14,14^FH\^FD"+str(fechaHoy)+"^FS^FT236,119^A0I,14,14^FH\^FD"+nombreRenta+"^FS^FT237,143^A0I,11,12^FH\^FDNombre vestido:^FS^FT376,143^A0I,17,16^FH\^FDCosto de renta^FS^FT376,110^A0I,28,28^FH\^FD$ "+str(costoRenta)+" ^FS^PQ1,0,1,Y^XZ")                        
                z = Zebra('ZDesigner GC420d')
                z.output(label)
        
            return redirect("/inventarioProductos/")

        
        
        
        
              
        
    # Si no hay una sesion iniciada..
    else:
        return render(request, "1 Login/login.html")

def xlInventarioProductosVenta(request):
    if request.method == "POST":
        tipoProductos= request.POST['tipoProductos'] #A o I
        sucursalInventarioProductosVenta = request.POST['sucursalInventarioProductosVenta']
            
    response = HttpResponse(content_type='application/ms-excel')
    if tipoProductos == "productosVenta":
    
        response['Content-Disposition'] = 'attachment; filename=Reporte Inventario Productos para venta '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    elif tipoProductos == "productosGasto":
        response['Content-Disposition'] = 'attachment; filename=Reporte Inventario Productos gasto '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    elif tipoProductos == "productosRenta":
        response['Content-Disposition'] = 'attachment; filename=Reporte Inventario Productos para renta '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Productos')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    if tipoProductos == "productosVenta":
        columnas = ['Id','Código Producto','Nombre','SKU','Costo unitario','Existencias','Costo Total en inventario', 'Margen de ganancia', 'Costo de venta', 'Stock', 'Fecha de agregado','Sucursal']
    elif tipoProductos == "productosGasto":
        columnas = ['Id','Código Producto','Nombre','SKU','Costo unitario','Existencias','Costo Total en inventario', 'Stock', 'Fecha de agregado','Sucursal']
    elif tipoProductos == "productosRenta":
        columnas = ['Id','Código Producto','Nombre','Costo compra','Existencias','Estado de renta','Costo de renta', 'Fecha de agregado','Sucursal']
    
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
       
    
    #lista de productos dependiento de la sucursal
    if sucursalInventarioProductosVenta == "todas":
        if tipoProductos == "productosVenta":
            productosVenta = ProductosVenta.objects.all()
        elif tipoProductos == "productosGasto":
            productosVenta = ProductosGasto.objects.all()
        elif tipoProductos == "productosRenta":
            productosVenta = ProductosRenta.objects.all()
        
    else:
        if tipoProductos == "productosVenta":
            productosVenta = ProductosVenta.objects.filter(sucursal_id__id_sucursal = sucursalInventarioProductosVenta)
        elif tipoProductos == "productosGasto":
            productosVenta = ProductosGasto.objects.filter(sucursal_id__id_sucursal = sucursalInventarioProductosVenta)
        elif tipoProductos == "productosRenta":
            productosVenta = ProductosRenta.objects.filter(sucursal_id__id_sucursal = sucursalInventarioProductosVenta)
    
    sucursales = []
    costosTotalesProductos = []
    for producto in productosVenta:
        sucursalProducto = producto.sucursal_id
        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
        for datoSucursal in consultaSucursal:
            nombreSucursal = datoSucursal.nombre
            
        sucursales.append(nombreSucursal)
        
        if tipoProductos == "productosRenta":
            jejej = True
        else:
            costoCompraProducto = producto.costo_compra
            cantidadExistenteProducto = producto.cantidad
            
            costoTotalProducto = float(costoCompraProducto) * float(cantidadExistenteProducto)
            costosTotalesProductos.append(costoTotalProducto)
        
    datosProductos = []
    cont=0
    for x in productosVenta:
        cont+=1
        if tipoProductos == "productosVenta":
            datosProductos.append([x.id_producto, x.codigo_producto, x.nombre_producto,x.sku_producto, x.costo_compra,x.cantidad
                               ,costosTotalesProductos[cont-1],x.margen_ganancia_producto,x.costo_venta,x.stock,x.fecha_alta, sucursales[cont-1]
                            ])
        elif tipoProductos == "productosGasto":
            datosProductos.append([x.id_producto, x.codigo_producto, x.nombre_producto,x.sku_producto, x.costo_compra,x.cantidad
                               ,costosTotalesProductos[cont-1],x.stock,x.fecha_alta, sucursales[cont-1]
                            ])
        elif tipoProductos == "productosRenta":
            datosProductos.append([x.id_producto, x.codigo_producto, x.nombre_producto, x.costo_de_compra,x.cantidad
                               ,x.estado_renta,x.costo_renta,x.fecha_alta, sucursales[cont-1]
                            ])
            
        
    estilo_fuente = xlwt.XFStyle()
    for productito in datosProductos:
        numero_fila+=1
        for columna in range(len(productito)):
            hoja.write(numero_fila, columna, str(productito[columna]), estilo_fuente)
        
    
    
    
        
    libro.save(response)
    return response    
    #creación   

def xlInventarioCiclicoProductosVenta(request):
    if request.method == "POST":
        tipoProductos= request.POST['tipoProductos'] #A o I
        sucursalInventarioProductosVenta = request.POST['sucursalInventarioProductosVenta']
            
    response = HttpResponse(content_type='application/ms-excel')
    if tipoProductos == "productosVenta":
    
        response['Content-Disposition'] = 'attachment; filename=Reporte Inventario cíclico Productos para venta '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    elif tipoProductos == "productosGasto":
        response['Content-Disposition'] = 'attachment; filename=Reporte Inventario cíclico Productos gasto '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    elif tipoProductos == "productosRenta":
        response['Content-Disposition'] = 'attachment; filename=Reporte Inventario cíclico Productos para renta '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Productos')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Sucursal','Id','Código Producto','Nombre','SKU','Stock','Costo unitario de compra','Existencias en sistema','Cantidad Contada', 'Diferencia +/-']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
       
    
    #lista de productos dependiento de la sucursal
    if sucursalInventarioProductosVenta == "todas":
        if tipoProductos == "productosVenta":
            productosVenta = ProductosVenta.objects.all()
        elif tipoProductos == "productosGasto":
            productosVenta = ProductosGasto.objects.all()
        elif tipoProductos == "productosRenta":
            productosVenta = ProductosRenta.objects.all()
    else:
        if tipoProductos == "productosVenta":
            productosVenta = ProductosVenta.objects.filter(sucursal_id__id_sucursal = sucursalInventarioProductosVenta)
        elif tipoProductos == "productosGasto":
            productosVenta = ProductosGasto.objects.filter(sucursal_id__id_sucursal = sucursalInventarioProductosVenta)
        elif tipoProductos == "productosRenta":
            productosVenta = ProductosRenta.objects.filter(sucursal_id__id_sucursal = sucursalInventarioProductosVenta)
        
    
    sucursales = []
    costosTotalesProductos = []
    for producto in productosVenta:
        sucursalProducto = producto.sucursal_id
        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
        for datoSucursal in consultaSucursal:
            nombreSucursal = datoSucursal.nombre
            
        sucursales.append(nombreSucursal)
        
       
        
    datosProductos = []
    cont=0
    for x in productosVenta:
        cont+=1
        datosProductos.append([sucursales[cont-1],x.id_producto, x.codigo_producto, x.nombre_producto,x.sku_producto, x.stock,x.costo_compra,x.cantidad,"",""
                            ])
            
        
    estilo_fuente = xlwt.XFStyle()
    for productito in datosProductos:
        numero_fila+=1
        for columna in range(len(productito)):
            hoja.write(numero_fila, columna, str(productito[columna]), estilo_fuente)
        
    
    
    
        
    libro.save(response)
    return response    
    #creación 
    
def informeStockBajoProductosVenta(request):
    if request.method == "POST":
        tipoProductos= request.POST['tipoProductos']
        sucursalInventarioProductosVenta = request.POST['sucursalInventarioProductosVenta']
        
        if tipoProductos == "productosVenta":
            if sucursalInventarioProductosVenta == "todas":
                consultaProductosVenta = ProductosVenta.objects.all()
            else:
                consultaProductosVenta = ProductosVenta.objects.filter(sucursal_id__id_sucursal = sucursalInventarioProductosVenta)
                
        if tipoProductos == "productosGasto":
            if sucursalInventarioProductosVenta == "todas":
                consultaProductosVenta = ProductosGasto.objects.all()
            else:
                consultaProductosVenta = ProductosGasto.objects.filter(sucursal_id__id_sucursal = sucursalInventarioProductosVenta)
                
        if tipoProductos == "productosRenta":
            if sucursalInventarioProductosVenta == "todas":
                consultaProductosVenta = ProductosRenta.objects.all()
            else:
                consultaProductosVenta = ProductosRenta.objects.filter(sucursal_id__id_sucursal = sucursalInventarioProductosVenta)
            
                
        productosBajosEnStock = []
        for producto in consultaProductosVenta:
            existenciaActual = producto.cantidad
            stockActual = producto.stock
            
            if existenciaActual <= stockActual:
                idProducto = producto.id_producto
                codigoProducto = producto.codigo_producto
                nombreProducto = producto.nombre_producto
                skuProducto = producto.sku_producto
                costoUnitarioProducto = producto.costo_compra
                fechaAgregadoProducto = producto.fecha_alta
                sucursalProducto = producto.sucursal_id
                
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                for datoSucursal in consultaSucursal:
                    nombreSucursalProducto = datoSucursal.nombre
                    
                productosBajosEnStock.append([idProducto,codigoProducto,nombreProducto,skuProducto,costoUnitarioProducto,stockActual,existenciaActual,fechaAgregadoProducto,
                                              nombreSucursalProducto])
                    
        try:
            #Excel.
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=Reporte Stock Bajo Productos Venta '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
            
            libro = xlwt.Workbook(encoding='utf-8')
            hoja = libro.add_sheet('Productos')
            
            numero_fila = 0
            estilo_fuente = xlwt.XFStyle()
            estilo_fuente.font.bold = True
            
            columnas = ['Id','Código Producto','Nombre','SKU','Costo unitario','Stock','Existencias','Fecha de agregado','Sucursal']
            for columna in range(len(columnas)):
                hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
            
            estilo_fuente = xlwt.XFStyle()
            for productito in productosBajosEnStock:
                numero_fila+=1
                for columna in range(len(productito)):
                    hoja.write(numero_fila, columna, str(productito[columna]), estilo_fuente)
            

            libro.save(response)
            
            #Datos a mandar en correo.
            
            #datos de sucursal
            if sucursalInventarioProductosVenta == "todas":
                nombreSucursalCorreo = "Todas las sucursales"
            else:
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalInventarioProductosVenta)
                for datoSucursal in consultaSucursal:
                    nombreSucursalCorreo = datoSucursal.nombre
                
            #datos empleado
            nombresEmpleado = request.session['nombresSesion']
            
            if tipoProductos == "productosVenta":
                productos = "venta"
            elif tipoProductos == "productosGasto":
                productos = "gasto"
                
            
            #Mandar correo.
            correo = "sistemas@customco.com.mx"
            asunto = "Costabella | Informe de Productos Venta con stock bajo."
            plantilla = "6 Productos/Correos/correoStockPv.html"
            html_mensaje = render_to_string(plantilla,{"nombreSucursalCorreo":nombreSucursalCorreo,"nombresEmpleado":nombresEmpleado, "productos":productos}) #Aqui va el diccionario de datos.
            email_remitente = settings.EMAIL_HOST_USER
            email_destino = [correo]
            mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
            mensaje.content_subtype = 'html'
            #Mandar excel en el correo.
            mensaje.attach('Reporte Stock Bajo Productos Venta '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls', response.getvalue())
            mensaje.send()
            request.session['correoEnviado'] = "Se ha mandado el informe a tu correo electrónico!"
            return redirect('/inventarioProductos/')
        except:
            request.session['correoNoEnviado'] = "Error en el proceso, avisar a Soporte!"
            return redirect('/inventarioProductos/')
    
def ajusteProductosVenta(request):
    
    if request.method == "POST":
        
        sucursal = request.POST['sucursal']
        myfile = request.FILES['archivoExcelAjusteProductosVenta']     
        
        '''try:'''
       
        data = pd.read_excel(myfile, sheet_name="Productos")  
        
        sucursalesProductos = data['Sucursal'].tolist()
        idsProductosVenta = data['Id'].tolist()
        codigosProductosVenta = data['Código Producto'].tolist()
        nombresProductosVenta = data['Nombre'].tolist()
        skuProductosVenta = data['SKU'].tolist()
        stocksProductosVenta = data['Stock'].tolist()
        costosUnitariosProductosVenta = data['Costo unitario de compra'].tolist()
        existenciasProductosVenta = data['Existencias en sistema'].tolist()
        cantidadContadaProductosVenta = data['Cantidad Contada'].tolist()
        diferenciaProductosVenta = data['Diferencia +/-'].tolist()
        
        
        
        
        
        if sucursal == "todas":
            consultaProductosVenta = ProductosVenta.objects.all()
            sucursalCoincide = True
        else:
            sucuralDelExcel = sucursalesProductos[0] #Se saca la sucursal de un producto
            
            sucursalCoincide = True
            consultaSucursalElegida = Sucursales.objects.filter(id_sucursal = sucursal)
            for datoSucursal in consultaSucursalElegida:
                nombreSucursal = datoSucursal.nombre
                
            if nombreSucursal == sucuralDelExcel:
                consultaProductosVenta = ProductosVenta.objects.filter(sucursal_id__id_sucursal = sucursal)
            else:
                sucursalCoincide = False
        
        if sucursalCoincide:
            for productoVenta in consultaProductosVenta:
                idProducto = productoVenta.id_producto
                codigoProducto = productoVenta.codigo_producto 
                listaExcel = zip(idsProductosVenta,codigosProductosVenta,stocksProductosVenta,costosUnitariosProductosVenta,existenciasProductosVenta,cantidadContadaProductosVenta,diferenciaProductosVenta)
                for ida, codigo, stock, costo, existencias, cantidadContada, diferencia in listaExcel:
                    idProductoExcel = int(ida)
                    codigoProductoExcel = str(codigo)
                    
                    
                    if idProducto == idProductoExcel and codigoProducto == codigoProductoExcel:
                        isNaN = np.isnan(cantidadContada) #Si el campo de cantidad contada es nulo
                        
                        if isNaN == False:
                            
                            
                            stockProductoExcel = int(stock)
                            costoProductoExcel = float(costo)
                            existenciasProductoExcel = int(existencias)
                            cantidadContadaProductoExcel = int(cantidadContada)
                            diferenciaProductoExcel = str(diferencia)
                            
                            print(str(codigoProductoExcel)+" "+str(cantidadContadaProductoExcel))
                        
                            try:
                                actualizacionProducto = ProductosVenta.objects.filter(id_producto = idProductoExcel, codigo_producto = codigoProductoExcel).update(
                                    stock = stockProductoExcel, costo_compra = costoProductoExcel,cantidad = cantidadContadaProductoExcel)
                                
                                productosActualizados = True
                                
                            except:
                                productosActualizados = False
        
                            
        
            if productosActualizados:
                
                #CORREEEEEOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO 
                #datos de sucursal
                if sucursal == "todas":
                    nombreSucursalCorreo = "Todas las sucursales"
                else:
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                    for datoSucursal in consultaSucursal:
                        nombreSucursalCorreo = datoSucursal.nombre
                    
                #datos empleado
                nombresEmpleado = request.session['nombresSesion']
                
                productos = "venta"
                
                #Mandar el excel
                listaExcelSubido = zip(sucursalesProductos,idsProductosVenta,codigosProductosVenta,nombresProductosVenta,skuProductosVenta,stocksProductosVenta,
                                       costosUnitariosProductosVenta,existenciasProductosVenta,cantidadContadaProductosVenta,diferenciaProductosVenta)
                
                listaParaGenerarExcel = []
                for sucursalES, idES, codigoES, nombreES,skuES, stokES, costoUnitarioES, existenciasProductoES, cantidadContadaES, diferenciaProductosES in listaExcelSubido:
                    listaParaGenerarExcel.append([sucursalES,idES,codigoES,nombreES,skuES,stokES,costoUnitarioES,existenciasProductoES,cantidadContadaES,diferenciaProductosES])
                
                 #Excel.
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename=Ajuste productos venta '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
                
                libro = xlwt.Workbook(encoding='utf-8')
                hoja = libro.add_sheet('Productos')
                
                numero_fila = 0
                estilo_fuente = xlwt.XFStyle()
                estilo_fuente.font.bold = True
                
                columnas = ['Sucursal','Id','Código Producto','Nombre','SKU','Stock','Costo unitario de compra','Exsitencias en sistema','Cantidad Contada','Diferencia +/-']
                for columna in range(len(columnas)):
                    hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
                
                estilo_fuente = xlwt.XFStyle()
                for productito in listaParaGenerarExcel:
                    numero_fila+=1
                    for columna in range(len(productito)):
                        hoja.write(numero_fila, columna, str(productito[columna]), estilo_fuente)
                

                libro.save(response)
                
                
                #Mandar correo.
                correo = "sistemas@customco.com.mx"
                asunto = "Costabella | Ajuste de productos para venta."
                plantilla = "6 Productos/Correos/correoAjustePv.html"
                html_mensaje = render_to_string(plantilla,{"nombreSucursalCorreo":nombreSucursalCorreo,"nombresEmpleado":nombresEmpleado, "productos":productos}) #Aqui va el diccionario de datos.
                email_remitente = settings.EMAIL_HOST_USER
                email_destino = [correo]
                mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                mensaje.content_subtype = 'html'
                #Mandar excel en el correo.
                mensaje.attach('Ajuste de productos para venta '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls', response.getvalue())
                mensaje.send()
                
                
                
                # FIN CORREEEEOOOOOOOOOOOOOOOOOOOO
                
                # MANDAR NOTIFICACIÓN A TELÉFONO.
                try:
                    tokenTelegram = keysBotCostabella.tokenBotCostabella
                    botCostabella = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCostabella.idGrupo

                    if sucursal == "todas":
                        mensajeSucursalesTotdas = True
                    else:
                        mensajeSucursalesTotdas = False

                    date = datetime.now()
                    hora = date.time().strftime("%H:%M")

                    if mensajeSucursalesTotdas:
                        mensaje = "Hola \U0001F44B! La empleada administradora "+nombresEmpleado+" ha realizado un ajuste de existencias de productos para venta en todas las sucursales costabella a las "+str(hora)+" horas. Favor de checar correo electrónico"
                    else:
                        mensaje = "Hola \U0001F44B! La empleada "+nombresEmpleado+" ha realizado un ajuste de existencias de productos para venta en la sucursal "+nombreSucursalCorreo+" a las "+str(hora)+" horas. Favor de checar correo electrónico."
                    botCostabella.sendMessage(idGrupoTelegram,mensaje)

                except:
                    print("An exception occurred")
                
                    
                request.session['productosActualizados'] = "Se han actualizado los productos para venta con el Excel subido!"
                return redirect('/inventarioProductos/')  
            else:  
                request.session['errorProductosActualizados'] = "Error al actualizar los datos, intente de nuevo más tarde."
                return redirect('/inventarioProductos/')   
        else:
            request.session['errorProductosActualizados'] = "La sucursal elegida no coincide con la sucursal del Excel, favor de elegir bien la sucursal."
            return redirect('/inventarioProductos/')                    
            
def ajusteProductosGasto(request):
    
    if request.method == "POST":
        
        sucursal = request.POST['sucursal']
        myfile = request.FILES['archivoExcelAjusteProductosGasto']     
        
        try:
       
            data = pd.read_excel(myfile, sheet_name="Productos")  
            
            sucursalesProductos = data['Sucursal'].tolist()
            idsProductosVenta = data['Id'].tolist()
            codigosProductosVenta = data['Código Producto'].tolist()
            nombresProductosVenta = data['Nombre'].tolist()
            skuProductosVenta = data['SKU'].tolist()
            stocksProductosVenta = data['Stock'].tolist()
            costosUnitariosProductosVenta = data['Costo unitario de compra'].tolist()
            existenciasProductosVenta = data['Existencias en sistema'].tolist()
            cantidadContadaProductosVenta = data['Cantidad Contada'].tolist()
            diferenciaProductosVenta = data['Diferencia +/-'].tolist()
            
            
            
            
            
            if sucursal == "todas":
                consultaProductosGasto = ProductosGasto.objects.all()
                sucursalCoincide = True
            else:
                sucuralDelExcel = sucursalesProductos[0] #Se saca la sucursal de un producto
                
                sucursalCoincide = True
                consultaSucursalElegida = Sucursales.objects.filter(id_sucursal = sucursal)
                for datoSucursal in consultaSucursalElegida:
                    nombreSucursal = datoSucursal.nombre
                    
                if nombreSucursal == sucuralDelExcel:
                    consultaProductosGasto = ProductosGasto.objects.filter(sucursal_id__id_sucursal = sucursal)
                else:
                    sucursalCoincide = False
            
            if sucursalCoincide:
                for productoVenta in consultaProductosGasto:
                    idProducto = productoVenta.id_producto
                    codigoProducto = productoVenta.codigo_producto 
                    listaExcel = zip(idsProductosVenta,codigosProductosVenta,stocksProductosVenta,costosUnitariosProductosVenta,existenciasProductosVenta,cantidadContadaProductosVenta,diferenciaProductosVenta)
                    for ida, codigo, stock, costo, existencias, cantidadContada, diferencia in listaExcel:
                        idProductoExcel = int(ida)
                        codigoProductoExcel = str(codigo)
                        
                        
                        if idProducto == idProductoExcel and codigoProducto == codigoProductoExcel:
                            isNaN = np.isnan(cantidadContada) #Si el campo de cantidad contada es nulo
                            
                            if isNaN == False:
                                
                                
                                stockProductoExcel = int(stock)
                                costoProductoExcel = float(costo)
                                existenciasProductoExcel = int(existencias)
                                cantidadContadaProductoExcel = int(cantidadContada)
                                diferenciaProductoExcel = str(diferencia)
                                
                                print(str(codigoProductoExcel)+" "+str(cantidadContadaProductoExcel))
                            
                                try:
                                    actualizacionProducto = ProductosGasto.objects.filter(id_producto = idProductoExcel, codigo_producto = codigoProductoExcel).update(
                                        stock = stockProductoExcel, costo_compra = costoProductoExcel,cantidad = cantidadContadaProductoExcel)
                                    
                                    productosActualizados = True
                                    
                                except:
                                    productosActualizados = False
            
                                
            
                if productosActualizados: 
                    
                     #CORREEEEEOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO 
                    #datos de sucursal
                    if sucursal == "todas":
                        nombreSucursalCorreo = "Todas las sucursales"
                    else:
                        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                        for datoSucursal in consultaSucursal:
                            nombreSucursalCorreo = datoSucursal.nombre
                    
                    #datos empleado
                    nombresEmpleado = request.session['nombresSesion']
                    
                    productos = "gasto"
            
                    #Mandar el excel
                    listaExcelSubido = zip(sucursalesProductos,idsProductosVenta,codigosProductosVenta,nombresProductosVenta,skuProductosVenta,stocksProductosVenta,
                                       costosUnitariosProductosVenta,existenciasProductosVenta,cantidadContadaProductosVenta,diferenciaProductosVenta)

                    listaParaGenerarExcel = []
                    for sucursalES, idES, codigoES, nombreES,skuES, stokES, costoUnitarioES, existenciasProductoES, cantidadContadaES, diferenciaProductosES in listaExcelSubido:
                        listaParaGenerarExcel.append([sucursalES,idES,codigoES,nombreES,skuES,stokES,costoUnitarioES,existenciasProductoES,cantidadContadaES,diferenciaProductosES])
                    
                    #Excel.
                    response = HttpResponse(content_type='application/ms-excel')
                    response['Content-Disposition'] = 'attachment; filename=Ajuste productos venta '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
                    
                    libro = xlwt.Workbook(encoding='utf-8')
                    hoja = libro.add_sheet('Productos')
                    
                    numero_fila = 0
                    estilo_fuente = xlwt.XFStyle()
                    estilo_fuente.font.bold = True
                    
                    columnas = ['Sucursal','Id','Código Producto','Nombre','SKU','Stock','Costo unitario de compra','Exsitencias en sistema','Cantidad Contada','Diferencia +/-']
                    for columna in range(len(columnas)):
                        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
                    
                    estilo_fuente = xlwt.XFStyle()
                    for productito in listaParaGenerarExcel:
                        numero_fila+=1
                        for columna in range(len(productito)):
                            hoja.write(numero_fila, columna, str(productito[columna]), estilo_fuente)
                    

                    libro.save(response)
                    
                    #Mandar correo.
                    correo = "sistemas@customco.com.mx"
                    asunto = "Costabella | Ajuste de productos para venta."
                    plantilla = "6 Productos/Correos/correoAjustePv.html"
                    html_mensaje = render_to_string(plantilla,{"nombreSucursalCorreo":nombreSucursalCorreo,"nombresEmpleado":nombresEmpleado, "productos":productos}) #Aqui va el diccionario de datos.
                    email_remitente = settings.EMAIL_HOST_USER
                    email_destino = [correo]
                    mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                    mensaje.content_subtype = 'html'
                    #Mandar excel en el correo.
                    mensaje.attach('Ajuste de productos gasto '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls', response.getvalue())
                    mensaje.send()
                    
                    
                    
                    # FIN CORREEEEOOOOOOOOOOOOOOOOOOOO
                    try:
                        tokenTelegram = keysBotCostabella.tokenBotCostabella
                        botCostabella = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCostabella.idGrupo

                        if sucursal == "todas":
                            mensajeSucursalesTotdas = True
                        else:
                            mensajeSucursalesTotdas = False

                        date = datetime.now()
                        hora = date.time().strftime("%H:%M")

                        if mensajeSucursalesTotdas:
                            mensaje = "Hola \U0001F44B! La empleada administradora "+nombresEmpleado+" ha realizado un ajuste de existencias de productos gasto en todas las sucursales costabella a las "+str(hora)+" horas. Favor de checar correo electrónico."
                        else:
                            mensaje = "Hola \U0001F44B! La empleada "+nombresEmpleado+" ha realizado un ajuste de existencias de productos gasto en la sucursal "+nombreSucursalCorreo+" a las "+str(hora)+" horas. Favor de chercar correo electrónico."
                        botCostabella.sendMessage(idGrupoTelegram,mensaje)

                    except:
                        print("An exception occurred")

                    # MANDAR NOTIFICACIÓN A TELÉFONO.
                    
                
                               
                    request.session['productosActualizados'] = "Se han actualizado los productos para venta con el Excel subido!"
                    return redirect('/inventarioProductos/')  
                else:  
                    request.session['errorProductosActualizados'] = "Error al actualizar los datos, intente de nuevo más tarde."
                    return redirect('/inventarioProductos/')   
            else:
                request.session['errorProductosActualizados'] = "La sucursal elegida no coincide con la sucursal del Excel, favor de elegir bien la sucursal."
                return redirect('/inventarioProductos/')            
        
        except:
            request.session['errorProductosActualizados'] = "Error al subir el archivo, contacte a soporte."
            return redirect('/inventarioProductos/')
        
    