# Importar vistas de aplicacion
from appCostabella import views


# Importar vistas ya acomodadas
from appCostabella.vInicio import viewInicio
from appCostabella.vEmpleados import viewEmpleados
from appCostabella.vClientes import viewClientes
from appCostabella.vSucursales import viewSucursales
from appCostabella.vProductos import viewProductos
from appCostabella.vCompras import viewCompras
from appCostabella.vCaja import viewCaja
from appCostabella.vRentas import viewRentas
from appCostabella.vServicios import viewServicios
from appCostabella.vDescuentos import viewDescuentos
from appCostabella.vVentas import viewVentas
from appCostabella.vCreditos import viewCreditos
from appCostabella.vPermisos import viewPermisos
from appCostabella.vInformes import viewInformes
from appCostabella.vTratamientos import viewTratamientos
from appCostabella.vPromocionesTratamientos import viewPromocionesTratamientos
from appCostabella.vCitas import viewCitas
from appCostabella.vCertificados import viewCertificados
from appCostabella.vMovimientosVestidos import viewMovimientosVestidos


from django.conf import settings  # Importar archivo de configuración.
from django.conf.urls.static import static  # Importar archivos estáticos
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),

# VIEWS INICIO ---------------------------------------------------------------------------------------------------------------
    # Login
    path("login/", viewInicio.login),
    # URL inicio
    path("inicio/", viewInicio.inicio),
    path("", viewInicio.inicio),
    # Cerrar sesion
    path("salir/", views.salir),

# VIEWS EMPLEADOS -------------------------------------------------------------------------------------------------------------
    # Empleados
    path("altaEmpleado/", viewEmpleados.altaEmpleado),
    path("verEmpleados/", viewEmpleados.verEmpleados),
    # Editar configuracion empleado
    path("editarConfiguracionEmpleado/", viewEmpleados.editarConfiguracionEmpleado),
    # Informe empleado
    path("informeEmpleado/", views.informeEmpleado),
    # Actualizacion de datos de empleado
    path("editarEmpleado/", viewEmpleados.editarEmpleado),
    path("actInfoPersonal/", viewEmpleados.actInfoPersonal),
    path("actInfoLaboral/", viewEmpleados.actInfoLaboral),
    path("actNombreUsuario/", viewEmpleados.actNombreUsuario),
    path("actContrasena/", viewEmpleados.actContrasena),
    # Alta y baja de empleado
    path("darAltaEmpleado/", viewEmpleados.darAltaEmpleado),
    path("darBajaEmpleado/", viewEmpleados.darBajaEmpleado),

# VIEWS SUCURSALES -------------------------------------------------------------------------------------------------------------
    # Sucursales 
    path("altaSucursal/", viewSucursales.altaSucursal),
    path("verSucursales/", viewSucursales.verSucursales),

# VIEWS CLIENTES ----------------------------------------------------------------------------------------------------------------
    # Clientes
    path("verClientes/", viewClientes.verClientes),
    path("altaCliente/", viewClientes.altaCliente),
    # Cambio de estatus de clientes
    path("activoCliente/", viewClientes.activoCliente),
    path("bloqueoCliente/", viewClientes.bloqueoCliente),
    # Información de cliente
    path("infoCliente/", viewClientes.infoCliente),
    # Actualizar telefono de contacto de cliente
    path("actTelCliente/", viewClientes.actTelCliente),
    
# VIEWS PRODUCTOS -----------------------------------------------------------------------------------------------------------------
    # Productos
    path("altaProductos/", viewProductos.altaProductos),
    path("inventarioProductos/", viewProductos.inventarioProductos),
    # Actualizacion de producto
    path("actualizarProductoV/", viewProductos.actualizarProductoV),
    path("actualizarProductoVentaCompra/", viewProductos.actualizarProductoVentaCompra),
    path("actualizarProductoGasto/", viewProductos.actualizarProductoGasto),
    path("actualizarProductoGastoCompra/", viewProductos.actualizarProductoGastoCompra),
    path("actualizarProductoRenta/", viewProductos.actualizarProductoRenta),
    # Impresion de código de barras
    path("imprimirCodigoBarras/", viewProductos.imprimirCodigoBarras),
    # Exceles
    path("xlInventarioProductosVenta/", viewProductos.xlInventarioProductosVenta),
    path("xlInventarioCiclicoProductosVenta/", viewProductos.xlInventarioCiclicoProductosVenta),
    # Ajustes
    path("ajusteProductosVenta/", viewProductos.ajusteProductosVenta),
    path("ajusteProductosGasto/", viewProductos.ajusteProductosGasto),
    # Informe de stock bajo en productosVenta
    path("informeStockBajoProductosVenta/", viewProductos.informeStockBajoProductosVenta),
    
# VIEWS COMPRAS ----------------------------------------------------------------------------------------------------------------------------------
    # compras
    path("inventarioCompras/", viewCompras.inventarioCompras),
    
# VIEWS CAJA --------------------------------------------------------------------------------------------------------------------------------------
    # Caja
    path("configuracionCaja/", viewCaja.configuracionCaja),
    path("agregarConfiguracionCaja/", viewCaja.agregarConfiguracionCaja),
    path("movimientosCaja/", viewCaja.movimientosCaja),
    path("agregarMovimientoCaja/", viewCaja.agregarMovimientoCaja),
    path("activarConfiguracionCaja/", viewCaja.activarConfiguracionCaja),
    path("seleccionarSucursalMovimientosDia/", viewCaja.seleccionarSucursalMovimientosDia),
    path("verSucursalMovimientosDia/", viewCaja.verSucursalMovimientosDia),
    path("seleccionarSucursalCortesDeCaja/", viewCaja.seleccionarSucursalCortesDeCaja),
    path("cortesDeCaja/", viewCaja.cortesDeCaja),
    path("realizarCorteDeCaja/", views.realizarCorteDeCaja),
    
# VIEWS RENTAS --------------------------------------------------------------------------------------------------------------------------------------
    # RENTAS
    path("rentas/", viewRentas.rentas),
    path("altaRenta/", viewRentas.altaRenta),
    path("entregarRentaApartada/", viewRentas.entregarRentaApartada),
    path("verCalendarioRentas/", viewRentas.verCalendarioRentas),
    path("seleccionarSucursalRentas/", viewRentas.seleccionarSucursalRentas),
    path("guardarRentas/", viewRentas.guardarRentas),
    path("recibirRentaDevolucionCliente/", viewRentas.recibirRentaDevolucionCliente),
    path("recibirPagoCuota/", viewRentas.recibirPagoCuota),
    path("notificacionRentasDeHoy/", viewRentas.notificacionRentasDeHoy),
    
# VIEWS SERVICIOS --------------------------------------------------------------------------------------------------------------------------------------
    # Servicios
    path("altaServicios/", viewServicios.altaServicios),
    path("inventarioServicios/", viewServicios.inventarioServicios),
    path("actualizarServiciosCoporales/", viewServicios.actualizarServiciosCoporales),
    path("actualizarServiciosFaciales/", viewServicios.actualizarServiciosFaciales),
    path("crearPaqueteServicios/", viewServicios.crearPaqueteServicios),
    path("crearPaqueteServicioConProductosVenta/",viewServicios.crearPaqueteServicioConProductosVenta),
    path("guardarPaquete/", viewServicios.guardarPaquete),
    path("guardarPaqueteEditadoProductosVenta/",viewServicios.guardarPaqueteEditadoProductosVenta),
    path("actualizarPaquete/", viewServicios.actualizarPaquete),
    path("actualizarPaqueteFacial/", viewServicios.actualizarPaqueteFacial),
    path("verProductoDePaqueteCorporalEditar/", viewServicios.verProductoDePaqueteCorporalEditar),
    path("verProductoDePaqueteFacialEditar/", viewServicios.verProductoDePaqueteFacialEditar),
    path("inventarioPaqueteServicios/", viewServicios.inventarioPaqueteServicios),
    
# VIEW DESCUENTOS -------------------------------------------------------------------------------------------------------------------------------
    # Descuentos
    path("descuentos/", viewDescuentos.descuentos),
    path("altaDescuentos/", viewDescuentos.altaDescuentos),
    path("actualizarDescuentos/", viewDescuentos.actualizarDescuentos),
    
# VIEW VENTAS ------------------------------------------------------------------------------------------------------------------------------------
    # Ventas
    path("ventas/", viewVentas.ventas),
    path("realizarVenta/", viewVentas.realizarVenta),
    path("seleccionarSucursalVentas/", viewVentas.seleccionarSucursalVentas),
    path("guardarVenta/", viewVentas.guardarVenta),
    path("infoVenta/", viewVentas.infoVenta),

# VIEWS CREDITOS -----------------------------------------------------------------------------------------------------------------------------------
    # Creditos
    path("configuracionCredito/", viewCreditos.configuracionCredito),
    path("agregarConfiguracionCredito/", viewCreditos.agregarConfiguracionCredito),
    path("verCreditosClientes/", viewCreditos.verCreditosClientes),
    path("activarConfiguracionCredito/", viewCreditos.activarConfiguracionCredito),
    path("pagosCreditosClientes/", viewCreditos.pagosCreditosClientes),
    path("guardarPago1/", viewCreditos.guardarPago1),
    path("guardarPago2/", viewCreditos.guardarPago2),
    path("guardarPago3/", viewCreditos.guardarPago3),
    path("guardarPago4/", viewCreditos.guardarPago4),

# VIEWS PERMISOS ---------------------------------------------------------------------------------------------------------------------------------------
    # Panel administrativo
    path("verPanelAdministrativo/", viewPermisos.verPanelAdministrativo),
    path("actualizarPermisosPanelAdministraativo/",viewPermisos.actualizarPermisosPanelAdministraativo),
    # Empleados
    path("actualizarPermisosEmpleados/", viewPermisos.actualizarPermisosEmpleados),
    # Clientes
    path("actualizarPermisosClientes/", viewPermisos.actualizarPermisosClientes),
    # Sucursales
    path("actualizarPermisosSucursales/", viewPermisos.actualizarPermisosSucursales),
    # Ventas
    path("actualizarPermisosVentas/", viewPermisos.actualizarPermisosVentas),
    # Descuentos
    path("actualizarPermisosDescuentos/", viewPermisos.actualizarPermisosDescuentos),
    # Caja
    path("actualizarPermisosCaja/", viewPermisos.actualizarPermisosCaja),
    # Movimientos totales de caja
    path("actualizarPermisosMovimientosTotalesCaja/",viewPermisos.actualizarPermisosMovimientosTotalesCaja),
    # Movimientos semanales caja
    path("actualizarPermisosMovimientosSemanalCaja/",viewPermisos.actualizarPermisosMovimientosSemanalCaja),
    # Rentas
    path("actualizarPermisosRentas/", viewPermisos.actualizarPermisosRentas),
    # Calendario rentas
    path("actualizarPermisosCalendarioRentas/", viewPermisos.actualizarPermisosCalendarioRentas),
    # Productos
    path("actualizarPermisosProductos/", viewPermisos.actualizarPermisosProductos),
    # Servicios
    path("actualizarPermisosServicios/", viewPermisos.actualizarPermisosServicios),
    # Paquetes servicios
    path("actualizarPermisosPaquetesServicios/",viewPermisos.actualizarPermisosPaquetesServicios),
    # Creditos
    path("actualizarPermisosCreditos/", viewPermisos.actualizarPermisosCreditos),
    # Configuracion creditos
    path("actualizarPermisosConfiguracionCreditos/",viewPermisos.actualizarPermisosConfiguracionCreditos),
    # Pagos creditos
    path("actualizarPermisosPagosCreditos/", viewPermisos.actualizarPermisosPagosCreditos),
    # Compras
    path("actualizarPermisosCompras/", viewPermisos.actualizarPermisosCompras),
    # Citas
    path("actualizarPermisosCitas/", viewPermisos.actualizarPermisosCitas),
    # Calendario citas
    path("actualizarPermisosCalendarioCitas/", viewPermisos.actualizarPermisosCalendarioCitas),
    # Codigos de barra
    path("actualizarPermisosCodigoBarras/", viewPermisos.actualizarPermisosCodigoBarras),
    # Tratamientos
    path("actualizarPermisosTratamientos/", viewPermisos.actualizarPermisosTratamientos),
    # Certificados de regalo
    path("actualizarPermisosCertificados/", viewPermisos.actualizarPermisosCertificados),
    
# VIEWS INFORMES ------------------------------------------------------------------------------------------------------------------------------
    # Informe de ventas
    path("informeDeVentas/", viewInformes.informeDeVentas),
    path("informeDeVentasAnual/", viewInformes.informeDeVentasAnual),
    path("informeDeVentasRangoFechas/", viewInformes.informeDeVentasRangoFechas),
    path("informeDeVentasRangoFechasEmpleado/", viewInformes.informeDeVentasRangoFechasEmpleado),
    path("informeDeSucursal/", viewInformes.informeDeSucursal),
    
# VIEWS TRATAMIENTOS ---------------------------------------------------------------------------------------------------------------------------
    # Agregar tratamiento
    path("agregarTratamiento/", viewTratamientos.agregarTratamiento),
    path("verTratamientos/", viewTratamientos.verTratamientos),
    path("actualizarTratamientosCorporales/", viewTratamientos.actualizarTratamientosCorporales),
    path("crearPaqueteTratamientos/", viewTratamientos.crearPaqueteTratamientos),
    path("guardarPaqueteTratamiento/", viewTratamientos.guardarPaqueteTratamiento),
    path("verProductosPaqueteTratamientoEditar/",viewTratamientos.verProductosPaqueteTratamientoEditar),
    path("actualizarPaqueteTratamiento/", viewTratamientos.actualizarPaqueteTratamiento),

# VIEWS PAQUETES PROMOCION TRATAMIENTO
    # Promociones tratamiento
    path("agregarPaquetePromocionTratamiento/", viewPromocionesTratamientos.agregarPaquetePromocionTratamiento),
    path("guardarPromocionTratamiento/", viewPromocionesTratamientos.guardarPromocionTratamiento),
    path("verPaquetesPromocionTratamientos/", viewPromocionesTratamientos.verPaquetesPromocionTratamientos),
    path("bajaPromocionTratamiento/", viewPromocionesTratamientos.bajaPromocionTratamiento),
    path("altaPromocionTratamiento/", viewPromocionesTratamientos.altaPromocionTratamiento),
    
    
# VIEWS CITAS ----------------------------------------------------------------------------------------------------------------------------------------
    # Citas
    path("agendarCita/", viewCitas.agendarCita),
    path("guardarCita/", viewCitas.guardarCita),
    path("citas/", viewCitas.citas),
    path("calendarioCitas/", viewCitas.calendarioCitas),
    path("vistaVenderCita/", viewCitas.vistaVenderCita),
    path("guardarVentaCita/", viewCitas.guardarVentaCita),
    path("paquetesPorCliente/", viewCitas.paquetesPorCliente),
    path("historialTratamientoCliente/", viewCitas.historialTratamientoCliente),
    path("guardarCitaSesion/", viewCitas.guardarCitaSesion),
    path("notificacionCitasDeHoy/", viewCitas.notificacionCitasDeHoy),
    path("reAgendarCita/", viewCitas.reAgendarCita),
    path("reAgendarCancelarCita/", viewCitas.reAgendarCancelarCita),
    
    
# VIEWS CERTIFICADOS ----------------------------------------------------------------------------------------------------------------------------------------
    # Certificados
    path("agregarCertificado/", viewCertificados.agregarCertificado),
    path("agregarServicioCertificado/", viewCertificados.agregarServicioCertificado),
    path("verServiciosCertificado/", viewCertificados.verServiciosCertificado),
    path("actualizarServicioCertificado/", viewCertificados.actualizarServicioCertificado),
    path("crearPaqueteServicioCertificado/", viewCertificados.crearPaqueteServicioCertificado),
    path("guardarPaqueteServicioCertificado/", viewCertificados.guardarPaqueteServicioCertificado),
    path("verProductoDePaqueteServicioCertificadoEditar/",viewCertificados.verProductoDePaqueteServicioCertificadoEditar),
    path("actualizarPaqueteCertificados/", viewCertificados.actualizarPaqueteCertificados),
    path("guardarVenderCertificado/", viewCertificados.guardarVenderCertificado),
    path("verCertificadosProgramados/", viewCertificados.verCertificadosProgramados),
    path("verServiciosParaCanjear/", viewCertificados.verServiciosParaCanjear),
    path("canjearCertificado/", viewCertificados.canjearCertificado),
    
    
# VIEWS MOVIMIENTOS DE VESTIDOS ----------------------------------------------------------------------------------------------------------------------
    # Movimiento de vestidos
    path("agregarMovimiento/", viewMovimientosVestidos.agregarMovimiento),
    path("guardarMovimiento/", viewMovimientosVestidos.guardarMovimiento),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
