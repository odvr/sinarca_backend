"""
@autor
El siguiente codigo permitira realizar el esquema de bases de datos para el metodo Post
"""
#importar los tipos de datos
# permite modelar los datos o crearlos
#,
from pydantic import BaseModel
from datetime import date
from typing import Optional,Union
from uuid import UUID
from decimal import Decimal

from pydantic.datetime_parse import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
#from passlib.context import CryptContext

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Esquema_Usuario(BaseModel):
    id_usuario : Optional[int]
    usuario_id :str
    hashed_password: str
    nombre_predio: Optional[str]
    correo_electronico: Optional[str]
    codigo_asociacion: Optional[str]
    telefono: Optional[str]
    tipo_usuario: Optional[str]
    ubicacion_predio: Optional[str]
    nombre_apellido: Optional[str]
    fecha_de_registro: Optional[date]
    ultimo_login: Optional[date]
    indicador_pais: Optional[int]

    class Config:
        orm_mode = True
        env_file = ".env"
class Esquema_Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        orm_mode = True
        env_file = ".env"



class User(BaseModel):
    id = str
    username = str
    hashed_password = str

class Usuarios(BaseModel):
    id_usuario : str
    full_name : Union[str,None]=None
    hashed_password: str


class UsuariosInDB(Usuarios):
     hashed_password:str


class TokenData(BaseModel):
    email:str

    class Config:
        orm_mode = True
        env_file = ".env"
class UserAuth(BaseModel):
    email:str
    username: str
    password: str

    class Config:
        orm_mode = True
        env_file = ".env"


class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        orm_mode = True
        env_file = ".env"


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        orm_mode = True
        env_file = ".env"


class TokenPayload(BaseModel):
    sub: UUID = None
    exp: int = None

    class Config:
        orm_mode = True
        env_file = ".env"

class Esquema_bovinos(BaseModel):
    id_bovino : int
    fecha_nacimiento: date
    edad: Optional[int] = None
    sexo :Optional[str] = None
    raza : Optional[str] = None
    peso: Optional[float] = None
    marca :Optional[str] = None
    proposito: Optional[str] = None
    mansedumbre :Optional[str] = None
    estado: Optional[str] = None
    compra_bovino: Optional[str] = None
    usuario_id:Optional[str] = None
    nombre_bovino:Optional[str] = None
    ruta_imagen_marca:Optional[str] = None
    ruta_fisica_foto_perfil: Optional[str] = None
    fecha_de_ingreso_hato: Optional[date] = None
    fecha_de_ingreso_sistema: Optional[date] = None
    edad_destete: Optional[int] = None
    nombre_lote_bovino: Optional[str] = None
    chip_asociado: Optional[str] = None
    id_finca   : Optional [int] = None
    nombre_finca: Optional[str] = None
    edad_YY_MM_DD: Optional[str] = None
    numero_chapeta: Optional[str] = None
    numero_upp: Optional[str] = None
    numero_siniiga: Optional[str] = None

    #Este Config La clase se utiliza para proporcionar configuraciones a Pydantic.
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_produccion_ceba(BaseModel):
    id_ceba: int
    proposito: Optional[str] = None
    id_bovino : Optional[int] = None
    edad: Optional[int] = None
    peso: Optional[int] = None
    estado: Optional[str] = None
    estado_optimo_ceba: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    ganancia_media_diaria: Optional[float] = None
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_produccion_levante(BaseModel):
    id_levante:int
    id_bovino:int
    edad: Optional[int] = None
    peso: Optional[int] = None
    estado: Optional[str] = None
    proposito: Optional[str] = None
    estado_optimo_levante : Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    ganancia_media_diaria:Optional[float] = None

    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_produccion_leche(BaseModel):
    id_leche: int
    id_bovino: int
    fecha_primer_parto: Optional[date] = None
    edad_primer_parto: Optional[int] = None
    datos_prenez: Optional[str] = None
    fecha_vida_util: Optional[date] = None
    ordeno: Optional[str] = None
    proposito: Optional[str] = None
    promedio_litros : Optional[float] = None
    num_partos: Optional[int] = None
    intervalo_entre_partos : Optional[float] = None
    tipo_ganado: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    dias_abiertos: Optional[int] = None
    cantidad_partos_manual: Optional[int] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_datos_muerte(BaseModel):
    id_datos_muerte: int
    id_bovino: int
    estado: Optional[str] = None
    razon_muerte: Optional[str] = None
    fecha_muerte: Optional[date] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_arbol_genealogico(BaseModel):
    id_arbol_genealogico: int
    id_bovino: int
    id_bovino_madre: Optional[int] = None
    id_bovino_padre: Optional[int] = None
    abuelo_paterno:Optional[int] = None
    abuela_paterna:Optional[int] = None
    abuelo_materno:Optional[int] = None
    abuela_materna:Optional[int] = None
    bisabuelo_materno:Optional[int] = None
    bisabuelo_paterno:Optional[int] = None
    tipo_de_apareamiento:Optional[str] = None
    consanguinidad:Optional[float] = None
    notificacion:Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    nombre_bovino_madre:Optional[str] = None
    nombre_bovino_padre:Optional[str] = None
    nombre_bovino_abuelo_paterno:Optional[str] = None
    nombre_bovino_abuela_paterna:Optional[str] = None
    nombre_bovino_abuelo_materno:Optional[str] = None
    nombre_bovino_abuela_materna:Optional[str] = None
    nombre_bovino_bisabuelo_materno:Optional[str] = None
    nombre_bovino_bisabuelo_paterno:Optional[str] = None
    inseminacion: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_indicadores(BaseModel):
    id_indicadores: str
    perdida_de_terneros: Optional[float] = None
    tasa_supervivencia: Optional[float] = None
    total_animales:Optional[int] = None
    vacas_prenadas_porcentaje:Optional[float] = None
    animales_levante:Optional[int] = None
    animales_ceba:Optional[int] = None
    animales_leche:Optional[int] = None
    vacas_prenadas:Optional[int] = None
    vacas_vacias:Optional[int] = None
    animales_fallecidos:Optional[int] = None
    animales_vendidos:Optional[int] = None
    machos:Optional[int] = None
    hembras:Optional[int] = None
    vacas_en_ordeno:Optional[int] = None
    vacas_no_ordeno:Optional[int] = None
    porcentaje_ordeno:Optional[float] = None
    animales_rango_edades_0_9:Optional[int] = None
    animales_rango_edades_9_12:Optional[int] = None
    animales_rango_edades_12_24:Optional[int] = None
    animales_rango_edades_24_36:Optional[int] = None
    animales_rango_edades_mayor_36:Optional[int] = None
    animales_optimos_levante:Optional[int] = None
    animales_optimos_ceba:Optional[int] = None
    vientres_aptos:Optional[int] = None
    relacion_toros_vientres_aptos:Optional[int]
    interpretacion_relacion_toros_vientres_aptos:Optional[str]
    total_unidades_animales:Optional[str] = None
    IEP_hato:Optional[float] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_macho_reproductor(BaseModel):
    id_macho: int
    id_bovino: int
    edad: Optional[int] = None
    peso: Optional[int] = None
    estado: Optional[str] = None
    fecha_vida_util: Optional[date] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_modelo_ventas(BaseModel):
    id_venta: int
    id_bovino: Optional[int] = None
    numero_bono_venta: Optional[str] = None
    estado: Optional[str] = None
    fecha_venta: Optional[date] = None
    precio_venta: Optional[int] = None
    razon_venta: Optional[str] = None
    medio_pago: Optional[str] = None
    comprador: Optional[str] = None
    peso_venta: Optional[str] = None
    valor_kg_venta: Optional[str] = None
    id_factura_asociada: Optional[int] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_modelo_compra(BaseModel):
    id_compra_bovino: int
    id_bovino: int
    numero_bono_compra: Optional[str] = None
    estado: Optional[str] = None
    fecha_compra: Optional[date] = None
    precio_compra: Optional[int] = None
    razon_compra: Optional[str] = None
    medio_pago_compra: Optional[str] = None
    comprador: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_modelo_Reporte_Pesaje(BaseModel):
    id_pesaje: int
    id_bovino: int
    fecha_pesaje: date
    peso:float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    tipo_pesaje:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_veterinaria(BaseModel):
    id_veterinaria:int
    id_bovino:Optional[int] = None
    sintomas:Optional[str] = None
    fecha_sintomas:Optional[date] = None
    comportamiento:Optional[str] = None
    condicion_corporal:Optional[str] = None
    postura:Optional[str] = None
    mucosa_ocular:Optional[str] = None
    mucosa_bucal:Optional[str] = None
    mucosa_rectal:Optional[str] = None
    mucosa_vulvar_prepusial:Optional[str] = None
    tratamiento:Optional[str] = None
    evolucion:Optional[str] = None
    piel_pelaje:Optional[str] = None
    estado_Historia_clinica:Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"





class esquema_veterinaria_evoluciones(BaseModel):
    id_evolucion: int
    id_bovino: int
    tratamiento_evolucion:Optional[str] = None
    fecha_evolucion: Optional[date] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_registro_vacunas_bovinos(BaseModel):
    id_vacunacion_bovinos: int
    id_bovino: int
    fecha_registrada_usuario:Optional[date] = None
    tipo_vacuna: Optional[str] = None
    nombre_lote_asociado: Optional[str] = None
    estado_evento_lotes: Optional[str] = None
    id_evento_lote_asociado: Optional[int] = None
    fecha_bitacora_Sistema: Optional[date] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_veterinaria_comentarios(BaseModel):
    id_comentario: int
    id_veterinaria: int
    comentarios:Optional[str] = None
    fecha_comentario: date
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"



class esquema_descarte(BaseModel):
    id_descarte: int
    id_bovino: int
    edad:Optional[int] = None
    peso:Optional[float] = None
    razon_descarte:Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_partos(BaseModel):
    id_parto: int
    id_bovino: int
    edad: Optional[int] = None
    peso: Optional[int] = None
    fecha_estimada_prenez: Optional[date] = None
    fecha_estimada_parto: Optional[date] = None
    notificacion: Optional[str] = None
    tipo: Optional[str] = None
    id_reproductor: Optional[str] = None
    nombre_bovino_reproductor: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None


    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_palpaciones(BaseModel):
    id_palpacion: int
    id_bovino:Optional[int] = None
    fecha_palpacion: Optional[date] = None
    diagnostico_prenez: Optional[str] = None
    observaciones: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    notificacion:Optional[str] = None
    tipo:Optional[str] = None
    id_reproductor:Optional[int] = None
    nombre_bovino_reproductor:Optional[str] = None
    dias_gestacion:Optional[int] = None
    fecha_estimada_prenez: Optional[date] = None
    fecha_estimada_parto: Optional[date] = None


    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_dias_abiertos(BaseModel):
    id_dias_abiertos: int
    id_bovino: int
    fecha_parto: Optional[date] = None
    fecha_prenez: Optional[date] = None
    dias_abiertos: Optional[int] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None


    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_carga_animal_y_consumo_agua(BaseModel):
    id_carga_animal: int
    id_bovino: Optional[int] = None
    edad: Optional[int] = None
    peso: Optional[int] = None
    valor_unidad_animal: float
    consumo_forraje_vivo:float
    raza: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    id_lote: Optional[int] = None
    nombre_lote: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_capacidad_carga(BaseModel):
    id_capacidad: int
    medicion_aforo: Optional[float]= None
    hectareas_predio: Optional[float]= None
    periodo_ocupacion: Optional[int] = None
    carga_animal_usuario: Optional[float]= None
    usuario_id: Optional[str] = None
    nombre_potrero:Optional[str] = None
    interpretacion: Optional[str] = None
    id_lote: Optional[int] = None
    nombre_lote: Optional[str] = None
    estado: Optional[str] = None
    fecha_inicio_ocupacion: Optional[date] = None
    fecha_final_recomendada: Optional[date] = None
    fecha_final_real: Optional[date] = None
    fecha_inicio_descanso: Optional[date] = None
    fecha_final_descanso: Optional[date] = None
    dias_descanso: Optional[int] = None
    id_finca   : Optional[int] = None
    nombre_finca: Optional[str] = None
    id_potrero: int
    nombre_potrero: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_registro_ocupaciones_potreros(BaseModel):
    id_ocupacion: int
    id_potrero: int
    nombre_potrero: Optional[str] = None
    id_lote: Optional[int] = None
    nombre_lote: Optional[str] = None
    fecha_inicio_ocupacion: Optional[date] = None
    fecha_final_recomendada: Optional[date] = None
    fecha_final_real: Optional[date] = None
    observacion: Optional[str] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_calculadora_hectareas_pastoreo(BaseModel):
    id_pastoreo: int
    id_bovino: int
    hectareas_necesarias: int
    consumo_agua: int
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_vientres_aptos(BaseModel):
    id_vientre: int
    id_bovino: Optional[int] = None
    edad: Optional[int] = None
    peso: Optional[float] = None
    raza: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_historial_partos(BaseModel):
    id_parto:Optional[int] = None
    id_bovino:Optional[int] = None
    fecha_parto: Optional[date] = None
    tipo_parto: Optional[str] = None
    id_bovino_hijo:Optional[int] = None
    usuario_id: Optional[str] = None
    id_bovino_madre:Optional[int] = None
    id_bovino_padre:Optional[int] = None
    nombre_madre:Optional[str] = None
    nombre_padre:Optional[str] = None
    cantidad:Optional[int] = None
    tecnica_reproduccion:Optional[str] = None
    observaciones:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_detalles_partos(BaseModel):
    id_detalle_parto:Optional[int] = None
    id_bovino_madre:Optional[int] = None
    id_bovino_padre:Optional[int] = None
    nombre_madre:Optional[str] = None
    nombre_padre:Optional[str] = None
    fecha_parto: Optional[date] = None
    id_bovino_hijo:Optional[int] = None
    nombre_hijo: Optional[str] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_intervalo_partos(BaseModel):
    id_intervalo: int
    id_bovino: int
    fecha_parto1: date
    fecha_parto2: date
    intervalo:float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_litros_leche(BaseModel):
    id_litros: int
    id_bovino: int
    fecha_medicion: date
    litros_leche:float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_reporte_curva_lactancia_General(BaseModel):
    id_curva_lactancia_general: int
    id_bovino:int
    anio: str
    mes: str
    promedio:float
    Hora_Reporte:date
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_orden_IEP(BaseModel):
    id_IEP: int
    id_bovino: int
    raza: str
    intervalo_promedio_raza: float
    intervalo_promedio_animal: float
    diferencia: float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_orden_litros(BaseModel):
    id_litros_leche: int
    id_bovino: int
    raza: str
    litros_promedio_raza: float
    litros_promedio_animal: float
    diferencia: float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_orden_peso(BaseModel):
    id_peso: int
    id_bovino: int
    raza: str
    peso_promedio_raza: float
    peso_promedio_animal: float
    diferencia: float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_historial_perdida_terneros(BaseModel):
    id_perdida: int
    periodo: int
    perdida:float
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_historial_supervivencia(BaseModel):
    id_supervivencia: int
    periodo: int
    supervivencia:float
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_registro_pajillas(BaseModel):
    id_pajillas: int
    Codigo_toro_pajilla: Optional[str] = None
    raza: Optional[str] = None
    nombre_toro: Optional[str] = None
    productor: Optional[str] = None
    unidades: Optional[int] = None
    precio: Optional[int] = None
    nombre_canastilla: Optional[str] = None
    id_canastilla: Optional[int] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"



class esquema_registro_marca(BaseModel):
    id_registro_marca:int
    nombre_marca_propietario: Optional[str] = None
    ruta_marca:Optional[str] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_parametros_levante_ceba(BaseModel):
    id_parametros: int
    peso_levante: Optional[int] = None
    edad_levante: Optional[int] = None
    peso_ceba: Optional[int] = None
    edad_ceba: Optional[int] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_canastillas(BaseModel):
    id_canastilla: int
    nombre_canastilla: Optional[str] = None
    unidades_disponibles: Optional[str] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_registro_celos(BaseModel):
    id_celo: int
    id_bovino: int
    nombre_bovino: Optional[str] = None
    fecha_celo: date
    observaciones: str
    servicio:Optional[str] = None
    id_servicio: Optional[int] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_tasas_concepcion(BaseModel):
    id_tasa: int
    id_bovino: int
    nombre_bovino: Optional[str] = None
    servicios_concepcion: int
    fecha_prenez: date
    tasa_concepcion: Optional[float] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"



class esquema_ganancia_historica_peso(BaseModel):
    id_ganancia: int
    id_bovino: int
    nombre_bovino: Optional[str] = None
    peso_anterior: Optional[float] = None
    peso_posterior: Optional[float] = None
    fecha_anterior: date
    fecha_posterior: date
    dias: int
    ganancia_diaria_media: float
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_natalidad_paricion_real(BaseModel):
    id_natalidad: int
    periodo: int
    intervalo_entre_partos_periodo: Optional[float] = None
    natalidad_paricion_real: Optional[float] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"



class esquema_periodos_lactancia(BaseModel):
    id_lactancia: int
    id_bovino: int
    nombre_bovino: Optional[str] = None
    fecha_inicio_lactancia: Optional[date] = None
    fecha_final_lactancia: Optional[date] = None
    duracion:Optional[int] = None
    total_litros_producidos:Optional[float] = None
    tipo: Optional[str] = None
    pico:Optional[float] = None
    fecha_pico: Optional[date] = None
    usuario_id: Optional[str] = None
    id_parto:Optional[int] = None
    mensaje:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_periodos_secado(BaseModel):
    id_secado: int
    id_bovino: int
    nombre_bovino: Optional[str] = None
    fecha_inicio_secado: Optional[date] = None
    fecha_final_secado: Optional[date] = None
    tratamiento: Optional[str] = None
    duracion:Optional[int] = None
    observaciones: Optional[str] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_evaluaciones_macho_reproductor(BaseModel):
    id_evaluacion: int
    id_bovino: int
    nombre_bovino: Optional[str] = None
    fecha_evaluacion: Optional[date] = None
    edad_evaluacion:Optional[int] = None
    circunferencia_escrotal: Optional[str] = None
    simetria_testicular: Optional[str] = None
    forma_escrotal:Optional[str] = None
    consistencia_testiculos: Optional[str] = None
    tamano_prepucio: Optional[str] = None
    linea_dorsal: Optional[str] = None
    tipo_pezuna: Optional[str] = None
    muculatura: Optional[str] = None
    pezunas: Optional[str] = None
    mensaje: Optional[str] = None
    estado_solicitud_reproductor: Optional[str] = None
    comentarios_evaluacion_reproductor: Optional[str] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_lotes_bovinos(BaseModel):
    id_lote_bovinos: int
    nombre_lote: Optional[str] = None
    estado: Optional[str] = None
    ubicacion: Optional[str] = None
    tipo_uso: Optional[str] = None
    observaciones: Optional[str] = None
    usuario_id: Optional[str] = None
    total_bovinos: Optional[int] = None
    id_finca   : Optional[int] = None
    nombre_finca: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_manejo_ternero_recien_nacido_lotes(BaseModel):
    manejo_ternero_recien_nacido_lotes: int
    estado_solicitud_recien_nacido: Optional[str] = None
    id_bovino: Optional[int] = None
    nombre_bovino: Optional[str] = None
    estado_respiratorio_inicial_lote: Optional[str] = None
    fecha_desinfeccion_lote: Optional[str] = None
    producto_usado_lote: Optional[str] = None
    metodo_aplicacion_lote: Optional[int] = None
    notificar_evento_lote: Optional[int] = None
    nombre_lote_asociado: Optional[int] = None


    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_eventos_asociados_lotes(BaseModel):
    id_eventos_asociados: int
    id_lote_asociado: Optional[str] = None
    nombre_lote: Optional[str] = None
    nombre_evento: Optional[str] = None
    estado_evento: Optional[str] = None
    comentario_evento: Optional[str] = None
    notificaciones_generadas: Optional[int] = None
    usuario_id: Optional[str] = None
    FechaNotificacion: Optional[date] = None

    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_descorne_lotes(BaseModel):
    id_descorne_lote : int
    estado_solicitud_descorne: Optional[str] = None
    metodo_descorne: Optional[str] = None
    fecha_descorne: Optional[date] = None
    id_bovino: Optional[int] = None
    id_evento_lote_asociado: Optional[int] = None
    nombre_bovino: Optional[str] = None
    nombre_lote_asociado: Optional[int] = None
    comentario_descorne: Optional[str] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_control_parasitos_lotes(BaseModel):
    id_control_parasitos : int
    fecha_tratamiento_lote: Optional[date] = None
    tipo_tratamiento: Optional[str] = None
    estado_solicitud_parasitos : Optional[str] = None
    producto_usado: Optional[str] = None
    id_bovino: Optional[int] = None
    nombre_bovino: Optional[str] = None
    id_evento_lote_asociado: Optional[int] = None
    nombre_lote_asociado: Optional[int] = None
    comentario_parasitos: Optional[str] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_control_podologia_lotes(BaseModel):
    id_control_podologia : int
    fecha_registro_podologia: Optional[date] = None
    espacialista_podologia: Optional[str] = None
    estado_solicitud_podologia : Optional[str] = None
    FechaNotificacionPodologia: Optional[date] = None
    id_evento_lote_asociado: Optional[int] = None
    id_bovino: Optional[int] = None
    nombre_bovino: Optional[str] = None
    nombre_lote_asociado: Optional[int] = None
    comentario_podologia: Optional[str] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_envio_correos_publicidad(BaseModel):
    enviar_correos_publicidad : int
    correo_enviado: Optional[str] = None
    fecha_envio: Optional[date] = None
    estado_envio : Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"


"""
Esquema para el sistema DRP
"""

class esquema_clientes(BaseModel):
    cliente_id   : int
    nombre_cliente: Optional[str] = None
    direccion: Optional[str] = None
    telefono : Optional[str] = None
    email: Optional[str] = None
    tipo_cliente: Optional[str] = None
    fecha_creacion: Optional[date] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_facturas(BaseModel):
    factura_id   : int
    cliente_id: Optional[int] = None
    nombre_cliente_proveedor: Optional[str] = None
    radicado_factura: Optional[str] = None
    fecha_emision: Optional[date] = None
    fecha_vencimiento : Optional[date] = None
    monto_total: Optional[int] = None
    saldo_restante: Optional[int] = None
    estado: Optional[str] = None
    destino: Optional[str] = None
    lote_asociado: Optional[str] = None
    tipo_venta: Optional[str] = None
    metodo_pago: Optional[str] = None
    detalle: Optional[str] = None
    usuario_id: Optional[str] = None
    descripcion: Optional[str] = None
    id_finca   : Optional[int] = None
    nombre_finca: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_pagos(BaseModel):
    pago_id   : int
    factura_id: Optional[int] = None
    fecha_pago: Optional[date] = None
    monto : Optional[int] = None
    metodo_pago: Optional[str] = None
    referencia_pago: Optional[str] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"



class esquema_productos(BaseModel):
    producto_id   : int
    nombre_producto: Optional[str] = None
    precio_unitario: Optional[float] = None
    stock_actual : Optional[int] = None
    unidad_medida: Optional[str] = None
    referencia_pago: Optional[str] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_provedores(BaseModel):
    proveedor_id   : int
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono : Optional[str] = None
    correo: Optional[str] = None
    tipoCliente: Optional[str] = None
    tipoPersona: Optional[str] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_movimientos_stock(BaseModel):
    movimiento_id   : int
    producto_id: Optional[int] = None
    tipo_movimiento: Optional[str] = None
    cantidad : Optional[int] = None
    fecha_movimiento: Optional[date] = None
    origen_destino: Optional[str] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_empleados(BaseModel):
    empleado_id  : int
    nombre_empleado: Optional[str] = None
    puesto: Optional[str] = None
    salario_base : Optional[float] = None
    fecha_contratacion: Optional[date] = None
    numero_seguridad_social: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    departamento: Optional[str] = None
    tipo_contrato: Optional[str] = None
    periodicidad_pago: Optional[str] = None
    detalles: Optional[str] = None
    estado: Optional[str] = None
    fecha_retiro: Optional[date] = None
    usuario_id: Optional[str] = None
    id_finca   : Optional[int] = None
    nombre_finca: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_nomina(BaseModel):
    nomina_id   : int
    empleado_id: Optional[int] = None
    periodo: Optional[str] = None
    salario_bruto : Optional[float] = None
    deducciones: Optional[float] = None
    recargos: Optional[float] = None
    salario_neto: Optional[float] = None
    fecha_pago: Optional[date] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_tareas(BaseModel):
    tarea_id   : int
    nombre_tarea: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_asignacion : Optional[date] = None
    fecha_entrega: Optional[date] = None
    empleado_id: Optional[int] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_cotizaciones(BaseModel):
    cotizacion_id   : int
    cliente_id: Optional[int] = None
    producto: Optional[str] = None
    cantidad: Optional[int] = None
    fecha_cotizacion: Optional[date] = None
    total_cotizacion : Optional[float] = None
    estado: Optional[str] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_kpis(BaseModel):
    kpi_id   : int
    nombre_kpi: Optional[str] = None
    valor_actual: Optional[float] = None
    meta : Optional[float] = None
    fecha_actualización: Optional[date] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_presupuestos(BaseModel):
    presupuesto_id   : int
    periodo: Optional[str] = None
    monto_presupuestado: Optional[float] = None
    monto_gastado : Optional[float] = None
    fecha_creacion: Optional[date] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_asociados(BaseModel):
    id_asociado   : int
    correo: Optional[str] = None
    telefono: Optional[str] = None
    codigo : Optional[str] = None
    fecha_creacion: Optional[date] = None

    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_fincas(BaseModel):
    id_finca   : int
    nombre_finca: Optional[str] = None
    departamento: Optional[str] = None
    municipio : Optional[str] = None
    extension: Optional[str] = None
    tipo: Optional[str] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_potreros(BaseModel):
    id_potrero   : int
    nombre_potrero: Optional[str] = None
    extension: Optional[str] = None
    id_finca   : Optional[int] = None
    nombre_finca: Optional[str] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_indicadores_finca(BaseModel):
    id_indicadores_finca:int
    perdida_de_terneros_finca: Optional[float] = None
    tasa_supervivencia_finca: Optional[float] = None
    total_animales_finca:Optional[int] = None
    vacas_prenadas_porcentaje_finca:Optional[float] = None
    animales_levante_finca:Optional[int] = None
    animales_ceba_finca:Optional[int] = None
    animales_leche_finca:Optional[int] = None
    vacas_prenadas_finca:Optional[int] = None
    vacas_vacias_finca:Optional[int] = None
    animales_fallecidos_finca:Optional[int] = None
    animales_vendidos_finca:Optional[int] = None
    machos_finca:Optional[int] = None
    hembras_finca:Optional[int] = None
    vacas_en_ordeno_finca:Optional[int] = None
    vacas_no_ordeno_finca:Optional[int] = None
    porcentaje_ordeno_finca:Optional[float] = None
    animales_rango_edades_0_9_finca:Optional[int] = None
    animales_rango_edades_9_12_finca:Optional[int] = None
    animales_rango_edades_12_24_finca:Optional[int] = None
    animales_rango_edades_24_36_finca:Optional[int] = None
    animales_rango_edades_mayor_36_finca:Optional[int] = None
    animales_optimos_levante_finca:Optional[int] = None
    animales_optimos_ceba_finca:Optional[int] = None
    vientres_aptos_finca:Optional[int] = None
    relacion_toros_vientres_aptos_finca:Optional[int]
    interpretacion_relacion_toros_vientres_aptos_finca:Optional[str]
    total_unidades_animales_finca:Optional[str] = None
    IEP_hato_finca:Optional[float] = None
    usuario_id: Optional[str] = None
    id_finca   :Optional[int] = None
    nombre_finca: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_notificacion_proximidad_parto(BaseModel):
    id_notificacion   : int
    id_bovino: Optional[int] = None
    nombre_bovino: Optional[str] = None
    fecha_estimada_parto : Optional[date] = None
    fecha_mensaje: Optional[date] = None
    mensaje: Optional[str] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_produccion_general_leche(BaseModel):
    id_produccion_leche   : int
    leche: Optional[int] = None
    fecha_ordeno: Optional[datetime] = None
    fecha_registro_sistema : Optional[date] = None
    precio_venta: Optional[str] = None
    factura_id: Optional[int] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"



class EsquemaReportesSemanales(BaseModel):
    id_reporte: int
    fecha_generacion: datetime
    total_animales: Optional[int] = None
    animales_produccion_leche: Optional[int] = None
    animales_levante: Optional[int] = None
    animales_ceba: Optional[int] = None
    nacimientos_semanales: Optional[str] = None
    porcentaje_endogamia: Optional[str] = None
    animales_muertos_semanales: Optional[str] = None
    animales_vendidos_semanales: Optional[str] = None
    animales_comprados_semanales: Optional[str] = None
    registro_pesos_semanales: Optional[str] = None
    historial_perdida_terneros_anual: Optional[str] = None
    bovinos_descartes: Optional[str] = None
    historial_natalidad_paricion_real: Optional[str] = None
    periodo_iep_promedio: Optional[str] = None
    natalidad_paricion_real: Optional[str] = None
    tasa_supervivencia_actual: Optional[str] = None
    intervalo_entre_partos: Optional[str] = None
    porcentaje_ordeno: Optional[str] = None
    vacas_vacias: Optional[str] = None
    vacas_prenadas: Optional[str] = None
    porcentaje_prenadas: Optional[str] = None
    proximos_periodos_secado: Optional[str] = None
    planes_sanitarios_lotes_agendados: Optional[str] = None
    proyecciones_partos: Optional[str] = None
    animales_optimos_levante: Optional[str] = None
    animales_optimos_ceba: Optional[str] = None
    ventas_totales: Optional[int] = None
    total_compras: Optional[int] = None
    total_nomina: Optional[int] = None
    saldos_totales: Optional[int] = None
    saldos_promedios: Optional[int] = None
    facturacion_anual: Optional[str] = None
    usuario_id: Optional[str] = None
    perdida_de_terneros: Optional[float] = None
    machos: Optional[int] = None
    hembras: Optional[int] = None
    vacas_en_ordeno: Optional[int] = None
    vacas_no_ordeno: Optional[int] = None
    animales_rango_edades_0_9: Optional[int] = None
    animales_rango_edades_9_12: Optional[int] = None
    animales_rango_edades_12_24: Optional[int] = None
    animales_rango_edades_24_36: Optional[int] = None
    animales_rango_edades_mayor_36: Optional[int] = None
    vientres_aptos: Optional[int] = None
    relacion_toros_vientres_aptos: Optional[int] = None
    interpretacion_relacion_toros_vientres_aptos: Optional[str] = None
    total_unidades_animales: Optional[str] = None
    IEP_hato: Optional[float] = None

    class Config:
        orm_mode = True
        env_file = ".env"



class esquema_embriones_transferencias(BaseModel):
    id_embrion:Optional[int] = None
    codigo_nombre_embrion: Optional[str] = None
    inf_madre_biologica: Optional[str] = None
    inf_padre_biologico: Optional[str] = None
    estado: Optional[str] = None
    fecha_implante: Optional[date] = None
    id_receptora:Optional[int] = None
    nombre_receptora:Optional[str] = None
    resultado_trasnplante:Optional[str] = None
    fecha_parto: Optional[date] = None
    id_bovino_hijo:Optional[int] = None
    nombre_hijo: Optional[str] = None
    usuario_id: Optional[str] = None
    observaciones:Optional[str] = None
    raza:Optional[str] = None
    raza_madre_biologica: Optional[str] = None
    genetica_madre_biologica: Optional[str] = None
    edad_madre_biologica: Optional[str] = None
    historial_madre_biologica: Optional[str] = None
    tratamientos_hormonales_madre_biologica: Optional[str] = None
    raza_padre_biologico: Optional[str] = None
    genetica_padre_biologico: Optional[str] = None
    edad_padre_biologico: Optional[str] = None
    historial_reproductivo_padre_biologico: Optional[str] = None
    fecha_extracion: Optional[date] = None
    calidad_embrion: Optional[str] = None
    metodo_recoleccion: Optional[str] = None
    codigo_unico: Optional[str] = None
    lote_procedencia: Optional[str] = None
    caracteristicas_geneticas: Optional[str] = None
    tanque_nitrogeno: Optional[str] = None
    pajilla: Optional[str] = None
    numero_canister: Optional[str] = None
    historial_completo: Optional[str] = None
    programacion_transferencia: Optional[str] = None
    tecnica_utilizada: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_hembras_donantes(BaseModel):
    id_donante:Optional[int] = None
    id_bovino:Optional[int] = None
    nombre_bovino: Optional[str] = None
    raza: Optional[str] = None
    edad:Optional[int] = None
    edad_AA_MM_DD: Optional[str] = None
    embriones_producidos:Optional[int] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_extracciones_embriones(BaseModel):
    id_extraccion:Optional[int] = None
    id_bovino:Optional[int] = None
    nombre_bovino: Optional[str] = None
    fecha_extraccion: Optional[date]
    observaciones: Optional[str] = None
    total_embriones:Optional[int] = None
    embriones_viables:Optional[int] = None
    responsable: Optional[str] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_embriones(BaseModel):
    id_embrion:Optional[int] = None
    codigo_identificador:Optional[str] = None
    id_extraccion:Optional[int] = None
    extraccion:Optional[str] = None
    metodo:Optional[str] = None
    id_donante:Optional[int] = None
    nombre_donante:Optional[str] = None
    padre_o_pajilla:Optional[str] = None
    id_padre_pajilla:Optional[int] = None
    nombre_padre_o_pajilla:Optional[str] = None
    calidad_embrion:Optional[str] = None
    estado_embrion:Optional[str] = None
    productor:Optional[str] = None
    raza_madre:Optional[str] = None
    raza_padre:Optional[str] = None
    pedigree_madre:Optional[str] = None
    pedigree_padre:Optional[str] = None
    fecha_produccion_embrion:Optional[date]
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_transferencias_embriones(BaseModel):
    id_transferencia:Optional[int] = None
    id_embrion:Optional[int] = None
    embrion:Optional[str] = None
    id_receptora:Optional[int] = None
    nombre_receptora:Optional[str] = None
    fecha_transferencia:Optional[date]
    resultado:Optional[str] = None
    id_parto:Optional[int] = None
    id_cria:Optional[int] = None
    nombre_cria: Optional[str] = None
    observaciones: Optional[str] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"







class esquema_termocriogenico_embriones(BaseModel):
    id_termo:Optional[int] = None
    nombre_termo_identificador:Optional[str] = None
    cantidad_canastillas:Optional[int] = None
    ubicacion:Optional[str] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_canastillas_embriones(BaseModel):
    id_canastilla_embrion:Optional[int] = None
    id_termo:Optional[int] = None
    nombre_termo_identificador:Optional[str] = None
    nombre_codigo_canastilla:Optional[str] = None
    gondolas:Optional[int] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_gondolas_embriones(BaseModel):
    id_gondola:Optional[int] = None
    id_termo:Optional[int] = None
    nombre_termo_identificador:Optional[str] = None
    id_canastilla_embrion:Optional[int] = None
    nombre_codigo_canastilla:Optional[str] = None
    nombre_posicion_gondola:Optional[str] = None
    estado:Optional[str] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"



class esquema_banco_embriones(BaseModel):
    id_banco:Optional[int] = None
    id_embrion:Optional[int] = None
    nombre_codigo_embrion:Optional[str] = None
    fecha_ingreso:Optional[date]
    fecha_salida:Optional[date]
    id_termo:Optional[int] = None
    termo:Optional[str] = None
    id_gondola:Optional[int] = None
    gondola_posicion:Optional[str] = None
    observaciones:Optional[str] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_hembras_receptoras(BaseModel):
    id_receptora:Optional[int] = None
    id_bovino:Optional[int] = None
    nombre_bovino: Optional[str] = None
    raza: Optional[str] = None
    edad:Optional[int] = None
    edad_AA_MM_DD: Optional[str] = None
    transferencias_recibidas:Optional[int] = None
    transferencias_exitosas:Optional[int] = None
    transferecnias_fallidas:Optional[int] = None
    tasa_exito:Optional[float] = None
    usuario_id: Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"