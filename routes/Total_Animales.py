
from config.db import  get_session
from sqlalchemy.orm import Session
from fastapi import  Depends
import crud
from fastapi import    APIRouter

from models.modelo_bovinos import modelo_indicadores
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario

Pruebas_TotalAnimales = APIRouter()


def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

@Pruebas_TotalAnimales.get("/Calcular_animales_totales",tags=["dashboard"])
async def animales_totales(db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        # consulta de total de animales vivos .ContarAnimalesCrud(db=db)
        total_animales = crud.TotalBovinos.ContarAnimalesCrud(db=db,current_user=current_user)
        # actualización de campos
        crud.indicadores.set_Cantidad_Total_Animales(db=db, CantidadAnimalesActuales=total_animales)

    except Exception as e:
      raise
    return total_animales