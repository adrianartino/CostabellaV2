#librerias
from operator import truediv
from pyexpat import model
from django.db import models
from django.db.models.deletion import CASCADE
from django.forms import SelectDateWidget


# Create your models here.

#Modelo sucursales

class Sucursales (models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    direccion = models.TextField(max_length=100)
    telefono = models.TextField( null=True)
    latitud = models.CharField(max_length=40, null=True)
    longitud = models.CharField(max_length=40, null=True)
    
    def __str__(self):
        return str (self.id_sucursal())
    
class Empleados (models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=20)
    contrasena = models.CharField(max_length=20)
    nombres = models.CharField(max_length=40)
    apellido_paterno = models.CharField(max_length=20)
    apellido_materno = models.CharField(max_length=20)
    telefono = models.TextField( null=True)
    puesto = models.CharField(max_length=30)
    fecha_alta = models.DateField()
    fecha_baja = models.DateField(null=True)
    estado_contratacion = models.CharField(max_length=2)
    id_sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, null=True)
    tipo_usuario = models.CharField(max_length=2, null=True)

    
    def __str__(self):
        return str (self.id_empleado())
    
class Clientes (models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=40)
    apellidoPaterno_cliente = models.CharField(max_length=20)
    apellidoMaterno_cliente = models.CharField(max_length=20)
    correo = models.CharField(max_length=30, null=True)
    telefono = models.TextField( null=True)
    direccion = models.TextField(max_length=100)
    fecha_agregado = models.DateField()
    agregado_por = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)
    estado = models.CharField(max_length=2, null=True)
    credito_libre = models.CharField(max_length=2, null=True)
    monto_credito_disponible = models.FloatField(max_length=8, null=True)

    
    def __str__(self):
        return str (self.id_cliente())
    
class ProductosVenta(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo_producto = models.CharField(max_length=6)
    codigo_barras = models.CharField(max_length=13, null=True)
    tipo_producto = models.CharField(max_length=100)
    nombre_producto = models.CharField(max_length=50)
    costo_compra = models.FloatField()
    margen_ganancia_producto = models.FloatField(null=True)
    costo_venta = models.FloatField()
    costo_venta_a_credito = models.FloatField(null=True)
    cantidad = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.CharField(max_length=255)
    imagen_producto=models.ImageField(upload_to="productosVentas", null = True)
    fecha_alta = models.DateField()
    sku_producto = models.CharField(max_length=30,null=True)
    creado_por = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str (self.id_producto())
    
    def json(self):
        return {
            'id_producto': self.id_producto,
            'codigo_producto':self.codigo_producto,
            'codigo_barras':self.codigo_barras,
            'tipo_producto':self.tipo_producto,
            'nombre_producto':self.nombre_producto,
            'costo_compra':self.costo_compra,
            'cantidad':self.cantidad,
            'stock':self.stock,
            'costo_venta':self.costo_venta,
            'costo_venta_a_credito':self.costo_venta_a_credito,
            'descripcion':self.descripcion,
            'imagen_producto':str(self.imagen_producto),
            'fecha_alta':str(self.fecha_alta),
            'sku_producto':str(self.sku_producto),
          
            
        }
    
    

class ProductosRenta(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo_producto = models.CharField(max_length=6)
    codigo_barras = models.CharField(max_length=13, null=True)
    tipo_producto = models.CharField(max_length=100)
    nombre_producto = models.CharField(max_length=50)
    costo_de_compra = models.FloatField(null=True)
    costo_renta = models.FloatField()
    cantidad = models.IntegerField()
    estado_renta = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=255)
    imagen_producto=models.ImageField(upload_to="productosRentas", null = True)
    fecha_alta = models.DateField()
    creado_por = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str (self.id_producto())
    
    def jsonRenta(self):
        return {
            'id_producto': str(self.id_producto),
            'codigo_producto':self.codigo_producto,
            'codigo_barras':self.codigo_barras,
            'tipo_producto':self.tipo_producto,
            'nombre_producto':self.nombre_producto,
            'costo_de_compra':self.costo_de_compra,
            'costo_renta':self.costo_renta,
            'cantidad':self.cantidad,
            'estado_renta':self.estado_renta,
            'descripcion':(self.descripcion),
            'imagen_producto':str(self.imagen_producto),
            'fecha_alta':str(self.fecha_alta)
        }

class ProductosGasto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo_producto = models.CharField(max_length=6)
    codigo_barras = models.CharField(max_length=13, null=True)
    tipo_producto = models.CharField(max_length=100)
    nombre_producto = models.CharField(max_length=50)
    costo_compra = models.FloatField()
    cantidad = models.IntegerField()
    stock = models.IntegerField()
    contenido_cuantificable = models.CharField(max_length=2, null = True)
    descripcion = models.CharField(max_length=255)
    imagen_producto=models.ImageField(upload_to="productosGastos", null = True)
    fecha_alta = models.DateField()
    sku_producto = models.CharField(max_length=30,null=True)
    creado_por = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str (self.id_producto())
    
    
    def json(self):
        return {
            'id_producto': self.id_producto,
            'codigo_producto':self.codigo_producto,
            'codigo_barras':self.codigo_barras,
            'tipo_producto':self.tipo_producto,
            'nombre_producto':self.nombre_producto,
            'costo_compra':self.costo_compra,
            'cantidad':self.cantidad,
            'stock':self.stock,
            'contenido_cuantificable':self.contenido_cuantificable,
            'descripcion':self.descripcion,
            'imagen_producto':str(self.imagen_producto),
            'fecha_alta':str(self.fecha_alta),
            'sku_producto':str(self.sku_producto),
          
            
        }
    
class ComprasVentas(models.Model):
    id_compraVenta = models.AutoField(primary_key = True)
    id_productoComprado = models.ForeignKey(ProductosVenta, on_delete=models.CASCADE, null=True)
    costo_unitario = models.FloatField()
    cantidad_comprada = models.IntegerField()
    total_costoCompra = models.FloatField()
    fecha_compra = models.DateField()
    
    def __str__(self):
        return str (self.id_compraVenta())
    
class ComprasRentas(models.Model):
    id_compraRenta = models.AutoField(primary_key = True)
    id_productoComprado = models.ForeignKey(ProductosRenta, on_delete=models.CASCADE, null=True)
    costo_unitario = models.FloatField()
    cantidad_comprada = models.IntegerField()
    total_costoCompra = models.FloatField()
    fecha_compra = models.DateField()
    
    def __str__(self):
        return str (self.id_compraRenta())
        
class ComprasGastos(models.Model):
    id_compraGasto = models.AutoField(primary_key = True)
    id_productoComprado = models.ForeignKey(ProductosGasto, on_delete=models.CASCADE, null=True)
    costo_unitario = models.FloatField()
    cantidad_comprada = models.IntegerField()
    total_costoCompra = models.FloatField()
    fecha_compra = models.DateField()
    
    def __str__(self):
        return str (self.id_compraGasto())
    
       
class ConfiguracionCaja(models.Model):
    id_configuracion = models.AutoField(primary_key = True)
    fondo = models.FloatField()
    minimo_corte_caja = models.FloatField()
    fecha = models.DateField()
    activo = models.CharField(max_length=3,null=True)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str (self.id_configuracion())

class ConfiguracionCredito(models.Model):
    id_configuracion_credito = models.AutoField(primary_key = True)
    limite_credito = models.FloatField()
    fecha = models.DateField()
    activo = models.CharField(max_length=3,null=True)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str (self.id_configuracion())
    
     
class MovimientosCaja(models.Model):
    id_movimiento = models.AutoField(primary_key = True)
    fecha = models.DateField()
    hora = models.TimeField(null=True)
    tipo = models.CharField(max_length=2, null = True)
    monto = models.FloatField()
    descripcion = models.CharField(max_length=255)
    realizado_por = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str (self.id_movimiento())
    
    
class Rentas(models.Model):
    id_renta = models.AutoField(primary_key = True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True)
    codigos_productos_renta = models.CharField(max_length=255, null=True)
    fecha_apartado = models.DateField(null=True)
    fecha_entrega_renta = models.DateField()
    fecha_limite_devolucion =models.DateField()
    fecha_devolucion = models.DateField(null=True)
    fecha_limite_devolucion_cuota =models.DateField(null=True)
    estado_devolucion = models.CharField(max_length=2, null = True)  #P de pendiente F de finalizadas A de apartdo
    descripcion_devolucion = models.CharField(max_length=255, null=True)
    cuota_retraso =models.CharField(max_length=2,null=True)
    monto_cuota = models.FloatField(null=True)
    cuota_saldada=models.CharField(max_length=2,null=True)
    monto_total_renta = models.FloatField(null=True)
    monto_min_apartado = models.FloatField(null=True)
    monto_pago_apartado = models.FloatField(null=True)
    monto_pago_restante = models.FloatField(null=True)
    monto_restante = models.FloatField(null=True)
    comentarios_renta = models.TextField(null=True)
    realizado_por = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str (self.id_renta())
    
    
class Servicios(models.Model):
    id_servicio = models.AutoField(primary_key = True)
    tipo_servicio = models.CharField(max_length=30)
    nombre_servicio = models.CharField(max_length=80)
    descripcion_servicio = models.CharField(max_length=255, null=True)
    tiempo_minimo = models.CharField(max_length=5)
    tiempo_maximo = models.CharField(max_length=5)
    precio_venta = models.FloatField()
    complementos_servicio = models.CharField(max_length=255, null=True)
    
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str (self.id_servicio())

    def jsonServicios(self):
        idServicio = int(self.id_servicio)
        consultaProductosQueUtilizaElServicio = ServiciosProductosGasto.objects.filter(servicio = idServicio) #2 pos. 


        servicioSePuedeVender = False
        productosQueUtiliza = []
        cuantosCaben = []
        for producto in consultaProductosQueUtilizaElServicio:
            idProducto = producto.producto_gasto_id
            cantidadQueSeUtilizaAlVender = producto.cantidad #Si se vende, se utiliza 1 producto
            consultaDatosProducto = ProductosGasto.objects.filter(id_producto = idProducto)
            for datoProducto in consultaDatosProducto:
                cantidadEnExistencia = datoProducto.cantidad # 4 unidades
                nombreProducto = datoProducto.nombre_producto
                codigo = datoProducto.codigo_producto
            if cantidadEnExistencia >= cantidadQueSeUtilizaAlVender:
                division = cantidadEnExistencia/cantidadQueSeUtilizaAlVender
                divisionRedondeada = round(division)
                cuantosCaben.append(divisionRedondeada)
                #Si se puede vendeeeeerr... 
                servicioSePuedeVender = True
                #Guardar los productos
                productosQueUtiliza.append([codigo,nombreProducto,cantidadQueSeUtilizaAlVender])
            else:
                #No se puede venderrrrr.... 
                servicioSePuedeVender = False
        
        menor=0
        if servicioSePuedeVender == True:
            menor = cuantosCaben[0]
            for dato in cuantosCaben:
                if dato < menor:
                    menor = dato
                    
        return {
            'id_servicio': str(self.id_servicio),
            'tipo_servicio':self.tipo_servicio,
            'nombre_servicio':self.nombre_servicio,
            'descripcion_servicio':self.descripcion_servicio,
            'tiempo_minimo':self.tiempo_minimo,
            'tiempo_maximo':self.tiempo_maximo,
            'precio_venta':self.precio_venta,
            'complementos_servicio':self.complementos_servicio,
            'maximo_servicio':int(menor)
        }
    
    
class ServiciosProductosVenta(models.Model):
    id_servicio_producto_venta = models.AutoField(primary_key = True)
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, null=True)
    producto_venta = models.ForeignKey(ProductosVenta, on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField(null=True)
    
    def __str__(self):
        return str (self.id_servicio_producto_venta())
    
class ServiciosProductosGasto(models.Model):
    id_servicio_producto_gasto = models.AutoField(primary_key = True)
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, null=True)
    producto_gasto = models.ForeignKey(ProductosGasto, on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField(null=True)
  
    
    
    def __str__(self):
        return str (self.id_servicio_producto_gasto())
    


    
class Descuentos(models.Model):
    id_descuento = models.AutoField(primary_key = True)
    nombre_descuento = models.CharField(max_length=80) 
    porcentaje =models.IntegerField()
    fecha_agregado = models.DateField()
    descripcion_descuento = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return str (self.id_descuento())
    

    
    
    


    
class Permisos(models.Model):
    id_permiso = models.AutoField(primary_key = True)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)
    ver =models.CharField(max_length=2,null=True)
    agregar =models.CharField(max_length=2,null=True)
    editar =models.CharField(max_length=2,null=True)
    bloquear =models.CharField(max_length=2,null=True)
    ver_detalles =models.CharField(max_length=2,null=True)
    activar =models.CharField(max_length=2,null=True)
    comprar =models.CharField(max_length=2,null=True)
    recibir_pagos =models.CharField(max_length=2,null=True)
    tabla_modulo =models.CharField(max_length=100,null=True)

    
    
    def __str__(self):
        return str (self.id_permiso())
    
class Tratamientos(models.Model):
    id_tratamiento = models.AutoField(primary_key = True)
    codigo_tratamiento = models.CharField(max_length=20)
    tipo_tratamiento = models.CharField(max_length=30)
    nombre_tratamiento = models.CharField(max_length=80)
    descripcion_tratamiento = models.CharField(max_length=255, null=True)
    costo_venta_tratamiento = models.FloatField()
    tiempo_minimo = models.CharField(max_length=5)
    tiempo_maximo = models.CharField(max_length=5)
    complementos_tratamiento = models.CharField(max_length=255, null=True)
    sesiones_rec_tratamiento = models.FloatField()
    periodo_rec_tratamiento = models.CharField(max_length=255)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str (self.id_tratamiento())
    
class TratamientosProductosGasto(models.Model):
    id_tratamiento_producto_gasto = models.AutoField(primary_key = True)
    tratamiento = models.ForeignKey(Tratamientos, on_delete=models.CASCADE, null=True)
    producto_gasto = models.ForeignKey(ProductosGasto, on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField(null=True)
  
    def __str__(self):
        return str (self.id_tratamiento_producto_gasto())

class PaquetesPromocionTratamientos(models.Model):
    id_paquete_tratamiento = models.AutoField(primary_key = True)
    tratamiento = models.ForeignKey(Tratamientos, on_delete=models.CASCADE, null=True)
    nombre_paquete = models.CharField(max_length=60, null = True)
    numero_sesiones = models.IntegerField()
    descuento = models.FloatField(null = True)
    precio_por_paquete = models.FloatField()
    promocion_activa = models.CharField(max_length=2)

    def __str__(self):
        return str (self.id_paquete_tratamiento())



class TratamientosClientes(models.Model):
    id_tratamiento_cliente = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True)
    paquete_tratamiento = models.ForeignKey(PaquetesPromocionTratamientos, on_delete=models.CASCADE, null=True)
    num_sesiones = models.IntegerField()
    sesionesPendientes = models.IntegerField()
    sesionesCanjeadas = models.IntegerField()

    def __str__(self):
        return str (self.id_tratamiento_cliente())



class HistorialTratamientosClientes(models.Model):
    id_historial_tratamiento = models.AutoField(primary_key=True)
    tratamiento_cliente = models.ForeignKey(TratamientosClientes, on_delete=models.CASCADE, null=True)
    sesion_efectuada = models.IntegerField()
    fecha_efectuado = models.DateField()
    fecha_proxima_sesion = models.DateField(null = True)

    def __str__(self):
        return str (self.id_historial_tratamiento())


class Ventas(models.Model):
    id_venta = models.AutoField(primary_key = True)
    fecha_venta =models.DateField()
    hora_venta = models.TimeField(null=True)
    tipo_pago = models.CharField(max_length=50, null = True)  #P de pendiente F de finalizadas
    tipo_tarjeta = models.CharField(max_length=50, null = True)
    referencia_pago_tarjeta = models.CharField(max_length=50, null=True)
    clave_rastreo_transferencia = models.CharField(max_length=50, null=True)
    empleado_vendedor = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True)
    ids_productos = models.CharField(max_length=255, null=True)
    cantidades_productos = models.CharField(max_length=255, null=True)
    ids_servicios_corporales = models.CharField(max_length=255, null=True)
    cantidades_servicios_corporales = models.CharField(max_length=255, null=True)
    ids_servicios_faciales = models.CharField(max_length=255, null=True)
    cantidades_servicios_faciales =models.CharField(max_length=255, null=True)
    id_tratamiento_vendido = models.ForeignKey(Tratamientos, on_delete=models.CASCADE, null=True)
    id_paquete_promo_vendido = models.ForeignKey(PaquetesPromocionTratamientos, on_delete=models.CASCADE, null=True)
    monto_pagar = models.FloatField()
    credito =models.CharField(max_length=2,null=True)
    cuota =models.CharField(max_length=2,null=True)
    
    descuento = models.ForeignKey(Descuentos, on_delete=models.CASCADE, null=True)
    comentariosVenta = models.TextField(null=True)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str (self.id_venta())

class Creditos(models.Model):
    id_credito = models.AutoField(primary_key = True)
    fecha_venta_credito =models.DateField()
    empleado_vendedor = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True)
    concepto_credito = models.CharField(max_length = 200, null=True) #renta o venta
    descripcion_credito = models.TextField(null=True) #se detalla el 
    renta = models.ForeignKey(Rentas, on_delete=models.CASCADE, null=True)
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE, null=True)
    monto_pagar = models.FloatField()
    fechas_pago = models.CharField(max_length = 200, null=True)
    monto_pagado = models.FloatField(null=True)
    monto_restante = models.FloatField()
    estatus = models.CharField(max_length=50) #Pendiente, Finalizado
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, null=True)
    
    
    def __str__(self):
        return str (self.id_credito())

class PagosCreditos(models.Model):
    id_historialCredito = models.AutoField(primary_key = True)
    id_credito = models.ForeignKey(Creditos, on_delete=models.CASCADE, null=True)
    fecha_pago1 = models.DateField(null=True)
    tipo_pago1 = models.CharField(max_length = 50, null=True)
    tipo_tarjeta1 = models.CharField(max_length=50, null = True)
    referencia_pago_tarjeta1 = models.CharField(max_length=50, null=True)
    clave_rastreo_pago_transferencia1 = models.CharField(max_length=50, null=True)
    monto_pago1 = models.FloatField(null=True)
    fecha_pago2 = models.DateField(null=True)
    tipo_pago2 = models.CharField(max_length = 50, null=True)
    tipo_tarjeta2 = models.CharField(max_length=50, null = True)
    referencia_pago_tarjeta2 = models.CharField(max_length=50, null=True)
    clave_rastreo_pago_transferencia2 = models.CharField(max_length=50, null=True)
    monto_pago2 = models.FloatField(null=True)
    fecha_pago3 = models.DateField(null=True)
    tipo_pago3 = models.CharField(max_length = 50, null=True)
    tipo_tarjeta3 = models.CharField(max_length=50, null = True)
    referencia_pago_tarjeta3 = models.CharField(max_length=50, null=True)
    clave_rastreo_pago_transferencia3 = models.CharField(max_length=50, null=True)
    monto_pago3 = models.FloatField(null=True)
    fecha_pago4 = models.DateField(null=True)
    tipo_pago4 = models.CharField(max_length = 50, null=True)
    tipo_tarjeta4 = models.CharField(max_length=50, null = True)
    referencia_pago_tarjeta4 = models.CharField(max_length=50, null=True)
    clave_rastreo_pago_transferencia4 = models.CharField(max_length=50, null=True)
    monto_pago4 = models.FloatField(null=True)
    
    def __str__(self):
        return str (self.id_historialCredito())

class Citas(models.Model):
    id_cita = models.AutoField(primary_key = True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, null=True)
    empleado_realizo = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)
    tipo_cita = models.CharField(max_length=50)
    id_serv_trat_paq = models.IntegerField(null = True)
    certificado_servicio = models.CharField(max_length=50, null = True)
    fecha_pactada = models.DateField()
    hora_pctada = models.CharField(max_length = 20, null = True)
    estado_cita = models.CharField(max_length = 10)
    cita_vendida = models.CharField(max_length = 10)
    venta = models.ForeignKey(Ventas,on_delete=models.CASCADE, null=True)
    comentarios = models.CharField(max_length=255, null = True)
    duracionCitaMinutos = models.FloatField(null=True)

    def __str__(self):
        return str (self.id_cita())

class citasTratamientos(models.Model):
    id_cita_tratamiento = models.AutoField(primary_key=True)
    cita = models.ForeignKey(Citas, on_delete=models.CASCADE, null=True)
    idTratamientoCliente = models.ForeignKey(TratamientosClientes, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str (self.id_cita_tratamiento())

class pagosPaquetesTratamientos(models.Model):
    id_pago_paquete = models.AutoField(primary_key=True)
    id_tratamiento_cliente = models.ForeignKey(TratamientosClientes, on_delete=models.CASCADE, null=True)
    total_pagar = models.FloatField()
    total_abonado = models.FloatField()
    total_restante = models.FloatField()
    estatus_pago = models.CharField(max_length=15)



class CortesDeCaja (models.Model):
    id_corte_caja = models.AutoField(primary_key=True)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE)
    fecha_corte = models.DateField()
    hora_corte = models.CharField(max_length=20)
    monto_ingresos_venta = models.FloatField()
    monto_ingresos_manuales = models.FloatField()
    monto_retiros_manuales = models.FloatField()
    monto_total_corte = models.FloatField()
    empleado_corte = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    
    def __str__(self):
        return str (self.id_corte_caja())



class ServiciosCertificados (models.Model):
    id_servicio_certificado = models.AutoField(primary_key=True)
    codigo_servocio = models.CharField(max_length=60, null=True)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60)
    precio = models.FloatField()
    tiempo_minimo = models.CharField(max_length=5, null = True)
    tiempo_maximo = models.CharField(max_length=5, null = True)
    descripcion = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str (self.id_servicio_certificado())

    def json(self):
        return {
            'id_servicio_certificado': str(self.id_servicio_certificado),
            'codigo_servocio':str(self.codigo_servocio),
            'nombre':str(self.nombre),
            'precio':str(self.precio),
            'descripcion':str(self.descripcion),
        }

class ProductosServiciosCertificados (models.Model):
    id_producto_servicio = models.AutoField(primary_key=True)
    servicio_certificado = models.ForeignKey(ServiciosCertificados, on_delete=models.CASCADE)
    producto_gasto = models.ForeignKey(ProductosGasto, on_delete=models.CASCADE)
    cantidad_utilizada = models.IntegerField()

    def __str__(self):
        return str (self.id_producto_servicio())

class CertificadosProgramados (models.Model):
    id_certificado = models.AutoField(primary_key=True)
    codigo_certificado = models.CharField(max_length=20)
    fecha_alta = models.DateField()
    vigencia = models.DateField()
    lista_servicios_certificados = models.CharField(max_length=100)
    lista_cantidades_servicios = models.CharField(max_length=100)
    lista_precios = models.CharField(max_length=200)
    lista_servicios_efectuados = models.CharField(max_length=200, null = True)
    cliente_compro = models.ForeignKey(Clientes, on_delete=models.CASCADE, null = True)
    nombre_beneficiaria = models.CharField(max_length=100, null=True)
    correo_beneficiaria = models.CharField(max_length=100, null=True)
    monto_total_pagar = models.FloatField()
    monto_total_canjeado = models.FloatField()
    estatus_certificado = models.CharField(max_length=4)
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)

    def __str__(self):
        return str (self.id_certificado())

