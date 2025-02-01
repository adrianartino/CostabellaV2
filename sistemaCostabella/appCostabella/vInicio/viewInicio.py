# Renderizado
import os

# Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

# Librerías de fecha
from datetime import date, datetime, time, timedelta

# Para mandar telegram
import telepot
from appCostabella import keysBotCostabella

# Importacion de modelos
from appCostabella.models import Empleados, Permisos, Sucursales

# Notificaciones
from appCostabella.notificaciones.notificaciones import (
    notificacionCitas,
    notificacionRentas,
)
from django.db.models import Q


# Vista salir
def salir(request):

    # Cerrar variables de sesión
    del request.session["idSesion"]
    del request.session["nombresSesion"]
    del request.session["tipoUsuario"]

    return redirect("/login/")


# Vista login
def login(request):

    # Si ya existe una sesion al teclear login...
    if "idSesion" in request.session:
        return redirect("/inicio/")
    # Si no hay una sesion iniciada..
    else:
        # si se apretó el botón.
        if request.method == "POST":
            nombreusuario = request.POST["nombreusuario"]
            contrasenaIngresada = request.POST["pwd"]

            consultaUsuario = Empleados.objects.filter(nombre_usuario=nombreusuario)

            if consultaUsuario:

                for dato in consultaUsuario:
                    idEmpleado = dato.id_empleado
                    nombres = dato.nombres
                    contrasena = dato.contrasena
                    sucursal = dato.id_sucursal_id
                    puesto = dato.puesto

                if contrasenaIngresada == contrasena:
                    # El usuario se loguea..
                    ingresado = "Bienvenido!"

                    request.session["idSesion"] = idEmpleado
                    request.session["nombresSesion"] = nombres
                    request.session["puestoSesion"] = puesto
                    request.session["recienIniciado"] = "primerInicio"

                    date = datetime.now()
                    hora = date.time().strftime("%H:%M")
                    if sucursal == None:  # Si no tiene una sucursal..
                        request.session["tipoUsuario"] = "esAdmin"
                        try:
                            tokenTelegram = keysBotCostabella.tokenBotCostabella
                            botCostabella = telepot.Bot(tokenTelegram)

                            idGrupoTelegram = keysBotCostabella.idGrupo
                            mensaje = (
                                "Hola \U0001F44B! La empleada administradora "
                                + nombres
                                + " ha iniciado sesión a las "
                                + str(hora)
                                + " horas."
                            )
                            botCostabella.sendMessage(idGrupoTelegram, mensaje)

                        except:
                            print("An exception occurred")

                        return redirect("/inicio/")
                    else:
                        consultaSucursal = Sucursales.objects.filter(
                            id_sucursal=sucursal
                        )

                        for datoSucursal in consultaSucursal:
                            nombreSucural = datoSucursal.nombre

                        request.session["tipoUsuario"] = "esEmpleado"
                        try:
                            tokenTelegram = keysBotCostabella.tokenBotCostabella
                            botCostabella = telepot.Bot(tokenTelegram)

                            idGrupoTelegram = keysBotCostabella.idGrupo
                            mensaje = (
                                "Hola \U0001F44B	! La empleada "
                                + nombres
                                + " ha iniciado sesión  en la sucursal "
                                + nombreSucural
                                + " a las "
                                + str(hora)
                                + " horas."
                            )
                            botCostabella.sendMessage(idGrupoTelegram, mensaje)

                        except:
                            print("An exception occurred")

                        return redirect("/inicio/")
                else:
                    error = "Ha ingresado una contraseña incorrecta!"
                    return render(
                        request,
                        "1 Login/login.html",
                        {"error": error, "nombreusuario": nombreusuario},
                    )
            else:
                error = "El usuario no existe!"
                return render(request, "1 Login/login.html", {"error": error})

        return render(request, "1 Login/login.html")


# Vista inicio
def inicio(request):

    # Si ya existe una sesion al teclear login...
    if "idSesion" in request.session:
        idEmpleado = request.session["idSesion"]
        idPerfil = idEmpleado
        idConfig = idEmpleado
        nombresEmpleado = request.session["nombresSesion"]
        tipoUsuario = request.session["tipoUsuario"]
        puestoEmpleado = request.session["puestoSesion"]

        # Variable para menu
        estaEnInicio = True

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

        # Si es la primera vez que inicia sesión.. Bienvenida
        if "recienIniciado" in request.session:
            bienvenida = "Bienvenida, " + nombresEmpleado + "!!"
            del request.session[
                "recienIniciado"
            ]  # se cierra la sesión del primer inicio de sesión
            return render(
                request,
                "2 Inicio/inicio.html",
                {
                    "idEmpleado": idEmpleado,
                    "nombresEmpleado": nombresEmpleado,
                    "tipoUsuario": tipoUsuario,
                    "letra": letra,
                    "puestoEmpleado": puestoEmpleado,
                    "estaEnInicio": estaEnInicio,
                    "bienvenida": bienvenida,
                    "idPerfil": idPerfil,
                    "idConfig": idConfig,
                    "notificacionRenta": notificacionRenta,
                    "notificacionCita": notificacionCita,
                    "consultaPermisos": consultaPermisos,
                },
            )
        else:
            return render(
                request,
                "2 Inicio/inicio.html",
                {
                    "idEmpleado": idEmpleado,
                    "nombresEmpleado": nombresEmpleado,
                    "tipoUsuario": tipoUsuario,
                    "letra": letra,
                    "puestoEmpleado": puestoEmpleado,
                    "estaEnInicio": estaEnInicio,
                    "idPerfil": idPerfil,
                    "idConfig": idConfig,
                    "notificacionRenta": notificacionRenta,
                    "notificacionCita": notificacionCita,
                    "consultaPermisos": consultaPermisos,
                },
            )
    # Si no hay una sesion iniciada..
    else:
        return render(request, "1 Login/login.html")
