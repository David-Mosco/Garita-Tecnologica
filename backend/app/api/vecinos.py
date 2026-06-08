from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.models import Vecino
from app.models.enums import Rol
from app.schemas.schemas import VecinoOut

router = APIRouter(prefix="/vecinos", tags=["Vecinos"])

@router.get("/codigo/{codigo}", response_model=VecinoOut)
def buscar_por_codigo(codigo: str, db: Session = Depends(get_db), user=Depends(require_roles(Rol.agente, Rol.admin))):
    vecino = db.query(Vecino).filter(Vecino.codigo_unico == codigo, Vecino.activo == True).first()
    if not vecino:
        raise HTTPException(status_code=404, detail="Código no encontrado")
    return vecino

@router.get("/mi-info", response_model=VecinoOut)
def mi_info(db: Session = Depends(get_db), user=Depends(get_current_user)):
    vecino = db.query(Vecino).filter(Vecino.usuario_id == user.id).first()
    if not vecino:
        raise HTTPException(status_code=404, detail="No tiene vecino asociado")
    return vecino
