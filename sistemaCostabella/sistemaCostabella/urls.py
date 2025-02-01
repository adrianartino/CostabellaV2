# Importar vistas de aplicacion
from appCostabella import views
from appCostabella.vEmpleados import viewEmpleados

# Importar vistas ya acomodadas
from appCostabella.vInicio import viewInicio
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
    # Sucursales Menu
    path("altaSucursal/", views.altaSucursal),
    path("verSucursales/", views.verSucursales),
    # clientes Menu
    path("verClientes/", views.verClientes),
    path("altaCliente/", views.altaCliente),
    path("activoCliente/", views.activoCliente),
    path("bloqueoCliente/", views.bloqueoCliente),
    path("infoCliente/", views.infoCliente),
    path("actTelCliente/", views.actTelCliente),
    # excel
    path("xlInventarioProductosVenta/", views.xlInventarioProductosVenta),
    path("xlInventarioCiclicoProductosVenta/", views.xlInventarioCiclicoProductosVenta),
    path("ajusteProductosVenta/", views.ajusteProductosVenta),
    path("ajusteProductosGasto/", views.ajusteProductosGasto),
    path("informeStockBajoProductosVenta/", views.informeStockBajoProductosVenta),
    # Productos
    path("altaProductos/", views.altaProductos),
    path("inventarioProductos/", views.inventarioProductos),
    path("actualizarProductoV/", views.actualizarProductoV),
    path("actualizarProductoVentaCompra/", views.actualizarProductoVentaCompra),
    path("actualizarProductoGasto/", views.actualizarProductoGasto),
    path("actualizarProductoGastoCompra/", views.actualizarProductoGastoCompra),
    path("actualizarProductoRenta/", views.actualizarProductoRenta),
    path("imprimirCodigoBarras/", views.imprimirCodigoBarras),
    # compras
    path("inventarioCompras/", views.inventarioCompras),
    # caja
    path("configuracionCaja/", views.configuracionCaja),
    path("agregarConfiguracionCaja/", views.agregarConfiguracionCaja),
    path("movimientosCaja/", views.movimientosCaja),
    path("agregarMovimientoCaja/", views.agregarMovimientoCaja),
    path("activarConfiguracionCaja/", views.activarConfiguracionCaja),
    path("seleccionarSucursalMovimientosDia/", views.seleccionarSucursalMovimientosDia),
    path("verSucursalMovimientosDia/", views.verSucursalMovimientosDia),
    path("seleccionarSucursalCortesDeCaja/", views.seleccionarSucursalCortesDeCaja),
    path("cortesDeCaja/", views.cortesDeCaja),
    # RENTAS
    path("rentas/", views.rentas),
    path("altaRenta/", views.altaRenta),
    path("entregarRentaApartada/", views.entregarRentaApartada),
    path("verCalendarioRentas/", views.verCalendarioRentas),
    path("seleccionarSucursalRentas/", views.seleccionarSucursalRentas),
    path("guardarRentas/", views.guardarRentas),
    path("recibirRentaDevolucionCliente/", views.recibirRentaDevolucionCliente),
    path("recibirPagoCuota/", views.recibirPagoCuota),
    path("notificacionRentasDeHoy/", views.notificacionRentasDeHoy),
    # Servicios
    path("altaServicios/", views.altaServicios),
    path("inventarioServicios/", views.inventarioServicios),
    path("actualizarServiciosCoporales/", views.actualizarServiciosCoporales),
    path("actualizarServiciosFaciales/", views.actualizarServiciosFaciales),
    path("crearPaqueteServicios/", views.crearPaqueteServicios),
    path(
        "crearPaqueteServicioConProductosVenta/",
        views.crearPaqueteServicioConProductosVenta,
    ),
    path("guardarPaquete/", views.guardarPaquete),
    path(
        "guardarPaqueteEditadoProductosVenta/",
        views.guardarPaqueteEditadoProductosVenta,
    ),
    path("actualizarPaquete/", views.actualizarPaquete),
    path("actualizarPaqueteFacial/", views.actualizarPaqueteFacial),
    path(
        "verProductoDePaqueteCorporalEditar/", views.verProductoDePaqueteCorporalEditar
    ),
    path("verProductoDePaqueteFacialEditar/", views.verProductoDePaqueteFacialEditar),
    path("inventarioPaqueteServicios/", views.inventarioPaqueteServicios),
    # DESCUENTOS
    path("descuentos/", views.descuentos),
    path("altaDescuentos/", views.altaDescuentos),
    path("actualizarDescuentos/", views.actualizarDescuentos),
    # VENTAS
    path("ventas/", views.ventas),
    path("realizarVenta/", views.realizarVenta),
    path("seleccionarSucursalVentas/", views.seleccionarSucursalVentas),
    path("guardarVenta/", views.guardarVenta),
    path("infoVenta/", views.infoVenta),
    # creditos
    path("configuracionCredito/", views.configuracionCredito),
    path("agregarConfiguracionCredito/", views.agregarConfiguracionCredito),
    path("verCreditosClientes/", views.verCreditosClientes),
    path("activarConfiguracionCredito/", views.activarConfiguracionCredito),
    path("pagosCreditosClientes/", views.pagosCreditosClientes),
    path("guardarPago1/", views.guardarPago1),
    path("guardarPago2/", views.guardarPago2),
    path("guardarPago3/", views.guardarPago3),
    path("guardarPago4/", views.guardarPago4),
    # Panel administrativo
    path("verPanelAdministrativo/", views.verPanelAdministrativo),
    path(
        "actualizarPermisosPanelAdministraativo/",
        views.actualizarPermisosPanelAdministraativo,
    ),
    # Empleados
    path("actualizarPermisosEmpleados/", views.actualizarPermisosEmpleados),
    # Clientes
    path("actualizarPermisosClientes/", views.actualizarPermisosClientes),
    # Sucursales
    path("actualizarPermisosSucursales/", views.actualizarPermisosSucursales),
    # Ventas
    path("actualizarPermisosVentas/", views.actualizarPermisosVentas),
    # Descuentos
    path("actualizarPermisosDescuentos/", views.actualizarPermisosDescuentos),
    # Caja
    path("actualizarPermisosCaja/", views.actualizarPermisosCaja),
    # Movimientos totales de caja
    path(
        "actualizarPermisosMovimientosTotalesCaja/",
        views.actualizarPermisosMovimientosTotalesCaja,
    ),
    # Movimientos semanales caja
    path(
        "actualizarPermisosMovimientosSemanalCaja/",
        views.actualizarPermisosMovimientosSemanalCaja,
    ),
    # Rentas
    path("actualizarPermisosRentas/", views.actualizarPermisosRentas),
    # Calendario rentas
    path(
        "actualizarPermisosCalendarioRentas/", views.actualizarPermisosCalendarioRentas
    ),
    # Productos
    path("actualizarPermisosProductos/", views.actualizarPermisosProductos),
    # Servicios
    path("actualizarPermisosServicios/", views.actualizarPermisosServicios),
    # Paquetes servicios
    path(
        "actualizarPermisosPaquetesServicios/",
        views.actualizarPermisosPaquetesServicios,
    ),
    # Creditos
    path("actualizarPermisosCreditos/", views.actualizarPermisosCreditos),
    # Configuracion creditos
    path(
        "actualizarPermisosConfiguracionCreditos/",
        views.actualizarPermisosConfiguracionCreditos,
    ),
    # Pagos creditos
    path("actualizarPermisosPagosCreditos/", views.actualizarPermisosPagosCreditos),
    # Compras
    path("actualizarPermisosCompras/", views.actualizarPermisosCompras),
    # Citas
    path("actualizarPermisosCitas/", views.actualizarPermisosCitas),
    # Calendario citas
    path("actualizarPermisosCalendarioCitas/", views.actualizarPermisosCalendarioCitas),
    # Codigos de barra
    path("actualizarPermisosCodigoBarras/", views.actualizarPermisosCodigoBarras),
    # Tratamientos
    path("actualizarPermisosTratamientos/", views.actualizarPermisosTratamientos),
    # Certificados de regalo
    path("actualizarPermisosCertificados/", views.actualizarPermisosCertificados),
    # Informe de ventas
    path("informeDeVentas/", views.informeDeVentas),
    path("informeDeVentasAnual/", views.informeDeVentasAnual),
    path("informeDeVentasRangoFechas/", views.informeDeVentasRangoFechas),
    path(
        "informeDeVentasRangoFechasEmpleado/", views.informeDeVentasRangoFechasEmpleado
    ),
    # informe de sucursales
    path("informeDeSucursal/", views.informeDeSucursal),
    # Certificado de regalo.
    path("agregarCertificado/", views.agregarCertificado),
    # Agregar tratamiento
    path("agregarTratamiento/", views.agregarTratamiento),
    path("verTratamientos/", views.verTratamientos),
    path("actualizarTratamientosCorporales/", views.actualizarTratamientosCorporales),
    path("crearPaqueteTratamientos/", views.crearPaqueteTratamientos),
    path("guardarPaqueteTratamiento/", views.guardarPaqueteTratamiento),
    path(
        "verProductosPaqueteTratamientoEditar/",
        views.verProductosPaqueteTratamientoEditar,
    ),
    path("actualizarPaqueteTratamiento/", views.actualizarPaqueteTratamiento),
    # Promociones tratamiento
    path(
        "agregarPaquetePromocionTratamiento/", views.agregarPaquetePromocionTratamiento
    ),
    path("guardarPromocionTratamiento/", views.guardarPromocionTratamiento),
    path("verPaquetesPromocionTratamientos/", views.verPaquetesPromocionTratamientos),
    path("bajaPromocionTratamiento/", views.bajaPromocionTratamiento),
    path("altaPromocionTratamiento/", views.altaPromocionTratamiento),
    # Citas
    path("agendarCita/", views.agendarCita),
    path("guardarCita/", views.guardarCita),
    path("citas/", views.citas),
    path("calendarioCitas/", views.calendarioCitas),
    path("vistaVenderCita/", views.vistaVenderCita),
    path("guardarVentaCita/", views.guardarVentaCita),
    path("paquetesPorCliente/", views.paquetesPorCliente),
    path("historialTratamientoCliente/", views.historialTratamientoCliente),
    path("guardarCitaSesion/", views.guardarCitaSesion),
    path("notificacionCitasDeHoy/", views.notificacionCitasDeHoy),
    path("reAgendarCita/", views.reAgendarCita),
    path("reAgendarCancelarCita/", views.reAgendarCancelarCita),
    # Corte de caja
    path("realizarCorteDeCaja/", views.realizarCorteDeCaja),
    # Certificados
    path("agregarServicioCertificado/", views.agregarServicioCertificado),
    path("verServiciosCertificado/", views.verServiciosCertificado),
    path("actualizarServicioCertificado/", views.actualizarServicioCertificado),
    path("crearPaqueteServicioCertificado/", views.crearPaqueteServicioCertificado),
    path("guardarPaqueteServicioCertificado/", views.guardarPaqueteServicioCertificado),
    path(
        "verProductoDePaqueteServicioCertificadoEditar/",
        views.verProductoDePaqueteServicioCertificadoEditar,
    ),
    path("actualizarPaqueteCertificados/", views.actualizarPaqueteCertificados),
    path("guardarVenderCertificado/", views.guardarVenderCertificado),
    path("verCertificadosProgramados/", views.verCertificadosProgramados),
    path("verServiciosParaCanjear/", views.verServiciosParaCanjear),
    path("canjearCertificado/", views.canjearCertificado),
    # Movimiento de vestidos
    path("agregarMovimiento/", views.agregarMovimiento),
    path("guardarMovimiento/", views.guardarMovimiento),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
