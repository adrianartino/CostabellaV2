# Renderizado
import os

# Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

# Librerías de fecha
from datetime import date, datetime, time, timedelta
from random import choice

# Importacion de modelos
from appCostabella.models import (
    Clientes,
    Creditos,
    Descuentos,
    Empleados,
    Permisos,
    ProductosRenta,
    ProductosVenta,
    Servicios,
    Sucursales,
    Ventas,
)

# Notificaciones
from appCostabella.notificaciones.notificaciones import (
    notificacionCitas,
    notificacionRentas,
)
from dateutil.relativedelta import relativedelta

def altaEmpleado(request):

    if "idSesion" in request.session:

        # Variables de sesión
        idEmpleado = request.session["idSesion"]
        nombresEmpleado = request.session["nombresSesion"]
        idPerfil = idEmpleado
        idConfig = idEmpleado

        tipoUsuario = request.session["tipoUsuario"]
        puestoEmpleado = request.session["puestoSesion"]

        # Variable para Menu
        estaEnAltaEmpleado = True

        # INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]

        # notificacionRentas
        notificacionRenta = notificacionRentas(request)

        # notificacionCitas
        notificacionCita = notificacionCitas(request)

        # permisosEmpleado
        consultaPermisos = Permisos.objects.filter(
            id_empleado_id__id_empleado=idEmpleado
        )

        # retornar sucrusales
        sucursales = Sucursales.objects.all()
        if request.method == "POST":
            nombresEmpleadoRecibido = request.POST["nombresEmpleado"]
            apellidoPat = request.POST["apellidoPat"]
            apellidoMat = request.POST["apellidoMat"]
            telefono = request.POST["telefono"]
            nombreUsuario = request.POST["nombreUsuario"]
            pwd = request.POST["pwd"]
            tipoUsuarioRecibido = request.POST["tipoUsuario"]
            puestoUsuario = request.POST["puestoUsuario"]
            sucursal = request.POST["sucursal"]

            fechaAlta = datetime.today().strftime("%Y-%m-%d")

            # Si usuario administrador..
            if sucursal == "Todas":
                altaEmpleado = Empleados(
                    nombre_usuario=nombreUsuario,
                    contrasena=pwd,
                    nombres=nombresEmpleadoRecibido,
                    apellido_paterno=apellidoPat,
                    apellido_materno=apellidoMat,
                    telefono=telefono,
                    puesto=puestoUsuario,
                    fecha_alta=fechaAlta,
                    estado_contratacion="A",
                )  # Sin sucursal porque Admin
                altaEmpleado.save()
            else:
                altaEmpleado = Empleados(
                    nombre_usuario=nombreUsuario,
                    contrasena=pwd,
                    nombres=nombresEmpleadoRecibido,
                    apellido_paterno=apellidoPat,
                    apellido_materno=apellidoMat,
                    telefono=telefono,
                    puesto=puestoUsuario,
                    fecha_alta=fechaAlta,
                    estado_contratacion="A",
                    id_sucursal=Sucursales.objects.get(id_sucursal=sucursal),
                )  # Sin sucursal porque Admin
                altaEmpleado.save()

            if altaEmpleado:
                empleadoAgregado = (
                    "El empleado "
                    + nombresEmpleadoRecibido
                    + " ha sido agregado satisfactoriamente!"
                )
                # Creacion de permisos
                tablas_modulos = [
                    "Panel administrativo",
                    "Empleados",
                    "Clientes",
                    "Sucursales",
                    "Ventas",
                    "Descuentos",
                    "Configuracion caja",
                    "Movimientos",
                    "Movimiento semanal",
                    "Rentas",
                    "Calendario rentas",
                    "Productos",
                    "Servicios",
                    "Paquetes",
                    "Creditos",
                    "Configuracion credito",
                    "Pagos creditos",
                    "Compras",
                    "Citas",
                    "Calendario citas",
                    "Codigos de barras",
                    "Tratamientos",
                    "Certificado",
                ]

                ultimoEmpleado = 0
                empleadosTotales = Empleados.objects.all()
                for empleado in empleadosTotales:

                    ultimoEmpleado = ultimoEmpleado + 1
                permiso = ""
                if tipoUsuarioRecibido == "Administrador":
                    permiso = "Si"
                else:
                    permiso = "No"
                for tablas in tablas_modulos:
                    tabla = tablas
                    if tabla == "Panel administrativo":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Empleados":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Clientes":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Sucursales":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Ventas":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Descuentos":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Configuracion caja":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Movimientos":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Movimiento semanal":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Rentas":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Calendario rentas":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Productos":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Servicios":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Paquetes":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Creditos":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Configuracion credito":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Pagos creditos":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Compras":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Citas":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Calendario citas":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                    elif tabla == "Codigos de barras":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()
                    elif tabla == "Tratamientos":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()
                    elif tabla == "Certificado":

                        altaPermisosEmpleado = Permisos(
                            id_empleado=Empleados.objects.get(
                                id_empleado=ultimoEmpleado
                            ),
                            ver=permiso,
                            agregar=permiso,
                            editar=permiso,
                            bloquear=permiso,
                            ver_detalles=permiso,
                            activar=permiso,
                            comprar=permiso,
                            recibir_pagos=permiso,
                            tabla_modulo=tabla,
                        )  # Sin sucursal porque Admin
                        altaPermisosEmpleado.save()

                return render(
                    request,
                    "3 Empleados/altaEmpleado.html",
                    {
                        "consultaPermisos": consultaPermisos,
                        "idEmpleado": idEmpleado,
                        "idPerfil": idPerfil,
                        "idConfig": idConfig,
                        "nombresEmpleado": nombresEmpleado,
                        "tipoUsuario": tipoUsuario,
                        "letra": letra,
                        "puestoEmpleado": puestoEmpleado,
                        "estaEnAltaEmpleado": estaEnAltaEmpleado,
                        "sucursales": sucursales,
                        "empleadoAgregado": empleadoAgregado,
                        "notificacionRenta": notificacionRenta,
                        "notificacionCita": notificacionCita,
                    },
                )
            else:
                empleadoNoAgregado = "Error en la base de datos, intentelo más tarde.."
                return render(
                    request,
                    "3 Empleados/altaEmpleado.html",
                    {
                        "consultaPermisos": consultaPermisos,
                        "idEmpleado": idEmpleado,
                        "idPerfil": idPerfil,
                        "idConfig": idConfig,
                        "nombresEmpleado": nombresEmpleado,
                        "tipoUsuario": tipoUsuario,
                        "letra": letra,
                        "puestoEmpleado": puestoEmpleado,
                        "estaEnAltaEmpleado": estaEnAltaEmpleado,
                        "sucursales": sucursales,
                        "empleadoNoAgregado": empleadoNoAgregado,
                        "notificacionRenta": notificacionRenta,
                        "notificacionCita": notificacionCita,
                    },
                )

        return render(
            request,
            "3 Empleados/altaEmpleado.html",
            {
                "consultaPermisos": consultaPermisos,
                "idEmpleado": idEmpleado,
                "idPerfil": idPerfil,
                "idConfig": idConfig,
                "nombresEmpleado": nombresEmpleado,
                "tipoUsuario": tipoUsuario,
                "letra": letra,
                "puestoEmpleado": puestoEmpleado,
                "estaEnAltaEmpleado": estaEnAltaEmpleado,
                "sucursales": sucursales,
                "notificacionRenta": notificacionRenta,
                "notificacionCita": notificacionCita,
            },
        )
    else:
        return render(request, "1 Login/login.html")


def verEmpleados(request):

    if "idSesion" in request.session:

        # Variables de sesión
        idEmpleado = request.session["idSesion"]
        nombresEmpleado = request.session["nombresSesion"]
        tipoUsuario = request.session["tipoUsuario"]
        puestoEmpleado = request.session["puestoSesion"]
        idPerfil = idEmpleado
        idConfig = idEmpleado

        # INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]

        # notificacionRentas
        notificacionRenta = notificacionRentas(request)

        # notificacionCitas
        notificacionCita = notificacionCitas(request)

        # permisosEmpleado
        consultaPermisos = Permisos.objects.filter(
            id_empleado_id__id_empleado=idEmpleado
        )

        usuariosSpan = []
        sucursalesEmpleados = []
        tipoEmpleados = []
        colores = [
            "bg-blue",
            "bg-azure",
            "bg-indigo",
            "bg.purple",
            "bg-pink",
            "bg-orange",
            "bg-teal",
            "bg-red",
            "bg-gray",
        ]
        coloresRandom = []
        empleados = Empleados.objects.all()

        contadorActivos = 0
        contadorInactivos = 0
        empleadosActivos = Empleados.objects.filter(estado_contratacion="A")
        empleadosInactivos = Empleados.objects.filter(estado_contratacion="I")

        for activo in empleadosActivos:
            contadorActivos = contadorActivos + 1
        for inactivo in empleadosInactivos:
            contadorInactivos = contadorInactivos + 1

        for empleado in empleados:
            nombre = empleado.nombres
            apellidoPat = empleado.apellido_paterno
            apellidoMat = empleado.apellido_materno

            if empleado.id_sucursal_id == None:
                esAdministrador = True
                sucursal = "Todas"
            else:
                esAdministrador = False

                sucursal = empleado.id_sucursal_id

            letraNombre = nombre[0]
            letraPaterno = apellidoPat[0]
            letraMaterno = apellidoMat[0]

            usuariosSpan.append([letraNombre, letraPaterno, letraMaterno])

            if esAdministrador == False:

                sucursales = Sucursales.objects.filter(id_sucursal=sucursal)
                for suc in sucursales:
                    nombreSucursal = suc.nombre

                tipo = "Empleado"

            elif esAdministrador == True:
                nombreSucursal = "Todas"
                tipo = "Administrador"

            colorRandom = choice(colores)
            coloresRandom.append(colorRandom)
            sucursalesEmpleados.append(nombreSucursal)
            tipoEmpleados.append(tipo)

        usuariosSpanA = []
        sucursalesEmpleadosA = []
        tipoEmpleadosA = []
        coloresA = [
            "bg-blue",
            "bg-azure",
            "bg-indigo",
            "bg.purple",
            "bg-pink",
            "bg-orange",
            "bg-teal",
            "bg-red",
            "bg-gray",
        ]
        coloresRandomA = []
        for empleadoActivo in empleadosActivos:
            nombreA = empleadoActivo.nombres
            apellidoPatA = empleadoActivo.apellido_paterno
            apellidoMatA = empleadoActivo.apellido_materno

            if empleadoActivo.id_sucursal_id == None:
                esAdministradorA = True
                sucursalA = "Todas"
            else:
                esAdministradorA = False

                sucursalA = empleadoActivo.id_sucursal_id

            letraNombreA = nombreA[0]
            letraPaternoA = apellidoPatA[0]
            letraMaternoA = apellidoMatA[0]

            usuariosSpanA.append([letraNombreA, letraPaternoA, letraMaternoA])

            if esAdministradorA == False:

                sucursalesA = Sucursales.objects.filter(id_sucursal=sucursalA)
                for sucA in sucursalesA:
                    nombreSucursalA = sucA.nombre

                tipoA = "Empleado"

            elif esAdministradorA == True:
                nombreSucursalA = "Todas"
                tipoA = "Administrador"

            colorRandomA = choice(coloresA)
            coloresRandomA.append(colorRandomA)
            sucursalesEmpleadosA.append(nombreSucursalA)
            tipoEmpleadosA.append(tipoA)

        usuariosSpanI = []
        sucursalesEmpleadosI = []
        tipoEmpleadosI = []
        coloresI = [
            "bg-blue",
            "bg-azure",
            "bg-indigo",
            "bg.purple",
            "bg-pink",
            "bg-orange",
            "bg-teal",
            "bg-red",
            "bg-gray",
        ]
        coloresRandomI = []
        for empleadoInactivo in empleadosInactivos:
            nombreI = empleadoInactivo.nombres
            apellidoPatI = empleadoInactivo.apellido_paterno
            apellidoMatI = empleadoInactivo.apellido_materno

            if empleadoInactivo.id_sucursal_id == None:
                esAdministradorI = True
                sucursalI = "Todas"
            else:
                esAdministradorI = False

                sucursalI = empleadoInactivo.id_sucursal_id

            letraNombreI = nombreI[0]
            letraPaternoI = apellidoPatI[0]
            letraMaternoI = apellidoMatI[0]

            usuariosSpanI.append([letraNombreI, letraPaternoI, letraMaternoI])

            if esAdministradorI == False:

                sucursalesI = Sucursales.objects.filter(id_sucursal=sucursalI)
                for sucI in sucursalesI:
                    nombreSucursalI = sucI.nombre

                tipoI = "Empleado"

            elif esAdministradorI == True:
                nombreSucursalI = "Todas"
                tipoI = "Administrador"

            colorRandomI = choice(coloresI)
            coloresRandomI.append(colorRandomI)
            sucursalesEmpleadosI.append(nombreSucursalI)
            tipoEmpleadosI.append(tipoI)

        lista = zip(
            empleados, usuariosSpan, sucursalesEmpleados, tipoEmpleados, coloresRandom
        )
        listaActivos = zip(
            empleadosActivos,
            usuariosSpanA,
            sucursalesEmpleadosA,
            tipoEmpleadosA,
            coloresRandomA,
        )
        listaInactivos = zip(
            empleadosInactivos,
            usuariosSpanI,
            sucursalesEmpleadosI,
            tipoEmpleadosI,
            coloresRandomI,
        )
        if "empleadoActualizado" in request.session:
            mensaje = request.session["empleadoActualizado"]
            del request.session["empleadoActualizado"]

            return render(
                request,
                "3 Empleados/verEmpleados.html",
                {
                    "consultaPermisos": consultaPermisos,
                    "idEmpleado": idEmpleado,
                    "idPerfil": idPerfil,
                    "idConfig": idConfig,
                    "nombresEmpleado": nombresEmpleado,
                    "tipoUsuario": tipoUsuario,
                    "letra": letra,
                    "puestoEmpleado": puestoEmpleado,
                    "empleados": empleados,
                    "usuariosSpan": usuariosSpan,
                    "lista": lista,
                    "contadorActivos": contadorActivos,
                    "contadorInactivos": contadorInactivos,
                    "mensaje": mensaje,
                    "listaActivos": listaActivos,
                    "listaInactivos": listaInactivos,
                    "notificacionRenta": notificacionRenta,
                    "notificacionCita": notificacionCita,
                },
            )

        return render(
            request,
            "3 Empleados/verEmpleados.html",
            {
                "consultaPermisos": consultaPermisos,
                "idEmpleado": idEmpleado,
                "idPerfil": idPerfil,
                "idConfig": idConfig,
                "nombresEmpleado": nombresEmpleado,
                "tipoUsuario": tipoUsuario,
                "letra": letra,
                "puestoEmpleado": puestoEmpleado,
                "empleados": empleados,
                "usuariosSpan": usuariosSpan,
                "lista": lista,
                "contadorActivos": contadorActivos,
                "contadorInactivos": contadorInactivos,
                "listaActivos": listaActivos,
                "listaInactivos": listaInactivos,
                "notificacionRenta": notificacionRenta,
                "notificacionCita": notificacionCita,
            },
        )
    else:
        return render(request, "1 Login/login.html")


def editarEmpleado(request):

    if "idSesion" in request.session:

        # Variables de sesión
        idEmpleado = request.session["idSesion"]
        nombresEmpleado = request.session["nombresSesion"]
        tipoUsuario = request.session["tipoUsuario"]
        puestoEmpleado = request.session["puestoSesion"]
        idPerfil = idEmpleado
        idConfig = idEmpleado

        # INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]

        # notificacionRentas
        notificacionRenta = notificacionRentas(request)

        # notificacionCitas
        notificacionCita = notificacionCitas(request)

        # permisosEmpleado
        consultaPermisos = Permisos.objects.filter(
            id_empleado_id__id_empleado=idEmpleado
        )

        listaSucursales = []
        listaSucursalesFaltantes = []

        if request.method == "POST":
            idEmpleadoEditar = request.POST["idEmpleadoEditar"]

            consultaEmpleado = Empleados.objects.filter(id_empleado=idEmpleadoEditar)

            for dato in consultaEmpleado:
                idEmpleadoEditar2 = dato.id_empleado
                idEmpleadoEditar3 = dato.id_empleado
                idEmpleadoEditar4 = dato.id_empleado
                nombreUsuario = dato.nombre_usuario
                nombres = dato.nombres
                apellidoPaterno = dato.apellido_paterno
                apellidoMaterno = dato.apellido_materno
                telefono = dato.telefono
                puesto = dato.puesto
                estatus = dato.estado_contratacion
                fecha_alta = dato.fecha_alta

                fecha_baja = dato.fecha_baja
                if dato.id_sucursal_id == None:
                    sucursal = "Todas"
                    idsucursal = ""
                    tipo = "Administrador"
                else:

                    idsucursal = dato.id_sucursal_id
                    tipo = "Empleado"
                    sucursales = Sucursales.objects.filter(id_sucursal=idsucursal)
                    for dato in sucursales:
                        sucursal = dato.nombre

                letrasEmpleado = nombres[0] + apellidoPaterno[0] + apellidoMaterno[0]

            sucursalesTotales = Sucursales.objects.all()
            for totales in sucursalesTotales:
                sucursal_TotalID = totales.id_sucursal
                nombre_sucursal = totales.nombre
                listaSucursales.append([sucursal_TotalID, nombre_sucursal])
                listaSucursalesFaltantes.append([sucursal_TotalID, nombre_sucursal])

            if idsucursal != "":
                listaSucursalesFaltantes.pop(idsucursal - 1)

            if estatus == "A":
                activo = True
                activo2 = True
            elif estatus == "I":
                activo = False
                activo2 = False

            totalVentas = 0
            contadorVentas = 0
            consultaVentas = Ventas.objects.filter(
                empleado_vendedor_id__id_empleado=idEmpleadoEditar
            )
            for venta in consultaVentas:
                montoVendido = venta.monto_pagar
                contadorVentas = contadorVentas + 1
                totalVentas = totalVentas + montoVendido

            return render(
                request,
                "3 Empleados/editarEmpleado.html",
                {
                    "consultaPermisos": consultaPermisos,
                    "idEmpleado": idEmpleado,
                    "idPerfil": idPerfil,
                    "idConfig": idConfig,
                    "nombresEmpleado": nombresEmpleado,
                    "tipoUsuario": tipoUsuario,
                    "letra": letra,
                    "puestoEmpleado": puestoEmpleado,
                    "nombres": nombres,
                    "apellidoPaterno": apellidoPaterno,
                    "apellidoMaterno": apellidoMaterno,
                    "telefono": telefono,
                    "puesto": puesto,
                    "nombreUsuario": nombreUsuario,
                    "letrasEmpleado": letrasEmpleado,
                    "tipo": tipo,
                    "sucursal": sucursal,
                    "idsucursal": idsucursal,
                    "listaSucursales": listaSucursales,
                    "listaSucursalesFaltantes": listaSucursalesFaltantes,
                    "idEmpleadoEditar2": idEmpleadoEditar2,
                    "activo": activo,
                    "fecha_alta": fecha_alta,
                    "fecha_baja": fecha_baja,
                    "idEmpleadoEditar3": idEmpleadoEditar3,
                    "idEmpleadoEditar4": idEmpleadoEditar4,
                    "activo2": activo2,
                    "contadorVentas": contadorVentas,
                    "totalVentas": totalVentas,
                    "notificacionRenta": notificacionRenta,
                    "notificacionCita": notificacionCita,
                },
            )

        return redirect("/verEmpleados/")
    else:
        return render(request, "1 Login/login.html")


def actInfoPersonal(request):

    if "idSesion" in request.session:

        idEmpleado = request.session["idSesion"]

        if request.method == "POST":
            idActualizado = request.POST["idActualizado"]
            nombreActualizado = request.POST["nombreActualizado"]
            apellidoPatActualizado = request.POST["apellidoPatActualizado"]
            apellidoMatActualizado = request.POST["apellidoMatActualizado"]
            telefonoActualizado = request.POST["telefonoActualizado"]

            if str(idEmpleado) == str(idActualizado):
                del request.session["nombresSesion"]
                request.session["nombresSesion"] = nombreActualizado

            actualizarInfoPersonal = Empleados.objects.filter(
                id_empleado=idActualizado
            ).update(
                nombres=nombreActualizado,
                apellido_paterno=apellidoPatActualizado,
                apellido_materno=apellidoMatActualizado,
                telefono=telefonoActualizado,
            )

            if actualizarInfoPersonal:
                # falta notificacion
                request.session["empleadoActualizado"] = (
                    "La empleada "
                    + nombreActualizado
                    + " ha sido actualizado satisfactoriamente."
                )
                return redirect("/verEmpleados/")

        return redirect("/verEmpleados/")
    else:
        return render(request, "1 Login/login.html")


def actInfoLaboral(request):

    if "idSesion" in request.session:

        idEmpleado = request.session["idSesion"]

        if request.method == "POST":
            idActualizado = request.POST["idActualizado"]
            tipoUsuarioActualizado = request.POST["tipoUsuario"]
            puestoActualizado = request.POST["puestoUsuario"]
            idSucursalActualizado = request.POST["idSucursal"]  # Id o puede ser "Todas"

            if str(idEmpleado) == str(idActualizado):
                request.session["tipoUsuario"] = tipoUsuarioActualizado
                request.session["puestoEmpleado"] = puestoActualizado

            consultaEmpleado = Empleados.objects.filter(id_empleado=idActualizado)

            for dato in consultaEmpleado:
                nombre = dato.nombres

            if idSucursalActualizado == "Todas":
                actualizarInfoLaboral = Empleados.objects.filter(
                    id_empleado=idActualizado
                ).update(puesto=puestoActualizado, id_sucursal=None)

                # Darle todos los permisos..

            else:
                actualizarInfoLaboral = Empleados.objects.filter(
                    id_empleado=idActualizado
                ).update(
                    puesto=puestoActualizado,
                    id_sucursal=Sucursales.objects.get(
                        id_sucursal=idSucursalActualizado
                    ),
                )
                # falta notificacion

                # Quitarle todos los permisos..

            if actualizarInfoLaboral:
                request.session["empleadoActualizado"] = (
                    "El empleado " + nombre + " ha sido actualizado satisfactoriamente."
                )
                return redirect("/verEmpleados/")

        return redirect("/verEmpleados/")
    else:
        return render(request, "1 Login/login.html")


def darAltaEmpleado(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idEmpleadoAlta = request.POST["idEmpleadoAlta"]

            consultaEmpleado = Empleados.objects.filter(id_empleado=idEmpleadoAlta)

            for dato in consultaEmpleado:
                nombre = dato.nombres

            fechaAlta = datetime.today().strftime("%Y-%m-%d")

            actualizacionEmpleado = Empleados.objects.filter(
                id_empleado=idEmpleadoAlta
            ).update(estado_contratacion="A", fecha_baja=None, fecha_alta=fechaAlta)

            if actualizacionEmpleado:
                request.session["empleadoActualizado"] = (
                    "El empleado " + nombre + " ha sido dado de alta en el sistema."
                )
                return redirect("/verEmpleados/")

        return redirect("/verEmpleados/")
    else:
        return render(request, "1 Login/login.html")


def darBajaEmpleado(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idEmpleadoBaja = request.POST["idEmpleadoBaja"]

            consultaEmpleado = Empleados.objects.filter(id_empleado=idEmpleadoBaja)

            for dato in consultaEmpleado:
                nombre = dato.nombres

            fechaBaja = datetime.today().strftime("%Y-%m-%d")

            actualizacionEmpleado = Empleados.objects.filter(
                id_empleado=idEmpleadoBaja
            ).update(estado_contratacion="I", fecha_baja=fechaBaja)

            if actualizacionEmpleado:
                request.session["empleadoActualizado"] = (
                    "El empleado " + nombre + " ha sido dado de baja del sistema."
                )
                return redirect("/verEmpleados/")

        return redirect("/verEmpleados/")
    else:
        return render(request, "1 Login/login.html")


def editarConfiguracionEmpleado(request):

    if "idSesion" in request.session:

        # Variables de sesión
        idEmpleado = request.session["idSesion"]
        nombresEmpleado = request.session["nombresSesion"]
        tipoUsuario = request.session["tipoUsuario"]
        puestoEmpleado = request.session["puestoSesion"]
        idPerfil = idEmpleado
        idConfig = idEmpleado

        # INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]

        # notificacionRentas
        notificacionRenta = notificacionRentas(request)

        # notificacionCitas
        notificacionCita = notificacionCitas(request)

        # permisosEmpleado
        consultaPermisos = Permisos.objects.filter(
            id_empleado_id__id_empleado=idEmpleado
        )

        listaSucursales = []
        listaSucursalesFaltantes = []

        if request.method == "POST":
            idEmpleadoConfigurar = request.POST["idEmpleadoConfigurar"]

            consultaEmpleado = Empleados.objects.filter(
                id_empleado=idEmpleadoConfigurar
            )

            for dato in consultaEmpleado:
                idEmpleadoEditar2 = dato.id_empleado
                idEmpleadoEditar3 = dato.id_empleado
                idEmpleadoEditar4 = dato.id_empleado
                nombreUsuario = dato.nombre_usuario
                nombres = dato.nombres
                apellidoPaterno = dato.apellido_paterno
                apellidoMaterno = dato.apellido_materno
                telefono = dato.telefono
                puesto = dato.puesto
                estatus = dato.estado_contratacion
                fecha_alta = dato.fecha_alta

                fecha_baja = dato.fecha_baja
                if dato.id_sucursal_id == None:
                    sucursal = "Todas"
                    idsucursal = ""
                    tipo = "Administrador"
                else:

                    idsucursal = dato.id_sucursal_id
                    tipo = "Empleado"
                    sucursales = Sucursales.objects.filter(id_sucursal=idsucursal)
                    for dato in sucursales:
                        sucursal = dato.nombre

                letrasEmpleado = nombres[0] + apellidoPaterno[0] + apellidoMaterno[0]

            sucursalesTotales = Sucursales.objects.all()
            for totales in sucursalesTotales:
                sucursal_TotalID = totales.id_sucursal
                nombre_sucursal = totales.nombre
                listaSucursales.append([sucursal_TotalID, nombre_sucursal])
                listaSucursalesFaltantes.append([sucursal_TotalID, nombre_sucursal])

            if idsucursal != "":
                listaSucursalesFaltantes.pop(idsucursal - 1)

            if estatus == "A":
                activo = True
            elif estatus == "I":
                activo = False

            totalVentas = 0
            contadorVentas = 0
            consultaVentas = Ventas.objects.filter(
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar
            )
            for venta in consultaVentas:
                montoVendido = venta.monto_pagar
                contadorVentas = contadorVentas + 1
                totalVentas = totalVentas + montoVendido

            return render(
                request,
                "3 Empleados/configEmpleado.html",
                {
                    "consultaPermisos": consultaPermisos,
                    "idEmpleado": idEmpleado,
                    "idPerfil": idPerfil,
                    "idConfig": idConfig,
                    "nombresEmpleado": nombresEmpleado,
                    "tipoUsuario": tipoUsuario,
                    "letra": letra,
                    "puestoEmpleado": puestoEmpleado,
                    "nombres": nombres,
                    "apellidoPaterno": apellidoPaterno,
                    "apellidoMaterno": apellidoMaterno,
                    "telefono": telefono,
                    "puesto": puesto,
                    "nombreUsuario": nombreUsuario,
                    "letrasEmpleado": letrasEmpleado,
                    "tipo": tipo,
                    "sucursal": sucursal,
                    "idsucursal": idsucursal,
                    "listaSucursales": listaSucursales,
                    "listaSucursalesFaltantes": listaSucursalesFaltantes,
                    "idEmpleadoEditar2": idEmpleadoEditar2,
                    "activo": activo,
                    "fecha_alta": fecha_alta,
                    "fecha_baja": fecha_baja,
                    "idEmpleadoEditar3": idEmpleadoEditar3,
                    "idEmpleadoEditar4": idEmpleadoEditar4,
                    "totalVentas": totalVentas,
                    "contadorVentas": contadorVentas,
                    "notificacionRenta": notificacionRenta,
                    "notificacionCita": notificacionCita,
                },
            )

        return redirect("/verEmpleados/")
    else:
        return render(request, "1 Login/login.html")


def actNombreUsuario(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idActualizado = request.POST["idActualizado"]
            nombreUsuarioActualizado = request.POST["nombreUsuarioActualizado"]

            consulta = Empleados.objects.filter(id_empleado=idActualizado)

            for dato in consulta:
                nombreActualizado = dato.nombres

            actualizarInfoPersonal = Empleados.objects.filter(
                id_empleado=idActualizado
            ).update(nombre_usuario=nombreUsuarioActualizado)

            if actualizarInfoPersonal:
                # falta notificacion
                request.session["empleadoActualizado"] = (
                    "Se ha actualizado el nombre de usuario de "
                    + nombreActualizado
                    + " correctamente!"
                )
                return redirect("/verEmpleados/")

        return redirect("/verEmpleados/")
    else:
        return render(request, "1 Login/login.html")


def actContrasena(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idActualizado = request.POST["idActualizado"]
            contraActualizada = request.POST["contraActualizada"]

            consulta = Empleados.objects.filter(id_empleado=idActualizado)

            for dato in consulta:
                nombreActualizado = dato.nombres

            actualizarInfoPersonal = Empleados.objects.filter(
                id_empleado=idActualizado
            ).update(contrasena=contraActualizada)

            if actualizarInfoPersonal:
                # falta notificacion
                request.session["empleadoActualizado"] = (
                    "Se ha actualizado la contraseña de "
                    + nombreActualizado
                    + " correctamente!"
                )
                return redirect("/verEmpleados/")

        return redirect("/verEmpleados/")
    else:
        return render(request, "1 Login/login.html")


def informeEmpleado(request):

    if "idSesion" in request.session:

        # Variables de sesión
        idEmpleado = request.session["idSesion"]
        nombresEmpleado = request.session["nombresSesion"]
        tipoUsuario = request.session["tipoUsuario"]
        puestoEmpleado = request.session["puestoSesion"]
        idPerfil = idEmpleado
        idConfig = idEmpleado

        # INFORMACION de empleado para menusito
        letra = nombresEmpleado[0]

        # notificacionRentas
        notificacionRenta = notificacionRentas(request)

        # notificacionCitas
        notificacionCita = notificacionCitas(request)

        # permisosEmpleado
        consultaPermisos = Permisos.objects.filter(
            id_empleado_id__id_empleado=idEmpleado
        )

        if request.method == "POST":
            idEmpleadoConfigurar = request.POST["idEmpleadoInforme"]

            consultaEmpleado = Empleados.objects.filter(
                id_empleado=idEmpleadoConfigurar
            )

            for dato in consultaEmpleado:
                idEmpleadoEditar2 = dato.id_empleado
                idEmpleadoEditar3 = dato.id_empleado
                idEmpleadoEditar4 = dato.id_empleado
                nombreUsuario = dato.nombre_usuario
                nombres = dato.nombres
                apellidoPaterno = dato.apellido_paterno
                apellidoMaterno = dato.apellido_materno
                telefono = dato.telefono
                puesto = dato.puesto
                estatus = dato.estado_contratacion
                fecha_alta = dato.fecha_alta

                fecha_baja = dato.fecha_baja
                if dato.id_sucursal_id == None:
                    sucursalEmpleado = "Todas"
                    idsucursal = ""
                    tipo = "Administrador"
                else:

                    idsucursal = dato.id_sucursal_id
                    tipo = "Empleado"
                    sucursales = Sucursales.objects.filter(id_sucursal=idsucursal)
                    for dato in sucursales:
                        sucursalEmpleado = dato.nombre

                letrasEmpleado = nombres[0] + apellidoPaterno[0] + apellidoMaterno[0]

            if estatus == "A":
                activo = True
            elif estatus == "I":
                activo = False

            totalVentas = 0
            contadorVentas = 0
            consultaVentas = Ventas.objects.filter(
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar
            )
            for venta in consultaVentas:
                montoVendido = venta.monto_pagar
                contadorVentas = contadorVentas + 1
                totalVentas = totalVentas + montoVendido

            # INFORME DE VENTAS DEL MES -----------------------------------------------------------------------------------------------------------------------------
            hoy = datetime.now()

            mesdehoynumero = hoy.strftime("%m")  # 06

            mesesDic = {
                "01": "Enero",
                "02": "Febrero",
                "03": "Marzo",
                "04": "Abril",
                "05": "Mayo",
                "06": "Junio",
                "07": "Julio",
                "08": "Agosto",
                "09": "Septiembre",
                "10": "Octubre",
                "11": "Noviembre",
                "12": "Diciembre",
            }

            diasMeses = {
                "Enero": "31",
                "Febrero": "28",
                "Marzo": "31",
                "Abril": "30",
                "Mayo": "31",
                "Junio": "30",
                "Julio": "31",
                "Agosto": "31",
                "Septiembre": "30",
                "Octubre": "31",
                "Noviembre": "30",
                "Diciembre": "31",
            }
            # Mes actual
            diadehoy = hoy.strftime("%d")
            añoHoy = hoy.strftime("%Y")
            mesdehoy = mesesDic[str(mesdehoynumero)]

            fechaDiaMesActual = (
                añoHoy + "-" + mesdehoynumero + "-" + diadehoy
            )  # Día actual  2022-06-07
            fechaInicioMesActual = (
                añoHoy + "-" + mesdehoynumero + "-01"
            )  # Primer día del mes 2022-06-01

            ventasEmpleadoEnElMes = Ventas.objects.filter(
                fecha_venta__range=[fechaInicioMesActual, fechaDiaMesActual],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            # arreglosTabla
            sucursales = []
            clientes = []
            boolProductos = []
            productos = []
            boolServCorporal = []
            servicioCorporal = []
            boolServFacial = []
            servicioFacial = []
            boolCredito = []
            idsCreditos = []
            boolPagado = []
            montos = []
            boolDescuentos = []
            datosDescuento = []
            costoReal = []
            descuentos = []
            tipoVenta = []

            ventasEnElMesActual = 0
            montoVentasEnElMesActual = 0
            for venta in ventasEmpleadoEnElMes:
                ventasEnElMesActual = ventasEnElMesActual + 1
                idVenta = venta.id_venta

                # montos
                montoVendido = venta.monto_pagar
                montoVentasEnElMesActual = montoVentasEnElMesActual + montoVendido

                # Para tabla de ventas
                sucursal = venta.sucursal_id
                consultaSucursal = Sucursales.objects.filter(id_sucursal=sucursal)
                for suc in consultaSucursal:
                    nombreSucursal = suc.nombre
                sucursales.append(nombreSucursal)

                cliente = venta.cliente_id
                if cliente == None:
                    clientes.append(["x", "Cliente momentaneo"])
                else:
                    consultaCliente = Clientes.objects.filter(id_cliente=cliente)
                    for datoCliente in consultaCliente:
                        nombreCliente = datoCliente.nombre_cliente
                        apellido = datoCliente.apellidoPaterno_cliente

                    nombreCompletoCliente = nombreCliente + " " + apellido

                    clientes.append([cliente, nombreCompletoCliente])

                # Productos
                codigosProductos = venta.ids_productos
                if codigosProductos == "":
                    boolProductos.append("Sin productos comprados")
                    productos.append("x")
                else:
                    boolProductos.append("Se compraron productos")
                    cantidadesProductos = venta.cantidades_productos
                    arregloCodigosProductos = codigosProductos.split(",")
                    arregloCantidadesProductos = cantidadesProductos.split(",")

                    listaProductos = zip(
                        arregloCodigosProductos, arregloCantidadesProductos
                    )

                    productitos = []
                    for producto, cantidades in listaProductos:
                        idcodigoProducto = str(producto)
                        cantidad = str(cantidades)

                        if "PV" in idcodigoProducto:
                            # Producto para venta
                            tipoVenta.append("Venta")
                            consultaProducto = ProductosVenta.objects.filter(
                                codigo_producto=idcodigoProducto
                            )
                        else:
                            # Producto para renta
                            tipoVenta.append("Renta")
                            consultaProducto = ProductosRenta.objects.filter(
                                codigo_producto=idcodigoProducto
                            )

                        for datoProducto in consultaProducto:
                            nombreProducto = datoProducto.nombre_producto
                        productitos.append([idcodigoProducto, nombreProducto, cantidad])
                    productos.append(productitos)

                # ServiciosCorporales
                serviciosCorporales = venta.ids_servicios_corporales
                if serviciosCorporales == "":
                    boolServCorporal.append("Sin servicios coorporales")
                    servicioCorporal.append("x")
                else:
                    boolServCorporal.append("Se compraron servicios")
                    cantidadesServiciosCorporales = (
                        venta.cantidades_servicios_corporales
                    )
                    arregloIdsServiciosCorporales = serviciosCorporales.split(",")
                    arregloCantidadesServiciosCorporales = (
                        cantidadesServiciosCorporales.split(",")
                    )

                    listaServiciosCorporales = zip(
                        arregloIdsServiciosCorporales,
                        arregloCantidadesServiciosCorporales,
                    )

                    serviciosCorporales = []
                    for (
                        idServicioCorporal,
                        cantidadServiciosCorporal,
                    ) in listaServiciosCorporales:
                        intId = int(idServicioCorporal)
                        strId = str(idServicioCorporal)
                        cantidad = str(cantidadServiciosCorporal)

                        consultaServicio = Servicios.objects.filter(id_servicio=intId)

                        for datoServicio in consultaServicio:
                            nombreDeServicio = datoServicio.nombre_servicio
                        serviciosCorporales.append([strId, nombreDeServicio, cantidad])
                    servicioCorporal.append(serviciosCorporales)

                # ServiciosFaciales
                serviciosFaciales = venta.ids_servicios_faciales
                if serviciosFaciales == "":
                    boolServFacial.append("Sin servicios faciales")
                    servicioFacial.append("x")
                else:
                    boolServFacial.append("Se compraron servicios")
                    cantiadesServiciosFaciales = venta.cantidades_servicios_faciales
                    arregloIdsServiciosFaciales = serviciosFaciales.split(",")
                    arregloCantidadesServiciosFaciales = (
                        cantiadesServiciosFaciales.split(",")
                    )

                    listaServiciosFaciales = zip(
                        arregloIdsServiciosFaciales, arregloCantidadesServiciosFaciales
                    )

                    serviciosFaciales = []
                    for (
                        idServiciosFacial,
                        cantidadServicioFacial,
                    ) in listaServiciosFaciales:
                        intId = int(idServiciosFacial)
                        strId = str(idServiciosFacial)
                        cantidad = str(cantidadServicioFacial)

                        consultaServicio = Servicios.objects.filter(id_servicio=intId)

                        for datoServicio in consultaServicio:
                            nombreDeServicio = datoServicio.nombre_servicio
                        serviciosFaciales.append([strId, nombreDeServicio, cantidad])
                    servicioFacial.append(serviciosFaciales)
                credito = venta.credito
                if credito == "S":
                    boolCredito.append("Si")
                    consultaCredito = Creditos.objects.filter(
                        venta_id__id_venta=idVenta
                    )
                    if consultaCredito:
                        for datoCredito in consultaCredito:
                            idCredito = datoCredito.id_credito
                            restante = datoCredito.monto_restante
                        idsCreditos.append(idCredito)
                        if restante == 0:
                            boolPagado.append("Si")
                        else:
                            boolPagado.append("No")
                    else:
                        idsCreditos.append("error")

                else:
                    boolCredito.append("No")
                    idsCreditos.append("No")
                    boolPagado.append("No")

                montoPagado = venta.monto_pagar  # 1360
                montos.append(montoPagado)

                descuento = venta.descuento_id
                if descuento == None:
                    boolDescuentos.append("Sin descuento")
                    datosDescuento.append("Sin descuento")
                    descuentos.append("Sin descuento")
                    costoReal.append("Sin descuento")
                else:
                    boolDescuentos.append("Con descuento")
                    consultaDescuento = Descuentos.objects.filter(
                        id_descuento=descuento
                    )
                    for datoDescuento in consultaDescuento:
                        nombreDescuento = datoDescuento.nombre_descuento
                        porcentajeDescuento = datoDescuento.porcentaje
                    porcentajeTotalDescuento = 100 - float(porcentajeDescuento)
                    totalSinDescuento = (100 * montoPagado) / porcentajeTotalDescuento
                    totalDescuento = totalSinDescuento - montoPagado

                    datosDescuento.append([porcentajeDescuento, nombreDescuento])
                    descuentos.append(totalDescuento)
                    costoReal.append(totalSinDescuento)

            listaVentasMes = zip(
                ventasEmpleadoEnElMes,
                sucursales,
                clientes,
                boolProductos,
                productos,
                boolServCorporal,
                servicioCorporal,
                boolServFacial,
                servicioFacial,
                boolCredito,
                idsCreditos,
                boolPagado,
                montos,
                boolDescuentos,
                datosDescuento,
                descuentos,
                costoReal,
                tipoVenta,
            )

            # Mes anterior
            haceUnMes = hoy - relativedelta(months=1)  # 2022-05-07
            mesHaceUnMes = haceUnMes.strftime("%m")  # 05
            añoHaceUnMes = haceUnMes.strftime("%Y")
            mesAnteriorTexto = mesesDic[str(mesHaceUnMes)]

            diasDeUltimoMes = diasMeses[str(mesAnteriorTexto)]

            fechaPrimerDiaMesAnterior = (
                añoHaceUnMes + "-" + mesHaceUnMes + "-01"
            )  # 2022-05-01
            fechaUltimoDiaMesAnterior = (
                añoHaceUnMes + "-" + mesHaceUnMes + "-" + diasDeUltimoMes
            )  # 2022-05-31

            ventasEmpleadoEnElMesAnterior = Ventas.objects.filter(
                fecha_venta__range=[
                    fechaPrimerDiaMesAnterior,
                    fechaUltimoDiaMesAnterior,
                ],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )

            ventasEnElMesAnterior = 0
            montoTotalDeVentaMesAnterior = 0
            for ventaMesAnterior in ventasEmpleadoEnElMesAnterior:
                montoTotalVenta = ventaMesAnterior.monto_pagar
                montoTotalDeVentaMesAnterior = (
                    montoTotalDeVentaMesAnterior + montoTotalVenta
                )

                ventasEnElMesAnterior = ventasEnElMesAnterior + 1

            # Verificación contra el mes anterior
            ventasEnElMesEsMayorAlMesAnterior = False
            if ventasEnElMesAnterior == 0:
                porcentajeVentasMes = 100
            else:
                porcentajeVentasMes = ventasEnElMesActual / ventasEnElMesAnterior
                porcentajeVentasMes = porcentajeVentasMes - 1
                porcentajeVentasMes = porcentajeVentasMes * 100

            if porcentajeVentasMes > 0:
                ventasEnElMesEsMayorAlMesAnterior = True

            else:
                ventasEnElMesEsMayorAlMesAnterior = False
            porcentajeVentasMes = round(porcentajeVentasMes, 2)

            # Semana actual
            diaActual = datetime.today().isoweekday()  # 2 martes
            intdiaActual = int(diaActual)
            diaLunes = intdiaActual - 1  # 3 dias para el lunes
            diaDomingo = 7 - intdiaActual  # 2 dias para el sabado

            # Montos totales de semana actual
            fechaLunes = datetime.now() - timedelta(days=diaLunes)
            fechaDomingo = datetime.now() + timedelta(days=diaDomingo)

            ventasEmpleadoEnLaSemana = Ventas.objects.filter(
                fecha_venta__range=[fechaLunes, fechaDomingo],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )

            ventasEnEnLaSemana = 0
            for ventaSemana in ventasEmpleadoEnLaSemana:
                ventasEnEnLaSemana = ventasEnEnLaSemana + 1

            # Montos totales de semana anterior
            fechaLunesAnterior = fechaLunes - timedelta(days=7)
            fechaDomingoAnterior = fechaLunes - timedelta(days=1)

            ventasEmpleadoEnLaSemanaAnterior = Ventas.objects.filter(
                fecha_venta__range=[fechaLunesAnterior, fechaDomingoAnterior],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )

            ventasEnEnLaSemanaAnterior = 0
            for ventaSemanaAnterior in ventasEmpleadoEnLaSemanaAnterior:
                ventasEnEnLaSemanaAnterior = ventasEnEnLaSemanaAnterior + 1

            # Verificación contra la semana anterior
            ventasEnLaSemanaEsMayorALaSemanaAnterior = False

            if ventasEnEnLaSemanaAnterior == 0:
                porcentajeVentasSemanal = 100
            else:
                porcentajeVentasSemanal = (
                    ventasEnEnLaSemana / ventasEnEnLaSemanaAnterior
                )
                porcentajeVentasSemanal = porcentajeVentasSemanal - 1
                porcentajeVentasSemanal = porcentajeVentasSemanal * 100

            if porcentajeVentasSemanal > 0:
                ventasEnLaSemanaEsMayorALaSemanaAnterior = True

            else:
                ventasEnLaSemanaEsMayorALaSemanaAnterior = False
            porcentajeVentasSemanal = round(porcentajeVentasSemanal, 2)

            # Meses para gráfica por mes
            inicioMesEnero = añoHoy + "-01-01"
            finMesEnero = añoHoy + "-01-31"
            contadorVentasEnero = 0
            ventasEnEnero = Ventas.objects.filter(
                fecha_venta__range=[inicioMesEnero, finMesEnero],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            for ventaEnero in ventasEnEnero:
                contadorVentasEnero = contadorVentasEnero + 1

            inicioMesFebrero = añoHoy + "-02-01"
            finMesFebrero = añoHoy + "-02-28"
            contadorVentasFebrero = 0
            ventasEnFebrero = Ventas.objects.filter(
                fecha_venta__range=[inicioMesFebrero, finMesFebrero],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            for ventaFebrero in ventasEnFebrero:
                contadorVentasFebrero = contadorVentasFebrero + 1

            inicioMesMarzo = añoHoy + "-03-01"
            finMesMarzo = añoHoy + "-03-31"
            contadorVentasMarzo = 0
            ventasEnMarzo = Ventas.objects.filter(
                fecha_venta__range=[inicioMesMarzo, finMesMarzo],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            for ventaMarzo in ventasEnMarzo:
                contadorVentasMarzo = contadorVentasMarzo + 1

            inicioMesAbril = añoHoy + "-04-01"
            finMesAbril = añoHoy + "-04-30"
            contadorVentasAbril = 0
            ventasEnAbril = Ventas.objects.filter(
                fecha_venta__range=[inicioMesAbril, finMesAbril],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            for ventaAbril in ventasEnAbril:
                contadorVentasAbril = contadorVentasAbril + 1

            inicioMesMayo = añoHoy + "-05-01"
            finMesMayo = añoHoy + "-05-31"
            contadorVentasMayo = 0
            ventasEnMayo = Ventas.objects.filter(
                fecha_venta__range=[inicioMesMayo, finMesMayo],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            for ventaMayo in ventasEnMayo:
                contadorVentasMayo = contadorVentasMayo + 1

            inicioMesJunio = añoHoy + "-06-01"
            finMesJunio = añoHoy + "-06-30"
            contadorVentasJunio = 0
            ventasEnJunio = Ventas.objects.filter(
                fecha_venta__range=[inicioMesJunio, finMesJunio],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            for ventaJunio in ventasEnJunio:
                contadorVentasJunio = contadorVentasJunio + 1

            inicioMesJulio = añoHoy + "-07-01"
            finMesJulio = añoHoy + "-07-31"
            contadorVentasJulio = 0
            ventasEnJulio = Ventas.objects.filter(
                fecha_venta__range=[inicioMesJulio, finMesJulio],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            for ventaJulio in ventasEnJulio:
                contadorVentasJulio = contadorVentasJulio + 1

            inicioMesAgosto = añoHoy + "-08-01"
            finMesAgosto = añoHoy + "-08-31"
            contadorVentasAgosto = 0
            ventasEnAgosto = Ventas.objects.filter(
                fecha_venta__range=[inicioMesAgosto, finMesAgosto],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            for ventaAgosto in ventasEnAgosto:
                contadorVentasAgosto = contadorVentasAgosto + 1

            inicioMesSeptiembre = añoHoy + "-09-01"
            finMesSeptiembre = añoHoy + "-09-30"
            contadorVentasSeptiembre = 0
            ventasEnSeptiembre = Ventas.objects.filter(
                fecha_venta__range=[inicioMesSeptiembre, finMesSeptiembre],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            for ventaSeptiembre in ventasEnSeptiembre:
                contadorVentasSeptiembre = contadorVentasSeptiembre + 1

            inicioMesOctubre = añoHoy + "-10-01"
            finMesOctubre = añoHoy + "-10-31"
            contadorVentasOctubre = 0
            ventasEnOctubre = Ventas.objects.filter(
                fecha_venta__range=[inicioMesOctubre, finMesOctubre],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            for ventaOctubre in ventasEnOctubre:
                contadorVentasOctubre = contadorVentasOctubre + 1

            inicioMesNoviembre = añoHoy + "-11-01"
            finMesNoviembre = añoHoy + "-11-30"
            contadorVentasNoviembre = 0
            ventasEnNoviembre = Ventas.objects.filter(
                fecha_venta__range=[inicioMesNoviembre, finMesNoviembre],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            for ventaNoviembre in ventasEnNoviembre:
                contadorVentasNoviembre = contadorVentasNoviembre + 1

            inicioMesDiciembre = añoHoy + "-12-01"
            finMesDiciembre = añoHoy + "-12-31"
            contadorVentasDiciembre = 0
            ventasEnDiciembre = Ventas.objects.filter(
                fecha_venta__range=[inicioMesDiciembre, finMesDiciembre],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            for ventaDiciembre in ventasEnDiciembre:
                contadorVentasDiciembre = contadorVentasDiciembre + 1

            if tipo == "Administrador":
                # Ventas totales
                ventasTotalesDeEmpleadosEnElMes = Ventas.objects.filter(
                    fecha_venta__range=[fechaInicioMesActual, fechaDiaMesActual]
                )
            else:
                ventasTotalesDeEmpleadosEnElMes = Ventas.objects.filter(
                    fecha_venta__range=[fechaInicioMesActual, fechaDiaMesActual],
                    sucursal_id__id_sucursal=idsucursal,
                )

            contadorVentasTotalesMes = 0
            for ventaMes in ventasTotalesDeEmpleadosEnElMes:
                contadorVentasTotalesMes = contadorVentasTotalesMes + 1

            if contadorVentasTotalesMes == 0:
                porcentajeVentasDelEmpleado = 0
            else:
                porcentajeVentasDelEmpleado = (
                    ventasEnElMesActual * 100
                ) / contadorVentasTotalesMes

            porcentajeDemasEmpleados = 100 - porcentajeVentasDelEmpleado

            if montoTotalDeVentaMesAnterior == 0:
                porcentajeMontoVentas = 100
            else:
                porcentajeMontoVentas = (
                    montoVentasEnElMesActual / montoTotalDeVentaMesAnterior
                )
                porcentajeMontoVentas = porcentajeMontoVentas - 1
                porcentajeMontoVentas = porcentajeMontoVentas * 100

            if porcentajeMontoVentas > 0:
                esteMesVendioMas = True

            else:
                esteMesVendioMas = False

            # INFORME DE EMPLEADO EN EL AÑO------------------------------------------------------------------------------------------------------------

            primeroDeEnero = añoHoy + "-01-01"
            ultimoDiciemte = añoHoy + "-12-31"

            ventasEmpleadoEnElAño = Ventas.objects.filter(
                fecha_venta__range=[primeroDeEnero, ultimoDiciemte],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )

            contadorVentasEnElAño = 0
            montoVentaEnElAño = 0
            for ventaAnual in ventasEmpleadoEnElAño:
                contadorVentasEnElAño = contadorVentasEnElAño + 1
                montoVenta = ventaAnual.monto_pagar
                montoVentaEnElAño = montoVentaEnElAño + montoVenta

            añoAnterior = int(añoHoy) - 1
            primeroDeEneroAnterior = str(añoAnterior) + "-01-01"
            ultimoDiciemteAnterior = str(añoAnterior) + "-12-31"

            ventasEmpleadoEnElAñoAnterior = Ventas.objects.filter(
                fecha_venta__range=[primeroDeEneroAnterior, ultimoDiciemteAnterior],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )

            contadorVentasEnElAñoAnterior = 0
            montoVentaEnElAñoAnterior = 0
            for ventaAnualAnterior in ventasEmpleadoEnElAñoAnterior:
                contadorVentasEnElAñoAnterior = contadorVentasEnElAñoAnterior + 1
                montoVenta = ventaAnual.monto_pagar
                montoVentaEnElAñoAnterior = montoVentaEnElAñoAnterior + montoVenta

            if contadorVentasEnElAñoAnterior == 0:
                porcentajeVentaAnual = 100
            else:
                porcentajeVentaAnual = (
                    contadorVentasEnElAño / contadorVentasEnElAñoAnterior
                )
                porcentajeVentaAnual = porcentajeVentaAnual - 1
                porcentajeVentaAnual = porcentajeVentaAnual * 100

            if porcentajeVentaAnual > 0:
                ventasMayores = True

            else:
                ventasMayores = False

            primerAñoAntes = int(añoHoy) - 1
            segundoAñoAntes = int(añoHoy) - 2
            tercerAñoAntes = int(añoHoy) - 3

            eneroHaceDosAños = str(segundoAñoAntes) + "-01-01"
            diciembreHaceDosAños = str(segundoAñoAntes) + "-12-31"
            ventasEmpleadoHaceDosAños = Ventas.objects.filter(
                fecha_venta__range=[eneroHaceDosAños, diciembreHaceDosAños],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )

            contadorVentasHaceDosAños = 0
            for venta in ventasEmpleadoHaceDosAños:
                contadorVentasHaceDosAños = contadorVentasHaceDosAños + 1

            eneroHaceTresAños = str(tercerAñoAntes) + "-01-01"
            diciembreHaceTresAños = str(tercerAñoAntes) + "-12-31"
            ventasEmpleadoHaceTresAños = Ventas.objects.filter(
                fecha_venta__range=[eneroHaceTresAños, diciembreHaceTresAños],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )

            contadorVentasHaceTresAños = 0
            for venta in ventasEmpleadoHaceTresAños:
                contadorVentasHaceTresAños = contadorVentasHaceTresAños + 1

            # pie chart
            if tipo == "Administrador":
                # Ventas totales
                ventasTotalesDeEmpleadosEnElAño = Ventas.objects.filter(
                    fecha_venta__range=[primeroDeEnero, ultimoDiciemte]
                )
            else:
                ventasTotalesDeEmpleadosEnElAño = Ventas.objects.filter(
                    fecha_venta__range=[primeroDeEnero, ultimoDiciemte],
                    sucursal_id__id_sucursal=idsucursal,
                )

            contadorVentasTotalesDelAño = 0
            for ventaMes in ventasTotalesDeEmpleadosEnElAño:
                contadorVentasTotalesDelAño = contadorVentasTotalesDelAño + 1

            if contadorVentasTotalesDelAño == 0:
                porcentajeVentasDelEmpleadoEnElAño = 0
            else:

                porcentajeVentasDelEmpleadoEnElAño = (
                    contadorVentasEnElAño * 100
                ) / contadorVentasTotalesDelAño

            porcentajeDemasEmpleadosEnElAño = 100 - porcentajeVentasDelEmpleadoEnElAño

            if montoVentaEnElAñoAnterior == 0:
                porcentajeMontoVentaAnual = 100
            else:
                porcentajeMontoVentaAnual = (
                    montoVentaEnElAño / montoVentaEnElAñoAnterior
                )
                porcentajeMontoVentaAnual = porcentajeMontoVentaAnual - 1
                porcentajeMontoVentaAnual = porcentajeMontoVentaAnual * 100

            if porcentajeMontoVentaAnual > 0:
                esteAñoVendioMas = True

            else:
                esteAñoVendioMas = False

            ventasEmpleadoEnElAño2 = Ventas.objects.filter(
                fecha_venta__range=[primeroDeEnero, ultimoDiciemte],
                empleado_vendedor_id__id_empleado=idEmpleadoConfigurar,
            )
            sucursalesAño = []
            clientesAño = []
            boolProductosAño = []
            productosAño = []
            boolServCorporalAño = []
            servicioCorporalAño = []
            boolServFacialAño = []
            servicioFacialAño = []
            boolCreditoAño = []
            idsCreditosAño = []
            boolPagadoAño = []
            montosAño = []
            boolDescuentosAño = []
            datosDescuentoAño = []
            costoRealAño = []
            descuentosAño = []
            tipoVentaAño = []

            for venta in ventasEmpleadoEnElAño2:
                idVenta = venta.id_venta

                # Para tabla de ventas
                sucursal = venta.sucursal_id
                consultaSucursal = Sucursales.objects.filter(id_sucursal=sucursal)
                for suc in consultaSucursal:
                    nombreSucursal = suc.nombre
                sucursalesAño.append(nombreSucursal)

                cliente = venta.cliente_id
                if cliente == None:
                    clientesAño.append(["x", "Cliente momentaneo"])
                else:
                    consultaCliente = Clientes.objects.filter(id_cliente=cliente)
                    for datoCliente in consultaCliente:
                        nombreCliente = datoCliente.nombre_cliente
                        apellido = datoCliente.apellidoPaterno_cliente

                    nombreCompletoCliente = nombreCliente + " " + apellido

                    clientesAño.append([cliente, nombreCompletoCliente])

                # Productos
                codigosProductos = venta.ids_productos
                if codigosProductos == "":
                    boolProductosAño.append("Sin productos comprados")
                    productosAño.append("x")
                else:
                    boolProductosAño.append("Se compraron productos")
                    cantidadesProductos = venta.cantidades_productos
                    arregloCodigosProductos = codigosProductos.split(",")
                    arregloCantidadesProductos = cantidadesProductos.split(",")

                    listaProductos = zip(
                        arregloCodigosProductos, arregloCantidadesProductos
                    )

                    productitos = []
                    for producto, cantidades in listaProductos:
                        idcodigoProducto = str(producto)
                        cantidad = str(cantidades)

                        if "PV" in idcodigoProducto:
                            # Producto para venta
                            tipoVentaAño.append("Venta")
                            consultaProducto = ProductosVenta.objects.filter(
                                codigo_producto=idcodigoProducto
                            )
                        else:
                            # Producto para renta
                            tipoVentaAño.append("Renta")
                            consultaProducto = ProductosRenta.objects.filter(
                                codigo_producto=idcodigoProducto
                            )

                        for datoProducto in consultaProducto:
                            nombreProducto = datoProducto.nombre_producto
                        productitos.append([idcodigoProducto, nombreProducto, cantidad])
                    productosAño.append(productitos)

                # ServiciosCorporales
                serviciosCorporales = venta.ids_servicios_corporales
                if serviciosCorporales == "":
                    boolServCorporalAño.append("Sin servicios coorporales")
                    servicioCorporalAño.append("x")
                else:
                    boolServCorporalAño.append("Se compraron servicios")
                    cantidadesServiciosCorporales = (
                        venta.cantidades_servicios_corporales
                    )
                    arregloIdsServiciosCorporales = serviciosCorporales.split(",")
                    arregloCantidadesServiciosCorporales = (
                        cantidadesServiciosCorporales.split(",")
                    )

                    listaServiciosCorporales = zip(
                        arregloIdsServiciosCorporales,
                        arregloCantidadesServiciosCorporales,
                    )

                    serviciosCorporales = []
                    for (
                        idServicioCorporal,
                        cantidadServiciosCorporal,
                    ) in listaServiciosCorporales:
                        intId = int(idServicioCorporal)
                        strId = str(idServicioCorporal)
                        cantidad = str(cantidadServiciosCorporal)

                        consultaServicio = Servicios.objects.filter(id_servicio=intId)

                        for datoServicio in consultaServicio:
                            nombreDeServicio = datoServicio.nombre_servicio
                        serviciosCorporales.append([strId, nombreDeServicio, cantidad])
                    servicioCorporalAño.append(serviciosCorporales)

                # ServiciosFaciales
                serviciosFaciales = venta.ids_servicios_faciales
                if serviciosFaciales == "":
                    boolServFacialAño.append("Sin servicios faciales")
                    servicioFacialAño.append("x")
                else:
                    boolServFacialAño.append("Se compraron servicios")
                    cantiadesServiciosFaciales = venta.cantidades_servicios_faciales
                    arregloIdsServiciosFaciales = serviciosFaciales.split(",")
                    arregloCantidadesServiciosFaciales = (
                        cantiadesServiciosFaciales.split(",")
                    )

                    listaServiciosFaciales = zip(
                        arregloIdsServiciosFaciales, arregloCantidadesServiciosFaciales
                    )

                    serviciosFaciales = []
                    for (
                        idServiciosFacial,
                        cantidadServicioFacial,
                    ) in listaServiciosFaciales:
                        intId = int(idServiciosFacial)
                        strId = str(idServiciosFacial)
                        cantidad = str(cantidadServicioFacial)

                        consultaServicio = Servicios.objects.filter(id_servicio=intId)

                        for datoServicio in consultaServicio:
                            nombreDeServicio = datoServicio.nombre_servicio
                        serviciosFaciales.append([strId, nombreDeServicio, cantidad])
                    servicioFacialAño.append(serviciosFaciales)
                credito = venta.credito
                if credito == "S":
                    boolCreditoAño.append("Si")
                    consultaCredito = Creditos.objects.filter(
                        venta_id__id_venta=idVenta
                    )
                    if consultaCredito:
                        for datoCredito in consultaCredito:
                            idCredito = datoCredito.id_credito
                            restante = datoCredito.monto_restante
                        idsCreditosAño.append(idCredito)
                        if restante == 0:
                            boolPagadoAño.append("Si")
                        else:
                            boolPagadoAño.append("No")
                    else:
                        idsCreditosAño.append("error")

                else:
                    boolCreditoAño.append("No")
                    idsCreditosAño.append("No")
                    boolPagadoAño.append("No")

                montoPagado = venta.monto_pagar
                montosAño.append(montoPagado)

                descuento = venta.descuento_id
                if descuento == None:
                    boolDescuentosAño.append("Sin descuento")
                    datosDescuentoAño.append("Sin descuento")
                    descuentosAño.append("Sin descuento")
                    costoRealAño.append("Sin descuento")
                else:
                    boolDescuentosAño.append("Con descuento")
                    consultaDescuento = Descuentos.objects.filter(
                        id_descuento=descuento
                    )
                    for datoDescuento in consultaDescuento:
                        nombreDescuento = datoDescuento.nombre_descuento
                        porcentajeDescuento = datoDescuento.porcentaje
                    porcentajeTotalDescuento = 100 - float(porcentajeDescuento)
                    totalSinDescuento = (100 * montoPagado) / porcentajeTotalDescuento
                    totalDescuento = totalSinDescuento - montoPagado

                    datosDescuentoAño.append([porcentajeDescuento, nombreDescuento])
                    descuentosAño.append(totalDescuento)
                    costoRealAño.append(totalSinDescuento)

            listaVentasAño = zip(
                ventasEmpleadoEnElAño2,
                sucursalesAño,
                clientesAño,
                boolProductosAño,
                productosAño,
                boolServCorporalAño,
                servicioCorporalAño,
                boolServFacialAño,
                servicioFacialAño,
                boolCreditoAño,
                idsCreditosAño,
                boolPagadoAño,
                montosAño,
                boolDescuentosAño,
                datosDescuentoAño,
                descuentosAño,
                costoRealAño,
                tipoVentaAño,
            )

            for nombreSucursal in boolDescuentosAño:
                print(nombreSucursal)

            return render(
                request,
                "3 Empleados/informeEmpleado.html",
                {
                    "consultaPermisos": consultaPermisos,
                    "idEmpleado": idEmpleado,
                    "idPerfil": idPerfil,
                    "idConfig": idConfig,
                    "nombresEmpleado": nombresEmpleado,
                    "tipoUsuario": tipoUsuario,
                    "letra": letra,
                    "puestoEmpleado": puestoEmpleado,
                    "nombres": nombres,
                    "apellidoPaterno": apellidoPaterno,
                    "apellidoMaterno": apellidoMaterno,
                    "telefono": telefono,
                    "puesto": puesto,
                    "nombreUsuario": nombreUsuario,
                    "letrasEmpleado": letrasEmpleado,
                    "tipo": tipo,
                    "sucursalEmpleado": sucursalEmpleado,
                    "idsucursal": idsucursal,
                    "idEmpleadoEditar2": idEmpleadoEditar2,
                    "activo": activo,
                    "fecha_alta": fecha_alta,
                    "fecha_baja": fecha_baja,
                    "idEmpleadoEditar3": idEmpleadoEditar3,
                    "idEmpleadoEditar4": idEmpleadoEditar4,
                    "totalVentas": totalVentas,
                    "contadorVentas": contadorVentas,
                    "notificacionRenta": notificacionRenta,
                    "diadehoy": diadehoy,
                    "mesdehoy": mesdehoy,
                    "añoHoy": añoHoy,
                    "ventasEnElMesActual": ventasEnElMesActual,
                    "ventasEnElMesAnterior": ventasEnElMesAnterior,
                    "mesAnteriorTexto": mesAnteriorTexto,
                    "ventasEnElMesEsMayorAlMesAnterior": ventasEnElMesEsMayorAlMesAnterior,
                    "porcentajeVentasMes": porcentajeVentasMes,
                    "ventasEnEnLaSemana": ventasEnEnLaSemana,
                    "ventasEnEnLaSemanaAnterior": ventasEnEnLaSemanaAnterior,
                    "porcentajeVentasSemanal": porcentajeVentasSemanal,
                    "ventasEnLaSemanaEsMayorALaSemanaAnterior": ventasEnLaSemanaEsMayorALaSemanaAnterior,
                    "contadorVentasEnero": contadorVentasEnero,
                    "contadorVentasFebrero": contadorVentasFebrero,
                    "contadorVentasMarzo": contadorVentasMarzo,
                    "contadorVentasAbril": contadorVentasAbril,
                    "contadorVentasMayo": contadorVentasMayo,
                    "contadorVentasJunio": contadorVentasJunio,
                    "contadorVentasJulio": contadorVentasJulio,
                    "contadorVentasAgosto": contadorVentasAgosto,
                    "contadorVentasSeptiembre": contadorVentasSeptiembre,
                    "contadorVentasOctubre": contadorVentasOctubre,
                    "contadorVentasNoviembre": contadorVentasNoviembre,
                    "contadorVentasDiciembre": contadorVentasDiciembre,
                    "porcentajeVentasDelEmpleado": porcentajeVentasDelEmpleado,
                    "porcentajeDemasEmpleados": porcentajeDemasEmpleados,
                    "contadorVentasTotalesMes": contadorVentasTotalesMes,
                    "listaVentasMes": listaVentasMes,
                    "montoVentasEnElMesActual": montoVentasEnElMesActual,
                    "montoTotalDeVentaMesAnterior": montoTotalDeVentaMesAnterior,
                    "porcentajeMontoVentas": porcentajeMontoVentas,
                    "esteMesVendioMas": esteMesVendioMas,
                    "contadorVentasEnElAño": contadorVentasEnElAño,
                    "contadorVentasEnElAñoAnterior": contadorVentasEnElAñoAnterior,
                    "porcentajeVentaAnual": porcentajeVentaAnual,
                    "ventasMayores": ventasMayores,
                    "primerAñoAntes": primerAñoAntes,
                    "segundoAñoAntes": segundoAñoAntes,
                    "tercerAñoAntes": tercerAñoAntes,
                    "contadorVentasHaceDosAños": contadorVentasHaceDosAños,
                    "contadorVentasHaceTresAños": contadorVentasHaceTresAños,
                    "porcentajeVentasDelEmpleadoEnElAño": porcentajeVentasDelEmpleadoEnElAño,
                    "porcentajeDemasEmpleadosEnElAño": porcentajeDemasEmpleadosEnElAño,
                    "montoVentaEnElAño": montoVentaEnElAño,
                    "montoVentaEnElAñoAnterior": montoVentaEnElAñoAnterior,
                    "porcentajeMontoVentaAnual": porcentajeMontoVentaAnual,
                    "esteAñoVendioMas": esteAñoVendioMas,
                    "listaVentasAño": listaVentasAño,
                    "idEmpleadoConfigurar": idEmpleadoConfigurar,
                    "notificacionCita": notificacionCita,
                },
            )

        return redirect("/verEmpleados/")
    else:
        return render(request, "1 Login/login.html")


def actNombreUsuario(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idActualizado = request.POST["idActualizado"]
            nombreUsuarioActualizado = request.POST["nombreUsuarioActualizado"]

            consulta = Empleados.objects.filter(id_empleado=idActualizado)

            for dato in consulta:
                nombreActualizado = dato.nombres

            actualizarInfoPersonal = Empleados.objects.filter(
                id_empleado=idActualizado
            ).update(nombre_usuario=nombreUsuarioActualizado)

            if actualizarInfoPersonal:
                # falta notificacion
                request.session["empleadoActualizado"] = (
                    "Se ha actualizado el nombre de usuario de "
                    + nombreActualizado
                    + " correctamente!"
                )
                return redirect("/verEmpleados/")

        return redirect("/verEmpleados/")
    else:
        return render(request, "1 Login/login.html")


def actContrasena(request):

    if "idSesion" in request.session:

        if request.method == "POST":
            idActualizado = request.POST["idActualizado"]
            contraActualizada = request.POST["contraActualizada"]

            consulta = Empleados.objects.filter(id_empleado=idActualizado)

            for dato in consulta:
                nombreActualizado = dato.nombres

            actualizarInfoPersonal = Empleados.objects.filter(
                id_empleado=idActualizado
            ).update(contrasena=contraActualizada)

            if actualizarInfoPersonal:
                # falta notificacion
                request.session["empleadoActualizado"] = (
                    "Se ha actualizado la contraseña de "
                    + nombreActualizado
                    + " correctamente!"
                )
                return redirect("/verEmpleados/")

        return redirect("/verEmpleados/")
    else:
        return render(request, "1 Login/login.html")
