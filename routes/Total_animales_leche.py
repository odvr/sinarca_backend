
from config.db import  get_session
from sqlalchemy.orm import Session
from fastapi import  Depends
import crud
from fastapi import    APIRouter

from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario

Pruebas_Leche = APIRouter()


def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

@Pruebas_Leche.get("/Animales_leche",tags=["dashboard"])
async def animales_leche(
        db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)
                  ):
    # consulta de total de animales vivos con propósito de leche

    prop_leche = crud.bovinos_inventario.count_animals(db=db, current_user=current_user)
    # actualización de campos
    crud.indicadores.set_prop_milk(db=db,milk_count=prop_leche,current_user=current_user)

    return  prop_leche