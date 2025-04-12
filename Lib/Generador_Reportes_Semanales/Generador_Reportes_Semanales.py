"""
Autor: odvr
Modificación: 07-03-2025


La siguiente Función debe recorrer toda la información para enviar reportes semanales a los clientes registrados en la Plataforma

"""
from datetime import datetime

from Lib.Notificaciones.Notificaciones_Whatsapp import enviar_Notificaciones_Whatsapp
# Librerias

from config.db import get_session
from sqlalchemy.orm import Session
import crud
from models.modelo_bovinos import modelo_indicadores, modelo_reporte_Semanal

def GenerarReportesSemanales():
    session: Session = get_session()

    IndicadoresClientes = session.query(modelo_indicadores).all()

    for IndicadoresCliente in IndicadoresClientes:
        try:
            usuario_id = IndicadoresCliente.id_indicadores
            fecha_generacionReporte = datetime.now()

            BuscarUltimosNacimientosUltimos7dias = crud.InformacionReportesUsuarios.Buscar_Animales_Nacidos_EnlosUltimos_7_dias(
                db=session, current_user=usuario_id)
            BuscarAnimalesMuertosUltimos7dias = crud.InformacionReportesUsuarios.Buscar_Animales_Muertos_Ultimos_7_dias(
                db=session, current_user=usuario_id)
            BuscarAnimalesVendidosUltimos7dias = crud.InformacionReportesUsuarios.Buscar_Animales_Vendidos_Ultimos_7_dias(
                db=session, current_user=usuario_id)
            Buscar_Animales_Comprado_Ultimos_7_dias = crud.InformacionReportesUsuarios.Buscar_Animales_Comprados_Ultimos_7_dias(
                db=session, current_user=usuario_id)
            BuscarTotalVentasUltimos7Dias = crud.InformacionReportesUsuarios.Buscar_Animales_TotalVentas_Ultimos_7_dias(
                db=session, current_user=usuario_id)
            TotalNomina = crud.InformacionReportesUsuarios.Buscar_Total_Nomina(db=session, current_user=usuario_id)

            # Obtener el número de celular
            NumeroCelular = crud.bovinos_inventario.Buscar_Celular_Usuario(db=session, usuario_id=usuario_id)
            if not NumeroCelular:
                print(f"Error: No se encontró un número de celular para usuario_id={usuario_id}")
                continue  # Salta al siguiente usuario si no hay número

            MensajeReporte = (
                f"📢 *Reporte Semanal del Inventario Ganadero* 📢\n"
                f"📅 *Fecha:* {fecha_generacionReporte.strftime('%d-%m-%Y')}\n"
                f"🏡 *Propietario:* {usuario_id}\n"
                f"-------------------------------------\n"
                f"🐄 *Total de animales:* {IndicadoresCliente.total_animales or 0}\n"
                f"🔄 *Tasa de Supervivencia:* {IndicadoresCliente.tasa_supervivencia or 0}%\n"
                f"🥛 *Producción de leche:* {IndicadoresCliente.animales_leche or 0} animales\n"
                f"🐮 *Animales en levante:* {IndicadoresCliente.animales_levante or 0}\n"
                f"🔹 *Óptimos para levante:* {IndicadoresCliente.animales_optimos_levante or 0}\n"
                f"🐂 *Animales en ceba:* {IndicadoresCliente.animales_ceba or 0}\n"
                f"🔹 *Óptimos para ceba:* {IndicadoresCliente.animales_optimos_ceba or 0}\n"
                f"🔄 *IEP promedio:* {IndicadoresCliente.IEP_hato or 0} días\n"
                f"👶 *Terneros perdidos:* {IndicadoresCliente.perdida_de_terneros or 0}\n"
                f"🍼 *Tasa de supervivencia:* {IndicadoresCliente.tasa_supervivencia or 0}%\n"
                f"🔹 *Vacas preñadas:* {IndicadoresCliente.vacas_prenadas or 0}\n"
                f"🔹 *Vacas vacías:* {IndicadoresCliente.vacas_vacias or 0}\n"
                f"🐂 *Machos:* {IndicadoresCliente.machos or 0}  |  🐄 *Hembras:* {IndicadoresCliente.hembras or 0}\n"
                f"⚖️ *Total unidades animales:* {IndicadoresCliente.total_unidades_animales or 0}\n"
                f"-------------------------------------\n"
                f"📊 *Eventos en los últimos 7 días:*\n"
                f"👶 *Nacimientos:* {BuscarUltimosNacimientosUltimos7dias or 0}\n"
                f"☠️ *Muertes:* {BuscarAnimalesMuertosUltimos7dias or 0}\n"
                f"💰 *Animales vendidos:* {BuscarAnimalesVendidosUltimos7dias or 0}\n"
                f"🛒 *Animales comprados:* {Buscar_Animales_Comprado_Ultimos_7_dias or 0}\n"
                f"💲 *Total de ventas:* {BuscarTotalVentasUltimos7Dias or 0}\n"
                f"👷‍♂️ *Total Nómina Empleados:* {TotalNomina or 0}\n"
                f"-------------------------------------\n"
                
                
                  f"🚀 *¿Tienes novedades para registrar? ¡Nosotros lo hacemos por ti!* 📲\n"
f"🔍 *Lleva el control de tu ganadería fácilmente.* Ingresa hoy y mantén tu información al día: 👉 [https://ganaderia.sinarca.co/](https://ganaderia.sinarca.co/) 🌱🐄\n"
 f"-------------------------------------\n"
f"✅ *Fin del reporte.*"
            )

            # Enviar el reporte vía WhatsApp
            enviar_Notificaciones_Whatsapp(NumeroCelular, MensajeReporte)

            # Insertar reporte en la base de datos
            IngresoReporteSemanal = modelo_reporte_Semanal.insert().values(
                usuario_id=usuario_id,
                fecha_generacion=fecha_generacionReporte,
                total_animales=IndicadoresCliente.total_animales,
                animales_produccion_leche=IndicadoresCliente.animales_leche,
                animales_levante=IndicadoresCliente.animales_levante,
                animales_ceba=IndicadoresCliente.animales_ceba,
                periodo_iep_promedio=IndicadoresCliente.IEP_hato,
                porcentaje_ordeno=IndicadoresCliente.porcentaje_ordeno,
                animales_optimos_ceba=IndicadoresCliente.animales_optimos_ceba,
                animales_optimos_levante=IndicadoresCliente.animales_optimos_levante,
                vacas_vacias=IndicadoresCliente.vacas_vacias,
                vacas_prenadas=IndicadoresCliente.vacas_prenadas,
                porcentaje_prenadas=IndicadoresCliente.vacas_prenadas_porcentaje,
                perdida_de_terneros=IndicadoresCliente.perdida_de_terneros,
                tasa_supervivencia_actual=IndicadoresCliente.tasa_supervivencia,
                machos=IndicadoresCliente.machos,
                hembras=IndicadoresCliente.hembras,
                vacas_en_ordeno=IndicadoresCliente.vacas_en_ordeno,
                vacas_no_ordeno=IndicadoresCliente.vacas_no_ordeno,
                animales_rango_edades_0_9=IndicadoresCliente.animales_rango_edades_0_9,
                animales_rango_edades_9_12=IndicadoresCliente.animales_rango_edades_9_12,
                animales_rango_edades_12_24=IndicadoresCliente.animales_rango_edades_12_24,
                animales_rango_edades_24_36=IndicadoresCliente.animales_rango_edades_24_36,
                animales_rango_edades_mayor_36=IndicadoresCliente.animales_rango_edades_mayor_36,
                vientres_aptos=IndicadoresCliente.vientres_aptos,
                relacion_toros_vientres_aptos=IndicadoresCliente.relacion_toros_vientres_aptos,
                interpretacion_relacion_toros_vientres_aptos=IndicadoresCliente.interpretacion_relacion_toros_vientres_aptos,
                total_unidades_animales=IndicadoresCliente.total_unidades_animales,
            )
            session.execute(IngresoReporteSemanal)
            session.commit()

        except Exception as e:
            session.rollback()  # Revierte cambios en caso de error
            print(f"Error al insertar reporte semanal: {e}")
    return


