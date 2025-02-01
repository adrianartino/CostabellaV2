
#Para ruta
from pathlib import Path

from django.shortcuts import redirect, render

BASE_DIR = Path(__file__).resolve().parent.parent

# Librerías de fecha
from datetime import date, datetime, time, timedelta

# Importacion de modelos
from appCostabella.models import (Clientes,
                                  ComprasGastos, ComprasRentas, ComprasVentas, Creditos, Descuentos,
                                  Empleados, PagosCreditos, Permisos,
                                  ProductosGasto, ProductosRenta,
                                  ProductosVenta, Rentas, Servicios, Sucursales, Ventas)
#Notificaciones
from appCostabella.notificaciones.notificaciones import (notificacionCitas,
                                                         notificacionRentas)
from dateutil.relativedelta import relativedelta


def informeDeVentas(request):

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

        hoy = datetime.now()
        
        mesdehoynumero = hoy.strftime('%m') #06
        
        mesesDic = {
            "01":'Enero',
            "02":'Febrero',
            "03":'Marzo',
            "04":'Abril',
            "05":'Mayo',
            "06":'Junio',
            "07":'Julio',
            "08":'Agosto',
            "09":'Septiembre',
            "10":'Octubre',
            "11":'Noviembre',
            "12":'Diciembre'
        }
        
        diasMeses = {
            'Enero':'31',
            'Febrero':'28',
            'Marzo':'31',
            'Abril':'30',
            'Mayo':'31',
            'Junio':'30',
            'Julio':'31',
            'Agosto':'31',
            'Septiembre':'30',
            'Octubre':'31',
            'Noviembre':'30',
            'Diciembre':'31'
        }
        #Mes actual
        diadehoy = hoy.strftime('%d')
        añoHoy = hoy.strftime('%Y')
        mesdehoy = mesesDic[str(mesdehoynumero)]
        
        fechaDiaMesActual = añoHoy+"-"+mesdehoynumero+"-"+diadehoy  #Día actual  2022-06-07
        fechaInicioMesActual = añoHoy+"-"+mesdehoynumero+"-01"  #Primer día del mes 2022-06-01  
        
        #Ingresos totales de mes actual, ventas, creditos y rentas
        consultaVentasMesActual = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual], credito="N")
        
        montoIngresoMesActual = 0
        contadorVentasmesActual = 0
        contadorRentasmesActual =0
        contadorCreditosmesActual =0

        numeroCreditos = 0
        numeroVentas =0
        numeroRentas =0



        
        if consultaVentasMesActual:
            for ventaRealizada in consultaVentasMesActual:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoMesActual = montoIngresoMesActual + montoVenta
                contadorVentasmesActual = contadorVentasmesActual + montoVenta
                numeroVentas = numeroVentas +1
        
        consultaCreditosMesActual = Creditos.objects.filter(fecha_venta_credito__range=[fechaInicioMesActual,fechaDiaMesActual], renta_id__isnull=True)
        
        if consultaCreditosMesActual:
            for crceditoRealizado in consultaCreditosMesActual:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoMesActual = montoIngresoMesActual + montoPagadoCredito
                contadorCreditosmesActual = contadorCreditosmesActual + montoPagadoCredito
                numeroCreditos = numeroCreditos +1
            
        consultaRentasMesActual = Rentas.objects.filter(fecha_apartado__range=[fechaInicioMesActual,fechaDiaMesActual])
        
        if consultaRentasMesActual:
            for rentaRealizada in consultaRentasMesActual:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado 
                montoIngresoMesActual = montoIngresoMesActual + sumaPagosRenta

                contadorRentasmesActual = contadorRentasmesActual + sumaPagosRenta
                numeroRentas = numeroRentas +1

        
        #totales efectivo, tarjeta, transferencia

        #EFECTIVO
        consultaVentasMesEfectivo = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual],tipo_pago="Efectivo",credito="N")
        totalEfectivo =0
        for efectivo in consultaVentasMesEfectivo:
            monto_efectivo = efectivo.monto_pagar
            totalEfectivo = totalEfectivo + monto_efectivo

       

        
        #TARJETA
        consultaVentasMesTarjeta = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual],tipo_pago="Tarjeta",credito="N")
        totalTarjeta =0
        for tarjeta in consultaVentasMesTarjeta:
            montoTarjeta = tarjeta.monto_pagar
            totalTarjeta = totalTarjeta + montoTarjeta
        
        #TRANSFERENCIA 
        consultaVentasMesTransferencia = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual],tipo_pago="Transferencia",credito="N")
        totalTransferencia =0
        for transferencia in consultaVentasMesTransferencia:
            montoTransferencia = transferencia.monto_pagar
            totalTransferencia = totalTransferencia + montoTransferencia
        
        #PAGOS DE LOS CREDITOS
        creditosEfectivo = Creditos.objects.filter(fecha_venta_credito__range=[fechaInicioMesActual,fechaDiaMesActual])
        for credito in creditosEfectivo:
            idCredito = credito.id_credito
        
            pagosCredito = PagosCreditos.objects.filter(id_credito_id__id_credito=idCredito)
            for pago in pagosCredito:
                tipoPago1 = pago.tipo_pago1
                tipoPago2 = pago.tipo_pago2
                tipoPago3 = pago.tipo_pago3
                tipoPago4 = pago.tipo_pago4

                if tipoPago1:
                    montoPagado1 = pago.monto_pago1
                    if tipoPago1 == "Efectivo":
                        totalEfectivo = totalEfectivo + montoPagado1
                    elif tipoPago1 == "Tarjeta":
                        totalTarjeta = totalTarjeta + montoPagado1
                    elif tipoPago1 == "Transferencia":
                        totalTransferencia = totalTransferencia + montoPagado1
                
                elif tipoPago2:
                    montoPagado2 = pago.monto_pago2
                    if tipoPago2 == "Efectivo":
                        totalEfectivo = totalEfectivo + montoPagado2
                    elif tipoPago2 == "Tarjeta":
                        totalTarjeta = totalTarjeta + montoPagado2
                    elif tipoPago2 == "Transferencia":
                        totalTransferencia = totalTransferencia + montoPagado2
                
                elif tipoPago3:
                    montoPagado3 =pago.monto_pago3
                    if tipoPago3 == "Efectivo":
                        totalEfectivo = totalEfectivo + montoPagado3
                    elif tipoPago3 == "Tarjeta":
                        totalTarjeta = totalTarjeta + montoPagado3
                    elif tipoPago3 == "Transferencia":
                        totalTransferencia = totalTransferencia + montoPagado3
                        
                elif tipoPago4:
                    montoPagado4 = pago.monto_pago4
                    if tipoPago4 == "Efectivo":
                        totalEfectivo = totalEfectivo + montoPagado4
                    elif tipoPago4 == "Tarjeta":
                        totalTarjeta = totalTarjeta + montoPagado4
                    elif tipoPago4 == "Transferencia":
                        totalTransferencia = totalTransferencia + montoPagado4
        
        
        
        #TOP CLIENTES CON MAS COMPRAS

        consultaVentasMesClientes = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual], cliente__isnull=False)

        clientesTop = []
        montosTop = []
        clientesMontosTotales = []
        clientesIds = []
        contadorClientesArray = []
        if consultaVentasMesClientes:
            for clienteVentas in consultaVentasMesClientes:
                cliente_ventas = clienteVentas.cliente_id
                monto_total_cliente = clienteVentas.monto_pagar
                clientesMontosTotales.append(monto_total_cliente) #180,600
                clientesIds.append(cliente_ventas) #1,1
                
            listaClientesCompradores = zip(clientesIds, clientesMontosTotales)
            
            listaClientes = []
            montoPorCliente = []
            contadorClientesArray = []
            
            
            for idcliente, montoTotalCliente in listaClientesCompradores:
                
                strIdCliente = str(idcliente)
                intMonto = float(montoTotalCliente)
                
                if strIdCliente in listaClientes:
                    indice = listaClientes.index(strIdCliente)
                    montoASumar = montoPorCliente[indice]
                    nuevaSumatoria = float(montoASumar) + intMonto
                    montoPorCliente[indice] = str(nuevaSumatoria)
                else:
                    listaClientes.append(strIdCliente)
                    montoPorCliente.append(str(intMonto))
            
            listaZipClientes = zip(listaClientes, montoPorCliente)
            
            listaOrdenadaMayorAMenor = sorted(listaZipClientes, key = lambda t: t[-1], reverse=True)
            tuples = zip(*listaOrdenadaMayorAMenor)
            listaClientesOrdenados, listaMontosOrdenados = [ list(tuple) for tuple in  tuples]
           
                    
            infoCliente = []

            
            cotadorClientes = 0
            for cliente in listaClientesOrdenados:
                cotadorClientes = cotadorClientes + 1
                contadorClientesArray.append(cotadorClientes)
                id_cliente_top = cliente
                clienteDatos = Clientes.objects.filter(id_cliente= id_cliente_top)
                for c in clienteDatos:

                    nombre_cliente_top = c.nombre_cliente
                    apellido =  c.apellidoPaterno_cliente
                    apellido2 = c.apellidoMaterno_cliente
                infoCliente.append([nombre_cliente_top,apellido,apellido2])

            clientesTops = zip (listaClientesOrdenados,listaMontosOrdenados,contadorClientesArray,infoCliente)
            clientesTopsModal =zip (listaClientesOrdenados,listaMontosOrdenados,contadorClientesArray,infoCliente) 
        else:
            clientesTops = None
            clientesTopsModal = None
            
        
        #TOP EMPLEADOS CON MÁS VENTAS

        consultaTodasLasVentasDelMes = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual])

        idsEmpleados = []
        montosTotalesDeVentaEmpleados = []
        if consultaTodasLasVentasDelMes:
            for venta in consultaTodasLasVentasDelMes:
                idEmpleado = venta.empleado_vendedor_id
                idsEmpleados.append(idEmpleado) #1,1
                montoVendido = venta.monto_pagar
                montosTotalesDeVentaEmpleados.append(montoVendido)
                
            
            listaEmpleados = []
            contadorVentasEmpleado = []
            contadorEmpleado = []
            listaMontosPorEmpleados = []
            
            listaEmpleadosVentas = zip(idsEmpleados, montosTotalesDeVentaEmpleados)
            
            contadorEmpleados = 0
            for idEmpleado, montoVentita in listaEmpleadosVentas:
                
                strIdEmpleado = str(idEmpleado)
                floatMontoVendido = float(montoVentita)
                
                if strIdEmpleado in listaEmpleados:
                    indice = listaEmpleados.index(strIdEmpleado)
                    ventaASumar = contadorVentasEmpleado[indice]
                    nuevaSumatoria = int(ventaASumar) + 1
                    contadorVentasEmpleado[indice] = nuevaSumatoria
                    
                    montoASumar = listaMontosPorEmpleados[indice]
                    nuevaSumatoriaMonto = float(montoASumar) + floatMontoVendido
                    listaMontosPorEmpleados[indice] = nuevaSumatoriaMonto
                else:
                    listaEmpleados.append(strIdEmpleado)
                    
                    contadorVentasEmpleado.append("1")
                    listaMontosPorEmpleados.append(floatMontoVendido)
            
            for montoVendido in listaMontosPorEmpleados:
                print(str(montoVendido))

            listaZipEmpleados = zip(listaEmpleados, contadorVentasEmpleado, listaMontosPorEmpleados)
            
            listaOrdenadaEmpleadosMayorAMenor = sorted(listaZipEmpleados, key = lambda t: t[-1], reverse=True)
            tuplesEmpleados = zip(*listaOrdenadaEmpleadosMayorAMenor)
            listaEmpleadosOrdenados, listaContadoresEmpleadosOrdenados, listaMontosEmpleadosOrdenados = [ list(tuple) for tuple in  tuplesEmpleados]
            
            for monto in listaMontosEmpleadosOrdenados:
                print("Monto:"+str(monto))
            
            infoEmpleado = []

            

            for empleado in listaEmpleadosOrdenados:
                
                contadorEmpleados = contadorEmpleados + 1
                contadorEmpleado.append(contadorEmpleados)
                idEmpleado = int(empleado)
                datosEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                
                for datoEmpleado in datosEmpleado:

                    nombresEm = datoEmpleado.nombres
                infoEmpleado.append(nombresEm)

            empleadosTops = zip (listaEmpleadosOrdenados,listaContadoresEmpleadosOrdenados,contadorEmpleado,infoEmpleado, listaMontosEmpleadosOrdenados)
            empleadosTopsModal =  zip (listaEmpleadosOrdenados,listaContadoresEmpleadosOrdenados,contadorEmpleado,infoEmpleado, listaMontosEmpleadosOrdenados)
        else:
            empleadosTops = None
            empleadosTopsModal = None
     
        








            









            
        
        
        
        
        
       
        
        #Mes anterior
        haceUnMes = hoy - relativedelta(months=1)  #2022-05-07
        mesHaceUnMes = haceUnMes.strftime('%m') #05
        añoHaceUnMes = haceUnMes.strftime('%Y')
        mesHaceUnMesLetra = mesesDic[str(mesHaceUnMes)]
        
        diasDeUltimoMes = diasMeses[str(mesHaceUnMesLetra)]
        
        fechaPrimerDiaMesAnterior = añoHaceUnMes + "-"+mesHaceUnMes+"-01"   #2022-05-01
        fechaUltimoDiaMesAnterior = añoHaceUnMes + "-"+mesHaceUnMes+"-"+diasDeUltimoMes  #2022-05-31


         #Ingresos totales de mes actual, ventas, creditos y rentas
        consultaVentasMesAnterior = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaMesAnterior,fechaUltimoDiaMesAnterior], credito="N")
        
        montoIngresoMesAnterior = 0
        
        if consultaVentasMesAnterior:
            for ventaRealizada in consultaVentasMesAnterior:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoMesAnterior = montoIngresoMesAnterior + montoVenta
        
        consultaCreditosMesAnterior = Creditos.objects.filter(fecha_venta_credito__range=[fechaPrimerDiaMesAnterior,fechaUltimoDiaMesAnterior],  renta_id__isnull=True)
        
        if consultaCreditosMesAnterior:
            for crceditoRealizado in consultaCreditosMesAnterior:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoMesAnterior = montoIngresoMesAnterior + montoPagadoCredito
            
        consultaRentasMesAnterior = Rentas.objects.filter(fecha_apartado__range=[fechaPrimerDiaMesAnterior,fechaUltimoDiaMesAnterior])
        
        if consultaRentasMesAnterior:
            for rentaRealizada in consultaRentasMesAnterior:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoMesAnterior = montoIngresoMesAnterior + sumaPagosRenta
        
        #comparativa de ingresos totales mensuales

        esMayor = False

        if montoIngresoMesAnterior == 0:
            porcentajeIngresosMes = 100
        else:
            porcentajeIngresosMes = (montoIngresoMesActual / montoIngresoMesAnterior)
            porcentajeIngresosMes = porcentajeIngresosMes - 1
            porcentajeIngresosMes = porcentajeIngresosMes *100
            
            
        if porcentajeIngresosMes > 0:
            esMayor = True
            
        else:
            esMayor = False
        porcentajeIngresosMes = round(porcentajeIngresosMes,2)
        
        
        #INGRESOS TOTALES SEMANAL
        fechaActual = datetime.today().strftime('%Y-%m-%d') #2022-06-07
        diaActual = datetime.today().isoweekday() #2 martes
        intdiaActual = int(diaActual)
        diaLunes = intdiaActual-1 #3 dias para el lunes
        diaDomingo = 7-intdiaActual # 2 dias para el sabado
        
    #Montos totales de semana actual
        fechaLunes = datetime.now()-timedelta(days =diaLunes)
        fechaDomingo = datetime.now() + timedelta(days =diaDomingo)
        
        #Ingresos totales de mes actual, ventas, creditos y rentas
        consultaVentasSemanaActual = Ventas.objects.filter(fecha_venta__range=[fechaLunes,fechaDomingo], credito="N")
        
        montoIngresoSemanaActual = 0
        
        if consultaVentasSemanaActual:
            for ventaRealizada in consultaVentasSemanaActual:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoSemanaActual = montoIngresoSemanaActual + montoVenta
        
        consultaCreditosSemanaActual = Creditos.objects.filter(fecha_venta_credito__range=[fechaLunes,fechaDomingo],  renta_id__isnull=True)
        
        if consultaCreditosSemanaActual:
            for crceditoRealizado in consultaCreditosSemanaActual:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoSemanaActual = montoIngresoSemanaActual + montoPagadoCredito
            
        consultaRentasSemanaActual = Rentas.objects.filter(fecha_apartado__range=[fechaLunes,fechaDomingo])
        
        if consultaRentasSemanaActual:
            for rentaRealizada in consultaRentasSemanaActual:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoSemanaActual = montoIngresoSemanaActual + sumaPagosRenta
                
        
    #Montos totales de semana anterior
        fechaLunesAnterior = fechaLunes-timedelta(days =7)
        fechaDomingoAnterior = fechaLunes - timedelta(days =1)
        
        #Ingresos totales de mes actual, ventas, creditos y rentas
        consultaVentasSemanaAnterior = Ventas.objects.filter(fecha_venta__range=[fechaLunesAnterior,fechaDomingoAnterior], credito="N")
        
        montoIngresoSemanaAnterior = 0
        
        if consultaVentasSemanaAnterior:
            for ventaRealizada in consultaVentasSemanaAnterior:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoSemanaAnterior = montoIngresoSemanaAnterior + montoVenta
        
        consultaCreditosSemanaAnterior = Creditos.objects.filter(fecha_venta_credito__range=[fechaLunesAnterior,fechaDomingoAnterior],  renta_id__isnull=True)
        
        if consultaCreditosSemanaAnterior:
            for crceditoRealizado in consultaCreditosSemanaAnterior:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoSemanaAnterior = montoIngresoSemanaAnterior + montoPagadoCredito
            
        consultaRentasSemanaAnterior = Rentas.objects.filter(fecha_apartado__range=[fechaLunesAnterior,fechaDomingoAnterior])
        
        if consultaRentasSemanaAnterior:
            for rentaRealizada in consultaRentasSemanaAnterior:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoSemanaAnterior = montoIngresoSemanaAnterior + sumaPagosRenta
        
        #comparativa de ingresos totales mensuales

        esMayorSemana = False

        if montoIngresoSemanaAnterior == 0:
            porcentajeIngresosSemana = 100
        else:
            porcentajeIngresosSemana = (montoIngresoSemanaActual / montoIngresoSemanaAnterior)
            porcentajeIngresosSemana = porcentajeIngresosSemana - 1
            porcentajeIngresosSemana = porcentajeIngresosSemana *100

        
        if porcentajeIngresosSemana > 0:
            esMayorSemana = True
        else:
            esMayorSemana = False
        porcentajeIngresosSemana = round(porcentajeIngresosSemana,2)

        
        
        
        #Fechas para chart de meses
        inicioMesEnero = añoHoy+"-01-01"
        finMesEnero = añoHoy+"-01-31"
        consultaVentasEnero = Ventas.objects.filter(fecha_venta__range=[inicioMesEnero,finMesEnero], credito="N")
        montoIngresoEnero = 0
        if consultaVentasEnero:
            for ventaRealizada in consultaVentasEnero:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoEnero = montoIngresoEnero + montoVenta
        consultaCreditosEnero = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesEnero,finMesEnero],  renta_id__isnull=True)
        if consultaCreditosEnero:
            for crceditoRealizado in consultaCreditosEnero:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoEnero = montoIngresoEnero + montoPagadoCredito
        consultaRentasEnero = Rentas.objects.filter(fecha_apartado__range=[inicioMesEnero,finMesEnero])
        if  consultaRentasEnero:
            for rentaRealizada in consultaRentasFebrero:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoEnero = montoIngresoEnero + sumaPagosRenta
        
        
        
        inicioMesFebrero = añoHoy+"-02-01"
        finMesFebrero = añoHoy+"-02-28"
        consultaVentasFebrero = Ventas.objects.filter(fecha_venta__range=[inicioMesFebrero,finMesFebrero], credito="N")
        montoIngresoFebrero = 0
        if consultaVentasFebrero:
            for ventaRealizada in consultaVentasFebrero:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoFebrero = montoIngresoFebrero + montoVenta
        consultaCreditosFebrero = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesFebrero,finMesFebrero],  renta_id__isnull=True)
        if consultaCreditosFebrero:
            for crceditoRealizado in consultaCreditosFebrero:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoFebrero = montoIngresoFebrero + montoPagadoCredito
        consultaRentasFebrero = Rentas.objects.filter(fecha_apartado__range=[inicioMesFebrero,finMesFebrero])
        if consultaRentasFebrero:
            for rentaRealizada in consultaRentasFebrero:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoFebrero = montoIngresoFebrero + sumaPagosRenta
        
        inicioMesMarzo = añoHoy+"-03-01"
        finMesMarzo = añoHoy+"-03-31"
        consultaVentasMarzo = Ventas.objects.filter(fecha_venta__range=[inicioMesMarzo,finMesMarzo], credito="N")
        montoIngresoMarzo = 0
        if consultaVentasMarzo:
            for ventaRealizada in consultaVentasMarzo:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoMarzo = montoIngresoMarzo + montoVenta
        consultaCreditosMarzo = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesMarzo,finMesMarzo],  renta_id__isnull=True)
        if consultaCreditosMarzo:
            for crceditoRealizado in consultaCreditosMarzo:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoMarzo = montoIngresoMarzo + montoPagadoCredito
        consultaRentasMarzo = Rentas.objects.filter(fecha_apartado__range=[inicioMesMarzo,finMesMarzo])
        if consultaRentasMarzo:
            for rentaRealizada in consultaRentasMarzo:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoMarzo = montoIngresoMarzo + sumaPagosRenta
        
        inicioMesAbril = añoHoy+"-04-01"
        finMesAbril = añoHoy+"-04-30"
        consultaVentasAbril = Ventas.objects.filter(fecha_venta__range=[inicioMesAbril,finMesAbril], credito="N")
        montoIngresoAbril = 0
        if consultaVentasAbril:
            for ventaRealizada in consultaVentasAbril:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoAbril = montoIngresoAbril + montoVenta
        consultaCreditosAbril = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesAbril,finMesAbril],  renta_id__isnull=True)
        if consultaCreditosAbril:
            for crceditoRealizado in consultaCreditosAbril:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoAbril = montoIngresoAbril + montoPagadoCredito
        consultaRentasAbril = Rentas.objects.filter(fecha_apartado__range=[inicioMesAbril,finMesAbril])
        if consultaRentasAbril:
            for rentaRealizada in consultaRentasAbril:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoAbril = montoIngresoAbril + sumaPagosRenta
        
        inicioMesMayo = añoHoy+"-05-01"
        finMesMayo = añoHoy+"-05-31"
        consultaVentasMayo = Ventas.objects.filter(fecha_venta__range=[inicioMesMayo,finMesMayo], credito="N")
        montoIngresoMayo = 0
        if consultaVentasMayo:
            for ventaRealizada in consultaVentasMayo:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoMayo = montoIngresoMayo + montoVenta
        consultaCreditosMayo = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesMayo,finMesMayo],  renta_id__isnull=True)
        if consultaCreditosMayo:
            for crceditoRealizado in consultaCreditosMayo:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoMayo = montoIngresoMayo + montoPagadoCredito
        consultaRentasMayo = Rentas.objects.filter(fecha_apartado__range=[inicioMesMayo,finMesMayo])
        if consultaRentasMayo:
            for rentaRealizada in consultaRentasMayo:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoMayo = montoIngresoMayo + sumaPagosRenta
        
        inicioMesJunio = añoHoy+"-06-01"
        finMesJunio = añoHoy+"-06-30"
        consultaVentasJunio = Ventas.objects.filter(fecha_venta__range=[inicioMesJunio,finMesJunio], credito="N")
        montoIngresoJunio = 0
        if consultaVentasJunio:
            for ventaRealizada in consultaVentasJunio:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoJunio = montoIngresoJunio + montoVenta
        consultaCreditosJunio = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesJunio,finMesJunio],  renta_id__isnull=True)
        if consultaCreditosJunio:
            for crceditoRealizado in consultaCreditosJunio:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoJunio = montoIngresoJunio + montoPagadoCredito
        consultaRentasJunio = Rentas.objects.filter(fecha_apartado__range=[inicioMesJunio,finMesJunio])
        if consultaRentasJunio:
            for rentaRealizada in consultaRentasJunio:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoJunio = montoIngresoJunio + sumaPagosRenta
        
        inicioMesJulio = añoHoy+"-07-01"
        finMesJulio = añoHoy+"-07-31"
        consultaVentasJulio = Ventas.objects.filter(fecha_venta__range=[inicioMesJulio,finMesJulio], credito="N")
        montoIngresoJulio = 0
        if consultaVentasJulio:
            for ventaRealizada in consultaVentasJulio:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoJulio = montoIngresoJulio + montoVenta
        consultaCreditosJulio = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesJulio,finMesJulio],  renta_id__isnull=True)
        if consultaCreditosJulio:
            for crceditoRealizado in consultaCreditosJulio:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoJulio = montoIngresoJulio + montoPagadoCredito
        consultaRentasJulio = Rentas.objects.filter(fecha_apartado__range=[inicioMesJulio,finMesJulio])
        if consultaRentasJulio:
            for rentaRealizada in consultaRentasJulio:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoJulio = montoIngresoJulio + sumaPagosRenta
        
        inicioMesAgosto = añoHoy+"-08-01"
        finMesAgosto = añoHoy+"-08-31"
        consultaVentasAgosto = Ventas.objects.filter(fecha_venta__range=[inicioMesAgosto,finMesAgosto], credito="N")
        montoIngresoAgosto = 0
        if consultaVentasAgosto:
            for ventaRealizada in consultaVentasAgosto:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoAgosto = montoIngresoAgosto + montoVenta
        consultaCreditosAgosto = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesAgosto,finMesAgosto],  renta_id__isnull=True)
        if consultaCreditosAgosto:
            for crceditoRealizado in consultaCreditosAgosto:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoAgosto = montoIngresoAgosto + montoPagadoCredito
        consultaRentasAgosto = Rentas.objects.filter(fecha_apartado__range=[inicioMesAgosto,finMesAgosto])
        if consultaRentasAgosto:
            for rentaRealizada in consultaRentasAgosto:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoAgosto = montoIngresoAgosto + sumaPagosRenta
        
        inicioMesSeptiembre = añoHoy+"-09-01"
        finMesSeptiembre = añoHoy+"-09-30"
        consultaVentasSeptiembre = Ventas.objects.filter(fecha_venta__range=[inicioMesSeptiembre,finMesSeptiembre], credito="N")
        montoIngresoSeptiembre = 0
        if consultaVentasSeptiembre:
            for ventaRealizada in consultaVentasSeptiembre:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoSeptiembre = montoIngresoSeptiembre + montoVenta
        consultaCreditosSeptiembre = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesSeptiembre,finMesSeptiembre],  renta_id__isnull=True)
        if consultaCreditosSeptiembre:
            for crceditoRealizado in consultaCreditosSeptiembre:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoSeptiembre = montoIngresoSeptiembre + montoPagadoCredito
        consultaRentasSeptiembre = Rentas.objects.filter(fecha_apartado__range=[inicioMesSeptiembre,finMesSeptiembre])
        if consultaRentasSeptiembre:
            for rentaRealizada in consultaRentasSeptiembre:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoSeptiembre = montoIngresoSeptiembre + sumaPagosRenta
        
        inicioMesOctubre = añoHoy+"-10-01"
        finMesOctubre = añoHoy+"-10-31"
        consultaVentasOctubre = Ventas.objects.filter(fecha_venta__range=[inicioMesOctubre,finMesOctubre], credito="N")
        montoIngresoOctubre = 0
        if consultaVentasOctubre:
            for ventaRealizada in consultaVentasOctubre:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoOctubre = montoIngresoOctubre + montoVenta
        consultaCreditosOctubre = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesOctubre,finMesOctubre],  renta_id__isnull=True)
        if consultaCreditosOctubre:
            for crceditoRealizado in consultaCreditosOctubre:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoOctubre = montoIngresoOctubre + montoPagadoCredito
        consultaRentasOctubre = Rentas.objects.filter(fecha_apartado__range=[inicioMesOctubre,finMesOctubre])
        if consultaRentasOctubre:
            for rentaRealizada in consultaRentasOctubre:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoOctubre = montoIngresoOctubre + sumaPagosRenta
        
        inicioMesNoviembre = añoHoy+"-11-01"
        finMesNoviembre = añoHoy+"-11-30"
        consultaVentasNoviembre = Ventas.objects.filter(fecha_venta__range=[inicioMesNoviembre,finMesNoviembre], credito="N")
        montoIngresoNoviembre = 0
        if consultaVentasNoviembre:
            for ventaRealizada in consultaVentasNoviembre:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoNoviembre = montoIngresoNoviembre + montoVenta
        consultaCreditosNoviembre = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesNoviembre,finMesNoviembre],  renta_id__isnull=True)
        if consultaCreditosNoviembre:
            for crceditoRealizado in consultaCreditosNoviembre:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoNoviembre = montoIngresoNoviembre + montoPagadoCredito
        consultaRentasNoviembre = Rentas.objects.filter(fecha_apartado__range=[inicioMesNoviembre,finMesNoviembre])
        if consultaRentasNoviembre:
            for rentaRealizada in consultaRentasNoviembre:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado 
                montoIngresoNoviembre = montoIngresoNoviembre + sumaPagosRenta
        
        inicioMesDiciembre = añoHoy+"-12-01"
        finMesDiciembre = añoHoy+"-12-31"
        consultaVentasDiciembre = Ventas.objects.filter(fecha_venta__range=[inicioMesDiciembre,finMesDiciembre], credito="N")
        montoIngresoDiciembre = 0
        if consultaVentasDiciembre:
            for ventaRealizada in consultaVentasDiciembre:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoDiciembre = montoIngresoDiciembre + montoVenta
        consultaCreditosDiciembre = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesDiciembre,finMesDiciembre],  renta_id__isnull=True)
        if consultaCreditosDiciembre:
            for crceditoRealizado in consultaCreditosDiciembre:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoDiciembre = montoIngresoDiciembre + montoPagadoCredito
        consultaRentasDiciembre = Rentas.objects.filter(fecha_apartado__range=[inicioMesDiciembre,finMesDiciembre])
        if consultaRentasDiciembre:
            for rentaRealizada in consultaRentasDiciembre:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoDiciembre = montoIngresoDiciembre + sumaPagosRenta
        
        
        
        
        # - COMPRAS DEL MEES ...................................................
        totalComprasMesGasto = 0
        totalComprasMesVenta = 0
        totalComprasMesRenta= 0
        numeroComprasGasto = 0
        numeroComprasVenta = 0
        numeroComprasRenta = 0
        
        comprasProductosGastos = []
        comprasGastoDelMes = ComprasGastos.objects.filter(fecha_compra__range=[fechaInicioMesActual,fechaDiaMesActual])
        if comprasGastoDelMes:
            for compra in comprasGastoDelMes:
                montoComprado = compra.total_costoCompra
                totalComprasMesGasto = totalComprasMesGasto + montoComprado
                numeroComprasGasto = numeroComprasGasto +1
                
                idCompra = compra.id_compraGasto
                idProducto = compra.id_productoComprado_id
                consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                
                for datoProducto in consultaProducto:
                    nombreProducto = datoProducto.nombre_producto
                    codigoProducto = datoProducto.codigo_producto
                    imagenProducto = datoProducto.imagen_producto
                    sucursalProducto = datoProducto.sucursal_id
                nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                
                fechaCompra = compra.fecha_compra
                costoUnitarioCompra = compra.costo_unitario
                cantidadComprada = compra.cantidad_comprada
                totalMontoCompra = compra.total_costoCompra
                
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
                
                
                
                comprasProductosGastos.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursal,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
        else:
            comprasProductosGastos = None
            
        
        comprasProductosVentas = []
        comprasVentaDelMes = ComprasVentas.objects.filter(fecha_compra__range=[fechaInicioMesActual,fechaDiaMesActual])
        if comprasVentaDelMes:
            for compra in comprasVentaDelMes:
                montoComprado = compra.total_costoCompra
                totalComprasMesVenta = totalComprasMesVenta + montoComprado
                numeroComprasVenta = numeroComprasVenta +1
                
                idCompra = compra.id_compraVenta
                idProducto = compra.id_productoComprado_id
                consultaProducto = ProductosVenta.objects.filter(id_producto = idProducto)
                
                for datoProducto in consultaProducto:
                    nombreProducto = datoProducto.nombre_producto
                    codigoProducto = datoProducto.codigo_producto
                    imagenProducto = datoProducto.imagen_producto
                    sucursalProducto = datoProducto.sucursal_id
                nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                
                fechaCompra = compra.fecha_compra
                costoUnitarioCompra = compra.costo_unitario
                cantidadComprada = compra.cantidad_comprada
                totalMontoCompra = compra.total_costoCompra
                
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
                
                
                comprasProductosVentas.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursal,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
        else:
            comprasProductosVentas = None
        
        
        comprasProductosRentas = []
        comprasRentasDelMes = ComprasRentas.objects.filter(fecha_compra__range=[fechaInicioMesActual,fechaDiaMesActual])
        if comprasRentasDelMes:
            for compra in comprasRentasDelMes:
                montoComprado = compra.total_costoCompra
                totalComprasMesRenta = totalComprasMesRenta + montoComprado
                numeroComprasRenta = numeroComprasRenta +1
                
                idCompra = compra.id_compraRenta
                idProducto = compra.id_productoComprado_id
                consultaProducto = ProductosRenta.objects.filter(id_producto = idProducto)
                
                for datoProducto in consultaProducto:
                    nombreProducto = datoProducto.nombre_producto
                    codigoProducto = datoProducto.codigo_producto
                    imagenProducto = datoProducto.imagen_producto
                    sucursalProducto = datoProducto.sucursal_id
                nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                
                fechaCompra = compra.fecha_compra
                costoUnitarioCompra = compra.costo_unitario
                cantidadComprada = compra.cantidad_comprada
                totalMontoCompra = compra.total_costoCompra
                
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
                
                
                comprasProductosRentas.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursal,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
        else:
            comprasProductosRentas = None            

        sumaTotalesCompras = totalComprasMesGasto + totalComprasMesVenta + totalComprasMesRenta
        
        
        
        
        #PRODUCTOS TOOOOOPP ------------------------------------------
      
        consultaVentasMesActual = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual])
        
       
        productosCantidades = []
        productosVenta =[]
        cantidadesProductosVenta =[]
        sinProductos = False
       
        
        for ventaMensual in consultaVentasMesActual:
            
            ids_productos = ventaMensual.ids_productos
            if ids_productos == "":
                sinProductos = True
            else:
                sinProductos = False
            
                productos = ids_productos.split(',')
                cantidades_productos = ventaMensual.cantidades_productos
                cantidades = cantidades_productos.split(',')

                productosCantidades = zip(productos, cantidades)
            
            if sinProductos == False:
                for idP,cant in productosCantidades:
                    productoVenta= str(idP)
                    cantidadProductoVenta = str(cant)
            
                
                    if "PV" in productoVenta:
                        productosVenta.append(productoVenta)   #['PV0001']
                        cantidadesProductosVenta.append(cantidadProductoVenta) #['1']
        
           
            
        if not productosVenta:
            listaFinalProductosMesTabla = None
            
        else:
                lProductos =zip(productosVenta,cantidadesProductosVenta)   #(['PV1000'],['1']) 
            
                
                
                listaFinalProductos = []
                listaFinalProductosSoloStrings = []
                for pr,ca in lProductos:
                    
                    stringProducto =str(pr)
                    stringCantidad =ca
                    
                    numero = productosVenta.count(stringProducto)
                    
                    if numero >1:
                        if stringProducto in listaFinalProductosSoloStrings:
                            elProductoYaFueAgregado = True
                        else:
                            contadorCantidadesDeProductos = 0
                            contadorProductos = 0
                            for producto in productosVenta:  #3
                                
                                contadorProductos = contadorProductos + 1
                                stringProducto2 = productosVenta[contadorProductos-1]
                                cantidadProducto2 = cantidadesProductosVenta[contadorProductos-1]

                                if stringProducto == stringProducto2:
                                    contadorCantidadesDeProductos = contadorCantidadesDeProductos + int(cantidadProducto2)

                            stringCantidad = str(contadorCantidadesDeProductos)
                            listaFinalProductosSoloStrings.append(stringProducto)
                            listaFinalProductos.append([stringProducto,stringCantidad])
                        #Borrar todos los elementos de las dos listas de strings y cantidades correspondientes a ese producto
                        
                    else:
                        listaFinalProductos.append([stringProducto,stringCantidad])

                    
                    listaProductosOrdenada = sorted(listaFinalProductos, key = lambda elemento:elemento[1])

                    listaProductosOrdenadaMayorAMenor = listaProductosOrdenada[::-1]


                    contadorParaTablaProductosMes = 0
                    arrayContadores = []
                    arrayInfoProducto = []
                    for producto in listaProductosOrdenadaMayorAMenor:
                        
                        contadorParaTablaProductosMes = contadorParaTablaProductosMes + 1
                        arrayContadores.append(contadorParaTablaProductosMes)

                        #info producto
                        codigoProducto = producto[0]
                        cantidadVendida = producto[1]
                        consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
                        for datoProducto in consultaProducto:
                            nombre = datoProducto.nombre_producto
                            costoVenta = datoProducto.costo_venta
                            imagen = datoProducto.imagen_producto
                        
                        costoTotalVendidoProducto = costoVenta * float(cantidadVendida)
                        arrayInfoProducto.append([nombre, costoVenta, costoTotalVendidoProducto, imagen])


                    listaFinalProductosMesTabla = zip(listaProductosOrdenadaMayorAMenor, arrayContadores, arrayInfoProducto)


        
        #SERVICIOS TOOOPP------------------------------------------------
        
        consultaVentasServiciosMesActual = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual])
        
       
        serviciosCantidades = []
        serviciosVenta =[]
        cantidadesServiciosVenta =[]
        sinServicioscorporales = False
        sinServiciosfaciales = False
       
        
        for ventaMensual in consultaVentasServiciosMesActual:
            
            ids_servicios_corporales = ventaMensual.ids_servicios_corporales #""
            if ids_servicios_corporales == "":
                sinServicioscorporales = True
            else:
                sinServicioscorporales = False
                serviciosCorporales = ids_servicios_corporales.split(',')
                cantidades_servicios_corporales = ventaMensual.cantidades_servicios_corporales
                cantidades_corporales = cantidades_servicios_corporales.split(',')

                serviciosCorporalesCantidades = zip(serviciosCorporales, cantidades_corporales)
            
            ids_servicios_faciales = ventaMensual.ids_servicios_faciales
            if ids_servicios_faciales == "":
                sinServiciosfaciales = True
            else:
                serviciosFaciales = ids_servicios_faciales.split(',')
                cantidades_servicios_faciales = ventaMensual.cantidades_servicios_faciales
                cantidades_faciales = cantidades_servicios_faciales.split(',')

                serviciosFacialesCantidades = zip(serviciosFaciales, cantidades_faciales)
                
            if sinServicioscorporales == False:
                for idServicioCorporal,cantCorporal in serviciosCorporalesCantidades:
                    servicioVenta= str(idServicioCorporal)
                    cantidadServicioVenta = str(cantCorporal)
            
            
            
                    serviciosVenta.append(servicioVenta)   #['PV0001']
                    cantidadesServiciosVenta.append(cantidadServicioVenta) #['1']
                
        
            if sinServiciosfaciales == False:
                for idServicioFacial,cantFacial in serviciosFacialesCantidades:
                    servicioVenta= str(idServicioFacial)
                    cantidadServicioVenta = str(cantFacial)
            
            
            
                    serviciosVenta.append(servicioVenta)   #['PV0001']
                    cantidadesServiciosVenta.append(cantidadServicioVenta) #['1'] for idServicioCorporal,cantCorporal in serviciosCorporalesCantidades:
                
        if not serviciosVenta:
            listaFinalServiciosMesTabla = None
        else:
            lServicios =zip(serviciosVenta,cantidadesServiciosVenta)   #(['PV1000'],['1']) 
        
            
            
            listaFinalServicios = []
            listaFinalServiciosSoloStrings = []
            for ser,can in lServicios:
                
                intIdServicio =ser
                stringCantidad =can
                
                numero = serviciosVenta.count(intIdServicio)
                
                if numero >1:
                    if intIdServicio in listaFinalServiciosSoloStrings:
                        elServicioYaFueAgregado = True
                    else:
                        contadorCantidadesDeServicios = 0
                        contadorServicios = 0
                        for servicio in serviciosVenta:  #3
                            
                            contadorServicios = contadorServicios + 1
                            idServicio2 = serviciosVenta[contadorServicios-1]
                            cantidadServicio2 = cantidadesServiciosVenta[contadorServicios-1]

                            if intIdServicio == idServicio2:
                                contadorCantidadesDeServicios = contadorCantidadesDeServicios + int(cantidadServicio2)

                        stringCantidad = str(contadorCantidadesDeServicios)
                        listaFinalServiciosSoloStrings.append(intIdServicio)
                        listaFinalServicios.append([intIdServicio,stringCantidad])
                    #Borrar todos los elementos de las dos listas de strings y cantidades correspondientes a ese producto
                    
                else:
                    listaFinalServicios.append([intIdServicio,stringCantidad])

                
                listaServiciosOrdenada = sorted(listaFinalServicios, key = lambda elemento:elemento[1])

                listaServiciosOrdenadaMayorAMenor = listaServiciosOrdenada[::-1]


                contadorParaTablaServiciosMes = 0
                arrayContadores = []
                arrayInfoServicio = []
                for servicio in listaServiciosOrdenadaMayorAMenor:
                    
                    contadorParaTablaServiciosMes = contadorParaTablaServiciosMes + 1
                    arrayContadores.append(contadorParaTablaServiciosMes)

                    #info producto
                    codigoServicio= servicio[0]
                    cantidadVendida = servicio[1]
                    consultaServicio = Servicios.objects.filter(id_servicio = codigoServicio)
                    for datoServicios in consultaServicio:
                        tipo = datoServicios.tipo_servicio
                        nombreServicio = datoServicios.nombre_servicio
                        costoVenta = datoServicios.precio_venta
                    
                    
                    costoTotalVendidoServicio = costoVenta * float(cantidadVendida)
                    arrayInfoServicio.append([tipo, nombreServicio, costoVenta,costoTotalVendidoServicio])


                listaFinalServiciosMesTabla = zip(listaServiciosOrdenadaMayorAMenor, arrayContadores, arrayInfoServicio)



        
        
        #PRODUCTOS RENTA TOPPP------------------------------------------

        consultaVentasRentasMesActual = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual])
        
       
        productosRentaCantidades = []
        productosRentaVenta =[]
        cantidadesProductosRentaVenta =[]
        sinProductosRenta = False
       
        
        for ventaMensual in consultaVentasRentasMesActual:
            
            ids_productos = ventaMensual.ids_productos
            if ids_productos == "":
                sinProductosRenta = True
            else: 
                sinProductosRenta = False
                productos = ids_productos.split(',')
                cantidades_productos = ventaMensual.cantidades_productos
                cantidades = cantidades_productos.split(',')

                productosCantidades = zip(productos, cantidades)
                
            if sinProductosRenta == False:
                for idP,cant in productosCantidades:
                    productoVenta= str(idP)
                    cantidadProductoVenta = str(cant)
            
                
                    if "PR" in productoVenta:
                        productosRentaVenta.append(productoVenta)   #['PV0001']
                        cantidadesProductosRentaVenta.append(cantidadProductoVenta) #['1']
            
        if not productosRentaVenta:
            listaFinalProductosRentaMesTabla = None
        else:

            lProductosRenta =zip(productosRentaVenta,cantidadesProductosRentaVenta)   #(['PV1000'],['1']) 
        
            
            
            listaFinalProductosRenta = []
            listaFinalProductosSoloStringsRenta = []
            for prren,caren in lProductosRenta:
                
                stringProducto =str(prren)
                stringCantidad =caren
                
                numero = productosRentaVenta.count(stringProducto)
                
                if numero >1:
                    if stringProducto in listaFinalProductosSoloStringsRenta:
                        elProductoYaFueAgregado = True
                    else:
                        contadorCantidadesDeProductosRenta = 0
                        contadorProductosRenta = 0
                        for producto in productosRentaVenta:  #3
                            
                            contadorProductosRenta = contadorProductosRenta + 1
                            stringProductorenta2 = productosRentaVenta[contadorProductosRenta-1]
                            cantidadProductorenta2 = cantidadesProductosRentaVenta[contadorProductosRenta-1]

                            if stringProducto == stringProductorenta2:
                                contadorCantidadesDeProductosRenta = contadorCantidadesDeProductosRenta + int(cantidadProductorenta2)

                        stringCantidad = str(contadorCantidadesDeProductosRenta)
                        listaFinalProductosSoloStringsRenta.append(stringProducto)
                        listaFinalProductosRenta.append([stringProducto,stringCantidad])
                    #Borrar todos los elementos de las dos listas de strings y cantidades correspondientes a ese producto
                    
                else:
                    listaFinalProductosRenta.append([stringProducto,stringCantidad])

                
                listaProductosRentaOrdenada = sorted(listaFinalProductosRenta, key = lambda elemento:elemento[1])

                listaProductosRentaOrdenadaMayorAMenor = listaProductosRentaOrdenada[::-1]


                contadorParaTablaProductosRentaMes = 0
                arrayContadores = []
                arrayInfoProductoRenta = []
                for productoRenta in listaProductosRentaOrdenadaMayorAMenor:
                    
                    contadorParaTablaProductosRentaMes = contadorParaTablaProductosRentaMes + 1
                    arrayContadores.append(contadorParaTablaProductosRentaMes)

                    #info producto
                    codigoProductoRenta = productoRenta[0]
                    cantidadVendidaRenta = productoRenta[1]
                    consultaProductoRenta = ProductosRenta.objects.filter(codigo_producto = codigoProductoRenta)
                    for datoProducto in consultaProductoRenta:
                        nombreRenta = datoProducto.nombre_producto
                        costoRenta = datoProducto.costo_renta
                        imagenRenta = datoProducto.imagen_producto
                    
                    costoTotalRentadoProducto = costoRenta * float(cantidadVendidaRenta)
                    arrayInfoProductoRenta.append([nombreRenta, costoRenta, costoTotalRentadoProducto, imagenRenta])


                listaFinalProductosRentaMesTabla = zip(listaProductosRentaOrdenadaMayorAMenor, arrayContadores, arrayInfoProductoRenta)
       
       

        return render(request, "17 Informe Ventas/informeDeVentas.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "notificacionRenta":notificacionRenta, "diadehoy":diadehoy,"mesdehoy":mesdehoy,"añoHoy":añoHoy,
                                                                          "mesHaceUnMesLetra":mesHaceUnMesLetra, "diasDeUltimoMes":diasDeUltimoMes, "montoIngresoMesActual":montoIngresoMesActual,"montoIngresoMesAnterior":montoIngresoMesAnterior,"porcentajeIngresosMes":porcentajeIngresosMes,"esMayor":esMayor,
                                                                          "montoIngresoSemanaActual":montoIngresoSemanaActual,"montoIngresoSemanaAnterior":montoIngresoSemanaAnterior, "esMayorSemana":esMayorSemana,"porcentajeIngresosSemana":porcentajeIngresosSemana,
                                                                          "montoIngresoEnero":montoIngresoEnero, "montoIngresoFebrero":montoIngresoFebrero, "montoIngresoMarzo":montoIngresoMarzo, "montoIngresoAbril":montoIngresoAbril, "montoIngresoMayo":montoIngresoMayo, "montoIngresoJunio":montoIngresoJunio, "montoIngresoJulio":montoIngresoJulio, "montoIngresoAgosto":montoIngresoAgosto, "montoIngresoSeptiembre":montoIngresoSeptiembre, "montoIngresoOctubre":montoIngresoOctubre, "montoIngresoNoviembre":montoIngresoNoviembre, "montoIngresoDiciembre":montoIngresoDiciembre,
                                                                          "totalComprasMesGasto":totalComprasMesGasto,"totalComprasMesVenta":totalComprasMesVenta,"totalComprasMesRenta":totalComprasMesRenta,"contadorVentasmesActual":contadorVentasmesActual,"contadorRentasmesActual":contadorRentasmesActual,"contadorCreditosmesActual":contadorCreditosmesActual,"numeroVentas":numeroVentas,"numeroRentas":numeroRentas,"numeroCreditos":numeroCreditos,
                                                                          "numeroComprasGasto":numeroComprasGasto,"numeroComprasVenta":numeroComprasVenta,"numeroComprasRenta":numeroComprasRenta,"sumaTotalesCompras":sumaTotalesCompras,"totalEfectivo":totalEfectivo,"totalTarjeta":totalTarjeta,"totalTransferencia":totalTransferencia,"clientesTops":clientesTops,
                                                                          "clientesTop":clientesTop,"montosTop":montosTop,"contadorClientesArray":contadorClientesArray,"listaFinalProductosMesTabla":listaFinalProductosMesTabla,
                                                                          "listaFinalServiciosMesTabla":listaFinalServiciosMesTabla, "listaFinalProductosRentaMesTabla":listaFinalProductosRentaMesTabla, "empleadosTops":empleadosTops,
                                                                          "clientesTopsModal":clientesTopsModal, "empleadosTopsModal":empleadosTopsModal,
                                                                          "comprasProductosGastos":comprasProductosGastos, "comprasProductosVentas":comprasProductosVentas, "comprasProductosRentas":comprasProductosRentas, "notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")

def informeDeVentasAnual(request):

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

        hoy = datetime.now()
        
        #Mes actual
        añoHoy = hoy.strftime('%Y')
        añoAnterior = int(añoHoy)-1
        strAñoAnterior = str(añoAnterior)
        
        fechaPrimerDiaDelAño = añoHoy+"-01-01" #Primer dia del presente año
        fechaUltimoDiaDelAño = añoHoy+"-12-31" #Ultimo dia del presente año
        
        #Año anterior
        añoAnterior = int(añoHoy)-1
        
        fechaPrimerDiaMesAnterior = str(añoAnterior) + "-01-01"   #2022-05-01
        fechaUltimoDiaMesAnterior = str(añoAnterior) + "-12-31"
        
        haceDosAños = int(añoHoy)-2
        strHaceDosAños = str(haceDosAños)
        
        fechaPrimerDiaHaceDosAños = str(haceDosAños) + "-01-01"   #2022-05-01
        fechaUltimoDiaHaceDosAños = str(haceDosAños) + "-12-31"
        
        haceTresAños = int(añoHoy)-3
        strHaceTresAños = str(haceTresAños)
        
        fechaPrimerDiaHaceTresAños = str(haceTresAños) + "-01-01"   #2022-05-01
        fechaUltimoDiaHaceTresAños = str(haceTresAños) + "-12-31"
        
        
        #Ingresos totales de mes actual, ventas, creditos y rentas
        consultaVentasAñoActual = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño], credito="N")
        
        montoIngresoAñoActual = 0
        
        contadorVentasAñoActual = 0
        numeroVentas =0
        
        contadorRentasAñoActual =0
        numeroRentas =0
        
        contadorCreditosAñoActual =0
        numeroCreditos = 0
        
        if consultaVentasAñoActual:
            for ventaRealizada in consultaVentasAñoActual:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoAñoActual = montoIngresoAñoActual + montoVenta
                contadorVentasAñoActual = contadorVentasAñoActual + montoVenta
                numeroVentas = numeroVentas +1
        
        consultaCreditosAñoActual = Creditos.objects.filter(fecha_venta_credito__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño], renta_id__isnull=True)
        
        if consultaCreditosAñoActual:
            for crceditoRealizado in consultaCreditosAñoActual:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoAñoActual = montoIngresoAñoActual + montoPagadoCredito
                contadorCreditosAñoActual = contadorCreditosAñoActual + montoPagadoCredito
                numeroCreditos = numeroCreditos +1
            
        consultaRentasAñoActual = Rentas.objects.filter(fecha_apartado__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño])
        
        if consultaRentasAñoActual:
            for rentaRealizada in consultaRentasAñoActual:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoAñoActual = montoIngresoAñoActual + sumaPagosRenta

                contadorRentasAñoActual = contadorRentasAñoActual + sumaPagosRenta
                numeroRentas = numeroRentas +1

        
        #totales efectivo, tarjeta, transferencia

        #EFECTIVO
        consultaVentasAnualEfectivo = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño],tipo_pago="Efectivo",credito="N")
        totalEfectivo =0
        for efectivo in consultaVentasAnualEfectivo:
            monto_efectivo = efectivo.monto_pagar
            totalEfectivo = totalEfectivo + monto_efectivo
            
        #TARJETA
        consultaVentasAnualTarjeta = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño],tipo_pago="Tarjeta",credito="N")
        totalTarjeta =0
        for tarjeta in consultaVentasAnualTarjeta:
            montoTarjeta = tarjeta.monto_pagar
            totalTarjeta = totalTarjeta + montoTarjeta
        
        #TRANSFERENCIA 
        consultaVentasAnualTransferencia = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño],tipo_pago="Transferencia",credito="N")
        totalTransferencia =0
        for transferencia in consultaVentasAnualTransferencia:
            montoTransferencia = transferencia.monto_pagar
            totalTransferencia = totalTransferencia + montoTransferencia
        
        #PAGOS DE LOS CREDITOS
        creditosEfectivo = Creditos.objects.filter(fecha_venta_credito__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño])
        for credito in creditosEfectivo:
            idCredito = credito.id_credito
        
            pagosCredito = PagosCreditos.objects.filter(id_credito_id__id_credito=idCredito)
            for pago in pagosCredito:
                tipoPago1 = pago.tipo_pago1
                tipoPago2 = pago.tipo_pago2
                tipoPago3 = pago.tipo_pago3
                tipoPago4 = pago.tipo_pago4

                if tipoPago1:
                    montoPagado1 = pago.monto_pago1
                    if tipoPago1 == "Efectivo":
                        totalEfectivo = totalEfectivo + montoPagado1
                    elif tipoPago1 == "Tarjeta":
                        totalTarjeta = totalTarjeta + montoPagado1
                    elif tipoPago1 == "Transferencia":
                        totalTransferencia = totalTransferencia + montoPagado1
                
                elif tipoPago2:
                    montoPagado2 = pago.monto_pago2
                    if tipoPago2 == "Efectivo":
                        totalEfectivo = totalEfectivo + montoPagado2
                    elif tipoPago2 == "Tarjeta":
                        totalTarjeta = totalTarjeta + montoPagado2
                    elif tipoPago2 == "Transferencia":
                        totalTransferencia = totalTransferencia + montoPagado2
                
                elif tipoPago3:
                    montoPagado3 =pago.monto_pago3
                    if tipoPago3 == "Efectivo":
                        totalEfectivo = totalEfectivo + montoPagado3
                    elif tipoPago3 == "Tarjeta":
                        totalTarjeta = totalTarjeta + montoPagado3
                    elif tipoPago3 == "Transferencia":
                        totalTransferencia = totalTransferencia + montoPagado3
                        
                elif tipoPago4:
                    montoPagado4 = pago.monto_pago4
                    if tipoPago4 == "Efectivo":
                        totalEfectivo = totalEfectivo + montoPagado4
                    elif tipoPago4 == "Tarjeta":
                        totalTarjeta = totalTarjeta + montoPagado4
                    elif tipoPago4 == "Transferencia":
                        totalTransferencia = totalTransferencia + montoPagado4
        
        
        
        #TOP CLIENTES CON MAS COMPRAS

        consultaVentasAnualClientes = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño], cliente__isnull=False)

        clientesTop = []
        montosTop = []
        clientesMontosTotales = []
        clientesIds = []
        contadorClientesArray = []
        if consultaVentasAnualClientes:
            for clienteVentas in consultaVentasAnualClientes:
                cliente_ventas = clienteVentas.cliente_id
                monto_total_cliente = clienteVentas.monto_pagar
                clientesMontosTotales.append(monto_total_cliente) #180,600
                clientesIds.append(cliente_ventas) #1,1
                
            listaClientesCompradores = zip(clientesIds, clientesMontosTotales)
            
            listaClientes = []
            montoPorCliente = []
            contadorClientesArray = []
            
            
            for idcliente, montoTotalCliente in listaClientesCompradores:
                
                strIdCliente = str(idcliente)
                intMonto = float(montoTotalCliente)
                
                if strIdCliente in listaClientes:
                    indice = listaClientes.index(strIdCliente)
                    montoASumar = montoPorCliente[indice]
                    nuevaSumatoria = float(montoASumar) + intMonto
                    montoPorCliente[indice] = str(nuevaSumatoria)
                else:
                    listaClientes.append(strIdCliente)
                    montoPorCliente.append(str(intMonto))
            
            listaZipClientes = zip(listaClientes, montoPorCliente)
            
            listaOrdenadaMayorAMenor = sorted(listaZipClientes, key = lambda t: t[-1], reverse=True)
            tuples = zip(*listaOrdenadaMayorAMenor)
            listaClientesOrdenados, listaMontosOrdenados = [ list(tuple) for tuple in  tuples]
           
                    
            infoCliente = []

            
            cotadorClientes = 0
            for cliente in listaClientesOrdenados:
                cotadorClientes = cotadorClientes + 1
                contadorClientesArray.append(cotadorClientes)
                id_cliente_top = cliente
                clienteDatos = Clientes.objects.filter(id_cliente= id_cliente_top)
                for c in clienteDatos:

                    nombre_cliente_top = c.nombre_cliente
                    apellido =  c.apellidoPaterno_cliente
                    apellido2 = c.apellidoMaterno_cliente
                infoCliente.append([nombre_cliente_top,apellido,apellido2])

            clientesTops = zip (listaClientesOrdenados,listaMontosOrdenados,contadorClientesArray,infoCliente)
            clientesTopsModal =zip (listaClientesOrdenados,listaMontosOrdenados,contadorClientesArray,infoCliente) 
        else:
            clientesTops = None
            clientesTopsModal = None
            listaZipClientes = None
        
        #TOP EMPLEADOS CON MÁS VENTAS

        consultaTodasLasVentasDelAño = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño])

        idsEmpleados = []
        montosTotalesDeVentaEmpleados = []
        if consultaTodasLasVentasDelAño:
            for venta in consultaTodasLasVentasDelAño:
                idEmpleado = venta.empleado_vendedor_id
                idsEmpleados.append(idEmpleado) #1,1
                montoVendido = venta.monto_pagar
                montosTotalesDeVentaEmpleados.append(montoVendido)
                
            
            listaEmpleados = []
            contadorVentasEmpleado = []
            contadorEmpleado = []
            listaMontosPorEmpleados = []
            
            listaEmpleadosVentas = zip(idsEmpleados, montosTotalesDeVentaEmpleados)
            
            contadorEmpleados = 0
            for idEmpleado, montoVentita in listaEmpleadosVentas:
                
                strIdEmpleado = str(idEmpleado)
                floatMontoVendido = float(montoVentita)
                
                if strIdEmpleado in listaEmpleados:
                    indice = listaEmpleados.index(strIdEmpleado)
                    ventaASumar = contadorVentasEmpleado[indice]
                    nuevaSumatoria = int(ventaASumar) + 1
                    contadorVentasEmpleado[indice] = nuevaSumatoria
                    
                    montoASumar = listaMontosPorEmpleados[indice]
                    nuevaSumatoriaMonto = float(montoASumar) + floatMontoVendido
                    listaMontosPorEmpleados[indice] = nuevaSumatoriaMonto
                else:
                    listaEmpleados.append(strIdEmpleado)
                    
                    contadorVentasEmpleado.append("1")
                    listaMontosPorEmpleados.append(floatMontoVendido)
            
            for montoVendido in listaMontosPorEmpleados:
                print(str(montoVendido))

            listaZipEmpleados = zip(listaEmpleados, contadorVentasEmpleado, listaMontosPorEmpleados)
            
            listaOrdenadaEmpleadosMayorAMenor = sorted(listaZipEmpleados, key = lambda t: t[-1], reverse=True)
            tuplesEmpleados = zip(*listaOrdenadaEmpleadosMayorAMenor)
            listaEmpleadosOrdenados, listaContadoresEmpleadosOrdenados, listaMontosEmpleadosOrdenados = [ list(tuple) for tuple in  tuplesEmpleados]
            
            for monto in listaMontosEmpleadosOrdenados:
                print("Monto:"+str(monto))
            
            infoEmpleado = []

            

            for empleado in listaEmpleadosOrdenados:
                
                contadorEmpleados = contadorEmpleados + 1
                contadorEmpleado.append(contadorEmpleados)
                idEmpleado = int(empleado)
                datosEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                
                for datoEmpleado in datosEmpleado:

                    nombresEm = datoEmpleado.nombres
                infoEmpleado.append(nombresEm)

            empleadosTops = zip (listaEmpleadosOrdenados,listaContadoresEmpleadosOrdenados,contadorEmpleado,infoEmpleado, listaMontosEmpleadosOrdenados)
            empleadosTopsModal =  zip (listaEmpleadosOrdenados,listaContadoresEmpleadosOrdenados,contadorEmpleado,infoEmpleado, listaMontosEmpleadosOrdenados)
        else:
            empleadosTops = None
            empleadosTopsModal = None
     
        
        


        #Ingresos totales año anterior
        consultaVentasMesAnterior = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaMesAnterior,fechaUltimoDiaMesAnterior], credito="N")
        
        montoIngresoAñoAnterior = 0
        
        if consultaVentasMesAnterior:
            for ventaRealizada in consultaVentasMesAnterior:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoAñoAnterior = montoIngresoAñoAnterior + montoVenta
        
        consultaCreditosMesAnterior = Creditos.objects.filter(fecha_venta_credito__range=[fechaPrimerDiaMesAnterior,fechaUltimoDiaMesAnterior],  renta_id__isnull=True)
        
        if consultaCreditosMesAnterior:
            for crceditoRealizado in consultaCreditosMesAnterior:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoAñoAnterior = montoIngresoAñoAnterior + montoPagadoCredito
            
        consultaRentasMesAnterior = Rentas.objects.filter(fecha_apartado__range=[fechaPrimerDiaMesAnterior,fechaUltimoDiaMesAnterior])
        
        if consultaRentasMesAnterior:
            for rentaRealizada in consultaRentasMesAnterior:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoAñoAnterior = montoIngresoAñoAnterior + sumaPagosRenta
                
        #Ingresos totales haceDosAños
        consultaVentasHaceDosAños = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaHaceDosAños,fechaUltimoDiaHaceDosAños], credito="N")
        
        montoIngresoHaceDosAños = 0
        
        if consultaVentasHaceDosAños:
            for ventaRealizada in consultaVentasHaceDosAños:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoHaceDosAños = montoIngresoHaceDosAños + montoVenta
        
        consultaCreditosHaceDosAños = Creditos.objects.filter(fecha_venta_credito__range=[fechaPrimerDiaHaceDosAños,fechaUltimoDiaHaceDosAños],  renta_id__isnull=True)
        
        if consultaCreditosHaceDosAños:
            for crceditoRealizado in consultaCreditosHaceDosAños:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoHaceDosAños = montoIngresoHaceDosAños + montoPagadoCredito
            
        consultaRentasHaceDosAños = Rentas.objects.filter(fecha_apartado__range=[fechaPrimerDiaHaceDosAños,fechaUltimoDiaHaceDosAños])
        
        if consultaRentasHaceDosAños:
            for rentaRealizada in consultaRentasHaceDosAños:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoHaceDosAños = montoIngresoHaceDosAños + sumaPagosRenta
                
                
        #Ingresos totales año anterior
        consultaVentasHaceTresAños = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaHaceTresAños,fechaUltimoDiaHaceTresAños], credito="N")
        
        montoIngresoHaceTresAños = 0
        
        if consultaVentasHaceTresAños:
            for ventaRealizada in consultaVentasHaceTresAños:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoHaceTresAños = montoIngresoHaceTresAños + montoVenta
        
        consultaCreditosHaceTresAños = Creditos.objects.filter(fecha_venta_credito__range=[fechaPrimerDiaHaceTresAños,fechaUltimoDiaHaceTresAños],  renta_id__isnull=True)
        
        if consultaCreditosHaceTresAños:
            for crceditoRealizado in consultaCreditosHaceTresAños:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoHaceTresAños = montoIngresoHaceTresAños + montoPagadoCredito
            
        consultaRentasHaceTresAños= Rentas.objects.filter(fecha_apartado__range=[fechaPrimerDiaHaceTresAños,fechaUltimoDiaHaceTresAños])
        
        if consultaRentasHaceTresAños:
            for rentaRealizada in consultaRentasHaceTresAños:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoHaceTresAños = montoIngresoHaceTresAños + sumaPagosRenta
        
        #comparativa de ingresos totales mensuales

        esMayor = False

        if montoIngresoAñoAnterior == 0:
            porcentajeIngresosAño = 100
        else:
            porcentajeIngresosAño = (montoIngresoAñoActual / montoIngresoAñoAnterior)
            porcentajeIngresosAño = porcentajeIngresosAño - 1
            porcentajeIngresosAño = porcentajeIngresosAño *100
            
            
        if porcentajeIngresosAño > 0:
            esMayor = True
            
        else:
            esMayor = False
        porcentajeIngresosAño = round(porcentajeIngresosAño,2)
        
        
        #INGRESOS TOTALES SEMANAL
        fechaActual = datetime.today().strftime('%Y-%m-%d') #2022-06-07
        diaActual = datetime.today().isoweekday() #2 martes
        intdiaActual = int(diaActual)
        diaLunes = intdiaActual-1 #3 dias para el lunes
        diaDomingo = 7-intdiaActual # 2 dias para el sabado
        
    #Montos totales de semana actual
        fechaLunes = datetime.now()-timedelta(days =diaLunes)
        fechaDomingo = datetime.now() + timedelta(days =diaDomingo)
        
        #Ingresos totales de mes actual, ventas, creditos y rentas
        consultaVentasSemanaActual = Ventas.objects.filter(fecha_venta__range=[fechaLunes,fechaDomingo], credito="N")
        
        montoIngresoSemanaActual = 0
        
        if consultaVentasSemanaActual:
            for ventaRealizada in consultaVentasSemanaActual:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoSemanaActual = montoIngresoSemanaActual + montoVenta
        
        consultaCreditosSemanaActual = Creditos.objects.filter(fecha_venta_credito__range=[fechaLunes,fechaDomingo],  renta_id__isnull=True)
        
        if consultaCreditosSemanaActual:
            for crceditoRealizado in consultaCreditosSemanaActual:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoSemanaActual = montoIngresoSemanaActual + montoPagadoCredito
            
        consultaRentasSemanaActual = Rentas.objects.filter(fecha_apartado__range=[fechaLunes,fechaDomingo])
        
        if consultaRentasSemanaActual:
            for rentaRealizada in consultaRentasSemanaActual:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoSemanaActual = montoIngresoSemanaActual + sumaPagosRenta
                
        
    #Montos totales de semana anterior
        fechaLunesAnterior = fechaLunes-timedelta(days =7)
        fechaDomingoAnterior = fechaLunes - timedelta(days =1)
        
        #Ingresos totales de mes actual, ventas, creditos y rentas
        consultaVentasSemanaAnterior = Ventas.objects.filter(fecha_venta__range=[fechaLunesAnterior,fechaDomingoAnterior], credito="N")
        
        montoIngresoSemanaAnterior = 0
        
        if consultaVentasSemanaAnterior:
            for ventaRealizada in consultaVentasSemanaAnterior:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoSemanaAnterior = montoIngresoSemanaAnterior + montoVenta
        
        consultaCreditosSemanaAnterior = Creditos.objects.filter(fecha_venta_credito__range=[fechaLunesAnterior,fechaDomingoAnterior],  renta_id__isnull=True)
        
        if consultaCreditosSemanaAnterior:
            for crceditoRealizado in consultaCreditosSemanaAnterior:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoSemanaAnterior = montoIngresoSemanaAnterior + montoPagadoCredito
            
        consultaRentasSemanaAnterior = Rentas.objects.filter(fecha_apartado__range=[fechaLunesAnterior,fechaDomingoAnterior])
        
        if consultaRentasSemanaAnterior:
            for rentaRealizada in consultaRentasSemanaAnterior:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoSemanaAnterior = montoIngresoSemanaAnterior + sumaPagosRenta
        
        #comparativa de ingresos totales mensuales

        esMayorSemana = False

        if montoIngresoSemanaAnterior == 0:
            porcentajeIngresosSemana = 100
        else:
            porcentajeIngresosSemana = (montoIngresoSemanaActual / montoIngresoSemanaAnterior)
            porcentajeIngresosSemana = porcentajeIngresosSemana - 1
            porcentajeIngresosSemana = porcentajeIngresosSemana *100

        
        if porcentajeIngresosSemana > 0:
            esMayorSemana = True
        else:
            esMayorSemana = False
        porcentajeIngresosSemana = round(porcentajeIngresosSemana,2)

        
        
        
        #Fechas para chart de meses
        inicioMesEnero = añoHoy+"-01-01"
        finMesEnero = añoHoy+"-01-31"
        consultaVentasEnero = Ventas.objects.filter(fecha_venta__range=[inicioMesEnero,finMesEnero], credito="N")
        montoIngresoEnero = 0
        if consultaVentasEnero:
            for ventaRealizada in consultaVentasEnero:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoEnero = montoIngresoEnero + montoVenta
        consultaCreditosEnero = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesEnero,finMesEnero],  renta_id__isnull=True)
        if consultaCreditosEnero:
            for crceditoRealizado in consultaCreditosEnero:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoEnero = montoIngresoEnero + montoPagadoCredito
        consultaRentasEnero = Rentas.objects.filter(fecha_apartado__range=[inicioMesEnero,finMesEnero])
        if  consultaRentasEnero:
            for rentaRealizada in consultaRentasFebrero:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoEnero = montoIngresoEnero + sumaPagosRenta
        
        
        
        inicioMesFebrero = añoHoy+"-02-01"
        finMesFebrero = añoHoy+"-02-28"
        consultaVentasFebrero = Ventas.objects.filter(fecha_venta__range=[inicioMesFebrero,finMesFebrero], credito="N")
        montoIngresoFebrero = 0
        if consultaVentasFebrero:
            for ventaRealizada in consultaVentasFebrero:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoFebrero = montoIngresoFebrero + montoVenta
        consultaCreditosFebrero = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesFebrero,finMesFebrero],  renta_id__isnull=True)
        if consultaCreditosFebrero:
            for crceditoRealizado in consultaCreditosFebrero:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoFebrero = montoIngresoFebrero + montoPagadoCredito
        consultaRentasFebrero = Rentas.objects.filter(fecha_apartado__range=[inicioMesFebrero,finMesFebrero])
        if consultaRentasFebrero:
            for rentaRealizada in consultaRentasFebrero:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoFebrero = montoIngresoFebrero + sumaPagosRenta
        
        inicioMesMarzo = añoHoy+"-03-01"
        finMesMarzo = añoHoy+"-03-31"
        consultaVentasMarzo = Ventas.objects.filter(fecha_venta__range=[inicioMesMarzo,finMesMarzo], credito="N")
        montoIngresoMarzo = 0
        if consultaVentasMarzo:
            for ventaRealizada in consultaVentasMarzo:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoMarzo = montoIngresoMarzo + montoVenta
        consultaCreditosMarzo = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesMarzo,finMesMarzo],  renta_id__isnull=True)
        if consultaCreditosMarzo:
            for crceditoRealizado in consultaCreditosMarzo:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoMarzo = montoIngresoMarzo + montoPagadoCredito
        consultaRentasMarzo = Rentas.objects.filter(fecha_apartado__range=[inicioMesMarzo,finMesMarzo])
        if consultaRentasMarzo:
            for rentaRealizada in consultaRentasMarzo:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoMarzo = montoIngresoMarzo + sumaPagosRenta
        
        inicioMesAbril = añoHoy+"-04-01"
        finMesAbril = añoHoy+"-04-30"
        consultaVentasAbril = Ventas.objects.filter(fecha_venta__range=[inicioMesAbril,finMesAbril], credito="N")
        montoIngresoAbril = 0
        if consultaVentasAbril:
            for ventaRealizada in consultaVentasAbril:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoAbril = montoIngresoAbril + montoVenta
        consultaCreditosAbril = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesAbril,finMesAbril],  renta_id__isnull=True)
        if consultaCreditosAbril:
            for crceditoRealizado in consultaCreditosAbril:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoAbril = montoIngresoAbril + montoPagadoCredito
        consultaRentasAbril = Rentas.objects.filter(fecha_apartado__range=[inicioMesAbril,finMesAbril])
        if consultaRentasAbril:
            for rentaRealizada in consultaRentasAbril:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoAbril = montoIngresoAbril + sumaPagosRenta
        
        inicioMesMayo = añoHoy+"-05-01"
        finMesMayo = añoHoy+"-05-31"
        consultaVentasMayo = Ventas.objects.filter(fecha_venta__range=[inicioMesMayo,finMesMayo], credito="N")
        montoIngresoMayo = 0
        if consultaVentasMayo:
            for ventaRealizada in consultaVentasMayo:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoMayo = montoIngresoMayo + montoVenta
        consultaCreditosMayo = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesMayo,finMesMayo],  renta_id__isnull=True)
        if consultaCreditosMayo:
            for crceditoRealizado in consultaCreditosMayo:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoMayo = montoIngresoMayo + montoPagadoCredito
        consultaRentasMayo = Rentas.objects.filter(fecha_apartado__range=[inicioMesMayo,finMesMayo])
        if consultaRentasMayo:
            for rentaRealizada in consultaRentasMayo:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoMayo = montoIngresoMayo + sumaPagosRenta
        
        inicioMesJunio = añoHoy+"-06-01"
        finMesJunio = añoHoy+"-06-30"
        consultaVentasJunio = Ventas.objects.filter(fecha_venta__range=[inicioMesJunio,finMesJunio], credito="N")
        montoIngresoJunio = 0
        if consultaVentasJunio:
            for ventaRealizada in consultaVentasJunio:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoJunio = montoIngresoJunio + montoVenta
        consultaCreditosJunio = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesJunio,finMesJunio],  renta_id__isnull=True)
        if consultaCreditosJunio:
            for crceditoRealizado in consultaCreditosJunio:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoJunio = montoIngresoJunio + montoPagadoCredito
        consultaRentasJunio = Rentas.objects.filter(fecha_apartado__range=[inicioMesJunio,finMesJunio])
        if consultaRentasJunio:
            for rentaRealizada in consultaRentasJunio:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoJunio = montoIngresoJunio + sumaPagosRenta
        
        inicioMesJulio = añoHoy+"-07-01"
        finMesJulio = añoHoy+"-07-31"
        consultaVentasJulio = Ventas.objects.filter(fecha_venta__range=[inicioMesJulio,finMesJulio], credito="N")
        montoIngresoJulio = 0
        if consultaVentasJulio:
            for ventaRealizada in consultaVentasJulio:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoJulio = montoIngresoJulio + montoVenta
        consultaCreditosJulio = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesJulio,finMesJulio],  renta_id__isnull=True)
        if consultaCreditosJulio:
            for crceditoRealizado in consultaCreditosJulio:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoJulio = montoIngresoJulio + montoPagadoCredito
        consultaRentasJulio = Rentas.objects.filter(fecha_apartado__range=[inicioMesJulio,finMesJulio])
        if consultaRentasJulio:
            for rentaRealizada in consultaRentasJulio:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoJulio = montoIngresoJulio + sumaPagosRenta
        
        inicioMesAgosto = añoHoy+"-08-01"
        finMesAgosto = añoHoy+"-08-31"
        consultaVentasAgosto = Ventas.objects.filter(fecha_venta__range=[inicioMesAgosto,finMesAgosto], credito="N")
        montoIngresoAgosto = 0
        if consultaVentasAgosto:
            for ventaRealizada in consultaVentasAgosto:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoAgosto = montoIngresoAgosto + montoVenta
        consultaCreditosAgosto = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesAgosto,finMesAgosto],  renta_id__isnull=True)
        if consultaCreditosAgosto:
            for crceditoRealizado in consultaCreditosAgosto:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoAgosto = montoIngresoAgosto + montoPagadoCredito
        consultaRentasAgosto = Rentas.objects.filter(fecha_apartado__range=[inicioMesAgosto,finMesAgosto])
        if consultaRentasAgosto:
            for rentaRealizada in consultaRentasAgosto:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoAgosto = montoIngresoAgosto + sumaPagosRenta
        
        inicioMesSeptiembre = añoHoy+"-09-01"
        finMesSeptiembre = añoHoy+"-09-30"
        consultaVentasSeptiembre = Ventas.objects.filter(fecha_venta__range=[inicioMesSeptiembre,finMesSeptiembre], credito="N")
        montoIngresoSeptiembre = 0
        if consultaVentasSeptiembre:
            for ventaRealizada in consultaVentasSeptiembre:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoSeptiembre = montoIngresoSeptiembre + montoVenta
        consultaCreditosSeptiembre = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesSeptiembre,finMesSeptiembre],  renta_id__isnull=True)
        if consultaCreditosSeptiembre:
            for crceditoRealizado in consultaCreditosSeptiembre:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoSeptiembre = montoIngresoSeptiembre + montoPagadoCredito
        consultaRentasSeptiembre = Rentas.objects.filter(fecha_apartado__range=[inicioMesSeptiembre,finMesSeptiembre])
        if consultaRentasSeptiembre:
            for rentaRealizada in consultaRentasSeptiembre:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoSeptiembre = montoIngresoSeptiembre + sumaPagosRenta
        
        inicioMesOctubre = añoHoy+"-10-01"
        finMesOctubre = añoHoy+"-10-31"
        consultaVentasOctubre = Ventas.objects.filter(fecha_venta__range=[inicioMesOctubre,finMesOctubre], credito="N")
        montoIngresoOctubre = 0
        if consultaVentasOctubre:
            for ventaRealizada in consultaVentasOctubre:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoOctubre = montoIngresoOctubre + montoVenta
        consultaCreditosOctubre = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesOctubre,finMesOctubre],  renta_id__isnull=True)
        if consultaCreditosOctubre:
            for crceditoRealizado in consultaCreditosOctubre:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoOctubre = montoIngresoOctubre + montoPagadoCredito
        consultaRentasOctubre = Rentas.objects.filter(fecha_apartado__range=[inicioMesOctubre,finMesOctubre])
        if consultaRentasOctubre:
            for rentaRealizada in consultaRentasOctubre:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoOctubre = montoIngresoOctubre + sumaPagosRenta
        
        inicioMesNoviembre = añoHoy+"-11-01"
        finMesNoviembre = añoHoy+"-11-30"
        consultaVentasNoviembre = Ventas.objects.filter(fecha_venta__range=[inicioMesNoviembre,finMesNoviembre], credito="N")
        montoIngresoNoviembre = 0
        if consultaVentasNoviembre:
            for ventaRealizada in consultaVentasNoviembre:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoNoviembre = montoIngresoNoviembre + montoVenta
        consultaCreditosNoviembre = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesNoviembre,finMesNoviembre],  renta_id__isnull=True)
        if consultaCreditosNoviembre:
            for crceditoRealizado in consultaCreditosNoviembre:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoNoviembre = montoIngresoNoviembre + montoPagadoCredito
        consultaRentasNoviembre = Rentas.objects.filter(fecha_apartado__range=[inicioMesNoviembre,finMesNoviembre])
        if consultaRentasNoviembre:
            for rentaRealizada in consultaRentasNoviembre:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado 
                montoIngresoNoviembre = montoIngresoNoviembre + sumaPagosRenta
        
        inicioMesDiciembre = añoHoy+"-12-01"
        finMesDiciembre = añoHoy+"-12-31"
        consultaVentasDiciembre = Ventas.objects.filter(fecha_venta__range=[inicioMesDiciembre,finMesDiciembre], credito="N")
        montoIngresoDiciembre = 0
        if consultaVentasDiciembre:
            for ventaRealizada in consultaVentasDiciembre:
                montoVenta = ventaRealizada.monto_pagar
                montoIngresoDiciembre = montoIngresoDiciembre + montoVenta
        consultaCreditosDiciembre = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesDiciembre,finMesDiciembre],  renta_id__isnull=True)
        if consultaCreditosDiciembre:
            for crceditoRealizado in consultaCreditosDiciembre:
                montoPagadoCredito = crceditoRealizado.monto_pagado
                montoIngresoDiciembre = montoIngresoDiciembre + montoPagadoCredito
        consultaRentasDiciembre = Rentas.objects.filter(fecha_apartado__range=[inicioMesDiciembre,finMesDiciembre])
        if consultaRentasDiciembre:
            for rentaRealizada in consultaRentasDiciembre:
                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                montoPagadoRestante = rentaRealizada.monto_restante
                sumaPagosRenta = 0
                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                    sumaPagosRenta = rentaRealizada.monto_total_renta
                else: #Si ya se pago el restante
                    sumaPagosRenta = montoPagadoApartado
                montoIngresoDiciembre = montoIngresoDiciembre + sumaPagosRenta
        
        
        
        
        # - COMPRAS DEL MEES ...................................................
        totalComprasMesGasto = 0
        totalComprasMesVenta = 0
        totalComprasMesRenta= 0
        numeroComprasGasto = 0
        numeroComprasVenta = 0
        numeroComprasRenta = 0
        
        comprasProductosGastos = []
        comprasGastoDelMes = ComprasGastos.objects.filter(fecha_compra__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño])
        if comprasGastoDelMes:
            for compra in comprasGastoDelMes:
                montoComprado = compra.total_costoCompra
                totalComprasMesGasto = totalComprasMesGasto + montoComprado
                numeroComprasGasto = numeroComprasGasto +1
                
                idCompra = compra.id_compraGasto
                idProducto = compra.id_productoComprado_id
                consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                
                for datoProducto in consultaProducto:
                    nombreProducto = datoProducto.nombre_producto
                    codigoProducto = datoProducto.codigo_producto
                    imagenProducto = datoProducto.imagen_producto
                    sucursalProducto = datoProducto.sucursal_id
                nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                
                fechaCompra = compra.fecha_compra
                costoUnitarioCompra = compra.costo_unitario
                cantidadComprada = compra.cantidad_comprada
                totalMontoCompra = compra.total_costoCompra
                
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
                
                
                
                comprasProductosGastos.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursal,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
        else:
            comprasProductosGastos = None
            
        
        comprasProductosVentas = []
        comprasVentaDelMes = ComprasVentas.objects.filter(fecha_compra__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño])
        if comprasVentaDelMes:
            for compra in comprasVentaDelMes:
                montoComprado = compra.total_costoCompra
                totalComprasMesVenta = totalComprasMesVenta + montoComprado
                numeroComprasVenta = numeroComprasVenta +1
                
                idCompra = compra.id_compraVenta
                idProducto = compra.id_productoComprado_id
                consultaProducto = ProductosVenta.objects.filter(id_producto = idProducto)
                
                for datoProducto in consultaProducto:
                    nombreProducto = datoProducto.nombre_producto
                    codigoProducto = datoProducto.codigo_producto
                    imagenProducto = datoProducto.imagen_producto
                    sucursalProducto = datoProducto.sucursal_id
                nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                
                fechaCompra = compra.fecha_compra
                costoUnitarioCompra = compra.costo_unitario
                cantidadComprada = compra.cantidad_comprada
                totalMontoCompra = compra.total_costoCompra
                
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
                
                
                comprasProductosVentas.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursal,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
        else:
            comprasProductosVentas = None
        
        
        comprasProductosRentas = []
        comprasRentasDelMes = ComprasRentas.objects.filter(fecha_compra__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño])
        if comprasRentasDelMes:
            for compra in comprasRentasDelMes:
                montoComprado = compra.total_costoCompra
                totalComprasMesRenta = totalComprasMesRenta + montoComprado
                numeroComprasRenta = numeroComprasRenta +1
                
                idCompra = compra.id_compraRenta
                idProducto = compra.id_productoComprado_id
                consultaProducto = ProductosRenta.objects.filter(id_producto = idProducto)
                
                for datoProducto in consultaProducto:
                    nombreProducto = datoProducto.nombre_producto
                    codigoProducto = datoProducto.codigo_producto
                    imagenProducto = datoProducto.imagen_producto
                    sucursalProducto = datoProducto.sucursal_id
                nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                
                fechaCompra = compra.fecha_compra
                costoUnitarioCompra = compra.costo_unitario
                cantidadComprada = compra.cantidad_comprada
                totalMontoCompra = compra.total_costoCompra
                
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                for datoSucursal in consultaSucursal:
                    nombreSucursal = datoSucursal.nombre
                
                
                comprasProductosRentas.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursal,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
        else:
            comprasProductosRentas = None            

        sumaTotalesCompras = totalComprasMesGasto + totalComprasMesVenta + totalComprasMesRenta
        
        
        
        
        #PRODUCTOS TOOOOOPP ------------------------------------------
      
        consultaVentasMesActual = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño])
        
       
        productosCantidades = []
        productosVenta =[]
        cantidadesProductosVenta =[]
        sinProductos = False
       
        
        for ventaMensual in consultaVentasMesActual:
            
            ids_productos = ventaMensual.ids_productos
            if ids_productos == "":
                sinProductos = True
            else:
                sinProductos = False
            
                productos = ids_productos.split(',')
                cantidades_productos = ventaMensual.cantidades_productos
                cantidades = cantidades_productos.split(',')

                productosCantidades = zip(productos, cantidades)
            
            if sinProductos == False:
                for idP,cant in productosCantidades:
                    productoVenta= str(idP)
                    cantidadProductoVenta = str(cant)
            
                
                    if "PV" in productoVenta:
                        productosVenta.append(productoVenta)   #['PV0001']
                        cantidadesProductosVenta.append(cantidadProductoVenta) #['1']
        
           
            
        if not productosVenta:
            listaFinalProductosMesTabla = None
            
        else:
                lProductos =zip(productosVenta,cantidadesProductosVenta)   #(['PV1000'],['1']) 
            
                
                
                listaFinalProductos = []
                listaFinalProductosSoloStrings = []
                for pr,ca in lProductos:
                    
                    stringProducto =str(pr)
                    stringCantidad =ca
                    
                    numero = productosVenta.count(stringProducto)
                    
                    if numero >1:
                        if stringProducto in listaFinalProductosSoloStrings:
                            elProductoYaFueAgregado = True
                        else:
                            contadorCantidadesDeProductos = 0
                            contadorProductos = 0
                            for producto in productosVenta:  #3
                                
                                contadorProductos = contadorProductos + 1
                                stringProducto2 = productosVenta[contadorProductos-1]
                                cantidadProducto2 = cantidadesProductosVenta[contadorProductos-1]

                                if stringProducto == stringProducto2:
                                    contadorCantidadesDeProductos = contadorCantidadesDeProductos + int(cantidadProducto2)

                            stringCantidad = str(contadorCantidadesDeProductos)
                            listaFinalProductosSoloStrings.append(stringProducto)
                            listaFinalProductos.append([stringProducto,stringCantidad])
                        #Borrar todos los elementos de las dos listas de strings y cantidades correspondientes a ese producto
                        
                    else:
                        listaFinalProductos.append([stringProducto,stringCantidad])

                    
                    listaProductosOrdenada = sorted(listaFinalProductos, key = lambda elemento:elemento[1])

                    listaProductosOrdenadaMayorAMenor = listaProductosOrdenada[::-1]


                    contadorParaTablaProductosMes = 0
                    arrayContadores = []
                    arrayInfoProducto = []
                    for producto in listaProductosOrdenadaMayorAMenor:
                        
                        contadorParaTablaProductosMes = contadorParaTablaProductosMes + 1
                        arrayContadores.append(contadorParaTablaProductosMes)

                        #info producto
                        codigoProducto = producto[0]
                        cantidadVendida = producto[1]
                        consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
                        for datoProducto in consultaProducto:
                            nombre = datoProducto.nombre_producto
                            costoVenta = datoProducto.costo_venta
                            imagen = datoProducto.imagen_producto
                        
                        costoTotalVendidoProducto = costoVenta * float(cantidadVendida)
                        arrayInfoProducto.append([nombre, costoVenta, costoTotalVendidoProducto, imagen])


                    listaFinalProductosMesTabla = zip(listaProductosOrdenadaMayorAMenor, arrayContadores, arrayInfoProducto)


        
        #SERVICIOS TOOOPP------------------------------------------------
        
        consultaVentasServiciosMesActual = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño])
        
       
        serviciosCantidades = []
        serviciosVenta =[]
        cantidadesServiciosVenta =[]
        sinServicioscorporales = False
        sinServiciosfaciales = False
       
        
        for ventaMensual in consultaVentasServiciosMesActual:
            
            ids_servicios_corporales = ventaMensual.ids_servicios_corporales #""
            if ids_servicios_corporales == "":
                sinServicioscorporales = True
            else:
                sinServicioscorporales = False
                serviciosCorporales = ids_servicios_corporales.split(',')
                cantidades_servicios_corporales = ventaMensual.cantidades_servicios_corporales
                cantidades_corporales = cantidades_servicios_corporales.split(',')

                serviciosCorporalesCantidades = zip(serviciosCorporales, cantidades_corporales)
            
            ids_servicios_faciales = ventaMensual.ids_servicios_faciales
            if ids_servicios_faciales == "":
                sinServiciosfaciales = True
            else:
                serviciosFaciales = ids_servicios_faciales.split(',')
                cantidades_servicios_faciales = ventaMensual.cantidades_servicios_faciales
                cantidades_faciales = cantidades_servicios_faciales.split(',')

                serviciosFacialesCantidades = zip(serviciosFaciales, cantidades_faciales)
                
            if sinServicioscorporales == False:
                for idServicioCorporal,cantCorporal in serviciosCorporalesCantidades:
                    servicioVenta= str(idServicioCorporal)
                    cantidadServicioVenta = str(cantCorporal)
            
            
            
                    serviciosVenta.append(servicioVenta)   #['PV0001']
                    cantidadesServiciosVenta.append(cantidadServicioVenta) #['1']
                
        
            if sinServiciosfaciales == False:
                for idServicioFacial,cantFacial in serviciosFacialesCantidades:
                    servicioVenta= str(idServicioFacial)
                    cantidadServicioVenta = str(cantFacial)
            
            
            
                    serviciosVenta.append(servicioVenta)   #['PV0001']
                    cantidadesServiciosVenta.append(cantidadServicioVenta) #['1'] for idServicioCorporal,cantCorporal in serviciosCorporalesCantidades:
                
        if not serviciosVenta:
            listaFinalServiciosMesTabla = None
        else:
            lServicios =zip(serviciosVenta,cantidadesServiciosVenta)   #(['PV1000'],['1']) 
        
            
            
            listaFinalServicios = []
            listaFinalServiciosSoloStrings = []
            for ser,can in lServicios:
                
                intIdServicio =ser
                stringCantidad =can
                
                numero = serviciosVenta.count(intIdServicio)
                
                if numero >1:
                    if intIdServicio in listaFinalServiciosSoloStrings:
                        elServicioYaFueAgregado = True
                    else:
                        contadorCantidadesDeServicios = 0
                        contadorServicios = 0
                        for servicio in serviciosVenta:  #3
                            
                            contadorServicios = contadorServicios + 1
                            idServicio2 = serviciosVenta[contadorServicios-1]
                            cantidadServicio2 = cantidadesServiciosVenta[contadorServicios-1]

                            if intIdServicio == idServicio2:
                                contadorCantidadesDeServicios = contadorCantidadesDeServicios + int(cantidadServicio2)

                        stringCantidad = str(contadorCantidadesDeServicios)
                        listaFinalServiciosSoloStrings.append(intIdServicio)
                        listaFinalServicios.append([intIdServicio,stringCantidad])
                    #Borrar todos los elementos de las dos listas de strings y cantidades correspondientes a ese producto
                    
                else:
                    listaFinalServicios.append([intIdServicio,stringCantidad])

                
                listaServiciosOrdenada = sorted(listaFinalServicios, key = lambda elemento:elemento[1])

                listaServiciosOrdenadaMayorAMenor = listaServiciosOrdenada[::-1]


                contadorParaTablaServiciosMes = 0
                arrayContadores = []
                arrayInfoServicio = []
                for servicio in listaServiciosOrdenadaMayorAMenor:
                    
                    contadorParaTablaServiciosMes = contadorParaTablaServiciosMes + 1
                    arrayContadores.append(contadorParaTablaServiciosMes)

                    #info producto
                    codigoServicio= servicio[0]
                    cantidadVendida = servicio[1]
                    consultaServicio = Servicios.objects.filter(id_servicio = codigoServicio)
                    for datoServicios in consultaServicio:
                        tipo = datoServicios.tipo_servicio
                        nombreServicio = datoServicios.nombre_servicio
                        costoVenta = datoServicios.precio_venta
                    
                    
                    costoTotalVendidoServicio = costoVenta * float(cantidadVendida)
                    arrayInfoServicio.append([tipo, nombreServicio, costoVenta,costoTotalVendidoServicio])


                listaFinalServiciosMesTabla = zip(listaServiciosOrdenadaMayorAMenor, arrayContadores, arrayInfoServicio)



        
        
        #PRODUCTOS RENTA TOPPP------------------------------------------

        consultaVentasRentasMesActual = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaDelAño,fechaUltimoDiaDelAño])
        
       
        productosRentaCantidades = []
        productosRentaVenta =[]
        cantidadesProductosRentaVenta =[]
        sinProductosRenta = False
       
        
        for ventaMensual in consultaVentasRentasMesActual:
            
            ids_productos = ventaMensual.ids_productos
            if ids_productos == "":
                sinProductosRenta = True
            else: 
                sinProductosRenta = False
                productos = ids_productos.split(',')
                cantidades_productos = ventaMensual.cantidades_productos
                cantidades = cantidades_productos.split(',')

                productosCantidades = zip(productos, cantidades)
                
            if sinProductosRenta == False:
                for idP,cant in productosCantidades:
                    productoVenta= str(idP)
                    cantidadProductoVenta = str(cant)
            
                
                    if "PR" in productoVenta:
                        productosRentaVenta.append(productoVenta)   #['PV0001']
                        cantidadesProductosRentaVenta.append(cantidadProductoVenta) #['1']
            
        if not productosRentaVenta:
            listaFinalProductosRentaMesTabla = None
        else:

            lProductosRenta =zip(productosRentaVenta,cantidadesProductosRentaVenta)   #(['PV1000'],['1']) 
        
            
            
            listaFinalProductosRenta = []
            listaFinalProductosSoloStringsRenta = []
            for prren,caren in lProductosRenta:
                
                stringProducto =str(prren)
                stringCantidad =caren
                
                numero = productosRentaVenta.count(stringProducto)
                
                if numero >1:
                    if stringProducto in listaFinalProductosSoloStringsRenta:
                        elProductoYaFueAgregado = True
                    else:
                        contadorCantidadesDeProductosRenta = 0
                        contadorProductosRenta = 0
                        for producto in productosRentaVenta:  #3
                            
                            contadorProductosRenta = contadorProductosRenta + 1
                            stringProductorenta2 = productosRentaVenta[contadorProductosRenta-1]
                            cantidadProductorenta2 = cantidadesProductosRentaVenta[contadorProductosRenta-1]

                            if stringProducto == stringProductorenta2:
                                contadorCantidadesDeProductosRenta = contadorCantidadesDeProductosRenta + int(cantidadProductorenta2)

                        stringCantidad = str(contadorCantidadesDeProductosRenta)
                        listaFinalProductosSoloStringsRenta.append(stringProducto)
                        listaFinalProductosRenta.append([stringProducto,stringCantidad])
                    #Borrar todos los elementos de las dos listas de strings y cantidades correspondientes a ese producto
                    
                else:
                    listaFinalProductosRenta.append([stringProducto,stringCantidad])

                
                listaProductosRentaOrdenada = sorted(listaFinalProductosRenta, key = lambda elemento:elemento[1])

                listaProductosRentaOrdenadaMayorAMenor = listaProductosRentaOrdenada[::-1]


                contadorParaTablaProductosRentaMes = 0
                arrayContadores = []
                arrayInfoProductoRenta = []
                for productoRenta in listaProductosRentaOrdenadaMayorAMenor:
                    
                    contadorParaTablaProductosRentaMes = contadorParaTablaProductosRentaMes + 1
                    arrayContadores.append(contadorParaTablaProductosRentaMes)

                    #info producto
                    codigoProductoRenta = productoRenta[0]
                    cantidadVendidaRenta = productoRenta[1]
                    consultaProductoRenta = ProductosRenta.objects.filter(codigo_producto = codigoProductoRenta)
                    for datoProducto in consultaProductoRenta:
                        nombreRenta = datoProducto.nombre_producto
                        costoRenta = datoProducto.costo_renta
                        imagenRenta = datoProducto.imagen_producto
                    
                    costoTotalRentadoProducto = costoRenta * float(cantidadVendidaRenta)
                    arrayInfoProductoRenta.append([nombreRenta, costoRenta, costoTotalRentadoProducto, imagenRenta])


                listaFinalProductosRentaMesTabla = zip(listaProductosRentaOrdenadaMayorAMenor, arrayContadores, arrayInfoProductoRenta)
       
       

        return render(request, "17 Informe Ventas/informeDeVentasAnual.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "notificacionRenta":notificacionRenta,"añoHoy":añoHoy,"strAñoAnterior":strAñoAnterior,"strHaceDosAños":strHaceDosAños, "strHaceTresAños":strHaceTresAños,
                                                                          "montoIngresoAñoActual":montoIngresoAñoActual,"montoIngresoAñoAnterior":montoIngresoAñoAnterior,"porcentajeIngresosAño":porcentajeIngresosAño,"esMayor":esMayor,
                                                                          "montoIngresoSemanaActual":montoIngresoSemanaActual,"montoIngresoSemanaAnterior":montoIngresoSemanaAnterior, "esMayorSemana":esMayorSemana,"porcentajeIngresosSemana":porcentajeIngresosSemana,
                                                                          "montoIngresoEnero":montoIngresoEnero, "montoIngresoFebrero":montoIngresoFebrero, "montoIngresoMarzo":montoIngresoMarzo, "montoIngresoAbril":montoIngresoAbril, "montoIngresoMayo":montoIngresoMayo, "montoIngresoJunio":montoIngresoJunio, "montoIngresoJulio":montoIngresoJulio, "montoIngresoAgosto":montoIngresoAgosto, "montoIngresoSeptiembre":montoIngresoSeptiembre, "montoIngresoOctubre":montoIngresoOctubre, "montoIngresoNoviembre":montoIngresoNoviembre, "montoIngresoDiciembre":montoIngresoDiciembre,
                                                                          "totalComprasMesGasto":totalComprasMesGasto,"totalComprasMesVenta":totalComprasMesVenta,"totalComprasMesRenta":totalComprasMesRenta,"contadorVentasAñoActual":contadorVentasAñoActual,"contadorRentasAñoActual":contadorRentasAñoActual,"contadorCreditosAñoActual":contadorCreditosAñoActual,"numeroVentas":numeroVentas,"numeroRentas":numeroRentas,"numeroCreditos":numeroCreditos,
                                                                          "numeroComprasGasto":numeroComprasGasto,"numeroComprasVenta":numeroComprasVenta,"numeroComprasRenta":numeroComprasRenta,"sumaTotalesCompras":sumaTotalesCompras,"totalEfectivo":totalEfectivo,"totalTarjeta":totalTarjeta,"totalTransferencia":totalTransferencia,"clientesTops":clientesTops,
                                                                          "clientesTop":clientesTop,"montosTop":montosTop,"contadorClientesArray":contadorClientesArray,"listaFinalProductosMesTabla":listaFinalProductosMesTabla,
                                                                          "listaFinalServiciosMesTabla":listaFinalServiciosMesTabla, "listaFinalProductosRentaMesTabla":listaFinalProductosRentaMesTabla, "empleadosTops":empleadosTops,
                                                                          "listaZipClientes":listaZipClientes, "clientesTopsModal":clientesTopsModal, "empleadosTopsModal":empleadosTopsModal,
                                                                          "comprasProductosGastos":comprasProductosGastos, "comprasProductosVentas":comprasProductosVentas, "comprasProductosRentas":comprasProductosRentas,
                                                                          "montoIngresoHaceTresAños":montoIngresoHaceTresAños, "montoIngresoHaceDosAños":montoIngresoHaceDosAños, "notificacionCita":notificacionCita})
    else:
        return render(request,"1 Login/login.html")
    
def informeDeVentasRangoFechas(request):
    if "idSesion" in request.session:
        #Empleado está logueado
        
        # Variables de sesión
        idEmpleado = request.session['idSesion']   #1
        nombresEmpleado = request.session['nombresSesion'] #
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
        
        if request.method == "POST": #Si le dio clic al botón y se mandaron variables..
            #fecha inicio
            fechaInicio = request.POST["fechaInicio"]    
            fechaInicioPartida = fechaInicio.split("-")    
            mesNumeroInicio = fechaInicioPartida[1]
            
            #Fecha final
            fechaFinal = request.POST["fechaFinal"] 
            fechaFinalPartida = fechaFinal.split("-")
            mesNumeroFinal = fechaFinalPartida[1]
            
            
            mesesTexto = {
            "01":'Enero',
            "02":'Febrero',
            "03":'Marzo',
            "04":'Abril',
            "05":'Mayo',
            "06":'Junio',
            "07":'Julio',
            "08":'Agosto',
            "09":'Septiembre',
            "10":'Octubre',
            "11":'Noviembre',
            "12":'Diciembre'
            }
            
            
            #Mes actual
            mesInicioTexto = mesesTexto[str(mesNumeroInicio)] #Junio
            mesFinalTexto = mesesTexto[str(mesNumeroFinal)]
            
            #fechas
            fefchaCompletaInicio = fechaInicioPartida[2] + " de "+ mesInicioTexto +" "+ fechaInicioPartida[0]
            fefchaCompletaFinal = fechaFinalPartida[2]+ " de " + mesFinalTexto +" "+ fechaFinalPartida[0]
            
            #fecha con formato de fecha
            fechaInicioFormato=datetime.strptime(fechaInicio,"%Y-%m-%d")
            fechaFinalFormato=datetime.strptime(fechaFinal,"%Y-%m-%d") 

            diferenciaEnDias=fechaFinalFormato-fechaInicioFormato
            numeroDiasDiferencia=diferenciaEnDias.days
            fechaRestaInicio=fechaInicioFormato-timedelta(days=numeroDiasDiferencia)
            fechaSumaFinal=fechaFinalFormato+timedelta(days=numeroDiasDiferencia)
            
            fechaRestaInicioFormato=fechaRestaInicio.strftime("%Y-%m-%d") 
            fechaSumaFinalFormato=fechaSumaFinal.strftime("%Y-%m-%d")
            
            #Formato de fecha inicio periodo anterior con texto
            
            fechaRestaInicioFormatoPartida = fechaRestaInicioFormato.split("-")
            fechaRestaInicioFormatoPartidaMes = fechaRestaInicioFormatoPartida[1]
            
            mesPeriodoAnterior = mesesTexto[str(fechaRestaInicioFormatoPartidaMes)]
            
            fechaTextoPeriodoAnterior = fechaRestaInicioFormatoPartida[2] + " de "+ mesPeriodoAnterior +" "+ fechaRestaInicioFormatoPartida[0]

            #Formato de fecha final periodo después con texto
            fechaSumaFinalFormatoPartida = fechaSumaFinalFormato.split("-")
            fechaSumaFinalFormatoPartidaMesDespues = fechaSumaFinalFormatoPartida[1]
            
            mesPeriodoDespues = mesesTexto[str(fechaSumaFinalFormatoPartidaMesDespues)]
            
            fechaTextoPeriodoDespues = fechaSumaFinalFormatoPartida[2] + " de "+ mesPeriodoDespues +" "+ fechaSumaFinalFormatoPartida[0]
            
            
            #ingresos por venta directa
            consultaVentasRangoFecha=Ventas.objects.filter(fecha_venta__range = [fechaInicioFormato,fechaFinalFormato],credito="N")
            montoIngresoRangoFecha=0
            montoVentasDirectas=0
            numeroVentasDirectas=0

            if consultaVentasRangoFecha:
                for venta in consultaVentasRangoFecha:
                    montoPagado=venta.monto_pagar
                    montoIngresoRangoFecha=montoIngresoRangoFecha+montoPagado
                    montoVentasDirectas=montoVentasDirectas+montoPagado
                    numeroVentasDirectas=numeroVentasDirectas+1
            
            #ingresos por pagos de creditos
            consultaCreditosRangoFecha=Creditos.objects.filter(fecha_venta_credito__range = [fechaInicioFormato,fechaFinalFormato],renta_id__isnull=True)

            montoCreditos=0
            numeroCreditos=0
            if consultaCreditosRangoFecha:
                for credito in consultaCreditosRangoFecha:
                    montoPagado=credito.monto_pagado
                    montoIngresoRangoFecha=montoIngresoRangoFecha+montoPagado
                    montoCreditos=montoCreditos+montoPagado
                    numeroCreditos=numeroCreditos+1
            #ingresos por rentas
            consultaRentasRangoFecha=Rentas.objects.filter(fecha_apartado__range = [fechaInicioFormato,fechaFinalFormato])
            montoRentas=0
            numeroRentas=0
            if consultaRentasRangoFecha:
                for renta in consultaRentasRangoFecha:
                    montoPagoApartado=renta.monto_pago_apartado
                    montoPagadoRestante=renta.monto_restante
                    sumaPagosRenta=0
                    if montoPagadoRestante == 0:
                        sumaPagosRenta=renta.monto_total_renta
                    else:
                        sumaPagosRenta=montoPagoApartado
                    montoIngresoRangoFecha=montoIngresoRangoFecha+sumaPagosRenta
                    montoRentas=montoRentas+sumaPagosRenta
                    numeroRentas=numeroRentas+1

            
            #rango fecha anterior
            
            #ingresos por venta directa
            consultaVentasRangoFechaAntes=Ventas.objects.filter(fecha_venta__range = [fechaRestaInicio,fechaInicioFormato],credito="N")
            montoIngresoRangoFechaAntes=0
            

            if consultaVentasRangoFechaAntes:
                for venta in consultaVentasRangoFechaAntes:
                    montoPagado=venta.monto_pagar
                    montoIngresoRangoFechaAntes=montoIngresoRangoFechaAntes+montoPagado
                   
            
            #ingresos por pagos de creditos
            consultaCreditosRangoFechaAntes=Creditos.objects.filter(fecha_venta_credito__range = [fechaRestaInicio,fechaInicioFormato],renta_id__isnull=True)

            
            if consultaCreditosRangoFechaAntes:
                for credito in consultaCreditosRangoFechaAntes:
                    montoPagado=credito.monto_pagado
                    montoIngresoRangoFechaAntes=montoIngresoRangoFechaAntes+montoPagado
                   
            #ingresos por rentas
            consultaRentasRangoFechaAntes=Rentas.objects.filter(fecha_apartado__range = [fechaRestaInicio,fechaInicioFormato])
            
            if consultaRentasRangoFechaAntes:
                for renta in consultaRentasRangoFechaAntes:
                    montoPagoApartado=renta.monto_pago_apartado
                    montoPagadoRestante=renta.monto_restante
                    sumaPagosRenta=0
                    if montoPagadoRestante == 0:
                        sumaPagosRenta=renta.monto_total_renta
                    else:
                        sumaPagosRenta=montoPagoApartado
                    montoIngresoRangoFechaAntes=montoIngresoRangoFechaAntes+sumaPagosRenta
            esMayor=False
            if montoIngresoRangoFechaAntes==0:
                porcentajeRangoFechas=100
            else:
                porcentajeRangoFechas=(montoIngresoRangoFecha/montoIngresoRangoFechaAntes)
                porcentajeRangoFechas=porcentajeRangoFechas-1
                porcentajeRangoFechas=porcentajeRangoFechas*100
            if porcentajeRangoFechas>0:
                esMayor=True
            else:
                esMayor=False
            porcentajeRangoFechas =round(porcentajeRangoFechas,2)

            #rango fecha después
            
            #ingresos por venta directa
            consultaVentasRangoFechaDespues=Ventas.objects.filter(fecha_venta__range = [fechaSumaFinal,fechaFinalFormato],credito="N")
            montoIngresoRangoFechaDespues=0
            

            if consultaVentasRangoFechaDespues:
                for venta in consultaVentasRangoFechaDespues:
                    montoPagado=venta.monto_pagar
                    montoIngresoRangoFechaDespues=montoIngresoRangoFechaDespues+montoPagado
                   
            
            #ingresos por pagos de creditos
            consultaCreditosRangoFechaDespues=Creditos.objects.filter(fecha_venta_credito__range = [fechaSumaFinal,fechaFinalFormato],renta_id__isnull=True)

            
            if consultaCreditosRangoFechaDespues:
                for credito in consultaCreditosRangoFechaDespues:
                    montoPagado=credito.monto_pagado
                    montoIngresoRangoFechaDespues=montoIngresoRangoFechaDespues+montoPagado
                   
            #ingresos por rentas
            consultaRentasRangoFechaDespues=Rentas.objects.filter(fecha_apartado__range = [fechaSumaFinal,fechaFinalFormato])
            
            if consultaRentasRangoFechaDespues:
                for renta in consultaRentasRangoFechaDespues:
                    montoPagoApartado=renta.monto_pago_apartado
                    montoPagadoRestante=renta.monto_restante
                    sumaPagosRenta=0
                    if montoPagadoRestante == 0:
                        sumaPagosRenta=renta.monto_total_renta
                    else:
                        sumaPagosRenta=montoPagoApartado
                    montoIngresoRangoFechaDespues=montoIngresoRangoFechaDespues+sumaPagosRenta

            #compras del periodo
            totalComprasGasto=0
            totalComprasVenta=0
            totalComprasRenta=0
            
            numeroComprasGasto=0
            numeroComprasVenta=0
            numeroComprasRenta=0
            
    #Tabla Productos Gastos
            comprasProductosGastos = []
            comprasGastodelPeriodo=ComprasGastos.objects.filter(fecha_compra__range=[fechaInicioFormato,fechaFinalFormato])
            if comprasGastodelPeriodo :
                for compraGasto in comprasGastodelPeriodo:
                    montoComprado=compraGasto.total_costoCompra
                    totalComprasGasto=totalComprasGasto+montoComprado
                    numeroComprasGasto=numeroComprasGasto+1 
                    #datos para tabla
                    idCompra=compraGasto.id_compraGasto
                    idProducto=compraGasto.id_productoComprado_id
                    consultaProducto=ProductosGasto.objects.filter(id_producto=idProducto)
                    for datoProducto in consultaProducto:
                        nombreProducto=datoProducto.nombre_producto
                        codigoProducto=datoProducto.codigo_producto
                        imagenProducto=datoProducto.imagen_producto
                        sucursalProducto=datoProducto.sucursal_id
                    nombreCompletoProducto=codigoProducto+" - "+nombreProducto
                    consultaSucursal=Sucursales.objects.filter(id_sucursal=sucursalProducto)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal=datoSucursal.nombre
                    fechaCompra=compraGasto.fecha_compra
                    costoUnitarioCompra=compraGasto.costo_unitario
                    cantidadComprada=compraGasto.cantidad_comprada
                    totalMontoCompra=compraGasto.total_costoCompra
                    comprasProductosGastos.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursal,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
            else:
                comprasProductosGastos= None
                
    #Tabla Productos Venta
            comprasProductosVentas = []
            comprasVentasdelPeriodo=ComprasVentas.objects.filter(fecha_compra__range=[fechaInicioFormato,fechaFinalFormato])
            if comprasVentasdelPeriodo :
                for compraVenta in comprasVentasdelPeriodo:
                    montoVendido=compraVenta.total_costoCompra
                    totalComprasVenta=totalComprasVenta+montoVendido
                    numeroComprasVenta=numeroComprasVenta+1 
                    #datos para tabla
                    idCompra=compraVenta.id_compraVenta
                    idProducto=compraVenta.id_productoComprado_id
                    consultaProducto=ProductosVenta.objects.filter(id_producto=idProducto)
                    for datoProducto in consultaProducto:
                        nombreProducto=datoProducto.nombre_producto
                        codigoProducto=datoProducto.codigo_producto
                        imagenProducto=datoProducto.imagen_producto
                        sucursalProducto=datoProducto.sucursal_id
                    nombreCompletoProducto=codigoProducto+" - "+nombreProducto
                    consultaSucursal=Sucursales.objects.filter(id_sucursal=sucursalProducto)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal=datoSucursal.nombre
                    fechaCompra=compraVenta.fecha_compra
                    costoUnitarioCompra=compraVenta.costo_unitario
                    cantidadComprada=compraVenta.cantidad_comprada
                    totalMontoCompra=compraVenta.total_costoCompra
                    comprasProductosVentas.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursal,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
            else:
                comprasProductosVentas= None
            
            #Tabla Productos Renta
            comprasProductosRenta = []
            comprasRentasdelPeriodo=ComprasRentas.objects.filter(fecha_compra__range=[fechaInicioFormato,fechaFinalFormato])
            if comprasRentasdelPeriodo :
                for compraRenta in comprasRentasdelPeriodo:
                    montoComprado=compraRenta.total_costoCompra
                    totalComprasRenta=totalComprasRenta+montoComprado
                    numeroComprasRenta=numeroComprasRenta+1 
                    #datos para tabla
                    idCompra=compraRenta.id_compraRenta
                    idProducto=compraRenta.id_productoComprado_id
                    consultaProducto=ProductosRenta.objects.filter(id_producto=idProducto)
                    for datoProducto in consultaProducto:
                        nombreProducto=datoProducto.nombre_producto
                        codigoProducto=datoProducto.codigo_producto
                        imagenProducto=datoProducto.imagen_producto
                        sucursalProducto=datoProducto.sucursal_id
                    nombreCompletoProducto=codigoProducto+" - "+nombreProducto
                    consultaSucursal=Sucursales.objects.filter(id_sucursal=sucursalProducto)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal=datoSucursal.nombre
                    fechaCompra=compraRenta.fecha_compra
                    costoUnitarioCompra=compraRenta.costo_unitario
                    cantidadComprada=compraRenta.cantidad_comprada
                    totalMontoCompra=compraRenta.total_costoCompra
                    comprasProductosRenta.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursal,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
            else:
                comprasProductosRenta= None

            
            
            totalCompraFechaRango=totalComprasGasto+totalComprasVenta+totalComprasRenta
                    
        	#Totales en efectivo, tarjeta, transferencia
            #Efectivo
            consultaVentasEnEfectivo=Ventas.objects.filter(fecha_venta__range=[fechaInicioFormato,fechaFinalFormato],tipo_pago="Efectivo", credito="N")
            totalEfectivo=0

            for ventaEfectivo in consultaVentasEnEfectivo:
                monto_efectivo=ventaEfectivo.monto_pagar
                totalEfectivo=totalEfectivo+monto_efectivo

            #Tarjeta
            consultaVentasEnTarjeta=Ventas.objects.filter(fecha_venta__range=[fechaInicioFormato,fechaFinalFormato],tipo_pago="Tarjeta", credito="N")
            totalTarjeta=0

            for ventaTarjeta in consultaVentasEnTarjeta:
                monto_tarjeta=ventaTarjeta.monto_pagar
                totalTarjeta=totalTarjeta+monto_tarjeta
            
            #Transferencia
            consultaVentasEnTransferencia=Ventas.objects.filter(fecha_venta__range=[fechaInicioFormato,fechaFinalFormato],tipo_pago="Transferencia", credito="N")
            totalTransferencia=0

            for ventaTransferencia in consultaVentasEnTransferencia:
                monto_transferencia=ventaTransferencia.monto_pagar
                totalTransferencia=totalTransferencia+monto_transferencia

            
            #PAGOS DE LOS CREDITOS
            creditos = Creditos.objects.filter(fecha_venta_credito__range=[fechaInicioFormato,fechaFinalFormato])
            for credito in creditos:
                idCredito = credito.id_credito
            
                pagosCredito = PagosCreditos.objects.filter(id_credito_id__id_credito=idCredito)
                for pago in pagosCredito:
                    tipoPago1 = pago.tipo_pago1
                    tipoPago2 = pago.tipo_pago2
                    tipoPago3 = pago.tipo_pago3
                    tipoPago4 = pago.tipo_pago4

                    if tipoPago1:
                        montoPagado1 = pago.monto_pago1
                        if tipoPago1 == "Efectivo":
                            totalEfectivo = totalEfectivo + montoPagado1
                        elif tipoPago1 == "Tarjeta":
                            totalTarjeta = totalTarjeta + montoPagado1
                        elif tipoPago1 == "Transferencia":
                            totalTransferencia = totalTransferencia + montoPagado1
                    
                    elif tipoPago2:
                        montoPagado2 = pago.monto_pago2
                        if tipoPago2 == "Efectivo":
                            totalEfectivo = totalEfectivo + montoPagado2
                        elif tipoPago2 == "Tarjeta":
                            totalTarjeta = totalTarjeta + montoPagado2
                        elif tipoPago2 == "Transferencia":
                            totalTransferencia = totalTransferencia + montoPagado2
                    
                    elif tipoPago3:
                        montoPagado3 =pago.monto_pago3
                        if tipoPago3 == "Efectivo":
                            totalEfectivo = totalEfectivo + montoPagado3
                        elif tipoPago3 == "Tarjeta":
                            totalTarjeta = totalTarjeta + montoPagado3
                        elif tipoPago3 == "Transferencia":
                            totalTransferencia = totalTransferencia + montoPagado3
                            
                    elif tipoPago4:
                        montoPagado4 = pago.monto_pago4
                        if tipoPago4 == "Efectivo":
                            totalEfectivo = totalEfectivo + montoPagado4
                        elif tipoPago4 == "Tarjeta":
                            totalTarjeta = totalTarjeta + montoPagado4
                        elif tipoPago4 == "Transferencia":
                            totalTransferencia = totalTransferencia + montoPagado4
            
            #TOP CLIENTES CON MAS COMPRAS

            consultaVentasClientes = Ventas.objects.filter(fecha_venta__range=[fechaInicioFormato,fechaFinalFormato], cliente__isnull=False)

            clientesMontosTotales = []
            clientesIds = []
            contadorClientesArray = []
            if consultaVentasClientes:
                for clienteVentas in consultaVentasClientes:
                    cliente_ventas = clienteVentas.cliente_id
                    monto_total_cliente = clienteVentas.monto_pagar
                    clientesMontosTotales.append(monto_total_cliente) #180,600
                    clientesIds.append(cliente_ventas) #1,1
                    
                listaClientesCompradores = zip(clientesIds, clientesMontosTotales)
                
                listaClientes = []
                montoPorCliente = []
                contadorClientesArray = []
                
                
                for idcliente, montoTotalCliente in listaClientesCompradores:
                    
                    strIdCliente = str(idcliente)
                    intMonto = float(montoTotalCliente)
                    
                    if strIdCliente in listaClientes:
                        indice = listaClientes.index(strIdCliente)
                        montoASumar = montoPorCliente[indice]
                        nuevaSumatoria = float(montoASumar) + intMonto
                        montoPorCliente[indice] = str(nuevaSumatoria)
                    else:
                        listaClientes.append(strIdCliente)
                        montoPorCliente.append(str(intMonto))
                
                listaZipClientes = zip(listaClientes, montoPorCliente)
                
                listaOrdenadaMayorAMenor = sorted(listaZipClientes, key = lambda t: t[-1], reverse=True)
                tuples = zip(*listaOrdenadaMayorAMenor)
                listaClientesOrdenados, listaMontosOrdenados = [ list(tuple) for tuple in  tuples]
            
                        
                infoCliente = []

                
                cotadorClientes = 0
                for cliente in listaClientesOrdenados:
                    cotadorClientes = cotadorClientes + 1
                    contadorClientesArray.append(cotadorClientes)
                    id_cliente_top = cliente
                    clienteDatos = Clientes.objects.filter(id_cliente= id_cliente_top)
                    for c in clienteDatos:

                        nombre_cliente_top = c.nombre_cliente
                        apellido =  c.apellidoPaterno_cliente
                        apellido2 = c.apellidoMaterno_cliente
                    infoCliente.append([nombre_cliente_top,apellido,apellido2])

                clientesTops = zip (listaClientesOrdenados,listaMontosOrdenados,contadorClientesArray,infoCliente)
                clientesTopsModal =zip (listaClientesOrdenados,listaMontosOrdenados,contadorClientesArray,infoCliente) 
            else:
                clientesTops = None
                clientesTopsModal = None            
                    
            #TOP EMPLEADOS CON MÁS VENTAS

            consultaTodasLasVentasDelAño = Ventas.objects.filter(fecha_venta__range=[fechaInicioFormato,fechaFinalFormato])

            idsEmpleados = []
            montosTotalesDeVentaEmpleados = []
            if consultaTodasLasVentasDelAño:
                for venta in consultaTodasLasVentasDelAño:
                    idEmpleado = venta.empleado_vendedor_id
                    idsEmpleados.append(idEmpleado) #1,1
                    montoVendido = venta.monto_pagar
                    montosTotalesDeVentaEmpleados.append(montoVendido)
                    
                
                listaEmpleados = []
                contadorVentasEmpleado = []
                contadorEmpleado = []
                listaMontosPorEmpleados = []
                
                listaEmpleadosVentas = zip(idsEmpleados, montosTotalesDeVentaEmpleados)
                
                contadorEmpleados = 0
                for idEmpleado, montoVentita in listaEmpleadosVentas:
                    
                    strIdEmpleado = str(idEmpleado)
                    floatMontoVendido = float(montoVentita)
                    
                    if strIdEmpleado in listaEmpleados:
                        indice = listaEmpleados.index(strIdEmpleado)
                        ventaASumar = contadorVentasEmpleado[indice]
                        nuevaSumatoria = int(ventaASumar) + 1
                        contadorVentasEmpleado[indice] = nuevaSumatoria
                        
                        montoASumar = listaMontosPorEmpleados[indice]
                        nuevaSumatoriaMonto = float(montoASumar) + floatMontoVendido
                        listaMontosPorEmpleados[indice] = nuevaSumatoriaMonto
                    else:
                        listaEmpleados.append(strIdEmpleado)
                        
                        contadorVentasEmpleado.append("1")
                        listaMontosPorEmpleados.append(floatMontoVendido)
                
                for montoVendido in listaMontosPorEmpleados:
                    print(str(montoVendido))

                listaZipEmpleados = zip(listaEmpleados, contadorVentasEmpleado, listaMontosPorEmpleados)
                
                listaOrdenadaEmpleadosMayorAMenor = sorted(listaZipEmpleados, key = lambda t: t[-1], reverse=True)
                tuplesEmpleados = zip(*listaOrdenadaEmpleadosMayorAMenor)
                listaEmpleadosOrdenados, listaContadoresEmpleadosOrdenados, listaMontosEmpleadosOrdenados = [ list(tuple) for tuple in  tuplesEmpleados]
                
                for monto in listaMontosEmpleadosOrdenados:
                    print("Monto:"+str(monto))
                
                infoEmpleado = []

                

                for empleado in listaEmpleadosOrdenados:
                    
                    contadorEmpleados = contadorEmpleados + 1
                    contadorEmpleado.append(contadorEmpleados)
                    idEmpleado = int(empleado)
                    datosEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                    
                    for datoEmpleado in datosEmpleado:

                        nombresEm = datoEmpleado.nombres
                    infoEmpleado.append(nombresEm)

                empleadosTops = zip (listaEmpleadosOrdenados,listaContadoresEmpleadosOrdenados,contadorEmpleado,infoEmpleado, listaMontosEmpleadosOrdenados)
                empleadosTopsModal =  zip (listaEmpleadosOrdenados,listaContadoresEmpleadosOrdenados,contadorEmpleado,infoEmpleado, listaMontosEmpleadosOrdenados)
            else:
                empleadosTops = None
                empleadosTopsModal = None
                
            #PRODUCTOS TOOOOOPP ------------------------------------------
      
            consultaVentasMesActual = Ventas.objects.filter(fecha_venta__range=[fechaInicioFormato,fechaFinalFormato])
            
        
            productosCantidades = []
            productosVenta =[]
            cantidadesProductosVenta =[]
            sinProductos = False
        
            
            for ventaMensual in consultaVentasMesActual:
                
                ids_productos = ventaMensual.ids_productos
                if ids_productos == "":
                    sinProductos = True
                else:
                    sinProductos = False
                
                    productos = ids_productos.split(',')
                    cantidades_productos = ventaMensual.cantidades_productos
                    cantidades = cantidades_productos.split(',')

                    productosCantidades = zip(productos, cantidades)
                
                if sinProductos == False:
                    for idP,cant in productosCantidades:
                        productoVenta= str(idP)
                        cantidadProductoVenta = str(cant)
                
                    
                        if "PV" in productoVenta:
                            productosVenta.append(productoVenta)   #['PV0001']
                            cantidadesProductosVenta.append(cantidadProductoVenta) #['1']
            
            
                
            if not productosVenta:
                listaFinalProductosMesTabla = None
                
            else:
                    lProductos =zip(productosVenta,cantidadesProductosVenta)   #(['PV1000'],['1']) 
                
                    
                    
                    listaFinalProductos = []
                    listaFinalProductosSoloStrings = []
                    for pr,ca in lProductos:
                        
                        stringProducto =str(pr)
                        stringCantidad =ca
                        
                        numero = productosVenta.count(stringProducto)
                        
                        if numero >1:
                            if stringProducto in listaFinalProductosSoloStrings:
                                elProductoYaFueAgregado = True
                            else:
                                contadorCantidadesDeProductos = 0
                                contadorProductos = 0
                                for producto in productosVenta:  #3
                                    
                                    contadorProductos = contadorProductos + 1
                                    stringProducto2 = productosVenta[contadorProductos-1]
                                    cantidadProducto2 = cantidadesProductosVenta[contadorProductos-1]

                                    if stringProducto == stringProducto2:
                                        contadorCantidadesDeProductos = contadorCantidadesDeProductos + int(cantidadProducto2)

                                stringCantidad = str(contadorCantidadesDeProductos)
                                listaFinalProductosSoloStrings.append(stringProducto)
                                listaFinalProductos.append([stringProducto,stringCantidad])
                            #Borrar todos los elementos de las dos listas de strings y cantidades correspondientes a ese producto
                            
                        else:
                            listaFinalProductos.append([stringProducto,stringCantidad])

                        
                        listaProductosOrdenada = sorted(listaFinalProductos, key = lambda elemento:elemento[1])

                        listaProductosOrdenadaMayorAMenor = listaProductosOrdenada[::-1]


                        contadorParaTablaProductosMes = 0
                        arrayContadores = []
                        arrayInfoProducto = []
                        for producto in listaProductosOrdenadaMayorAMenor:
                            
                            contadorParaTablaProductosMes = contadorParaTablaProductosMes + 1
                            arrayContadores.append(contadorParaTablaProductosMes)

                            #info producto
                            codigoProducto = producto[0]
                            cantidadVendida = producto[1]
                            consultaProducto = ProductosVenta.objects.filter(codigo_producto = codigoProducto)
                            for datoProducto in consultaProducto:
                                nombre = datoProducto.nombre_producto
                                costoVenta = datoProducto.costo_venta
                                imagen = datoProducto.imagen_producto
                            
                            costoTotalVendidoProducto = costoVenta * float(cantidadVendida)
                            arrayInfoProducto.append([nombre, costoVenta, costoTotalVendidoProducto, imagen])


                        listaFinalProductosMesTabla = zip(listaProductosOrdenadaMayorAMenor, arrayContadores, arrayInfoProducto)


            
            #SERVICIOS TOOOPP------------------------------------------------
            
            consultaVentasServiciosMesActual = Ventas.objects.filter(fecha_venta__range=[fechaInicioFormato,fechaFinalFormato])
            
        
            serviciosCantidades = []
            serviciosVenta =[]
            cantidadesServiciosVenta =[]
            sinServicioscorporales = False
            sinServiciosfaciales = False
        
            
            for ventaMensual in consultaVentasServiciosMesActual:
                
                ids_servicios_corporales = ventaMensual.ids_servicios_corporales #""
                if ids_servicios_corporales == "":
                    sinServicioscorporales = True
                else:
                    sinServicioscorporales = False
                    serviciosCorporales = ids_servicios_corporales.split(',')
                    cantidades_servicios_corporales = ventaMensual.cantidades_servicios_corporales
                    cantidades_corporales = cantidades_servicios_corporales.split(',')

                    serviciosCorporalesCantidades = zip(serviciosCorporales, cantidades_corporales)
                
                ids_servicios_faciales = ventaMensual.ids_servicios_faciales
                if ids_servicios_faciales == "":
                    sinServiciosfaciales = True
                else:
                    serviciosFaciales = ids_servicios_faciales.split(',')
                    cantidades_servicios_faciales = ventaMensual.cantidades_servicios_faciales
                    cantidades_faciales = cantidades_servicios_faciales.split(',')

                    serviciosFacialesCantidades = zip(serviciosFaciales, cantidades_faciales)
                    
                if sinServicioscorporales == False:
                    for idServicioCorporal,cantCorporal in serviciosCorporalesCantidades:
                        servicioVenta= str(idServicioCorporal)
                        cantidadServicioVenta = str(cantCorporal)
                
                
                
                        serviciosVenta.append(servicioVenta)   #['PV0001']
                        cantidadesServiciosVenta.append(cantidadServicioVenta) #['1']
                    
            
                if sinServiciosfaciales == False:
                    for idServicioFacial,cantFacial in serviciosFacialesCantidades:
                        servicioVenta= str(idServicioFacial)
                        cantidadServicioVenta = str(cantFacial)
                
                
                
                        serviciosVenta.append(servicioVenta)   #['PV0001']
                        cantidadesServiciosVenta.append(cantidadServicioVenta) #['1'] for idServicioCorporal,cantCorporal in serviciosCorporalesCantidades:
                    
            if not serviciosVenta:
                listaFinalServiciosMesTabla = None
            else:
                lServicios =zip(serviciosVenta,cantidadesServiciosVenta)   #(['PV1000'],['1']) 
            
                
                
                listaFinalServicios = []
                listaFinalServiciosSoloStrings = []
                for ser,can in lServicios:
                    
                    intIdServicio =ser
                    stringCantidad =can
                    
                    numero = serviciosVenta.count(intIdServicio)
                    
                    if numero >1:
                        if intIdServicio in listaFinalServiciosSoloStrings:
                            elServicioYaFueAgregado = True
                        else:
                            contadorCantidadesDeServicios = 0
                            contadorServicios = 0
                            for servicio in serviciosVenta:  #3
                                
                                contadorServicios = contadorServicios + 1
                                idServicio2 = serviciosVenta[contadorServicios-1]
                                cantidadServicio2 = cantidadesServiciosVenta[contadorServicios-1]

                                if intIdServicio == idServicio2:
                                    contadorCantidadesDeServicios = contadorCantidadesDeServicios + int(cantidadServicio2)

                            stringCantidad = str(contadorCantidadesDeServicios)
                            listaFinalServiciosSoloStrings.append(intIdServicio)
                            listaFinalServicios.append([intIdServicio,stringCantidad])
                        #Borrar todos los elementos de las dos listas de strings y cantidades correspondientes a ese producto
                        
                    else:
                        listaFinalServicios.append([intIdServicio,stringCantidad])

                    
                    listaServiciosOrdenada = sorted(listaFinalServicios, key = lambda elemento:elemento[1])

                    listaServiciosOrdenadaMayorAMenor = listaServiciosOrdenada[::-1]


                    contadorParaTablaServiciosMes = 0
                    arrayContadores = []
                    arrayInfoServicio = []
                    for servicio in listaServiciosOrdenadaMayorAMenor:
                        
                        contadorParaTablaServiciosMes = contadorParaTablaServiciosMes + 1
                        arrayContadores.append(contadorParaTablaServiciosMes)

                        #info producto
                        codigoServicio= servicio[0]
                        cantidadVendida = servicio[1]
                        consultaServicio = Servicios.objects.filter(id_servicio = codigoServicio)
                        for datoServicios in consultaServicio:
                            tipo = datoServicios.tipo_servicio
                            nombreServicio = datoServicios.nombre_servicio
                            costoVenta = datoServicios.precio_venta
                        
                        
                        costoTotalVendidoServicio = costoVenta * float(cantidadVendida)
                        arrayInfoServicio.append([tipo, nombreServicio, costoVenta,costoTotalVendidoServicio])


                    listaFinalServiciosMesTabla = zip(listaServiciosOrdenadaMayorAMenor, arrayContadores, arrayInfoServicio)



            
            
            #PRODUCTOS RENTA TOPPP------------------------------------------

            consultaVentasRentasMesActual = Ventas.objects.filter(fecha_venta__range=[fechaInicioFormato,fechaFinalFormato])
            
        
            productosRentaCantidades = []
            productosRentaVenta =[]
            cantidadesProductosRentaVenta =[]
            sinProductosRenta = False
        
            
            for ventaMensual in consultaVentasRentasMesActual:
                
                ids_productos = ventaMensual.ids_productos
                if ids_productos == "":
                    sinProductosRenta = True
                else: 
                    sinProductosRenta = False
                    productos = ids_productos.split(',')
                    cantidades_productos = ventaMensual.cantidades_productos
                    cantidades = cantidades_productos.split(',')

                    productosCantidades = zip(productos, cantidades)
                    
                if sinProductosRenta == False:
                    for idP,cant in productosCantidades:
                        productoVenta= str(idP)
                        cantidadProductoVenta = str(cant)
                
                    
                        if "PR" in productoVenta:
                            productosRentaVenta.append(productoVenta)   #['PV0001']
                            cantidadesProductosRentaVenta.append(cantidadProductoVenta) #['1']
                
            if not productosRentaVenta:
                listaFinalProductosRentaMesTabla = None
            else:

                lProductosRenta =zip(productosRentaVenta,cantidadesProductosRentaVenta)   #(['PV1000'],['1']) 
            
                
                
                listaFinalProductosRenta = []
                listaFinalProductosSoloStringsRenta = []
                for prren,caren in lProductosRenta:
                    
                    stringProducto =str(prren)
                    stringCantidad =caren
                    
                    numero = productosRentaVenta.count(stringProducto)
                    
                    if numero >1:
                        if stringProducto in listaFinalProductosSoloStringsRenta:
                            elProductoYaFueAgregado = True
                        else:
                            contadorCantidadesDeProductosRenta = 0
                            contadorProductosRenta = 0
                            for producto in productosRentaVenta:  #3
                                
                                contadorProductosRenta = contadorProductosRenta + 1
                                stringProductorenta2 = productosRentaVenta[contadorProductosRenta-1]
                                cantidadProductorenta2 = cantidadesProductosRentaVenta[contadorProductosRenta-1]

                                if stringProducto == stringProductorenta2:
                                    contadorCantidadesDeProductosRenta = contadorCantidadesDeProductosRenta + int(cantidadProductorenta2)

                            stringCantidad = str(contadorCantidadesDeProductosRenta)
                            listaFinalProductosSoloStringsRenta.append(stringProducto)
                            listaFinalProductosRenta.append([stringProducto,stringCantidad])
                        #Borrar todos los elementos de las dos listas de strings y cantidades correspondientes a ese producto
                        
                    else:
                        listaFinalProductosRenta.append([stringProducto,stringCantidad])

                    
                    listaProductosRentaOrdenada = sorted(listaFinalProductosRenta, key = lambda elemento:elemento[1])

                    listaProductosRentaOrdenadaMayorAMenor = listaProductosRentaOrdenada[::-1]


                    contadorParaTablaProductosRentaMes = 0
                    arrayContadores = []
                    arrayInfoProductoRenta = []
                    for productoRenta in listaProductosRentaOrdenadaMayorAMenor:
                        
                        contadorParaTablaProductosRentaMes = contadorParaTablaProductosRentaMes + 1
                        arrayContadores.append(contadorParaTablaProductosRentaMes)

                        #info producto
                        codigoProductoRenta = productoRenta[0]
                        cantidadVendidaRenta = productoRenta[1]
                        consultaProductoRenta = ProductosRenta.objects.filter(codigo_producto = codigoProductoRenta)
                        for datoProducto in consultaProductoRenta:
                            nombreRenta = datoProducto.nombre_producto
                            costoRenta = datoProducto.costo_renta
                            imagenRenta = datoProducto.imagen_producto
                        
                        costoTotalRentadoProducto = costoRenta * float(cantidadVendidaRenta)
                        arrayInfoProductoRenta.append([nombreRenta, costoRenta, costoTotalRentadoProducto, imagenRenta])


                    listaFinalProductosRentaMesTabla = zip(listaProductosRentaOrdenadaMayorAMenor, arrayContadores, arrayInfoProductoRenta)
                
                




                    

            return render(request, "17 Informe Ventas/informeDeVentasRangoFechas.html", {"totalCompraFechaRango":totalCompraFechaRango,"comprasProductosRenta":comprasProductosRenta,"comprasProductosVentas":comprasProductosVentas,"numeroComprasRenta":numeroComprasRenta,"numeroComprasVenta":numeroComprasVenta,"numeroComprasGasto":numeroComprasGasto,"totalComprasRenta":totalComprasRenta,"totalComprasVenta":totalComprasVenta,"totalComprasGasto":totalComprasGasto,"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "notificacionRenta":notificacionRenta,
                                                                                         "fefchaCompletaInicio":fefchaCompletaInicio,"montoIngresoRangoFechaDespues":montoIngresoRangoFechaDespues,"fechaTextoPeriodoAnterior":fechaTextoPeriodoAnterior, "fefchaCompletaFinal":fefchaCompletaFinal,"montoIngresoRangoFecha":montoIngresoRangoFecha,"montoVentasDirectas":montoVentasDirectas,"numeroVentasDirectas":numeroVentasDirectas,"montoCreditos":montoCreditos,"numeroCreditos":numeroCreditos,"montoRentas":montoRentas,"numeroRentas":numeroRentas,"porcentajeRangoFechas":porcentajeRangoFechas,"esMayor":esMayor,"montoIngresoRangoFechaAntes":montoIngresoRangoFechaAntes,"fechaTextoPeriodoDespues":fechaTextoPeriodoDespues,"numeroDiasDiferencia":numeroDiasDiferencia,
                                                                                         "totalEfectivo":totalEfectivo,"totalTarjeta":totalTarjeta,"totalTransferencia":totalTransferencia,
                                                                                         "clientesTops":clientesTops,"clientesTopsModal":clientesTopsModal,
                                                                                         "empleadosTops":empleadosTops, "empleadosTopsModal":empleadosTopsModal,
                                                                                         "listaFinalProductosMesTabla":listaFinalProductosMesTabla,
                                                                                         "listaFinalServiciosMesTabla":listaFinalServiciosMesTabla,
                                                                                         "listaFinalProductosRentaMesTabla":listaFinalProductosRentaMesTabla, "notificacionCita":notificacionCita})
            

        
        
    else:
        return render(request,"1 Login/login.html")

def informeDeVentasRangoFechasEmpleado(request):
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
            idEmpleadoConfigurar = request.POST['idEmpleadoInforme']
            
            fechaInicio = request.POST['fechaInicio']
            fechaFinal = request.POST['fechaFinal']

            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoConfigurar)

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
                    tipo ="Empleado"
                    sucursales = Sucursales.objects.filter(id_sucursal = idsucursal)
                    for dato in sucursales:
                        sucursalEmpleado = dato.nombre


                letrasEmpleado = nombres[0] + apellidoPaterno[0] + apellidoMaterno[0]
            
            if estatus == "A":
                activo = True
            elif estatus == "I":
                activo = False

            totalVentas = 0
            contadorVentas = 0
            consultaVentas = Ventas.objects.filter(empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)  
            for venta in consultaVentas:
                montoVendido = venta.monto_pagar
                contadorVentas = contadorVentas + 1
                totalVentas = totalVentas + montoVendido   
                
                
                
            # INFORME DE VENTAS DEL MES -----------------------------------------------------------------------------------------------------------------------------
            hoy = datetime.now()
        
            mesdehoynumero = hoy.strftime('%m') #06
            
            mesesDic = {
                "01":'Enero',
                "02":'Febrero',
                "03":'Marzo',
                "04":'Abril',
                "05":'Mayo',
                "06":'Junio',
                "07":'Julio',
                "08":'Agosto',
                "09":'Septiembre',
                "10":'Octubre',
                "11":'Noviembre',
                "12":'Diciembre'
            }
            
            diasMeses = {
                'Enero':'31',
                'Febrero':'28',
                'Marzo':'31',
                'Abril':'30',
                'Mayo':'31',
                'Junio':'30',
                'Julio':'31',
                'Agosto':'31',
                'Septiembre':'30',
                'Octubre':'31',
                'Noviembre':'30',
                'Diciembre':'31'
            }
            #Mes actual
            diadehoy = hoy.strftime('%d')
            añoHoy = hoy.strftime('%Y')
            mesdehoy = mesesDic[str(mesdehoynumero)]
            
            fechaDiaMesActual = añoHoy+"-"+mesdehoynumero+"-"+diadehoy  #Día actual  2022-06-07
            fechaInicioMesActual = añoHoy+"-"+mesdehoynumero+"-01"  #Primer día del mes 2022-06-01  
            
            
            ventasEmpleadoEnElMes = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            #arreglosTabla
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

                #montos
                montoVendido = venta.monto_pagar
                montoVentasEnElMesActual = montoVentasEnElMesActual + montoVendido
                
                #Para tabla de ventas
                sucursal = venta.sucursal_id
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                for suc in consultaSucursal:
                    nombreSucursal = suc.nombre
                sucursales.append(nombreSucursal)
                
                cliente = venta.cliente_id
                if cliente == None:
                    clientes.append(["x","Cliente momentaneo"])
                else:
                    consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                    for datoCliente in consultaCliente:
                        nombreCliente = datoCliente.nombre_cliente
                        apellido = datoCliente.apellidoPaterno_cliente
                    
                    nombreCompletoCliente = nombreCliente + " "+apellido
                    
                    clientes.append([cliente,nombreCompletoCliente])
                
                #Productos
                codigosProductos = venta.ids_productos
                if codigosProductos == "":
                    boolProductos.append("Sin productos comprados")
                    productos.append("x")
                else:
                    boolProductos.append("Se compraron productos")
                    cantidadesProductos = venta.cantidades_productos
                    arregloCodigosProductos = codigosProductos.split(",")
                    arregloCantidadesProductos = cantidadesProductos.split(",")
                    
                    listaProductos = zip(arregloCodigosProductos,arregloCantidadesProductos)
                    
                    productitos = []
                    for producto, cantidades in listaProductos:
                        idcodigoProducto = str(producto)
                        cantidad = str(cantidades)
                        
                        if "PV" in idcodigoProducto:
                            #Producto para venta
                            tipoVenta.append("Venta")
                            consultaProducto = ProductosVenta.objects.filter(codigo_producto = idcodigoProducto)
                        else:
                            #Producto para renta
                            tipoVenta.append("Renta")
                            consultaProducto = ProductosRenta.objects.filter(codigo_producto = idcodigoProducto)
                        
                        for datoProducto in consultaProducto:
                            nombreProducto = datoProducto.nombre_producto
                        productitos.append([idcodigoProducto, nombreProducto,cantidad ])
                    productos.append(productitos)
                
                #ServiciosCorporales
                serviciosCorporales = venta.ids_servicios_corporales
                if serviciosCorporales == "":
                    boolServCorporal.append("Sin servicios coorporales")
                    servicioCorporal.append("x")
                else:
                    boolServCorporal.append("Se compraron servicios")
                    cantidadesServiciosCorporales = venta.cantidades_servicios_corporales
                    arregloIdsServiciosCorporales = serviciosCorporales.split(",")
                    arregloCantidadesServiciosCorporales = cantidadesServiciosCorporales.split(",")
                    
                    listaServiciosCorporales = zip(arregloIdsServiciosCorporales,arregloCantidadesServiciosCorporales)
                    
                    serviciosCorporales = []
                    for idServicioCorporal, cantidadServiciosCorporal in listaServiciosCorporales:
                        intId = int(idServicioCorporal)
                        strId = str(idServicioCorporal)
                        cantidad = str(cantidadServiciosCorporal)
                        
                       
                        consultaServicio = Servicios.objects.filter(id_servicio = intId)
                        
                        for datoServicio in consultaServicio:
                            nombreDeServicio = datoServicio.nombre_servicio
                        serviciosCorporales.append([strId, nombreDeServicio,cantidad ])
                    servicioCorporal.append(serviciosCorporales)
                
                #ServiciosFaciales
                serviciosFaciales = venta.ids_servicios_faciales
                if serviciosFaciales == "":
                    boolServFacial.append("Sin servicios faciales")
                    servicioFacial.append("x")
                else:
                    boolServFacial.append("Se compraron servicios")
                    cantiadesServiciosFaciales = venta.cantidades_servicios_faciales
                    arregloIdsServiciosFaciales = serviciosFaciales.split(",")
                    arregloCantidadesServiciosFaciales = cantiadesServiciosFaciales.split(",")
                    
                    listaServiciosFaciales = zip(arregloIdsServiciosFaciales, arregloCantidadesServiciosFaciales)
                    
                    serviciosFaciales = []
                    for idServiciosFacial, cantidadServicioFacial in listaServiciosFaciales:
                        intId = int(idServiciosFacial)
                        strId = str(idServiciosFacial)
                        cantidad = str(cantidadServicioFacial)
                        
                       
                        consultaServicio = Servicios.objects.filter(id_servicio = intId)
                        
                        for datoServicio in consultaServicio:
                            nombreDeServicio = datoServicio.nombre_servicio
                        serviciosFaciales.append([strId, nombreDeServicio,cantidad ])
                    servicioFacial.append(serviciosFaciales)
                credito = venta.credito
                if credito == "S":
                    boolCredito.append("Si")
                    consultaCredito = Creditos.objects.filter(venta_id__id_venta = idVenta)
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
                
                montoPagado = venta.monto_pagar
                montos.append(montoPagado)
                
                descuento = venta.descuento_id
                if descuento == None:
                    boolDescuentos.append("Sin descuento")
                    datosDescuento.append("Sin descuento")
                    descuentos.append("Sin descuento")
                    costoReal.append("Sin descuento")
                else:
                    boolDescuentos.append("Con descuento")
                    consultaDescuento = Descuentos.objects.filter(id_descuento = descuento)
                    for datoDescuento in consultaDescuento:
                        nombreDescuento = datoDescuento.nombre_descuento
                        porcentajeDescuento = datoDescuento.porcentaje
                    porcentajeTotalDescuento = 100 - float(porcentajeDescuento)
                    totalSinDescuento = (100*montoPagado)/porcentajeTotalDescuento
                    totalDescuento = totalSinDescuento - montoPagado
                
                
                    datosDescuento.append([porcentajeDescuento,nombreDescuento])
                    descuentos.append(totalDescuento)
                    costoReal.append(totalSinDescuento)

                    
                
            listaVentasMes = zip(ventasEmpleadoEnElMes, sucursales, clientes,boolProductos,productos, boolServCorporal, servicioCorporal, boolServFacial, servicioFacial, boolCredito, idsCreditos, boolPagado, montos, boolDescuentos, datosDescuento, descuentos, costoReal, tipoVenta)
                
                
            #Mes anterior
            haceUnMes = hoy - relativedelta(months=1)  #2022-05-07
            mesHaceUnMes = haceUnMes.strftime('%m') #05
            añoHaceUnMes = haceUnMes.strftime('%Y')
            mesAnteriorTexto = mesesDic[str(mesHaceUnMes)]
            
            diasDeUltimoMes = diasMeses[str(mesAnteriorTexto)]
            
            fechaPrimerDiaMesAnterior = añoHaceUnMes + "-"+mesHaceUnMes+"-01"   #2022-05-01
            fechaUltimoDiaMesAnterior = añoHaceUnMes + "-"+mesHaceUnMes+"-"+diasDeUltimoMes  #2022-05-31
            
            
            ventasEmpleadoEnElMesAnterior = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaMesAnterior,fechaUltimoDiaMesAnterior],empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            
            ventasEnElMesAnterior = 0
            montoTotalDeVentaMesAnterior = 0
            for ventaMesAnterior in ventasEmpleadoEnElMesAnterior:
                montoTotalVenta = ventaMesAnterior.monto_pagar
                montoTotalDeVentaMesAnterior = montoTotalDeVentaMesAnterior + montoTotalVenta
                
                ventasEnElMesAnterior = ventasEnElMesAnterior + 1
                
            #Verificación contra el mes anterior
            ventasEnElMesEsMayorAlMesAnterior = False
            if ventasEnElMesAnterior == 0:
                porcentajeVentasMes = 100
            else:
                porcentajeVentasMes = (ventasEnElMesActual / ventasEnElMesAnterior)
                porcentajeVentasMes = porcentajeVentasMes - 1
                porcentajeVentasMes = porcentajeVentasMes *100

            if porcentajeVentasMes > 0:
                ventasEnElMesEsMayorAlMesAnterior = True
                
            else:
                ventasEnElMesEsMayorAlMesAnterior = False
            porcentajeVentasMes = round(porcentajeVentasMes,2)
            
            
            #Semana actual
            diaActual = datetime.today().isoweekday() #2 martes
            intdiaActual = int(diaActual)
            diaLunes = intdiaActual-1 #3 dias para el lunes
            diaDomingo = 7-intdiaActual # 2 dias para el sabado
            
            #Montos totales de semana actual
            fechaLunes = datetime.now()-timedelta(days =diaLunes)
            fechaDomingo = datetime.now() + timedelta(days =diaDomingo)
            
            ventasEmpleadoEnLaSemana = Ventas.objects.filter(fecha_venta__range=[fechaLunes,fechaDomingo], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            
            ventasEnEnLaSemana = 0
            for ventaSemana in ventasEmpleadoEnLaSemana:
                ventasEnEnLaSemana = ventasEnEnLaSemana + 1
                    
            
            #Montos totales de semana anterior
            fechaLunesAnterior = fechaLunes-timedelta(days =7)
            fechaDomingoAnterior = fechaLunes - timedelta(days =1)
            
            ventasEmpleadoEnLaSemanaAnterior = Ventas.objects.filter(fecha_venta__range=[fechaLunesAnterior,fechaDomingoAnterior], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            
            ventasEnEnLaSemanaAnterior = 0
            for ventaSemanaAnterior in ventasEmpleadoEnLaSemanaAnterior:
                ventasEnEnLaSemanaAnterior = ventasEnEnLaSemanaAnterior + 1
                
            #Verificación contra la semana anterior
            ventasEnLaSemanaEsMayorALaSemanaAnterior = False

            if ventasEnEnLaSemanaAnterior == 0:
                porcentajeVentasSemanal = 100
            else:
                porcentajeVentasSemanal = (ventasEnEnLaSemana / ventasEnEnLaSemanaAnterior)
                porcentajeVentasSemanal = porcentajeVentasSemanal - 1
                porcentajeVentasSemanal = porcentajeVentasSemanal *100

            if porcentajeVentasSemanal > 0:
                ventasEnLaSemanaEsMayorALaSemanaAnterior = True
                
            else:
                ventasEnLaSemanaEsMayorALaSemanaAnterior = False
            porcentajeVentasSemanal = round(porcentajeVentasSemanal,2)
            
            
            
            #Meses para gráfica por mes
            inicioMesEnero = añoHoy+"-01-01"
            finMesEnero = añoHoy+"-01-31"
            contadorVentasEnero = 0
            ventasEnEnero = Ventas.objects.filter(fecha_venta__range=[inicioMesEnero,finMesEnero], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            for ventaEnero in ventasEnEnero:
                contadorVentasEnero = contadorVentasEnero + 1
            
            
            inicioMesFebrero = añoHoy+"-02-01"
            finMesFebrero = añoHoy+"-02-28"
            contadorVentasFebrero = 0
            ventasEnFebrero = Ventas.objects.filter(fecha_venta__range=[inicioMesFebrero,finMesFebrero], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            for ventaFebrero in ventasEnFebrero:
                contadorVentasFebrero = contadorVentasFebrero + 1
            
            inicioMesMarzo = añoHoy+"-03-01"
            finMesMarzo = añoHoy+"-03-31"
            contadorVentasMarzo = 0
            ventasEnMarzo = Ventas.objects.filter(fecha_venta__range=[inicioMesMarzo,finMesMarzo], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            for ventaMarzo in ventasEnMarzo:
                contadorVentasMarzo = contadorVentasMarzo + 1
            
            
            inicioMesAbril = añoHoy+"-04-01"
            finMesAbril = añoHoy+"-04-30"
            contadorVentasAbril = 0
            ventasEnAbril = Ventas.objects.filter(fecha_venta__range=[inicioMesAbril,finMesAbril], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            for ventaAbril in ventasEnAbril:
                contadorVentasAbril = contadorVentasAbril + 1
            
            inicioMesMayo = añoHoy+"-05-01"
            finMesMayo = añoHoy+"-05-31"
            contadorVentasMayo = 0
            ventasEnMayo = Ventas.objects.filter(fecha_venta__range=[inicioMesMayo,finMesMayo], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            for ventaMayo in ventasEnMayo:
                contadorVentasMayo = contadorVentasMayo + 1
            
            inicioMesJunio = añoHoy+"-06-01"
            finMesJunio = añoHoy+"-06-30"
            contadorVentasJunio = 0
            ventasEnJunio = Ventas.objects.filter(fecha_venta__range=[inicioMesJunio,finMesJunio], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            for ventaJunio in ventasEnJunio:
                contadorVentasJunio = contadorVentasJunio + 1
            
            inicioMesJulio = añoHoy+"-07-01"
            finMesJulio = añoHoy+"-07-31"
            contadorVentasJulio = 0
            ventasEnJulio = Ventas.objects.filter(fecha_venta__range=[inicioMesJulio,finMesJulio], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            for ventaJulio in ventasEnJulio:
                contadorVentasJulio = contadorVentasJulio + 1
            
            inicioMesAgosto = añoHoy+"-08-01"
            finMesAgosto = añoHoy+"-08-31"
            contadorVentasAgosto = 0
            ventasEnAgosto = Ventas.objects.filter(fecha_venta__range=[inicioMesAgosto,finMesAgosto],empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            for ventaAgosto in ventasEnAgosto:
                contadorVentasAgosto = contadorVentasAgosto + 1
            
            inicioMesSeptiembre = añoHoy+"-09-01"
            finMesSeptiembre = añoHoy+"-09-30"
            contadorVentasSeptiembre = 0
            ventasEnSeptiembre = Ventas.objects.filter(fecha_venta__range=[inicioMesSeptiembre,finMesSeptiembre], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            for ventaSeptiembre in ventasEnSeptiembre:
                contadorVentasSeptiembre = contadorVentasSeptiembre + 1
            
            inicioMesOctubre = añoHoy+"-10-01"
            finMesOctubre = añoHoy+"-10-31"
            contadorVentasOctubre = 0
            ventasEnOctubre = Ventas.objects.filter(fecha_venta__range=[inicioMesOctubre,finMesOctubre], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            for ventaOctubre in ventasEnOctubre:
                contadorVentasOctubre = contadorVentasOctubre + 1
            
            inicioMesNoviembre = añoHoy+"-11-01"
            finMesNoviembre = añoHoy+"-11-30"
            contadorVentasNoviembre = 0
            ventasEnNoviembre = Ventas.objects.filter(fecha_venta__range=[inicioMesNoviembre,finMesNoviembre], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            for ventaNoviembre in ventasEnNoviembre:
                contadorVentasNoviembre = contadorVentasNoviembre + 1
            
            inicioMesDiciembre = añoHoy+"-12-01"
            finMesDiciembre = añoHoy+"-12-31"
            contadorVentasDiciembre = 0
            ventasEnDiciembre = Ventas.objects.filter(fecha_venta__range=[inicioMesDiciembre,finMesDiciembre], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            for ventaDiciembre in ventasEnDiciembre:
                contadorVentasDiciembre = contadorVentasDiciembre + 1
                
            
            if tipo == "Administrador":
            #Ventas totales
                ventasTotalesDeEmpleadosEnElMes = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual])
            else:
                ventasTotalesDeEmpleadosEnElMes = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual], sucursal_id__id_sucursal = idsucursal)
            
            contadorVentasTotalesMes = 0
            for ventaMes in ventasTotalesDeEmpleadosEnElMes:
                contadorVentasTotalesMes = contadorVentasTotalesMes + 1
            
            if contadorVentasTotalesMes == 0:
                porcentajeVentasDelEmpleado = 0
            else:
                porcentajeVentasDelEmpleado = (ventasEnElMesActual * 100)/contadorVentasTotalesMes
            
            porcentajeDemasEmpleados = 100 - porcentajeVentasDelEmpleado
            
            
            if montoTotalDeVentaMesAnterior == 0:
                porcentajeMontoVentas = 100
            else:
                porcentajeMontoVentas = (montoVentasEnElMesActual / montoTotalDeVentaMesAnterior)
                porcentajeMontoVentas = porcentajeMontoVentas - 1
                porcentajeMontoVentas = porcentajeMontoVentas *100

            if porcentajeMontoVentas > 0:
                esteMesVendioMas = True
                
            else:
                esteMesVendioMas = False
            
            
            
            #INFORME DE EMPLEADO EN EL AÑO------------------------------------------------------------------------------------------------------------
            
            primeroDeEnero = añoHoy+"-01-01"
            ultimoDiciemte = añoHoy+"-12-31"
            
            ventasEmpleadoEnElAño = Ventas.objects.filter(fecha_venta__range=[primeroDeEnero,ultimoDiciemte], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            
            contadorVentasEnElAño = 0
            montoVentaEnElAño = 0
            for ventaAnual in ventasEmpleadoEnElAño:
                contadorVentasEnElAño = contadorVentasEnElAño+1
                montoVenta = ventaAnual.monto_pagar
                montoVentaEnElAño = montoVentaEnElAño + montoVenta
            
            añoAnterior = int(añoHoy)-1
            primeroDeEneroAnterior = str(añoAnterior)+"-01-01"
            ultimoDiciemteAnterior = str(añoAnterior)+"-12-31"
            
            ventasEmpleadoEnElAñoAnterior = Ventas.objects.filter(fecha_venta__range=[primeroDeEneroAnterior,ultimoDiciemteAnterior], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            
            contadorVentasEnElAñoAnterior = 0
            montoVentaEnElAñoAnterior = 0
            for ventaAnualAnterior in ventasEmpleadoEnElAñoAnterior:
                contadorVentasEnElAñoAnterior = contadorVentasEnElAñoAnterior+1
                montoVenta = ventaAnual.monto_pagar
                montoVentaEnElAñoAnterior = montoVentaEnElAñoAnterior + montoVenta
                
                
            if contadorVentasEnElAñoAnterior == 0:
                porcentajeVentaAnual = 100
            else:
                porcentajeVentaAnual = (contadorVentasEnElAño / contadorVentasEnElAñoAnterior)
                porcentajeVentaAnual = porcentajeVentaAnual - 1
                porcentajeVentaAnual = porcentajeVentaAnual *100

            if porcentajeVentaAnual > 0:
                ventasMayores = True
                
            else:
                ventasMayores = False
                
            primerAñoAntes = int(añoHoy)-1
            segundoAñoAntes = int(añoHoy)-2
            tercerAñoAntes = int(añoHoy)-3
            
            eneroHaceDosAños = str(segundoAñoAntes)+"-01-01"
            diciembreHaceDosAños = str(segundoAñoAntes)+"-12-31"
            ventasEmpleadoHaceDosAños = Ventas.objects.filter(fecha_venta__range=[eneroHaceDosAños,diciembreHaceDosAños], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            
            contadorVentasHaceDosAños = 0
            for venta in ventasEmpleadoHaceDosAños:
                contadorVentasHaceDosAños = contadorVentasHaceDosAños+1
            
            eneroHaceTresAños = str(tercerAñoAntes)+"-01-01"
            diciembreHaceTresAños = str(tercerAñoAntes)+"-12-31"
            ventasEmpleadoHaceTresAños = Ventas.objects.filter(fecha_venta__range=[eneroHaceTresAños,diciembreHaceTresAños], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            
            contadorVentasHaceTresAños = 0
            for venta in ventasEmpleadoHaceTresAños:
                contadorVentasHaceTresAños = contadorVentasHaceTresAños+1

            #pie chart
            if tipo == "Administrador":
            #Ventas totales
                ventasTotalesDeEmpleadosEnElAño= Ventas.objects.filter(fecha_venta__range=[primeroDeEnero,ultimoDiciemte])
            else:
                ventasTotalesDeEmpleadosEnElAño = Ventas.objects.filter(fecha_venta__range=[primeroDeEnero,ultimoDiciemte], sucursal_id__id_sucursal = idsucursal)
            
            contadorVentasTotalesDelAño = 0
            for ventaMes in ventasTotalesDeEmpleadosEnElAño:
                contadorVentasTotalesDelAño = contadorVentasTotalesDelAño + 1
            
            if contadorVentasTotalesDelAño == 0:
                porcentajeVentasDelEmpleadoEnElAño = 0
            else:
                porcentajeVentasDelEmpleadoEnElAño = (contadorVentasEnElAño * 100)/contadorVentasTotalesDelAño
            
            porcentajeDemasEmpleadosEnElAño = 100 - porcentajeVentasDelEmpleadoEnElAño
                
            if montoVentaEnElAñoAnterior == 0:
                porcentajeMontoVentaAnual = 100
            else:
                porcentajeMontoVentaAnual = (montoVentaEnElAño / montoVentaEnElAñoAnterior)
                porcentajeMontoVentaAnual = porcentajeMontoVentaAnual - 1
                porcentajeMontoVentaAnual = porcentajeMontoVentaAnual *100
            
            if porcentajeMontoVentaAnual > 0:
                esteAñoVendioMas = True
                
            else:
                esteAñoVendioMas = False
                
                
            ventasEmpleadoEnElAño2 = Ventas.objects.filter(fecha_venta__range=[primeroDeEnero,ultimoDiciemte], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
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
                
                #Para tabla de ventas
                sucursal = venta.sucursal_id
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                for suc in consultaSucursal:
                    nombreSucursal = suc.nombre
                sucursalesAño.append(nombreSucursal)
                
                cliente = venta.cliente_id
                if cliente == None:
                    clientesAño.append(["x","Cliente momentaneo"])
                else:
                    consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                    for datoCliente in consultaCliente:
                        nombreCliente = datoCliente.nombre_cliente
                        apellido = datoCliente.apellidoPaterno_cliente
                    
                    nombreCompletoCliente = nombreCliente + " "+apellido
                    
                    clientesAño.append([cliente,nombreCompletoCliente])
                
                #Productos
                codigosProductos = venta.ids_productos
                if codigosProductos == "":
                    boolProductosAño.append("Sin productos comprados")
                    productosAño.append("x")
                else:
                    boolProductosAño.append("Se compraron productos")
                    cantidadesProductos = venta.cantidades_productos
                    arregloCodigosProductos = codigosProductos.split(",")
                    arregloCantidadesProductos = cantidadesProductos.split(",")
                    
                    listaProductos = zip(arregloCodigosProductos,arregloCantidadesProductos)
                    
                    productitos = []
                    for producto, cantidades in listaProductos:
                        idcodigoProducto = str(producto)
                        cantidad = str(cantidades)
                        
                        if "PV" in idcodigoProducto:
                            #Producto para venta
                            tipoVentaAño.append("Venta")
                            consultaProducto = ProductosVenta.objects.filter(codigo_producto = idcodigoProducto)
                        else:
                            #Producto para renta
                            tipoVentaAño.append("Renta")
                            consultaProducto = ProductosRenta.objects.filter(codigo_producto = idcodigoProducto)
                        
                        for datoProducto in consultaProducto:
                            nombreProducto = datoProducto.nombre_producto
                        productitos.append([idcodigoProducto, nombreProducto,cantidad ])
                    productosAño.append(productitos)
                
                #ServiciosCorporales
                serviciosCorporales = venta.ids_servicios_corporales
                if serviciosCorporales == "":
                    boolServCorporalAño.append("Sin servicios coorporales")
                    servicioCorporalAño.append("x")
                else:
                    boolServCorporalAño.append("Se compraron servicios")
                    cantidadesServiciosCorporales = venta.cantidades_servicios_corporales
                    arregloIdsServiciosCorporales = serviciosCorporales.split(",")
                    arregloCantidadesServiciosCorporales = cantidadesServiciosCorporales.split(",")
                    
                    listaServiciosCorporales = zip(arregloIdsServiciosCorporales,arregloCantidadesServiciosCorporales)
                    
                    serviciosCorporales = []
                    for idServicioCorporal, cantidadServiciosCorporal in listaServiciosCorporales:
                        intId = int(idServicioCorporal)
                        strId = str(idServicioCorporal)
                        cantidad = str(cantidadServiciosCorporal)
                        
                       
                        consultaServicio = Servicios.objects.filter(id_servicio = intId)
                        
                        for datoServicio in consultaServicio:
                            nombreDeServicio = datoServicio.nombre_servicio
                        serviciosCorporales.append([strId, nombreDeServicio,cantidad ])
                    servicioCorporalAño.append(serviciosCorporales)
                
                #ServiciosFaciales
                serviciosFaciales = venta.ids_servicios_faciales
                if serviciosFaciales == "":
                    boolServFacialAño.append("Sin servicios faciales")
                    servicioFacialAño.append("x")
                else:
                    boolServFacialAño.append("Se compraron servicios")
                    cantiadesServiciosFaciales = venta.cantidades_servicios_faciales
                    arregloIdsServiciosFaciales = serviciosFaciales.split(",")
                    arregloCantidadesServiciosFaciales = cantiadesServiciosFaciales.split(",")
                    
                    listaServiciosFaciales = zip(arregloIdsServiciosFaciales, arregloCantidadesServiciosFaciales)
                    
                    serviciosFaciales = []
                    for idServiciosFacial, cantidadServicioFacial in listaServiciosFaciales:
                        intId = int(idServiciosFacial)
                        strId = str(idServiciosFacial)
                        cantidad = str(cantidadServicioFacial)
                        
                       
                        consultaServicio = Servicios.objects.filter(id_servicio = intId)
                        
                        for datoServicio in consultaServicio:
                            nombreDeServicio = datoServicio.nombre_servicio
                        serviciosFaciales.append([strId, nombreDeServicio,cantidad ])
                    servicioFacialAño.append(serviciosFaciales)
                credito = venta.credito
                if credito == "S":
                    boolCreditoAño.append("Si")
                    consultaCredito = Creditos.objects.filter(venta_id__id_venta = idVenta)
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
                    consultaDescuento = Descuentos.objects.filter(id_descuento = descuento)
                    for datoDescuento in consultaDescuento:
                        nombreDescuento = datoDescuento.nombre_descuento
                        porcentajeDescuento = datoDescuento.porcentaje
                    porcentajeTotalDescuento = 100 - float(porcentajeDescuento)
                    totalSinDescuento = (100*montoPagado)/porcentajeTotalDescuento
                    totalDescuento = totalSinDescuento - montoPagado
                
                
                    datosDescuentoAño.append([porcentajeDescuento,nombreDescuento])
                    descuentosAño.append(totalDescuento)
                    costoRealAño.append(totalSinDescuento)

                    
                
            listaVentasAño = zip(ventasEmpleadoEnElAño2, sucursalesAño, clientesAño,boolProductosAño,productosAño, boolServCorporalAño, servicioCorporalAño
                                 , boolServFacialAño, servicioFacialAño, boolCreditoAño, idsCreditosAño, boolPagadoAño, montosAño, boolDescuentosAño
                                 , datosDescuentoAño, descuentosAño, costoRealAño, tipoVentaAño)
              
            
            
             #INFORME DE EMPLEADO EN LA FECHA ESPECIFICADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA------------------------------------------------------------------------------------------------------------
            
            
            #Rango de fechas de empleado
            rangoFechasEmpleado = True
            rangoFechasEmpleado2 = True
            
            fechaInicio = request.POST['fechaInicio']
            fechaFinal = request.POST['fechaFinal']
            
            #fecha con formato de fecha
            fechaInicioFormato=datetime.strptime(fechaInicio,"%Y-%m-%d")
            fechaFinalFormato=datetime.strptime(fechaFinal,"%Y-%m-%d") 

            diferenciaEnDias=fechaFinalFormato-fechaInicioFormato
            numeroDiasDiferencia=diferenciaEnDias.days
            fechaRestaInicio=fechaInicioFormato-timedelta(days=numeroDiasDiferencia)
            fechaSumaFinal=fechaFinalFormato+timedelta(days=numeroDiasDiferencia)
            
           
            ventasEmpleadoPeriodo = Ventas.objects.filter(fecha_venta__range=[fechaInicioFormato,fechaFinalFormato], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            
            contadorVentasPeriodo = 0
            montoVentaPeriodo = 0
            for ventaPeriodo in ventasEmpleadoPeriodo:
                contadorVentasPeriodo = contadorVentasPeriodo+1
                montoVenta = ventaPeriodo.monto_pagar
                montoVentaPeriodo = montoVentaPeriodo + montoVenta
            
            
            ventasEmpleadoEnElPeriodoAnterior = Ventas.objects.filter(fecha_venta__range=[fechaRestaInicio,fechaInicioFormato], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            
            contadorVentasPeriodoAnterior = 0
            montoVentaPeriodoAnterior = 0
            for ventaPeriodoAnterior in ventasEmpleadoEnElPeriodoAnterior:
                contadorVentasPeriodoAnterior = contadorVentasPeriodoAnterior+1
                montoVenta = ventaPeriodoAnterior.monto_pagar
                montoVentaPeriodoAnterior = montoVentaPeriodoAnterior + montoVenta
                
            ventasEmpleadoEnElPeriodoSiguiente = Ventas.objects.filter(fecha_venta__range=[fechaFinalFormato,fechaSumaFinal], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            
            contadorVentasPeriodoSiguiente = 0
            montoVentaPeriodoSiguiente = 0
            for ventaPeriodoSiguiente in ventasEmpleadoEnElPeriodoSiguiente:
                contadorVentasPeriodoSiguiente = contadorVentasPeriodoSiguiente+1
                montoVenta = ventaPeriodoSiguiente.monto_pagar
                montoVentaPeriodoSiguiente = montoVentaPeriodoSiguiente + montoVenta
            
            fechaInicioPartida = fechaInicio.split("-")
            mesNumeroInicio = fechaInicioPartida[1]
            
            
            fechaFinalPartida = fechaFinal.split("-")
            mesNumeroFinal = fechaFinalPartida[1]
            
            mesNumeroRestaInicio=fechaRestaInicio.strftime('%m')
            mesNumeroSumaFinal=fechaSumaFinal.strftime('%m')
            
            
            mesesTexto = {
            "01":'Enero',
            "02":'Febrero',
            "03":'Marzo',
            "04":'Abril',
            "05":'Mayo',
            "06":'Junio',
            "07":'Julio',
            "08":'Agosto',
            "09":'Septiembre',
            "10":'Octubre',
            "11":'Noviembre',
            "12":'Diciembre'
            }
            
            
            #Mes actual
            mesInicioTexto = mesesTexto[str(mesNumeroInicio)] #Junio
            mesFinalTexto = mesesTexto[str(mesNumeroFinal)]
            mesRestaInicioTexto = mesesTexto[str(mesNumeroRestaInicio)]
            mesSumaFinalTexto = mesesTexto[str(mesNumeroSumaFinal)]
            #fechas
            fefchaCompletaInicio = fechaInicioPartida[2] + " de "+ mesInicioTexto +" "+ fechaInicioPartida[0]
            fefchaCompletaFinal = fechaFinalPartida[2]+ " de " + mesFinalTexto +" "+ fechaFinalPartida[0]  
            fechaTextoInicioPeriodoAnterior = str(fechaRestaInicio.strftime('%d'))+ " de " + mesRestaInicioTexto +" "+ str(fechaRestaInicio.strftime('%Y'))  
            fechaTextoFinalPeriodoDespues=str(fechaSumaFinal.strftime('%d'))+ " de "+ mesFinalTexto + " de " + str(fechaSumaFinal.strftime('%Y'))
                
            
            if contadorVentasPeriodoAnterior == 0:
                porcentajeVentaPeriodo = 100
            else:
                porcentajeVentaPeriodo = (contadorVentas / contadorVentasPeriodoAnterior)
                porcentajeVentaPeriodo = porcentajeVentaPeriodo - 1
                porcentajeVentaPeriodo = porcentajeVentaPeriodo *100

            if porcentajeVentaPeriodo > 0:
                ventasMayoresPeriodo = True
                
            else:
                ventasMayoresPeriodo = False
                
            #Porcentajes para pie chart.
            
            if tipo == "Administrador":
            #Ventas totales
                ventasTotalesDeEmpleadosEnElPeriodo= Ventas.objects.filter(fecha_venta__range=[fechaInicioFormato,fechaFinalFormato])
            else:
                ventasTotalesDeEmpleadosEnElPeriodo = Ventas.objects.filter(fecha_venta__range=[fechaInicioFormato,fechaFinalFormato], sucursal_id__id_sucursal = idsucursal)
            
            contadorVentasTotalesDelPeriodo = 0
            for ventaMes in ventasTotalesDeEmpleadosEnElPeriodo:
                contadorVentasTotalesDelPeriodo = contadorVentasTotalesDelPeriodo + 1
            if contadorVentasTotalesDelPeriodo == 0:
                porcentajeVentasDelEmpleadoEnElPeriodo = 0
            else:
                porcentajeVentasDelEmpleadoEnElPeriodo = (contadorVentasPeriodo * 100)/contadorVentasTotalesDelPeriodo
            
            porcentajeDemasEmpleadosEnElPeriodo = 100 - porcentajeVentasDelEmpleadoEnElAño
            
            
                
                
            ventasEmpleadoEnElPeriodo2 = Ventas.objects.filter(fecha_venta__range=[fechaInicioFormato,fechaFinalFormato], empleado_vendedor_id__id_empleado = idEmpleadoConfigurar)
            
            #Arreglos RangoFecha Periodo
            sucursalesPeriodo = []
            clientesPeriodo = []
            boolProductosPeriodo = []
            productosPeriodo = []
            boolServCorporalPeriodo= []
            servicioCorporalPeriodo = []
            boolServFacialPeriodo = []
            servicioFacialPeriodo = []
            boolCreditoPeriodo = []
            idsCreditosPeriodo = []
            boolPagadoPeriodo= []
            montosPeriodo = []
            boolDescuentosPeriodo = []
            datosDescuentoPeriodo = []
            costoRealPeriodo = []
            descuentosPeriodo = []
            tipoVentaPeriodo = []
            
            for venta in ventasEmpleadoEnElPeriodo2:
                idVenta = venta.id_venta
                
                #Para tabla de ventas
                sucursal = venta.sucursal_id
                consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursal)
                for suc in consultaSucursal:
                    nombreSucursal = suc.nombre
                sucursalesPeriodo.append(nombreSucursal)
                
                cliente = venta.cliente_id
                if cliente == None:
                    clientesAño.append(["x","Cliente momentaneo"])
                else:
                    consultaCliente = Clientes.objects.filter(id_cliente = cliente)
                    for datoCliente in consultaCliente:
                        nombreCliente = datoCliente.nombre_cliente
                        apellido = datoCliente.apellidoPaterno_cliente
                    
                    nombreCompletoCliente = nombreCliente + " " +apellido
                    
                    clientesPeriodo.append([cliente,nombreCompletoCliente])
                
                #Productos
                codigosProductos = venta.ids_productos      
                if codigosProductos == "":
                    boolProductosPeriodo.append("Sin productos comprados")
                    productosPeriodo.append("x")
                else:
                    boolProductosPeriodo.append("Se compraron productos")
                    cantidadesProductos = venta.cantidades_productos
                    arregloCodigosProductos = codigosProductos.split(",")
                    arregloCantidadesProductos = cantidadesProductos.split(",")
                    
                    listaProductos = zip(arregloCodigosProductos,arregloCantidadesProductos)
                    
                    productitos = []
                    for producto, cantidades in listaProductos:
                        idcodigoProducto = str(producto)
                        cantidad = str(cantidades)
                        
                        if "PV" in idcodigoProducto:
                            #Producto para venta
                            tipoVentaPeriodo.append("Venta")
                            consultaProducto = ProductosVenta.objects.filter(codigo_producto = idcodigoProducto)
                        else:
                            #Producto para renta
                            tipoVentaPeriodo.append("Renta")
                            consultaProducto = ProductosRenta.objects.filter(codigo_producto = idcodigoProducto)
                        
                        for datoProducto in consultaProducto:
                            nombreProducto = datoProducto.nombre_producto
                        productitos.append([idcodigoProducto, nombreProducto,cantidad ])
                    productosPeriodo.append(productitos)
                
                #ServiciosCorporales
                serviciosCorporales = venta.ids_servicios_corporales
                if serviciosCorporales == "":
                    boolServCorporalPeriodo.append("Sin servicios coorporales")
                    servicioCorporalPeriodo.append("x")
                else:
                    boolServCorporalPeriodo.append("Se compraron servicios")
                    cantidadesServiciosCorporales = venta.cantidades_servicios_corporales
                    arregloIdsServiciosCorporales = serviciosCorporales.split(",")
                    arregloCantidadesServiciosCorporales = cantidadesServiciosCorporales.split(",")
                    
                    listaServiciosCorporales = zip(arregloIdsServiciosCorporales,arregloCantidadesServiciosCorporales)
                    
                    serviciosCorporales = []
                    for idServicioCorporal, cantidadServiciosCorporal in listaServiciosCorporales:
                        intId = int(idServicioCorporal)
                        strId = str(idServicioCorporal)
                        cantidad = str(cantidadServiciosCorporal)
                        
                       
                        consultaServicio = Servicios.objects.filter(id_servicio = intId)
                        
                        for datoServicio in consultaServicio:
                            nombreDeServicio = datoServicio.nombre_servicio
                        serviciosCorporales.append([strId, nombreDeServicio,cantidad ])
                    servicioCorporalPeriodo.append(serviciosCorporales)
                
                #ServiciosFaciales
                serviciosFaciales = venta.ids_servicios_faciales #consultamos la id de de servicios faciales
                if serviciosFaciales == "": #Si serviciosFaciales está vacía agregaremos dos campos a los arreglos que no hay servicios faciales
                    boolServFacialPeriodo.append("Sin servicios faciales")
                    servicioFacialPeriodo.append("x")
                else:
                    boolServFacialPeriodo.append("Se compraron servicios") #Si el campo no está vacío agregaremos en el arreglo, que se compraron servicios
                    cantiadesServiciosFaciales = venta.cantidades_servicios_faciales #Ahora tomaremos de venta las cantidades de servicios faciales
                    arregloIdsServiciosFaciales = serviciosFaciales.split(",") #Ahora juntaremos las id en un arreglo divididas entre comas
                    arregloCantidadesServiciosFaciales = cantiadesServiciosFaciales.split(",")#Haremos lo mismo pero ahora con las cantidades
                    
                    listaServiciosFaciales = zip(arregloIdsServiciosFaciales, arregloCantidadesServiciosFaciales)#Ahora haremos un arreglo contatenando los dos arreglos
                    
                    serviciosFaciales = [] #creamos un arreglo vacío
                    for idServiciosFacial, cantidadServicioFacial in listaServiciosFaciales: #hacemos un ciclo for el cual tome las id 
                        intId = int(idServiciosFacial)  	    #y cantidad de nuestro arreglo recién zipeado y nos regrese los valores en entero y string
                        strId = str(idServiciosFacial)          #de las Id Para usarlos después y de la cantidad en string
                        cantidad = str(cantidadServicioFacial)  
                        
                       
                        consultaServicio = Servicios.objects.filter(id_servicio = intId)
                        
                        for datoServicio in consultaServicio:
                            nombreDeServicio = datoServicio.nombre_servicio
                        serviciosFaciales.append([strId, nombreDeServicio,cantidad ])
                    servicioFacialPeriodo.append(serviciosFaciales)
                credito = venta.credito
                if credito == "S":
                    boolCreditoPeriodo.append("Si")
                    consultaCredito = Creditos.objects.filter(venta_id__id_venta = idVenta)
                    if consultaCredito:
                        for datoCredito in consultaCredito:
                            idCredito = datoCredito.id_credito
                            restante = datoCredito.monto_restante
                        idsCreditosPeriodo.append(idCredito)
                        if restante == 0:
                            boolPagadoPeriodo.append("Si")
                        else:
                            boolPagadoPeriodo.append("No")
                    else:
                        idsCreditosPeriodo.append("error")
                        
                else:
                    boolCreditoPeriodo.append("No")
                    idsCreditosPeriodo.append("No")
                    boolPagadoPeriodo.append("No")
                
                montoPagado = venta.monto_pagar
                montosPeriodo.append(montoPagado)
                
                descuento = venta.descuento_id
                if descuento == None:
                    boolDescuentosPeriodo.append("Sin descuento")
                    datosDescuentoPeriodo.append("Sin descuento")
                    descuentosPeriodo.append("Sin descuento")
                    costoRealPeriodo.append("Sin descuento")
                else:
                    boolDescuentosPeriodo.append("Con descuento")
                    consultaDescuento = Descuentos.objects.filter(id_descuento = descuento)
                    for datoDescuento in consultaDescuento:
                        nombreDescuento = datoDescuento.nombre_descuento
                        porcentajeDescuento = datoDescuento.porcentaje
                    porcentajeTotalDescuento = 100 - float(porcentajeDescuento)
                    totalDescuento = (100*montoPagado)/porcentajeTotalDescuento
                    totalSinDescuento = montoPagado + totalDescuento
                
                
                    datosDescuentoPeriodo.append([porcentajeDescuento,nombreDescuento])
                    descuentosPeriodo.append(totalDescuento)
                    costoRealPeriodo.append(totalSinDescuento)

                    
                
            listaVentasPeriodo = zip(ventasEmpleadoEnElPeriodo2, sucursalesPeriodo, clientesPeriodo,boolProductosPeriodo,productosPeriodo, boolServCorporalPeriodo, servicioCorporalPeriodo
                                 , boolServFacialPeriodo, servicioFacialPeriodo, boolCreditoPeriodo, idsCreditosPeriodo, boolPagadoPeriodo, montosPeriodo, boolDescuentosPeriodo
                                 , datosDescuentoPeriodo, descuentosPeriodo, costoRealPeriodo, tipoVentaPeriodo)
              
            
            
            

            return render(request, "3 Empleados/informeEmpleado.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado, "idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado,
        "nombres":nombres,"apellidoPaterno":apellidoPaterno, "apellidoMaterno":apellidoMaterno, "telefono":telefono,
        "puesto":puesto, "nombreUsuario":nombreUsuario, "letrasEmpleado":letrasEmpleado, "tipo":tipo,"sucursalEmpleado":sucursalEmpleado, "idsucursal":idsucursal, "idEmpleadoEditar2":idEmpleadoEditar2, "activo":activo, "fecha_alta":fecha_alta, 
        "fecha_baja":fecha_baja, "idEmpleadoEditar3":idEmpleadoEditar3, "idEmpleadoEditar4":idEmpleadoEditar4, "totalVentas":totalVentas, "contadorVentas":contadorVentas,"notificacionRenta":notificacionRenta,
        "diadehoy":diadehoy,"mesdehoy":mesdehoy,"añoHoy":añoHoy, "ventasEnElMesActual":ventasEnElMesActual, "ventasEnElMesAnterior":ventasEnElMesAnterior, "mesAnteriorTexto":mesAnteriorTexto, "ventasEnElMesEsMayorAlMesAnterior":ventasEnElMesEsMayorAlMesAnterior,"porcentajeVentasMes":porcentajeVentasMes,
        "ventasEnEnLaSemana":ventasEnEnLaSemana, "ventasEnEnLaSemanaAnterior":ventasEnEnLaSemanaAnterior, "porcentajeVentasSemanal":porcentajeVentasSemanal, "ventasEnLaSemanaEsMayorALaSemanaAnterior":ventasEnLaSemanaEsMayorALaSemanaAnterior,
        "contadorVentasEnero":contadorVentasEnero, "contadorVentasFebrero":contadorVentasFebrero, "contadorVentasMarzo":contadorVentasMarzo,
        "contadorVentasAbril":contadorVentasAbril, "contadorVentasMayo":contadorVentasMayo, "contadorVentasJunio":contadorVentasJunio, "contadorVentasJulio":contadorVentasJulio,
        "contadorVentasAgosto":contadorVentasAgosto, "contadorVentasSeptiembre":contadorVentasSeptiembre, "contadorVentasOctubre":contadorVentasOctubre,
        "contadorVentasNoviembre":contadorVentasNoviembre, "contadorVentasDiciembre":contadorVentasDiciembre, "porcentajeVentasDelEmpleado":porcentajeVentasDelEmpleado, "porcentajeDemasEmpleados":porcentajeDemasEmpleados, "contadorVentasTotalesMes":contadorVentasTotalesMes,
        "listaVentasMes":listaVentasMes, "montoVentasEnElMesActual":montoVentasEnElMesActual, "montoTotalDeVentaMesAnterior":montoTotalDeVentaMesAnterior, "porcentajeMontoVentas":porcentajeMontoVentas, "esteMesVendioMas":esteMesVendioMas,
        "contadorVentasEnElAño":contadorVentasEnElAño, "contadorVentasEnElAñoAnterior":contadorVentasEnElAñoAnterior, "porcentajeVentaAnual":porcentajeVentaAnual, "ventasMayores":ventasMayores,
        "primerAñoAntes":primerAñoAntes, "segundoAñoAntes":segundoAñoAntes, "tercerAñoAntes":tercerAñoAntes, "contadorVentasHaceDosAños":contadorVentasHaceDosAños, "contadorVentasHaceTresAños":contadorVentasHaceTresAños,
        "porcentajeVentasDelEmpleadoEnElAño":porcentajeVentasDelEmpleadoEnElAño, "porcentajeDemasEmpleadosEnElAño":porcentajeDemasEmpleadosEnElAño,
        "montoVentaEnElAño":montoVentaEnElAño, "montoVentaEnElAñoAnterior":montoVentaEnElAñoAnterior, "porcentajeMontoVentaAnual":porcentajeMontoVentaAnual, "esteAñoVendioMas":esteAñoVendioMas, "listaVentasAño":listaVentasAño,
        "rangoFechasEmpleado":rangoFechasEmpleado, "rangoFechasEmpleado2":rangoFechasEmpleado2, "fefchaCompletaInicio":fefchaCompletaInicio, "fefchaCompletaFinal":fefchaCompletaFinal, "contadorVentasPeriodo":contadorVentasPeriodo, "montoVentaPeriodo":montoVentaPeriodo, "contadorVentasPeriodoAnterior":contadorVentasPeriodoAnterior, "montoVentaPeriodoAnterior":montoVentaPeriodoAnterior, "contadorVentasPeriodoSiguiente":contadorVentasPeriodoSiguiente, "montoVentaPeriodoSiguiente":montoVentaPeriodoSiguiente, "fechaTextoInicioPeriodoAnterior":fechaTextoInicioPeriodoAnterior, "idEmpleadoConfigurar":idEmpleadoConfigurar,"fechaTextoFinalPeriodoDespues":fechaTextoFinalPeriodoDespues,
        "ventasMayoresPeriodo":ventasMayoresPeriodo, "porcentajeVentasDelEmpleadoEnElPeriodo":porcentajeVentasDelEmpleadoEnElPeriodo, "porcentajeDemasEmpleadosEnElPeriodo":porcentajeDemasEmpleadosEnElPeriodo,
        "contadorVentasTotalesDelPeriodo":contadorVentasTotalesDelPeriodo, "porcentajeVentaPeriodo":porcentajeVentaPeriodo, "listaVentasPeriodo":listaVentasPeriodo, "notificacionCita":notificacionCita})

        return redirect('/verEmpleados/')
    else:
        return render(request,"1 Login/login.html")

def informeDeSucursal(request):
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
            idSucursalInforme = request.POST['idSucursalInforme']
            
            rangoFechaRecibida = False
            if 'fechaInicioRango' in request.POST:
                rangoFechaRecibida = True
                fechaInicioRango = request.POST['fechaInicioRango']
                fechaFinalRango = request.POST['fechaFinalRango']
                
            
            consultaSucursal = Sucursales.objects.filter(id_sucursal = idSucursalInforme)
            for datoConsulta in consultaSucursal:
                nombreSucursal = datoConsulta.nombre
                direccion = datoConsulta.direccion
                telefono = datoConsulta.telefono
                latitud = datoConsulta.latitud
                longitud = datoConsulta.longitud
            
            hoy = datetime.now()
        
            mesdehoynumero = hoy.strftime('%m')
            
            mesesDic = {
                "01":'Enero',
                "02":'Febrero',
                "03":'Marzo',
                "04":'Abril',
                "05":'Mayo',
                "06":'Junio',
                "07":'Julio',
                "08":'Agosto',
                "09":'Septiembre',
                "10":'Octubre',
                "11":'Noviembre',
                "12":'Diciembre'
            }
            
            diasMeses = {
            'Enero':'31',
            'Febrero':'28',
            'Marzo':'31',
            'Abril':'30',
            'Mayo':'31',
            'Junio':'30',
            'Julio':'31',
            'Agosto':'31',
            'Septiembre':'30',
            'Octubre':'31',
            'Noviembre':'30',
            'Diciembre':'31'
            }
            
            #fecha para mes actual en texto
            diadehoy = hoy.strftime('%d')
            mesdehoy = mesesDic[str(mesdehoynumero)]
            añoHoy = hoy.strftime('%Y')
            
            #fecha mes actual en formato
            fechaDiaMesActual = añoHoy+"-"+mesdehoynumero+"-"+diadehoy
            fechaInicioMesActual = añoHoy+"-"+mesdehoynumero+"-01" 
            
            fechaPrimerDiaDelAñoActual = añoHoy +"-01-01"
            fechaUltimoDiaDelAñoActual = añoHoy+"-12-31"
            
            
            #Ingresos totales del mes actual, en, tre entascreditos y rentas
            
            montoIngresoSucursalMes = 0
            
            contadorVentasSucursalMes = 0
            contadorRentasSucursalMes = 0
            contadorCreditosSucursalMes = 0
            
            numeroVentasSucursalMes = 0
            numeroRentasSucursalMes = 0
            numeroCreditosSucursalMes = 0
            
            consultaVentasSucursalMes = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual], credito="N", sucursal = idSucursalInforme)
            
            if consultaVentasSucursalMes:
                for ventaRealizada in consultaVentasSucursalMes:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoSucursalMes = montoIngresoSucursalMes + montoVenta
                    contadorVentasSucursalMes = contadorVentasSucursalMes + montoVenta
                    numeroVentasSucursalMes = numeroVentasSucursalMes + 1
            
            consultaCreditosSucursalMes = Creditos.objects.filter(fecha_venta_credito__range=[fechaInicioMesActual,fechaDiaMesActual], renta_id__isnull=True, sucursal = idSucursalInforme)
        
            if consultaCreditosSucursalMes:
                for crceditoRealizado in consultaCreditosSucursalMes:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoSucursalMes = montoIngresoSucursalMes + montoPagadoCredito
                    contadorRentasSucursalMes = contadorRentasSucursalMes + montoPagadoCredito
                    numeroCreditosSucursalMes = numeroCreditosSucursalMes +1
                    
            consultaRentasMesActual = Rentas.objects.filter(fecha_apartado__range=[fechaInicioMesActual,fechaDiaMesActual])
        
            if consultaRentasMesActual:
                for rentaRealizada in consultaRentasMesActual:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado 
                                    montoIngresoSucursalMes = montoIngresoSucursalMes + sumaPagosRenta

                                    contadorCreditosSucursalMes = contadorCreditosSucursalMes + sumaPagosRenta
                                    numeroRentasSucursalMes = numeroRentasSucursalMes +1
                                    
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoSucursalMes = montoIngresoSucursalMes + sumaPagosRenta

                            contadorCreditosSucursalMes = contadorCreditosSucursalMes + sumaPagosRenta
                            numeroRentasSucursalMes = numeroRentasSucursalMes +1
                        
            #Mes anterior
            haceUnMes = hoy - relativedelta(months=1)  #2022-05-07
            mesHaceUnMes = haceUnMes.strftime('%m') #05
            añoHaceUnMes = haceUnMes.strftime('%Y')
            mesHaceUnMesLetra = mesesDic[str(mesHaceUnMes)]
            
            diasDeUltimoMes = diasMeses[str(mesHaceUnMesLetra)]
            
            fechaPrimerDiaMesAnterior = añoHaceUnMes + "-"+mesHaceUnMes+"-01"   
            fechaUltimoDiaMesAnterior = añoHaceUnMes + "-"+mesHaceUnMes+"-"+diasDeUltimoMes 
            
            #Ingresos totales de mes actual, ventas, creditos y rentas
            consultaVentasSucursalMesAnterior = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaMesAnterior,fechaUltimoDiaMesAnterior], credito="N", sucursal = idSucursalInforme)
            
            montoIngresoMesSucursalAnterior = 0
            
            if consultaVentasSucursalMesAnterior:
                for ventaRealizada in consultaVentasSucursalMesAnterior:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoMesSucursalAnterior = montoIngresoMesSucursalAnterior + montoVenta
            
            consultaCreditosSucursalMesAnterior = Creditos.objects.filter(fecha_venta_credito__range=[fechaPrimerDiaMesAnterior,fechaUltimoDiaMesAnterior],  renta_id__isnull=True, sucursal = idSucursalInforme)
            
            if consultaCreditosSucursalMesAnterior:
                for crceditoRealizado in consultaCreditosSucursalMesAnterior:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoMesSucursalAnterior = montoIngresoMesSucursalAnterior + montoPagadoCredito
                
            consultaRentasSucursalMesAnterior = Rentas.objects.filter(fecha_apartado__range=[fechaPrimerDiaMesAnterior,fechaUltimoDiaMesAnterior])
            
            if consultaRentasSucursalMesAnterior:
                for rentaRealizada in consultaRentasSucursalMesAnterior:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    montoIngresoMesSucursalAnterior = montoIngresoSucursalMes + sumaPagosRenta

                                  
                                    
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoMesSucursalAnterior = montoIngresoSucursalMes + sumaPagosRenta

                            
            #comparativa de ingresos totales mensuales

            esMayor = False

            if montoIngresoMesSucursalAnterior == 0:
                porcentajeIngresosSucursalMes = 100
            else:
                porcentajeIngresosSucursalMes = (montoIngresoSucursalMes / montoIngresoMesSucursalAnterior)
                porcentajeIngresosSucursalMes = porcentajeIngresosSucursalMes - 1
                porcentajeIngresosSucursalMes = porcentajeIngresosSucursalMes *100
                
                
            if porcentajeIngresosSucursalMes > 0:
                esMayor = True
                
            else:
                esMayor = False
            porcentajeIngresosSucursalMes = round(porcentajeIngresosSucursalMes,2)
            
            #Ingresos por mes de la sucursal
            #Fechas para chart de meses
            inicioMesEnero = añoHoy+"-01-01"
            finMesEnero = añoHoy+"-01-31"
            consultaVentasEnero = Ventas.objects.filter(fecha_venta__range=[inicioMesEnero,finMesEnero], credito="N", sucursal = idSucursalInforme)
            montoIngresoEnero = 0
            if consultaVentasEnero:
                for ventaRealizada in consultaVentasEnero:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoEnero = montoIngresoEnero + montoVenta
            consultaCreditosEnero = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesEnero,finMesEnero],  renta_id__isnull=True, sucursal = idSucursalInforme)
            if consultaCreditosEnero:
                for crceditoRealizado in consultaCreditosEnero:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoEnero = montoIngresoEnero + montoPagadoCredito
            consultaRentasEnero = Rentas.objects.filter(fecha_apartado__range=[inicioMesEnero,finMesEnero])
            if  consultaRentasEnero:
                for rentaRealizada in consultaRentasFebrero:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    montoIngresoEnero = montoIngresoEnero + sumaPagosRenta
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoEnero = montoIngresoEnero + sumaPagosRenta
        
        
        
            inicioMesFebrero = añoHoy+"-02-01"
            finMesFebrero = añoHoy+"-02-28"
            consultaVentasFebrero = Ventas.objects.filter(fecha_venta__range=[inicioMesFebrero,finMesFebrero], credito="N", sucursal = idSucursalInforme)
            montoIngresoFebrero = 0
            if consultaVentasFebrero:
                for ventaRealizada in consultaVentasFebrero:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoFebrero = montoIngresoFebrero + montoVenta
            consultaCreditosFebrero = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesFebrero,finMesFebrero],  renta_id__isnull=True, sucursal = idSucursalInforme)
            if consultaCreditosFebrero:
                for crceditoRealizado in consultaCreditosFebrero:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoFebrero = montoIngresoFebrero + montoPagadoCredito
            consultaRentasFebrero = Rentas.objects.filter(fecha_apartado__range=[inicioMesFebrero,finMesFebrero])
            if consultaRentasFebrero:
                for rentaRealizada in consultaRentasFebrero:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    montoIngresoFebrero = montoIngresoFebrero + sumaPagosRenta
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoFebrero = montoIngresoFebrero + sumaPagosRenta
            
            inicioMesMarzo = añoHoy+"-03-01"
            finMesMarzo = añoHoy+"-03-31"
            consultaVentasMarzo = Ventas.objects.filter(fecha_venta__range=[inicioMesMarzo,finMesMarzo], credito="N", sucursal = idSucursalInforme)
            montoIngresoMarzo = 0
            if consultaVentasMarzo:
                for ventaRealizada in consultaVentasMarzo:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoMarzo = montoIngresoMarzo + montoVenta
            consultaCreditosMarzo = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesMarzo,finMesMarzo],  renta_id__isnull=True, sucursal = idSucursalInforme)
            if consultaCreditosMarzo:
                for crceditoRealizado in consultaCreditosMarzo:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoMarzo = montoIngresoMarzo + montoPagadoCredito
            consultaRentasMarzo = Rentas.objects.filter(fecha_apartado__range=[inicioMesMarzo,finMesMarzo])
            if consultaRentasMarzo:
                for rentaRealizada in consultaRentasMarzo:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    montoIngresoMarzo = montoIngresoMarzo + sumaPagosRenta
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoMarzo = montoIngresoMarzo + sumaPagosRenta
            
            inicioMesAbril = añoHoy+"-04-01"
            finMesAbril = añoHoy+"-04-30"
            consultaVentasAbril = Ventas.objects.filter(fecha_venta__range=[inicioMesAbril,finMesAbril], credito="N", sucursal = idSucursalInforme)
            montoIngresoAbril = 0
            if consultaVentasAbril:
                for ventaRealizada in consultaVentasAbril:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoAbril = montoIngresoAbril + montoVenta
            consultaCreditosAbril = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesAbril,finMesAbril],  renta_id__isnull=True, sucursal = idSucursalInforme)
            if consultaCreditosAbril:
                for crceditoRealizado in consultaCreditosAbril:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoAbril = montoIngresoAbril + montoPagadoCredito
            consultaRentasAbril = Rentas.objects.filter(fecha_apartado__range=[inicioMesAbril,finMesAbril])
            if consultaRentasAbril:
                for rentaRealizada in consultaRentasAbril:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    montoIngresoAbril = montoIngresoAbril + sumaPagosRenta
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoAbril = montoIngresoAbril + sumaPagosRenta
            
            inicioMesMayo = añoHoy+"-05-01"
            finMesMayo = añoHoy+"-05-31"
            consultaVentasMayo = Ventas.objects.filter(fecha_venta__range=[inicioMesMayo,finMesMayo], credito="N", sucursal = idSucursalInforme)
            montoIngresoMayo = 0
            if consultaVentasMayo:
                for ventaRealizada in consultaVentasMayo:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoMayo = montoIngresoMayo + montoVenta
            consultaCreditosMayo = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesMayo,finMesMayo],  renta_id__isnull=True, sucursal = idSucursalInforme)
            if consultaCreditosMayo:
                for crceditoRealizado in consultaCreditosMayo:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoMayo = montoIngresoMayo + montoPagadoCredito
            consultaRentasMayo = Rentas.objects.filter(fecha_apartado__range=[inicioMesMayo,finMesMayo])
            if consultaRentasMayo:
                for rentaRealizada in consultaRentasMayo:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    montoIngresoMayo = montoIngresoMayo + sumaPagosRenta
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoMayo = montoIngresoMayo + sumaPagosRenta
            
            inicioMesJunio = añoHoy+"-06-01"
            finMesJunio = añoHoy+"-06-30"
            consultaVentasJunio = Ventas.objects.filter(fecha_venta__range=[inicioMesJunio,finMesJunio], credito="N", sucursal = idSucursalInforme)
            montoIngresoJunio = 0
            if consultaVentasJunio:
                for ventaRealizada in consultaVentasJunio:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoJunio = montoIngresoJunio + montoVenta
            consultaCreditosJunio = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesJunio,finMesJunio],  renta_id__isnull=True, sucursal = idSucursalInforme)
            if consultaCreditosJunio:
                for crceditoRealizado in consultaCreditosJunio:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoJunio = montoIngresoJunio + montoPagadoCredito
            consultaRentasJunio = Rentas.objects.filter(fecha_apartado__range=[inicioMesJunio,finMesJunio])
            if consultaRentasJunio:
                for rentaRealizada in consultaRentasJunio:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    montoIngresoJunio = montoIngresoJunio + sumaPagosRenta
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoJunio = montoIngresoJunio + sumaPagosRenta
            
            inicioMesJulio = añoHoy+"-07-01"
            finMesJulio = añoHoy+"-07-31"
            consultaVentasJulio = Ventas.objects.filter(fecha_venta__range=[inicioMesJulio,finMesJulio], credito="N", sucursal = idSucursalInforme)
            montoIngresoJulio = 0
            if consultaVentasJulio:
                for ventaRealizada in consultaVentasJulio:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoJulio = montoIngresoJulio + montoVenta
            consultaCreditosJulio = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesJulio,finMesJulio],  renta_id__isnull=True, sucursal = idSucursalInforme)
            if consultaCreditosJulio:
                for crceditoRealizado in consultaCreditosJulio:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoJulio = montoIngresoJulio + montoPagadoCredito
            consultaRentasJulio = Rentas.objects.filter(fecha_apartado__range=[inicioMesJulio,finMesJulio])
            if consultaRentasJulio:
                for rentaRealizada in consultaRentasJulio:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    montoIngresoJulio = montoIngresoJulio + sumaPagosRenta
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoJulio = montoIngresoJulio + sumaPagosRenta
            
            inicioMesAgosto = añoHoy+"-08-01"
            finMesAgosto = añoHoy+"-08-31"
            consultaVentasAgosto = Ventas.objects.filter(fecha_venta__range=[inicioMesAgosto,finMesAgosto], credito="N", sucursal = idSucursalInforme)
            montoIngresoAgosto = 0
            if consultaVentasAgosto:
                for ventaRealizada in consultaVentasAgosto:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoAgosto = montoIngresoAgosto + montoVenta
            consultaCreditosAgosto = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesAgosto,finMesAgosto],  renta_id__isnull=True, sucursal = idSucursalInforme)
            if consultaCreditosAgosto:
                for crceditoRealizado in consultaCreditosAgosto:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoAgosto = montoIngresoAgosto + montoPagadoCredito
            consultaRentasAgosto = Rentas.objects.filter(fecha_apartado__range=[inicioMesAgosto,finMesAgosto])
            if consultaRentasAgosto:
                for rentaRealizada in consultaRentasAgosto:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado 
                                    montoIngresoAgosto = montoIngresoAgosto + sumaPagosRenta
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoAgosto = montoIngresoAgosto + sumaPagosRenta
            
            inicioMesSeptiembre = añoHoy+"-09-01"
            finMesSeptiembre = añoHoy+"-09-30"
            consultaVentasSeptiembre = Ventas.objects.filter(fecha_venta__range=[inicioMesSeptiembre,finMesSeptiembre], credito="N", sucursal = idSucursalInforme)
            montoIngresoSeptiembre = 0
            if consultaVentasSeptiembre:
                for ventaRealizada in consultaVentasSeptiembre:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoSeptiembre = montoIngresoSeptiembre + montoVenta
            consultaCreditosSeptiembre = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesSeptiembre,finMesSeptiembre],  renta_id__isnull=True, sucursal = idSucursalInforme)
            if consultaCreditosSeptiembre:
                for crceditoRealizado in consultaCreditosSeptiembre:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoSeptiembre = montoIngresoSeptiembre + montoPagadoCredito
            consultaRentasSeptiembre = Rentas.objects.filter(fecha_apartado__range=[inicioMesSeptiembre,finMesSeptiembre])
            if consultaRentasSeptiembre:
                for rentaRealizada in consultaRentasSeptiembre:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    montoIngresoSeptiembre = montoIngresoSeptiembre + sumaPagosRenta
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoSeptiembre = montoIngresoSeptiembre + sumaPagosRenta
            
            inicioMesOctubre = añoHoy+"-10-01"
            finMesOctubre = añoHoy+"-10-31"
            consultaVentasOctubre = Ventas.objects.filter(fecha_venta__range=[inicioMesOctubre,finMesOctubre], credito="N", sucursal = idSucursalInforme)
            montoIngresoOctubre = 0
            if consultaVentasOctubre:
                for ventaRealizada in consultaVentasOctubre:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoOctubre = montoIngresoOctubre + montoVenta
            consultaCreditosOctubre = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesOctubre,finMesOctubre],  renta_id__isnull=True, sucursal = idSucursalInforme)
            if consultaCreditosOctubre:
                for crceditoRealizado in consultaCreditosOctubre:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoOctubre = montoIngresoOctubre + montoPagadoCredito
            consultaRentasOctubre = Rentas.objects.filter(fecha_apartado__range=[inicioMesOctubre,finMesOctubre])
            if consultaRentasOctubre:
                for rentaRealizada in consultaRentasOctubre:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado 
                                    montoIngresoOctubre = montoIngresoOctubre + sumaPagosRenta
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoOctubre = montoIngresoOctubre + sumaPagosRenta
            
            inicioMesNoviembre = añoHoy+"-11-01"
            finMesNoviembre = añoHoy+"-11-30"
            consultaVentasNoviembre = Ventas.objects.filter(fecha_venta__range=[inicioMesNoviembre,finMesNoviembre], credito="N", sucursal = idSucursalInforme)
            montoIngresoNoviembre = 0
            if consultaVentasNoviembre:
                for ventaRealizada in consultaVentasNoviembre:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoNoviembre = montoIngresoNoviembre + montoVenta
            consultaCreditosNoviembre = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesNoviembre,finMesNoviembre],  renta_id__isnull=True, sucursal = idSucursalInforme)
            if consultaCreditosNoviembre:
                for crceditoRealizado in consultaCreditosNoviembre:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoNoviembre = montoIngresoNoviembre + montoPagadoCredito
            consultaRentasNoviembre = Rentas.objects.filter(fecha_apartado__range=[inicioMesNoviembre,finMesNoviembre])
            if consultaRentasNoviembre:
                for rentaRealizada in consultaRentasNoviembre:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    montoIngresoNoviembre = montoIngresoNoviembre + sumaPagosRenta
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoNoviembre = montoIngresoNoviembre + sumaPagosRenta
            
            inicioMesDiciembre = añoHoy+"-12-01"
            finMesDiciembre = añoHoy+"-12-31"
            consultaVentasDiciembre = Ventas.objects.filter(fecha_venta__range=[inicioMesDiciembre,finMesDiciembre], credito="N", sucursal = idSucursalInforme)
            montoIngresoDiciembre = 0
            if consultaVentasDiciembre:
                for ventaRealizada in consultaVentasDiciembre:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoDiciembre = montoIngresoDiciembre + montoVenta
            consultaCreditosDiciembre = Creditos.objects.filter(fecha_venta_credito__range=[inicioMesDiciembre,finMesDiciembre],  renta_id__isnull=True, sucursal = idSucursalInforme)
            if consultaCreditosDiciembre:
                for crceditoRealizado in consultaCreditosDiciembre:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoDiciembre = montoIngresoDiciembre + montoPagadoCredito
            consultaRentasDiciembre = Rentas.objects.filter(fecha_apartado__range=[inicioMesDiciembre,finMesDiciembre])
            if consultaRentasDiciembre:
                for rentaRealizada in consultaRentasDiciembre:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    montoIngresoDiciembre = montoIngresoDiciembre + sumaPagosRenta
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado 
                            montoIngresoDiciembre = montoIngresoDiciembre + sumaPagosRenta
                            
            # - COMPRAS DEL MEES ...................................................
            totalComprasMesGasto = 0
            totalComprasMesVenta = 0
            totalComprasMesRenta= 0
            
            numeroComprasGasto = 0
            numeroComprasVenta = 0
            numeroComprasRenta = 0
            
            comprasProductosGastosSucursalMes= []
            comprasGastoSucursalDelMes = ComprasGastos.objects.filter(fecha_compra__range=[fechaInicioMesActual,fechaDiaMesActual])
            if comprasGastoSucursalDelMes:
                for compra in comprasGastoSucursalDelMes:
                    montoComprado = compra.total_costoCompra
                    
                    
                    idCompra = compra.id_compraGasto
                    idProducto = compra.id_productoComprado_id
                    consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                    
                    for datoProducto in consultaProducto:
                        nombreProducto = datoProducto.nombre_producto
                        codigoProducto = datoProducto.codigo_producto
                        imagenProducto = datoProducto.imagen_producto
                        sucursalProducto = datoProducto.sucursal_id
                    nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                    
                    fechaCompra = compra.fecha_compra
                    costoUnitarioCompra = compra.costo_unitario
                    cantidadComprada = compra.cantidad_comprada
                    totalMontoCompra = compra.total_costoCompra
                    
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                    
                    idSucursalInforme = int(idSucursalInforme)
                    
                    if sucursalProducto == idSucursalInforme:
                        totalComprasMesGasto = totalComprasMesGasto + montoComprado
                        numeroComprasGasto = numeroComprasGasto +1
                        comprasProductosGastosSucursalMes.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursal,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
            else:
                comprasProductosGastosSucursalMes = None
                
            
            comprasProductosVentasSucursalMes = []
            comprasVentaSucursalDelMes = ComprasVentas.objects.filter(fecha_compra__range=[fechaInicioMesActual,fechaDiaMesActual])
            if comprasVentaSucursalDelMes:
                for compra in comprasVentaSucursalDelMes:
                    montoComprado = compra.total_costoCompra
                   
                    
                    idCompra = compra.id_compraVenta
                    idProducto = compra.id_productoComprado_id
                    consultaProducto = ProductosVenta.objects.filter(id_producto = idProducto)
                    
                    for datoProducto in consultaProducto:
                        nombreProducto = datoProducto.nombre_producto
                        codigoProducto = datoProducto.codigo_producto
                        imagenProducto = datoProducto.imagen_producto
                        sucursalProducto = datoProducto.sucursal_id
                    nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                    
                    fechaCompra = compra.fecha_compra
                    costoUnitarioCompra = compra.costo_unitario
                    cantidadComprada = compra.cantidad_comprada
                    totalMontoCompra = compra.total_costoCompra
                    
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        
                    idSucursalInforme = int(idSucursalInforme)
                    
                    if sucursalProducto == idSucursalInforme:
                        totalComprasMesVenta = totalComprasMesVenta + montoComprado
                        numeroComprasVenta = numeroComprasVenta +1
                        comprasProductosVentasSucursalMes.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursal,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
            else:
                comprasProductosVentasSucursalMes = None
            
            
            comprasProductosRentasSucursalMes = []
            comprasRentasSucursalesDelMes = ComprasRentas.objects.filter(fecha_compra__range=[fechaInicioMesActual,fechaDiaMesActual])
            if comprasRentasSucursalesDelMes:
                for compra in comprasRentasSucursalesDelMes:
                    montoComprado = compra.total_costoCompra
                    
                    
                    idCompra = compra.id_compraRenta
                    idProducto = compra.id_productoComprado_id
                    consultaProducto = ProductosRenta.objects.filter(id_producto = idProducto)
                    
                    for datoProducto in consultaProducto:
                        nombreProducto = datoProducto.nombre_producto
                        codigoProducto = datoProducto.codigo_producto
                        imagenProducto = datoProducto.imagen_producto
                        sucursalProducto = datoProducto.sucursal_id
                    nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                    
                    fechaCompra = compra.fecha_compra
                    costoUnitarioCompra = compra.costo_unitario
                    cantidadComprada = compra.cantidad_comprada
                    totalMontoCompra = compra.total_costoCompra
                    
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                    for datoSucursal in consultaSucursal:
                        nombreSucursal = datoSucursal.nombre
                        
                    idSucursalInforme = int(idSucursalInforme)
                    
                    if sucursalProducto == idSucursalInforme:
                        totalComprasMesRenta = totalComprasMesRenta + montoComprado
                        numeroComprasRenta = numeroComprasRenta +1
                        comprasProductosRentasSucursalMes.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursal,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
            else:
                comprasProductosRentasSucursalMes = None            

            sumaTotalesCompras = totalComprasMesGasto + totalComprasMesVenta + totalComprasMesRenta
            
            utilidadSucursalMes = montoIngresoSucursalMes - sumaTotalesCompras
            
            utilidadMayor = False
            if utilidadSucursalMes < 0:
                utilidadMayor = False
            else:
                utilidadMayor = True
                
            #Tabla de ganancias por sucursales
            sucursales = Sucursales.objects.all()
            infoSucursales = []
            montosVendidos =[]
            montosCompras = []
            gananciaSucursales = []
            margenDeGanancia = []
            
            for sucursal in sucursales:
                idSucursal = sucursal.id_sucursal
                nombre = sucursal.nombre
                
                infoSucursales.append([idSucursal,nombre])
                #ventas
                consultaVentas = Ventas.objects.filter(fecha_venta__range=[fechaInicioMesActual,fechaDiaMesActual], credito="N", sucursal = idSucursal)
                montoIngresoSucursalMesTabla = 0
                
                if consultaVentas:
                    for ventaRealizada in consultaVentas:
                        montoVenta = ventaRealizada.monto_pagar
                        montoIngresoSucursalMesTabla = montoIngresoSucursalMesTabla + montoVenta
            
                consultaCreditos = Creditos.objects.filter(fecha_venta_credito__range=[fechaInicioMesActual,fechaDiaMesActual], renta_id__isnull=True, sucursal = idSucursal)
            
                if consultaCreditos:
                    for crceditoRealizado in consultaCreditos:
                        montoPagadoCredito = crceditoRealizado.monto_pagado
                        montoIngresoSucursalMesTabla = montoIngresoSucursalMesTabla + montoPagadoCredito
                        
                consultaRentas = Rentas.objects.filter(fecha_apartado__range=[fechaInicioMesActual,fechaDiaMesActual])
        
                if consultaRentas:
                    for rentaRealizada in consultaRentas:
                        empleadoQueRealizo = rentaRealizada.realizado_por_id
                        consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                        for datoEmpleado in consultaEmpleado:
                            idSucursalEmpleado = datoEmpleado.id_sucursal_id
                        if idSucursalEmpleado == None:
                            codigosProductosRentados = rentaRealizada.codigos_productos_renta
                            arregloCodigosProductos = codigosProductosRentados.split("-")
                            
                            contadorProductosRentados = 0
                            for producto in arregloCodigosProductos:
                                contadorProductosRentados = contadorProductosRentados + 1
                                strCodigoProducto = str(producto)
                                if contadorProductosRentados == 1:
                                    consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                    for datoProducto in consultaProducto:
                                        sucursalProducto = datoProducto.sucursal_id
                                    intSucursalInforme = int(idSucursalInforme)
                                    if sucursalProducto == intSucursalInforme:
                                
                                        montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                        montoPagadoRestante = rentaRealizada.monto_restante
                                        
                                        sumaPagosRenta = 0
                                        if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                            sumaPagosRenta = rentaRealizada.monto_total_renta
                                        else: #Si ya se pago el restante
                                            sumaPagosRenta = montoPagadoApartado
                                        montoIngresoSucursalMesTabla = montoIngresoSucursalMesTabla + sumaPagosRenta

                                        
                        else:
                            intSucursalInforme = int(idSucursalInforme)
                            if idSucursalEmpleado == intSucursalInforme:
                                
                                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                montoPagadoRestante = rentaRealizada.monto_restante
                                
                                sumaPagosRenta = 0
                                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                    sumaPagosRenta = rentaRealizada.monto_total_renta
                                else: #Si ya se pago el restante
                                    sumaPagosRenta = montoPagadoApartado
                                montoIngresoSucursalMesTabla = montoIngresoSucursalMesTabla + sumaPagosRenta
                                
                
                
                #Compras
                montoCompradoSucursalMes = 0
                comprasGastoSucursal = ComprasGastos.objects.filter(fecha_compra__range=[fechaInicioMesActual,fechaDiaMesActual])
                if comprasGastoSucursal:
                    for compra in comprasGastoSucursal:
                        montoComprado = compra.total_costoCompra
                        montoCompradoSucursalMes = montoCompradoSucursalMes + montoComprado
                        
                comprasVentaSucursalDelMes = ComprasVentas.objects.filter(fecha_compra__range=[fechaInicioMesActual,fechaDiaMesActual])
                if comprasVentaSucursalDelMes:
                    for compra in comprasVentaSucursalDelMes:
                        montoComprado = compra.total_costoCompra
                        montoCompradoSucursalMes = montoCompradoSucursalMes + montoComprado

                    
                comprasRentasSucursalesDelMes = ComprasRentas.objects.filter(fecha_compra__range=[fechaInicioMesActual,fechaDiaMesActual])
                if comprasRentasSucursalesDelMes:
                    for compra in comprasRentasSucursalesDelMes:
                        montoComprado = compra.total_costoCompra
                        montoCompradoSucursalMes = montoCompradoSucursalMes + montoComprado
                        
                #Ganancia
                gananciaSucursalMes = montoIngresoSucursalMesTabla - montoCompradoSucursalMes
                if gananciaSucursalMes > 0:
                    signo = "+"
                else:
                    signo = "-"
                    
                #margen
                if montoCompradoSucursalMes == 0:
                    margenSucursalMes = montoIngresoSucursalMesTabla
                else:
                    margenSucursalMes = (montoIngresoSucursalMesTabla * 100)/montoCompradoSucursalMes
                    margenSucursalMes = round(margenSucursalMes,2)
                    margenSucursalMes = margenSucursalMes - 100
                margenDeGanancia.append(margenSucursalMes)
                
                
                montosVendidos.append(montoIngresoSucursalMesTabla)
                montosCompras.append(montoCompradoSucursalMes)
                gananciaSucursales.append([gananciaSucursalMes, signo])
                
            listaComparativaSucursalesMes = zip(infoSucursales,montosVendidos,montosCompras,gananciaSucursales, margenDeGanancia)
            
                    
                    
                    

            
            #EN EL AÑO DE LA SUCURSAAAL .............................................................................................................................................
            #Ingresos totales del mes actual, en, tre entascreditos y rentas
            
            fechaPrimerDiaDelAñoActual = añoHoy +"-01-01"
            fechaUltimoDiaDelAñoActual = añoHoy+"-12-31"
            
            
            
            montoIngresoSucursalAño = 0
            
            contadorVentasSucursalAño = 0
            contadorCreditosSucursalAño = 0
            contadorRentasSucursalAño = 0
            
            numeroVentasSucursalAño = 0
            numeroCreditosSucursalAño = 0
            numeroRentasSucursalAño = 0
            
            consultaVentasSucursalAño = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaDelAñoActual,fechaUltimoDiaDelAñoActual], credito="N", sucursal = idSucursalInforme)
            
            if consultaVentasSucursalAño:
                for ventaRealizada in consultaVentasSucursalAño:
                    montoVenta = ventaRealizada.monto_pagar
                    montoIngresoSucursalAño = montoIngresoSucursalAño + montoVenta
                    contadorVentasSucursalAño = contadorVentasSucursalAño + montoVenta
                    numeroVentasSucursalAño = numeroVentasSucursalAño + 1
            
            consultaCreditosSucursalAño = Creditos.objects.filter(fecha_venta_credito__range=[fechaPrimerDiaDelAñoActual,fechaUltimoDiaDelAñoActual], renta_id__isnull=True, sucursal = idSucursalInforme)
        
            if consultaCreditosSucursalAño:
                for crceditoRealizado in consultaCreditosSucursalAño:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    montoIngresoSucursalAño = montoIngresoSucursalAño + montoPagadoCredito
                    contadorCreditosSucursalAño = contadorCreditosSucursalAño + montoPagadoCredito
                    numeroCreditosSucursalAño = numeroCreditosSucursalAño +1
                    
            consultaRentasAñoActual = Rentas.objects.filter(fecha_apartado__range=[fechaPrimerDiaDelAñoActual,fechaUltimoDiaDelAñoActual])
        
            if consultaRentasAñoActual:
                for rentaRealizada in consultaRentasAñoActual:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductosAño = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductosAño:
                            contadorProductosRentados = contadorProductosRentados + 1
                            
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)
                               
                                for datoProducto in consultaProducto:
                                    sucursalProductoAño = datoProducto.sucursal_id
                                    
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProductoAño == intSucursalInforme:
                                    
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto y no le queda restante
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si aun no paga el restante
                                        sumaPagosRenta = montoPagadoApartado 
                                    montoIngresoSucursalAño = montoIngresoSucursalAño + sumaPagosRenta

                                    contadorRentasSucursalAño = contadorRentasSucursalAño + sumaPagosRenta
                                    numeroRentasSucursalAño = numeroRentasSucursalAño +1
                                    
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            montoIngresoSucursalAño = montoIngresoSucursalAño + sumaPagosRenta

                            contadorRentasSucursalAño = contadorRentasSucursalAño + sumaPagosRenta
                            numeroRentasSucursalAño = numeroRentasSucursalAño +1
                
            #años anteriores
            añoMenosUno = int(añoHoy)-1
            añoMenosDos = int(añoHoy)-2
            añoMenosTres = int(añoHoy)-3
            
            haceUnAñoInicio = str(añoMenosUno)+"-01-01"
            haceUnAñoFinal = str(añoMenosUno)+"-12-31"
            
            haceDosAñosInicio = str(añoMenosDos)+"-01-01"
            haceDosAñosFinal = str(añoMenosDos)+"-12-31"
            
            haceTresAñosInicio = str(añoMenosTres)+"-01-01"
            haceTresAñosFinal = str(añoMenosTres)+"-12-31"
            
            
            contadorVentasHaceUnAño = 0
            contadorVentasHaceDosAños = 0
            contadorVentasHaceTresAños = 0
            
            #Hace un año
            consultaVentasSucursalHaceUnAño = Ventas.objects.filter(fecha_venta__range=[haceUnAñoInicio,haceUnAñoFinal], credito="N", sucursal = idSucursalInforme)
            
            if consultaVentasSucursalHaceUnAño:
                for ventaRealizada in consultaVentasSucursalHaceUnAño:
                    montoVenta = ventaRealizada.monto_pagar
                    contadorVentasHaceUnAño = contadorVentasHaceUnAño + montoVenta
            
            consultaCreditosSucursalHaceUnAño = Creditos.objects.filter(fecha_venta_credito__range=[haceUnAñoInicio,haceUnAñoFinal], renta_id__isnull=True, sucursal = idSucursalInforme)
        
            if consultaCreditosSucursalHaceUnAño:
                for crceditoRealizado in consultaCreditosSucursalHaceUnAño:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    contadorVentasHaceUnAño = contadorVentasHaceUnAño + montoPagadoCredito
                    
            consultaRentasHaceUnAño = Rentas.objects.filter(fecha_apartado__range=[haceUnAñoInicio,haceUnAñoFinal])
        
            if consultaRentasHaceUnAño:
                for rentaRealizada in consultaRentasHaceUnAño:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    contadorVentasHaceUnAño = contadorVentasHaceUnAño + sumaPagosRenta
                                    
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            contadorVentasHaceUnAño = contadorVentasHaceUnAño + sumaPagosRenta
            
            #Hace dos años
            consultaVentasSucursalHaceDosAños = Ventas.objects.filter(fecha_venta__range=[haceDosAñosInicio,haceDosAñosFinal], credito="N", sucursal = idSucursalInforme)
            
            if consultaVentasSucursalHaceDosAños:
                for ventaRealizada in consultaVentasSucursalHaceDosAños:
                    montoVenta = ventaRealizada.monto_pagar
                    contadorVentasHaceDosAños = contadorVentasHaceDosAños + montoVenta
            
            consultaCreditosSucursalHaceDosAños = Creditos.objects.filter(fecha_venta_credito__range=[haceDosAñosInicio,haceDosAñosFinal], renta_id__isnull=True, sucursal = idSucursalInforme)
        
            if consultaCreditosSucursalHaceDosAños:
                for crceditoRealizado in consultaCreditosSucursalHaceDosAños:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    contadorVentasHaceDosAños = contadorVentasHaceDosAños + montoPagadoCredito
                    
            consultaRentasHaceDosAños = Rentas.objects.filter(fecha_apartado__range=[haceDosAñosInicio,haceDosAñosFinal])
        
            if consultaRentasHaceDosAños:
                for rentaRealizada in consultaRentasHaceDosAños:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    contadorVentasHaceDosAños = contadorVentasHaceDosAños + sumaPagosRenta
                                    
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            contadorVentasHaceDosAños = contadorVentasHaceDosAños + sumaPagosRenta
                            
            #Hace 3 años
            consultaVentasSucursalHaceTresAños = Ventas.objects.filter(fecha_venta__range=[haceTresAñosInicio,haceTresAñosFinal], credito="N", sucursal = idSucursalInforme)
            
            if consultaVentasSucursalHaceTresAños:
                for ventaRealizada in consultaVentasSucursalHaceTresAños:
                    montoVenta = ventaRealizada.monto_pagar
                    contadorVentasHaceTresAños = contadorVentasHaceTresAños + montoVenta
            
            consultaCreditosSucursalHaceTresAños = Creditos.objects.filter(fecha_venta_credito__range=[haceTresAñosInicio,haceTresAñosFinal], renta_id__isnull=True, sucursal = idSucursalInforme)
        
            if consultaCreditosSucursalHaceTresAños:
                for crceditoRealizado in consultaCreditosSucursalHaceTresAños:
                    montoPagadoCredito = crceditoRealizado.monto_pagado
                    contadorVentasHaceTresAños = contadorVentasHaceTresAños + montoPagadoCredito
                    
            consultaRentasHaceTresAños = Rentas.objects.filter(fecha_apartado__range=[haceTresAñosInicio,haceTresAñosFinal])
        
            if consultaRentasHaceTresAños:
                for rentaRealizada in consultaRentasHaceTresAños:
                    empleadoQueRealizo = rentaRealizada.realizado_por_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                    for datoEmpleado in consultaEmpleado:
                        idSucursal = datoEmpleado.id_sucursal_id
                    if idSucursal == None:
                        codigosProductosRentados = rentaRealizada.codigos_productos_renta
                        arregloCodigosProductos = codigosProductosRentados.split("-")
                        
                        contadorProductosRentados = 0
                        for producto in arregloCodigosProductos:
                            contadorProductosRentados = contadorProductosRentados + 1
                            strCodigoProducto = str(producto)
                            if contadorProductosRentados == 1:
                                consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                for datoProducto in consultaProducto:
                                    sucursalProducto = datoProducto.sucursal_id
                                intSucursalInforme = int(idSucursalInforme)
                                if sucursalProducto == intSucursalInforme:
                            
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    contadorVentasHaceTresAños = contadorVentasHaceTresAños + sumaPagosRenta
                                    
                    else:
                        intSucursalInforme = int(idSucursalInforme)
                        if idSucursal == intSucursalInforme:
                            
                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                            montoPagadoRestante = rentaRealizada.monto_restante
                            
                            sumaPagosRenta = 0
                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                sumaPagosRenta = rentaRealizada.monto_total_renta
                            else: #Si ya se pago el restante
                                sumaPagosRenta = montoPagadoApartado
                            contadorVentasHaceTresAños = contadorVentasHaceTresAños + sumaPagosRenta
                            
            #Porcentaje si ingresos son mayores en sucursal
            esMayorAñoSucursal = False

            if contadorVentasHaceUnAño == 0:
                porcentajeIngresosSucursalAño = 100
            else:
                porcentajeIngresosSucursalAño = (montoIngresoSucursalAño / contadorVentasHaceUnAño)
                porcentajeIngresosSucursalAño = porcentajeIngresosSucursalAño - 1
                porcentajeIngresosSucursalAño = porcentajeIngresosSucursalAño *100
                
                
            if porcentajeIngresosSucursalAño > 0:
                esMayorAñoSucursal = True
                
            else:
                esMayorAñoSucursal = False
            porcentajeIngresosSucursalAño = round(porcentajeIngresosSucursalAño,2)
            
            
            # - COMPRAS DEL AÑOOOOOOO ...................................................
            totalComprasAñoGasto = 0
            totalComprasAñoVenta = 0
            totalComprasAñoRenta= 0
            
            numeroComprasGastoAño = 0
            numeroComprasVentaAño = 0
            numeroComprasRentaAño = 0
            
            comprasProductosGastosSucursalAño= []
            comprasGastoSucursalDelAño = ComprasGastos.objects.filter(fecha_compra__range=[fechaPrimerDiaDelAñoActual,fechaUltimoDiaDelAñoActual])
            if comprasGastoSucursalDelAño:
                for compra in comprasGastoSucursalDelAño:
                    montoComprado = compra.total_costoCompra
                    
                    
                    idCompra = compra.id_compraGasto
                    idProducto = compra.id_productoComprado_id
                    consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                    
                    for datoProducto in consultaProducto:
                        nombreProducto = datoProducto.nombre_producto
                        codigoProducto = datoProducto.codigo_producto
                        imagenProducto = datoProducto.imagen_producto
                        sucursalProducto = datoProducto.sucursal_id
                    nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                    
                    fechaCompra = compra.fecha_compra
                    costoUnitarioCompra = compra.costo_unitario
                    cantidadComprada = compra.cantidad_comprada
                    totalMontoCompra = compra.total_costoCompra
                    
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                    for datoSucursal in consultaSucursal:
                        nombreSucursalProducto = datoSucursal.nombre
                    
                    idSucursalInforme = int(idSucursalInforme)
                    
                    if sucursalProducto == idSucursalInforme:
                        totalComprasAñoGasto = totalComprasAñoGasto + montoComprado
                        numeroComprasGastoAño = numeroComprasGastoAño +1
                        comprasProductosGastosSucursalAño.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursalProducto,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
            else:
                comprasProductosGastosSucursalAño = None
                
            
            comprasProductosVentasSucursalAño = []
            comprasVentaSucursalDelAño = ComprasVentas.objects.filter(fecha_compra__range=[fechaPrimerDiaDelAñoActual,fechaUltimoDiaDelAñoActual])
            if comprasVentaSucursalDelAño:
                for compra in comprasVentaSucursalDelAño:
                    montoComprado = compra.total_costoCompra
                   
                    
                    idCompra = compra.id_compraVenta
                    idProducto = compra.id_productoComprado_id
                    consultaProducto = ProductosVenta.objects.filter(id_producto = idProducto)
                    
                    for datoProducto in consultaProducto:
                        nombreProducto = datoProducto.nombre_producto
                        codigoProducto = datoProducto.codigo_producto
                        imagenProducto = datoProducto.imagen_producto
                        sucursalProducto = datoProducto.sucursal_id
                    nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                    
                    fechaCompra = compra.fecha_compra
                    costoUnitarioCompra = compra.costo_unitario
                    cantidadComprada = compra.cantidad_comprada
                    totalMontoCompra = compra.total_costoCompra
                    
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                    for datoSucursal in consultaSucursal:
                        nombreSucursalProducto = datoSucursal.nombre
                        
                    idSucursalInforme = int(idSucursalInforme)
                    
                    if sucursalProducto == idSucursalInforme:
                        totalComprasAñoVenta = totalComprasAñoVenta + montoComprado
                        numeroComprasVentaAño = numeroComprasVentaAño +1
                        comprasProductosVentasSucursalAño.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursalProducto,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
            else:
                comprasProductosVentasSucursalAño = None
            
            
            comprasProductosRentasSucursalAño = []
            comprasRentasSucursalesDelAño = ComprasRentas.objects.filter(fecha_compra__range=[fechaPrimerDiaDelAñoActual,fechaUltimoDiaDelAñoActual])
            if comprasRentasSucursalesDelAño:
                for compra in comprasRentasSucursalesDelAño:
                    montoComprado = compra.total_costoCompra
                    
                    
                    idCompra = compra.id_compraRenta
                    idProducto = compra.id_productoComprado_id
                    consultaProducto = ProductosRenta.objects.filter(id_producto = idProducto)
                    
                    for datoProducto in consultaProducto:
                        nombreProducto = datoProducto.nombre_producto
                        codigoProducto = datoProducto.codigo_producto
                        imagenProducto = datoProducto.imagen_producto
                        sucursalProducto = datoProducto.sucursal_id
                    nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                    
                    fechaCompra = compra.fecha_compra
                    costoUnitarioCompra = compra.costo_unitario
                    cantidadComprada = compra.cantidad_comprada
                    totalMontoCompra = compra.total_costoCompra
                    
                    consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                    for datoSucursal in consultaSucursal:
                        nombreSucursalProducto = datoSucursal.nombre
                        
                    idSucursalInforme = int(idSucursalInforme)
                    
                    if sucursalProducto == idSucursalInforme:
                        totalComprasAñoRenta = totalComprasAñoRenta + montoComprado
                        numeroComprasRentaAño = numeroComprasRentaAño +1
                        comprasProductosRentasSucursalAño.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursalProducto,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
            else:
                comprasProductosRentasSucursalAño = None            

            sumaTotalesComprasDelAño = totalComprasAñoGasto + totalComprasAñoVenta + totalComprasAñoRenta
            
            utilidadSucursalAño = montoIngresoSucursalAño - sumaTotalesComprasDelAño
            
            utilidadMayorAño = False
            if utilidadSucursalAño < 0:
                utilidadMayorAño = False
            else:
                utilidadMayorAño = True
            
            
            #Tabla de sucursales en el año
            #Tabla de ganancias por sucursales
            sucursalesAño = Sucursales.objects.all()
            infoSucursalesAño = []
            montosVendidosAño =[]
            montosComprasAño = []
            gananciaSucursalesAño = []
            margenDeGananciaAño = []
            
            for sucursal in sucursalesAño:
                idSucursal = sucursal.id_sucursal
                nombre = sucursal.nombre
                
                infoSucursalesAño.append([idSucursal,nombre])
                #ventas
                consultaVentasSucursalAño = Ventas.objects.filter(fecha_venta__range=[fechaPrimerDiaDelAñoActual,fechaUltimoDiaDelAñoActual], credito="N", sucursal = idSucursal)
                montoIngresoSucursalAñoTabla = 0
                
                if consultaVentasSucursalAño:
                    for ventaRealizada in consultaVentasSucursalAño:
                        montoVenta = ventaRealizada.monto_pagar
                        montoIngresoSucursalAñoTabla = montoIngresoSucursalAñoTabla + montoVenta
            
                consultaCreditosSucursalAño = Creditos.objects.filter(fecha_venta_credito__range=[fechaPrimerDiaDelAñoActual,fechaUltimoDiaDelAñoActual], renta_id__isnull=True, sucursal = idSucursal)
            
                if consultaCreditosSucursalAño:
                    for crceditoRealizado in consultaCreditosSucursalAño:
                        montoPagadoCredito = crceditoRealizado.monto_pagado
                        montoIngresoSucursalAñoTabla = montoIngresoSucursalAñoTabla + montoPagadoCredito
                        
                consultaRentasSucursalAño = Rentas.objects.filter(fecha_apartado__range=[fechaPrimerDiaDelAñoActual,fechaUltimoDiaDelAñoActual])
        
                if consultaRentasSucursalAño:
                    for rentaRealizada in consultaRentasSucursalAño:
                        empleadoQueRealizo = rentaRealizada.realizado_por_id
                        consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                        for datoEmpleado in consultaEmpleado:
                            idSucursalEmpleado = datoEmpleado.id_sucursal_id
                        if idSucursalEmpleado == None:
                            codigosProductosRentados = rentaRealizada.codigos_productos_renta
                            arregloCodigosProductos = codigosProductosRentados.split("-")
                            
                            contadorProductosRentados = 0
                            for producto in arregloCodigosProductos:
                                contadorProductosRentados = contadorProductosRentados + 1
                                strCodigoProducto = str(producto)
                                if contadorProductosRentados == 1:
                                    consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                    for datoProducto in consultaProducto:
                                        sucursalProducto = datoProducto.sucursal_id
                                        
                                    if sucursalProducto == idSucursal:
                                
                                        montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                        montoPagadoRestante = rentaRealizada.monto_restante
                                        
                                        sumaPagosRenta = 0
                                        if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                            sumaPagosRenta = rentaRealizada.monto_total_renta
                                        else: #Si ya se pago el restante
                                            sumaPagosRenta = montoPagadoApartado
                                        montoIngresoSucursalAñoTabla = montoIngresoSucursalAñoTabla + sumaPagosRenta

                                        
                        else:
                            if idSucursalEmpleado == idSucursal:
                                
                                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                montoPagadoRestante = rentaRealizada.monto_restante
                                
                                sumaPagosRenta = 0
                                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                    sumaPagosRenta = rentaRealizada.monto_total_renta
                                else: #Si ya se pago el restante
                                    sumaPagosRenta = montoPagadoApartado
                                montoIngresoSucursalAñoTabla = montoIngresoSucursalAñoTabla + sumaPagosRenta
                                
                
                
                #Compras
                montoCompradoSucursalAño = 0
                comprasGastoSucursalAño = ComprasGastos.objects.filter(fecha_compra__range=[fechaPrimerDiaDelAñoActual,fechaUltimoDiaDelAñoActual])
                if comprasGastoSucursalAño:
                    for compra in comprasGastoSucursalAño:
                        montoComprado = compra.total_costoCompra
                        idCompra = compra.id_compraGasto
                        idProducto = compra.id_productoComprado_id
                        consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                        
                        for datoProducto in consultaProducto:
                            sucursalProducto = datoProducto.sucursal_id
                            
                        idSucursal = int(idSucursal)
                        
                        if sucursalProducto == idSucursal:
                            montoCompradoSucursalAño = montoCompradoSucursalAño + montoComprado
                        
                comprasVentaSucursalDelAño = ComprasVentas.objects.filter(fecha_compra__range=[fechaPrimerDiaDelAñoActual,fechaUltimoDiaDelAñoActual])
                if comprasVentaSucursalDelAño:
                    for compra in comprasVentaSucursalDelAño:
                        montoComprado = compra.total_costoCompra
                        idCompra = compra.id_compraVenta
                        idProducto = compra.id_productoComprado_id
                        consultaProducto = ProductosVenta.objects.filter(id_producto = idProducto)
                        
                        for datoProducto in consultaProducto:
                            sucursalProducto = datoProducto.sucursal_id
                            
                        idSucursal = int(idSucursal)
                        
                        if sucursalProducto == idSucursal:
                            montoCompradoSucursalAño = montoCompradoSucursalAño + montoComprado

                    
                comprasRentasSucursalesDelAño = ComprasRentas.objects.filter(fecha_compra__range=[fechaPrimerDiaDelAñoActual,fechaUltimoDiaDelAñoActual])
                if comprasRentasSucursalesDelAño:
                    for compra in comprasRentasSucursalesDelAño:
                        montoComprado = compra.total_costoCompra
                        idCompra = compra.id_compraRenta
                        idProducto = compra.id_productoComprado_id
                        consultaProducto = ProductosRenta.objects.filter(id_producto = idProducto)
                        
                        for datoProducto in consultaProducto:
                            sucursalProducto = datoProducto.sucursal_id
                            
                        idSucursal = int(idSucursal)
                        
                        if sucursalProducto == idSucursal:
                            montoCompradoSucursalAño = montoCompradoSucursalAño + montoComprado
                        
                #Ganancia
                gananciaSucursalAño = montoIngresoSucursalAñoTabla - montoCompradoSucursalAño
                if gananciaSucursalAño > 0:
                    signoAño = "+"
                else:
                    signoAño = "-"
                    
                #margen
                if montoCompradoSucursalAño == 0:
                    margenSucursalAño = montoIngresoSucursalAñoTabla
                else:
                    margenSucursalAño = (montoIngresoSucursalAñoTabla * 100)/montoCompradoSucursalAño
                    margenSucursalAño = round(margenSucursalAño,2)
                    margenSucursalAño = margenSucursalAño - 100
                margenDeGananciaAño.append(margenSucursalAño)
                
                
                montosVendidosAño.append(montoIngresoSucursalAñoTabla)
                montosComprasAño.append(montoCompradoSucursalAño)
                gananciaSucursalesAño.append([gananciaSucursalAño, signoAño])
                
            listaComparativaSucursalesAño = zip(infoSucursalesAño,montosVendidosAño,montosComprasAño,gananciaSucursalesAño, margenDeGananciaAño)

            
            #RANGO DE FECHAS INFORME SUCURSAL
            if rangoFechaRecibida:
                
                arregloFechaInicioRango = fechaInicioRango.split("-")
                arregloFechaFinalRango = fechaFinalRango.split("-")
                 
                
                mesdeInicioRango = mesesDic[str(arregloFechaInicioRango[1])]
                mesdeFinalRango = mesesDic[str(arregloFechaFinalRango[1])]
                
                stringFechaInicioRango = str(arregloFechaInicioRango[2]) + " de " + mesdeInicioRango + " del "+str(arregloFechaInicioRango[0])
                stringFechaFinalRango = str(arregloFechaFinalRango[2]) + " de " + mesdeFinalRango + " del "+str(arregloFechaFinalRango[0])
                
                
                #fechas de otros periodos
                fechaInicioFormato=datetime.strptime(fechaInicioRango,"%Y-%m-%d")
                fechaFinalFormato=datetime.strptime(fechaFinalRango,"%Y-%m-%d") 

                diferenciaEnDias=fechaFinalFormato-fechaInicioFormato
                numeroDiasDiferencia=diferenciaEnDias.days
                fechaRestaInicio=fechaInicioFormato-timedelta(days=numeroDiasDiferencia)
                fechaSumaFinal=fechaFinalFormato+timedelta(days=numeroDiasDiferencia)
                mesNumeroRestaInicio=fechaRestaInicio.strftime('%m')
                mesNumeroSumaFinal=fechaSumaFinal.strftime('%m')
                
                mesNumeroRestaInicioTexto = mesesDic[str(mesNumeroRestaInicio)]
                mesNumeroSumaFinalTexto = mesesDic[str(mesNumeroSumaFinal)]
                
                fechaTextoInicioPeriodoAnterior = str(fechaRestaInicio.strftime('%d'))+ " de " + mesNumeroRestaInicioTexto +" "+ str(fechaRestaInicio.strftime('%Y'))  
                fechaTextoFinalPeriodoDespues=str(fechaSumaFinal.strftime('%d'))+ " de "+ mesNumeroSumaFinalTexto + " de " + str(fechaSumaFinal.strftime('%Y'))
            
                #INGRESOS
                montoIngresoSucursalRango = 0
                
                contadorVentasSucursalRango = 0
                contadorCreditosSucursalRango = 0
                contadorRentasSucursalRango = 0
                
                numeroVentasSucursalRango = 0
                numeroCreditosSucursalRango = 0
                numeroRentasSucursalRango = 0
                
                consultaVentasSucursalRango = Ventas.objects.filter(fecha_venta__range=[fechaInicioRango,fechaFinalRango], credito="N", sucursal = idSucursalInforme)
                
                if consultaVentasSucursalRango:
                    for ventaRealizada in consultaVentasSucursalRango:
                        montoVenta = ventaRealizada.monto_pagar
                        montoIngresoSucursalRango = montoIngresoSucursalRango + montoVenta
                        contadorVentasSucursalRango = contadorVentasSucursalRango + montoVenta
                        numeroVentasSucursalRango = numeroVentasSucursalRango + 1
                
                consultaCreditosSucursalRango = Creditos.objects.filter(fecha_venta_credito__range=[fechaInicioRango,fechaFinalRango], renta_id__isnull=True, sucursal = idSucursalInforme)
                
                if consultaCreditosSucursalRango:
                    for creditoRealizado in consultaCreditosSucursalRango:
                        montoPagadoCredito = creditoRealizado.monto_pagado
                        montoIngresoSucursalRango = montoIngresoSucursalRango + montoPagadoCredito
                        contadorCreditosSucursalRango = contadorCreditosSucursalRango + montoVenta
                        numeroCreditosSucursalRango = numeroCreditosSucursalRango + 1
                
                consultaRentasSucursalRango = Rentas.objects.filter(fecha_apartado__range=[fechaInicioRango,fechaFinalRango])
        
                if consultaRentasSucursalRango:
                    for rentaRealizada in consultaRentasSucursalRango:
                        empleadoQueRealizo = rentaRealizada.realizado_por_id
                        consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                        for datoEmpleado in consultaEmpleado:
                            idSucursal = datoEmpleado.id_sucursal_id
                        if idSucursal == None:
                            codigosProductosRentados = rentaRealizada.codigos_productos_renta
                            arregloCodigosProductosAño = codigosProductosRentados.split("-")
                            
                            contadorProductosRentados = 0
                            for producto in arregloCodigosProductosAño:
                                contadorProductosRentados = contadorProductosRentados + 1
                                
                                strCodigoProducto = str(producto)
                                if contadorProductosRentados == 1:
                                    consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)
                                
                                    for datoProducto in consultaProducto:
                                        sucursalProductoAño = datoProducto.sucursal_id
                                        
                                    intSucursalInforme = int(idSucursalInforme)
                                    if sucursalProductoAño == intSucursalInforme:
                                        
                                        montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                        montoPagadoRestante = rentaRealizada.monto_restante
                                        
                                        sumaPagosRenta = 0
                                        if montoPagadoRestante == 0: #Ya aparto y no le queda restante
                                            sumaPagosRenta = rentaRealizada.monto_total_renta
                                        else: #Si aun no paga el restante
                                            sumaPagosRenta = montoPagadoApartado 
                                        montoIngresoSucursalRango = montoIngresoSucursalRango + sumaPagosRenta

                                        contadorRentasSucursalRango = contadorRentasSucursalRango + sumaPagosRenta
                                        numeroRentasSucursalRango = numeroRentasSucursalRango +1
                                        
                        else:
                            intSucursalInforme = int(idSucursalInforme)
                            if idSucursal == intSucursalInforme:
                                
                                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                montoPagadoRestante = rentaRealizada.monto_restante
                                
                                sumaPagosRenta = 0
                                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                    sumaPagosRenta = rentaRealizada.monto_total_renta
                                else: #Si ya se pago el restante
                                    sumaPagosRenta = montoPagadoApartado
                                montoIngresoSucursalRango = montoIngresoSucursalRango + sumaPagosRenta

                                contadorRentasSucursalRango = contadorRentasSucursalRango + sumaPagosRenta
                                numeroRentasSucursalRango = numeroRentasSucursalRango +1
                                
                                
                contadorVentasPeriodoAnterior = 0
                contadorVentasPeriodoDespues = 0   
                #INGRESOS PERIODO ANTERIOR
                #Periodo anterior
                consultaVentasSucursalPeriodoAnterior = Ventas.objects.filter(fecha_venta__range=[fechaRestaInicio,fechaInicioRango], credito="N", sucursal = idSucursalInforme)
            
                if consultaVentasSucursalPeriodoAnterior:
                    for ventaRealizada in consultaVentasSucursalPeriodoAnterior:
                        montoVenta = ventaRealizada.monto_pagar
                        contadorVentasPeriodoAnterior = contadorVentasPeriodoAnterior + montoVenta
                
                consultaVentasSucursalPeriodoAnterior = Creditos.objects.filter(fecha_venta_credito__range=[fechaRestaInicio,fechaInicioRango], renta_id__isnull=True, sucursal = idSucursalInforme)
            
                if consultaVentasSucursalPeriodoAnterior:
                    for crceditoRealizado in consultaVentasSucursalPeriodoAnterior:
                        montoPagadoCredito = crceditoRealizado.monto_pagado
                        contadorVentasPeriodoAnterior = contadorVentasPeriodoAnterior + montoPagadoCredito
                        
                consultaRentasSucursalPeriodoAnterior = Rentas.objects.filter(fecha_apartado__range=[fechaRestaInicio,fechaInicioRango])
            
                if consultaRentasSucursalPeriodoAnterior:
                    for rentaRealizada in consultaRentasSucursalPeriodoAnterior:
                        empleadoQueRealizo = rentaRealizada.realizado_por_id
                        consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                        for datoEmpleado in consultaEmpleado:
                            idSucursal = datoEmpleado.id_sucursal_id
                        if idSucursal == None:
                            codigosProductosRentados = rentaRealizada.codigos_productos_renta
                            arregloCodigosProductos = codigosProductosRentados.split("-")
                            
                            contadorProductosRentados = 0
                            for producto in arregloCodigosProductos:
                                contadorProductosRentados = contadorProductosRentados + 1
                                strCodigoProducto = str(producto)
                                if contadorProductosRentados == 1:
                                    consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                    for datoProducto in consultaProducto:
                                        sucursalProducto = datoProducto.sucursal_id
                                    intSucursalInforme = int(idSucursalInforme)
                                    if sucursalProducto == intSucursalInforme:
                                
                                        montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                        montoPagadoRestante = rentaRealizada.monto_restante
                                        
                                        sumaPagosRenta = 0
                                        if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                            sumaPagosRenta = rentaRealizada.monto_total_renta
                                        else: #Si ya se pago el restante
                                            sumaPagosRenta = montoPagadoApartado
                                        contadorVentasPeriodoAnterior = contadorVentasPeriodoAnterior + sumaPagosRenta
                                        
                        else:
                            intSucursalInforme = int(idSucursalInforme)
                            if idSucursal == intSucursalInforme:
                                
                                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                montoPagadoRestante = rentaRealizada.monto_restante
                                
                                sumaPagosRenta = 0
                                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                    sumaPagosRenta = rentaRealizada.monto_total_renta
                                else: #Si ya se pago el restante
                                    sumaPagosRenta = montoPagadoApartado
                                contadorVentasPeriodoAnterior = contadorVentasPeriodoAnterior + sumaPagosRenta
                
                #Periodo después.
                consultaVentasSucursalPeriodoDespues = Ventas.objects.filter(fecha_venta__range=[fechaFinalRango,fechaSumaFinal], credito="N", sucursal = idSucursalInforme)
            
                if consultaVentasSucursalPeriodoDespues:
                    for ventaRealizada in consultaVentasSucursalPeriodoDespues:
                        montoVenta = ventaRealizada.monto_pagar
                        contadorVentasPeriodoDespues = contadorVentasPeriodoDespues + montoVenta
                
                consultaCreditosSucursalPeriodoDespues = Creditos.objects.filter(fecha_venta_credito__range=[fechaFinalRango,fechaSumaFinal], renta_id__isnull=True, sucursal = idSucursalInforme)
            
                if consultaCreditosSucursalPeriodoDespues:
                    for crceditoRealizado in consultaCreditosSucursalPeriodoDespues:
                        montoPagadoCredito = crceditoRealizado.monto_pagado
                        contadorVentasPeriodoDespues = contadorVentasPeriodoDespues + montoPagadoCredito
                        
                consultaRentasSucursalPeriodoDespues = Rentas.objects.filter(fecha_apartado__range=[fechaFinalRango,fechaSumaFinal])
            
                if consultaRentasSucursalPeriodoDespues:
                    for rentaRealizada in consultaRentasSucursalPeriodoDespues:
                        empleadoQueRealizo = rentaRealizada.realizado_por_id
                        consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                        for datoEmpleado in consultaEmpleado:
                            idSucursal = datoEmpleado.id_sucursal_id
                        if idSucursal == None:
                            codigosProductosRentados = rentaRealizada.codigos_productos_renta
                            arregloCodigosProductos = codigosProductosRentados.split("-")
                            
                            contadorProductosRentados = 0
                            for producto in arregloCodigosProductos:
                                contadorProductosRentados = contadorProductosRentados + 1
                                strCodigoProducto = str(producto)
                                if contadorProductosRentados == 1:
                                    consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                    for datoProducto in consultaProducto:
                                        sucursalProducto = datoProducto.sucursal_id
                                    intSucursalInforme = int(idSucursalInforme)
                                    if sucursalProducto == intSucursalInforme:
                                
                                        montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                        montoPagadoRestante = rentaRealizada.monto_restante
                                        
                                        sumaPagosRenta = 0
                                        if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                            sumaPagosRenta = rentaRealizada.monto_total_renta
                                        else: #Si ya se pago el restante
                                            sumaPagosRenta = montoPagadoApartado
                                        contadorVentasPeriodoDespues = contadorVentasPeriodoDespues + sumaPagosRenta
                                        
                        else:
                            intSucursalInforme = int(idSucursalInforme)
                            if idSucursal == intSucursalInforme:
                                
                                montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                montoPagadoRestante = rentaRealizada.monto_restante
                                
                                sumaPagosRenta = 0
                                if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                    sumaPagosRenta = rentaRealizada.monto_total_renta
                                else: #Si ya se pago el restante
                                    sumaPagosRenta = montoPagadoApartado
                                contadorVentasPeriodoDespues = contadorVentasPeriodoDespues + sumaPagosRenta
            
                
                #Porcentaje si ingresos son mayores en sucursal
                esMayorPeriodoSucursal = False

                if contadorVentasPeriodoAnterior == 0:
                    porcentajeIngresosSucursalRango = 100
                else:
                    porcentajeIngresosSucursalRango = (montoIngresoSucursalRango / contadorVentasPeriodoAnterior)
                    porcentajeIngresosSucursalRango = porcentajeIngresosSucursalRango - 1
                    porcentajeIngresosSucursalRango = porcentajeIngresosSucursalRango *100
                    
                    
                if porcentajeIngresosSucursalRango > 0:
                    esMayorPeriodoSucursal = True
                    
                else:
                    esMayorPeriodoSucursal = False
                porcentajeIngresosSucursalRango = round(porcentajeIngresosSucursalRango,2)   
                    
                    
                # - COMPRAS DEL AÑOOOOOOO ...................................................
                totalComprasRangoGasto = 0
                totalComprasRangoVenta = 0
                totalComprasRangoRenta= 0
                
                numeroComprasGastoRango = 0
                numeroComprasVentaRango = 0
                numeroComprasRentaRango = 0
                
                comprasProductosGastosSucursalRango= []
                comprasGastoSucursalDelRango = ComprasGastos.objects.filter(fecha_compra__range=[fechaInicioRango,fechaFinalRango])
                if comprasGastoSucursalDelRango:
                    for compra in comprasGastoSucursalDelRango:
                        montoComprado = compra.total_costoCompra
                        
                        
                        idCompra = compra.id_compraGasto
                        idProducto = compra.id_productoComprado_id
                        consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                        
                        for datoProducto in consultaProducto:
                            nombreProducto = datoProducto.nombre_producto
                            codigoProducto = datoProducto.codigo_producto
                            imagenProducto = datoProducto.imagen_producto
                            sucursalProducto = datoProducto.sucursal_id
                        nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                        
                        fechaCompra = compra.fecha_compra
                        costoUnitarioCompra = compra.costo_unitario
                        cantidadComprada = compra.cantidad_comprada
                        totalMontoCompra = compra.total_costoCompra
                        
                        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                        for datoSucursal in consultaSucursal:
                            nombreSucursalProducto = datoSucursal.nombre
                        
                        idSucursalInforme = int(idSucursalInforme)
                        
                        if sucursalProducto == idSucursalInforme:
                            totalComprasRangoGasto = totalComprasRangoGasto + montoComprado
                            numeroComprasGastoRango = numeroComprasGastoRango +1
                            comprasProductosGastosSucursalRango.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursalProducto,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
                else:
                    comprasProductosGastosSucursalRango = None
                    
                
                comprasProductosVentasSucursalRango = []
                comprasVentaSucursalDelRango = ComprasVentas.objects.filter(fecha_compra__range=[fechaInicioRango,fechaFinalRango])
                if comprasVentaSucursalDelRango:
                    for compra in comprasVentaSucursalDelRango:
                        montoComprado = compra.total_costoCompra
                    
                        
                        idCompra = compra.id_compraVenta
                        idProducto = compra.id_productoComprado_id
                        consultaProducto = ProductosVenta.objects.filter(id_producto = idProducto)
                        
                        for datoProducto in consultaProducto:
                            nombreProducto = datoProducto.nombre_producto
                            codigoProducto = datoProducto.codigo_producto
                            imagenProducto = datoProducto.imagen_producto
                            sucursalProducto = datoProducto.sucursal_id
                        nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                        
                        fechaCompra = compra.fecha_compra
                        costoUnitarioCompra = compra.costo_unitario
                        cantidadComprada = compra.cantidad_comprada
                        totalMontoCompra = compra.total_costoCompra
                        
                        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                        for datoSucursal in consultaSucursal:
                            nombreSucursalProducto = datoSucursal.nombre
                            
                        idSucursalInforme = int(idSucursalInforme)
                        
                        if sucursalProducto == idSucursalInforme:
                            totalComprasRangoVenta = totalComprasRangoVenta + montoComprado
                            numeroComprasVentaRango = numeroComprasVentaRango +1
                            comprasProductosVentasSucursalRango.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursalProducto,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
                else:
                    comprasProductosVentasSucursalRango = None
                
                
                comprasProductosRentasSucursalRango = []
                comprasRentasSucursalesDelRango = ComprasRentas.objects.filter(fecha_compra__range=[fechaInicioRango,fechaFinalRango])
                if comprasRentasSucursalesDelRango:
                    for compra in comprasRentasSucursalesDelRango:
                        montoComprado = compra.total_costoCompra
                        
                        
                        idCompra = compra.id_compraRenta
                        idProducto = compra.id_productoComprado_id
                        consultaProducto = ProductosRenta.objects.filter(id_producto = idProducto)
                        
                        for datoProducto in consultaProducto:
                            nombreProducto = datoProducto.nombre_producto
                            codigoProducto = datoProducto.codigo_producto
                            imagenProducto = datoProducto.imagen_producto
                            sucursalProducto = datoProducto.sucursal_id
                        nombreCompletoProducto = codigoProducto + " - "+nombreProducto
                        
                        fechaCompra = compra.fecha_compra
                        costoUnitarioCompra = compra.costo_unitario
                        cantidadComprada = compra.cantidad_comprada
                        totalMontoCompra = compra.total_costoCompra
                        
                        consultaSucursal = Sucursales.objects.filter(id_sucursal = sucursalProducto)
                        for datoSucursal in consultaSucursal:
                            nombreSucursalProducto = datoSucursal.nombre
                            
                        idSucursalInforme = int(idSucursalInforme)
                        
                        if sucursalProducto == idSucursalInforme:
                            totalComprasRangoRenta = totalComprasRangoRenta + montoComprado
                            numeroComprasRentaRango = numeroComprasRentaRango +1
                            comprasProductosRentasSucursalRango.append([idCompra,nombreCompletoProducto,imagenProducto,fechaCompra,nombreSucursalProducto,costoUnitarioCompra,cantidadComprada,totalMontoCompra])
                else:
                    comprasProductosRentasSucursalRango = None            

                sumaTotalesComprasDelRango = totalComprasRangoGasto + totalComprasRangoVenta + totalComprasRangoRenta
                
                utilidadSucursalRango = montoIngresoSucursalRango - sumaTotalesComprasDelRango
                
                utilidadMayorRango = False
                if utilidadSucursalRango < 0:
                    utilidadMayorRango = False
                else:
                    utilidadMayorRango = True
                
                
                #TABLA COMPARATIVA RANGO DE FECHAS SUCURSAL.
 
                sucursalesRango = Sucursales.objects.all()
                infoSucursalesRango = []
                montosIngresosSucursalRango = []
                montosComprasSucursalRango = []
                gananciaSucursalesRango = []
                margenDeGananciaSucursalRango = []

                for sucursal in sucursalesRango:
                    idSucursal = sucursal.id_sucursal
                    nombre = sucursal.nombre

                    infoSucursalesRango.append([idSucursal, nombre])

                    #Ingresos de venta en el rango por sucursal.
                    consultaVentasSucursalRango = Ventas.objects.filter(fecha_venta__range=[fechaInicioRango,fechaFinalRango], credito="N", sucursal = idSucursal)
                    montoIngresoSucursalRangoTabla = 0

                    if consultaVentasSucursalRango:
                        for ventaRealizada in consultaVentasSucursalRango:
                            montoVenta = ventaRealizada.monto_pagar
                            montoIngresoSucursalRangoTabla = montoIngresoSucursalRangoTabla + montoVenta

                    consultaCreditosSucursalRango = Creditos.objects.filter(fecha_venta_credito__range=[fechaInicioRango,fechaFinalRango], renta_id__isnull=True, sucursal = idSucursal)
                    if consultaCreditosSucursalRango:
                        for creditoRealizado in consultaCreditosSucursalRango:
                            montoPagadoCredito = creditoRealizado.monto_pagado
                            montoIngresoSucursalRangoTabla = montoIngresoSucursalRangoTabla + montoPagadoCredito 

                    consultaRentasSucursalRango = Rentas.objects.filter(fecha_apartado__range=[fechaInicioRango,fechaFinalRango])
                    if consultaRentasSucursalRango:
                        for rentaRealizada in consultaRentasSucursalRango:
                            empleadoQueRealizo = rentaRealizada.realizado_por_id
                            consultaEmpleado = Empleados.objects.filter(id_empleado = empleadoQueRealizo)
                            for datoEmpleado in consultaEmpleado:
                                idSucursalEmpleado = datoEmpleado.id_sucursal_id
                            if idSucursalEmpleado == None:
                                codigosProductosRentados = rentaRealizada.codigos_productos_renta
                                arregloCodigosProductos = codigosProductosRentados.split("-")
                                
                                contadorProductosRentados = 0
                                for producto in arregloCodigosProductos:
                                    contadorProductosRentados = contadorProductosRentados + 1
                                    strCodigoProducto = str(producto)
                                    if contadorProductosRentados == 1:
                                        consultaProducto = ProductosRenta.objects.filter(codigo_producto = strCodigoProducto)

                                        for datoProducto in consultaProducto:
                                            sucursalProducto = datoProducto.sucursal_id
                                            
                                        if sucursalProducto == idSucursal:
                                    
                                            montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                            montoPagadoRestante = rentaRealizada.monto_restante
                                            
                                            sumaPagosRenta = 0
                                            if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                                sumaPagosRenta = rentaRealizada.monto_total_renta
                                            else: #Si ya se pago el restante
                                                sumaPagosRenta = montoPagadoApartado
                                            montoIngresoSucursalRangoTabla = montoIngresoSucursalRangoTabla + sumaPagosRenta

                                            
                            else:
                                if idSucursalEmpleado == idSucursal:
                                    
                                    montoPagadoApartado = rentaRealizada.monto_pago_apartado
                                    montoPagadoRestante = rentaRealizada.monto_restante
                                    
                                    sumaPagosRenta = 0
                                    if montoPagadoRestante == 0: #Ya aparto pero no ha pagado el restante..
                                        sumaPagosRenta = rentaRealizada.monto_total_renta
                                    else: #Si ya se pago el restante
                                        sumaPagosRenta = montoPagadoApartado
                                    montoIngresoSucursalRangoTabla = montoIngresoSucursalRangoTabla + sumaPagosRenta

                    #Compras de la sucursal.
                    montoCompradoSucursalRango = 0
                    comprasGastoSucursalRango = ComprasGastos.objects.filter(fecha_compra__range=[fechaInicioRango,fechaFinalRango])
                    if comprasGastoSucursalRango:
                        for compra in comprasGastoSucursalRango:
                            montoComprado = compra.total_costoCompra
                            idCompra = compra.id_compraGasto
                            idProducto = compra.id_productoComprado_id
                            consultaProducto = ProductosGasto.objects.filter(id_producto = idProducto)
                        
                            for datoProducto in consultaProducto:
                                sucursalProducto = datoProducto.sucursal_id
                                
                            idSucursal = int(idSucursal)
                            
                            if sucursalProducto == idSucursal:
                                montoCompradoSucursalRango = montoCompradoSucursalRango + montoComprado

                    comprasVentaSucursalDelRango = ComprasVentas.objects.filter(fecha_compra__range=[fechaInicioRango,fechaFinalRango])
                    if comprasVentaSucursalDelRango:
                        for compra in comprasVentaSucursalDelRango:
                            montoComprado = compra.total_costoCompra
                            idCompra = compra.id_compraVenta
                            idProducto = compra.id_productoComprado_id
                            consultaProducto = ProductosVenta.objects.filter(id_producto = idProducto)
                            
                            for datoProducto in consultaProducto:
                                sucursalProducto = datoProducto.sucursal_id
                                
                            idSucursal = int(idSucursal)
                            
                            if sucursalProducto == idSucursal:
                                montoCompradoSucursalRango = montoCompradoSucursalRango + montoComprado

                        
                    comprasRentasSucursalesDelRango = ComprasRentas.objects.filter(fecha_compra__range=[fechaInicioRango,fechaFinalRango])
                    if comprasRentasSucursalesDelRango:
                        for compra in comprasRentasSucursalesDelRango:
                            montoComprado = compra.total_costoCompra
                            idCompra = compra.id_compraRenta
                            idProducto = compra.id_productoComprado_id
                            consultaProducto = ProductosRenta.objects.filter(id_producto = idProducto)
                            
                            for datoProducto in consultaProducto:
                                sucursalProducto = datoProducto.sucursal_id
                                
                            idSucursal = int(idSucursal)
                            
                            if sucursalProducto == idSucursal:
                                montoCompradoSucursalRango = montoCompradoSucursalRango + montoComprado


                    #COMPRAS
                    
                    gananciaSucursalRango = montoIngresoSucursalRangoTabla - montoCompradoSucursalRango
                    if gananciaSucursalRango > 0:
                        signoRango = "+"
                    else:
                        signoRango = "-"
                        
                    #margen
                    if montoCompradoSucursalRango == 0:
                        margenSucursalRango = montoIngresoSucursalRangoTabla
                    else:
                        margenSucursalRango = (montoIngresoSucursalRangoTabla * 100)/montoCompradoSucursalRango
                        margenSucursalRango = round(margenSucursalRango,2)
                        margenSucursalRango = margenSucursalRango - 100
                        margenSucursalRango=round(margenSucursalRango,2)
                    margenDeGananciaSucursalRango.append(margenSucursalRango)
                    
                    
                    montosIngresosSucursalRango.append(montoIngresoSucursalRangoTabla)
                    montosComprasSucursalRango.append(montoCompradoSucursalRango)
                    gananciaSucursalesRango.append([gananciaSucursalRango, signoRango])
                    
                listaComparativaSucursalesRango = zip(infoSucursalesRango, montosIngresosSucursalRango,montosComprasSucursalRango, gananciaSucursalesRango, margenDeGananciaSucursalRango)

            
            
                
                return render(request, "18 Informe Ventas Sucursal/informeDeSucursal.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "notificacionRenta":notificacionRenta,
                                                                                         "nombreSucursal":nombreSucursal,"direccion":direccion, "telefono":telefono,"latitud":latitud, "longitud":longitud,
                                                                                         "diadehoy":diadehoy, "mesdehoy":mesdehoy, "añoHoy":añoHoy,"idSucursalInforme":idSucursalInforme,
                                                                                         "montoIngresoSucursalMes":montoIngresoSucursalMes, "contadorVentasSucursalMes":contadorVentasSucursalMes, "contadorRentasSucursalMes":contadorRentasSucursalMes, "contadorCreditosSucursalMes":contadorCreditosSucursalMes,
                                                                                         "numeroVentasSucursalMes":numeroVentasSucursalMes, "numeroRentasSucursalMes":numeroRentasSucursalMes, "numeroCreditosSucursalMes":numeroCreditosSucursalMes,
                                                                                         "porcentajeIngresosSucursalMes":porcentajeIngresosSucursalMes,"esMayor":esMayor, "montoIngresoMesSucursalAnterior":montoIngresoMesSucursalAnterior, "mesHaceUnMesLetra":mesHaceUnMesLetra,
                                                                                         "montoIngresoEnero":montoIngresoEnero,"montoIngresoFebrero":montoIngresoFebrero, "montoIngresoMarzo":montoIngresoMarzo, "montoIngresoAbril":montoIngresoAbril, "montoIngresoMayo":montoIngresoMayo, "montoIngresoJunio":montoIngresoJunio, "montoIngresoJulio":montoIngresoJulio,"montoIngresoAgosto":montoIngresoAgosto,
                                                                                         "montoIngresoSeptiembre":montoIngresoSeptiembre, "montoIngresoOctubre":montoIngresoOctubre, "montoIngresoNoviembre":montoIngresoNoviembre, "montoIngresoDiciembre":montoIngresoDiciembre,
                                                                                         "totalComprasMesGasto":totalComprasMesGasto, "totalComprasMesVenta":totalComprasMesVenta, "totalComprasMesRenta":totalComprasMesRenta, "sumaTotalesCompras":sumaTotalesCompras, 
                                                                                         "numeroComprasGasto":numeroComprasGasto, "numeroComprasVenta":numeroComprasVenta, "numeroComprasRenta":numeroComprasRenta, 
                                                                                         "comprasProductosGastosSucursalMes":comprasProductosGastosSucursalMes,"comprasProductosVentasSucursalMes":comprasProductosVentasSucursalMes,"comprasProductosRentasSucursalMes":comprasProductosRentasSucursalMes, "utilidadSucursalMes":utilidadSucursalMes,"utilidadMayor":utilidadMayor,
                                                                                         "infoSucursales":infoSucursales, "montosVendidos":montosVendidos, "listaComparativaSucursalesMes":listaComparativaSucursalesMes,
                                                                                         "montoIngresoSucursalAño":montoIngresoSucursalAño, "añoMenosUno":añoMenosUno, "añoMenosDos":añoMenosDos,"añoMenosTres":añoMenosTres, "contadorVentasHaceUnAño":contadorVentasHaceUnAño,
                                                                                         "esMayorAñoSucursal":esMayorAñoSucursal, "porcentajeIngresosSucursalAño":porcentajeIngresosSucursalAño,
                                                                                         "contadorVentasHaceUnAño":contadorVentasHaceUnAño, "contadorVentasHaceDosAños":contadorVentasHaceDosAños, "contadorVentasHaceTresAños":contadorVentasHaceTresAños,
                                                                                         "sumaTotalesComprasDelAño":sumaTotalesComprasDelAño, "utilidadSucursalAño":utilidadSucursalAño, "utilidadMayorAño":utilidadMayorAño,
                                                                                         "totalComprasAñoGasto":totalComprasAñoGasto,"totalComprasAñoVenta":totalComprasAñoVenta,"totalComprasAñoRenta":totalComprasAñoRenta,
                                                                                         "numeroComprasGastoAño":numeroComprasGastoAño,"numeroComprasVentaAño":numeroComprasVentaAño, "numeroComprasRentaAño":numeroComprasRentaAño,
                                                                                         "comprasProductosGastosSucursalAño":comprasProductosGastosSucursalAño,"comprasProductosVentasSucursalAño":comprasProductosVentasSucursalAño, "comprasProductosRentasSucursalAño":comprasProductosRentasSucursalAño,
                                                                                         "listaComparativaSucursalesAño":listaComparativaSucursalesAño,
                                                                                         "rangoFechaRecibida":rangoFechaRecibida, "stringFechaInicioRango":stringFechaInicioRango,"stringFechaFinalRango":stringFechaFinalRango, "montoIngresoSucursalRango":montoIngresoSucursalRango,
                                                                                         "fechaTextoInicioPeriodoAnterior":fechaTextoInicioPeriodoAnterior, "fechaTextoFinalPeriodoDespues":fechaTextoFinalPeriodoDespues,
                                                                                         "contadorVentasPeriodoAnterior":contadorVentasPeriodoAnterior,"contadorVentasPeriodoDespues":contadorVentasPeriodoDespues, "esMayorPeriodoSucursal":esMayorPeriodoSucursal,
                                                                                         "porcentajeIngresosSucursalRango":porcentajeIngresosSucursalRango,
                                                                                         "totalComprasRangoGasto":totalComprasRangoGasto, "totalComprasRangoVenta":totalComprasRangoVenta, "totalComprasRangoRenta":totalComprasRangoRenta,
                                                                                         "numeroComprasGastoRango":numeroComprasGastoRango,"numeroComprasVentaRango":numeroComprasVentaRango, "numeroComprasRentaRango":numeroComprasRentaRango, "utilidadSucursalRango":utilidadSucursalRango,"utilidadMayorRango":utilidadMayorRango, "sumaTotalesComprasDelRango":sumaTotalesComprasDelRango, "listaComparativaSucursalesRango":listaComparativaSucursalesRango,"notificacionCita":notificacionCita})
                
                

            return render(request, "18 Informe Ventas Sucursal/informeDeSucursal.html", {"consultaPermisos":consultaPermisos,"idEmpleado":idEmpleado,"idPerfil":idPerfil, "idConfig":idConfig, "nombresEmpleado":nombresEmpleado,"tipoUsuario":tipoUsuario, "letra":letra, "puestoEmpleado":puestoEmpleado, "notificacionRenta":notificacionRenta,
                                                                                         "nombreSucursal":nombreSucursal,"direccion":direccion, "telefono":telefono,"latitud":latitud, "longitud":longitud,
                                                                                         "diadehoy":diadehoy, "mesdehoy":mesdehoy, "añoHoy":añoHoy,"idSucursalInforme":idSucursalInforme,
                                                                                         "montoIngresoSucursalMes":montoIngresoSucursalMes, "contadorVentasSucursalMes":contadorVentasSucursalMes, "contadorRentasSucursalMes":contadorRentasSucursalMes, "contadorCreditosSucursalMes":contadorCreditosSucursalMes,
                                                                                         "numeroVentasSucursalMes":numeroVentasSucursalMes, "numeroRentasSucursalMes":numeroRentasSucursalMes, "numeroCreditosSucursalMes":numeroCreditosSucursalMes,
                                                                                         "porcentajeIngresosSucursalMes":porcentajeIngresosSucursalMes,"esMayor":esMayor, "montoIngresoMesSucursalAnterior":montoIngresoMesSucursalAnterior, "mesHaceUnMesLetra":mesHaceUnMesLetra,
                                                                                         "montoIngresoEnero":montoIngresoEnero,"montoIngresoFebrero":montoIngresoFebrero, "montoIngresoMarzo":montoIngresoMarzo, "montoIngresoAbril":montoIngresoAbril, "montoIngresoMayo":montoIngresoMayo, "montoIngresoJunio":montoIngresoJunio, "montoIngresoJulio":montoIngresoJulio,"montoIngresoAgosto":montoIngresoAgosto,
                                                                                         "montoIngresoSeptiembre":montoIngresoSeptiembre, "montoIngresoOctubre":montoIngresoOctubre, "montoIngresoNoviembre":montoIngresoNoviembre, "montoIngresoDiciembre":montoIngresoDiciembre,
                                                                                         "totalComprasMesGasto":totalComprasMesGasto, "totalComprasMesVenta":totalComprasMesVenta, "totalComprasMesRenta":totalComprasMesRenta, "sumaTotalesCompras":sumaTotalesCompras, 
                                                                                         "numeroComprasGasto":numeroComprasGasto, "numeroComprasVenta":numeroComprasVenta, "numeroComprasRenta":numeroComprasRenta, 
                                                                                         "comprasProductosGastosSucursalMes":comprasProductosGastosSucursalMes,"comprasProductosVentasSucursalMes":comprasProductosVentasSucursalMes,"comprasProductosRentasSucursalMes":comprasProductosRentasSucursalMes, "utilidadSucursalMes":utilidadSucursalMes,"utilidadMayor":utilidadMayor,
                                                                                         "infoSucursales":infoSucursales, "montosVendidos":montosVendidos, "listaComparativaSucursalesMes":listaComparativaSucursalesMes,
                                                                                         "montoIngresoSucursalAño":montoIngresoSucursalAño, "añoMenosUno":añoMenosUno, "añoMenosDos":añoMenosDos,"añoMenosTres":añoMenosTres, "contadorVentasHaceUnAño":contadorVentasHaceUnAño,
                                                                                         "esMayorAñoSucursal":esMayorAñoSucursal, "porcentajeIngresosSucursalAño":porcentajeIngresosSucursalAño,
                                                                                         "contadorVentasHaceUnAño":contadorVentasHaceUnAño, "contadorVentasHaceDosAños":contadorVentasHaceDosAños, "contadorVentasHaceTresAños":contadorVentasHaceTresAños,
                                                                                         "sumaTotalesComprasDelAño":sumaTotalesComprasDelAño, "utilidadSucursalAño":utilidadSucursalAño, "utilidadMayorAño":utilidadMayorAño,
                                                                                         "totalComprasAñoGasto":totalComprasAñoGasto,"totalComprasAñoVenta":totalComprasAñoVenta,"totalComprasAñoRenta":totalComprasAñoRenta,
                                                                                         "numeroComprasGastoAño":numeroComprasGastoAño,"numeroComprasVentaAño":numeroComprasVentaAño, "numeroComprasRentaAño":numeroComprasRentaAño,
                                                                                         "comprasProductosGastosSucursalAño":comprasProductosGastosSucursalAño,"comprasProductosVentasSucursalAño":comprasProductosVentasSucursalAño, "comprasProductosRentasSucursalAño":comprasProductosRentasSucursalAño,
                                                                                         "listaComparativaSucursalesAño":listaComparativaSucursalesAño, "notificacionCita":notificacionCita})
    else:
        
        return render(request,"1 Login/login.html")
    