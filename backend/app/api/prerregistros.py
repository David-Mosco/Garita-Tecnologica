from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.models import Prerregistro, Vecino
from app.models.enums import Rol
from app.schemas.schemas import PrerregistroCreate, PrerregistroOut
from app.services.code_service import generar_token_qr
from app.services.qr_service import crear_qr
from app.services.audit import log_audit

router = APIRouter(prefix="/prerregistros", tags=["Prerregistros QR"])

@router.post("", response_model=PrerregistroOut)
def crear_prerregistro(data: PrerregistroCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if data.valido_hasta <= data.valido_desde:
        raise HTTPException(status_code=400, detail="La fecha final debe ser mayor a la inicial")
    vecino_id = data.vecino_id
    if user.rol == Rol.vecino:
        vecino = db.query(Vecino).filter(Vecino.usuario_id == user.id, Vecino.activo == True).first()
        if not vecino:
            raise HTTPException(status_code=404, detail="El usuario vecino no tiene vecino asociado")
        vecino_id = vecino.id
    elif user.rol not in [Rol.admin, Rol.agente]:
        raise HTTPException(status_code=403, detail="No autorizado")
    if not vecino_id:
        raise HTTPException(status_code=400, detail="Debe indicar vecino_id")
    vecino = db.query(Vecino).filter(Vecino.id == vecino_id, Vecino.activo == True).first()
    if not vecino:
        raise HTTPException(status_code=404, detail="Vecino no encontrado")
    token = generar_token_qr()
    qr_url = crear_qr(token)
    pre = Prerregistro(**data.model_dump(exclude={"vecino_id"}), vecino_id=vecino_id, token_qr=token, qr_url=qr_url)
    db.add(pre); db.commit(); db.refresh(pre)
    log_audit(db, user, "CREAR", "prerregistros", pre.id, "QR generado")
    return pre

@router.get("", response_model=list[PrerregistroOut])
def listar_prerregistros(db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(Prerregistro).order_by(Prerregistro.creado_en.desc())
    if user.rol == Rol.vecino:
        vecino = db.query(Vecino).filter(Vecino.usuario_id == user.id).first()
        if not vecino: return []
        query = query.filter(Prerregistro.vecino_id == vecino.id)
    return query.limit(100).all()

@router.get("/validar/{token}")
def validar_qr(token: str, db: Session = Depends(get_db), user=Depends(require_roles(Rol.agente, Rol.admin))):
    pre = db.query(Prerregistro).filter(Prerregistro.token_qr == token).first()
    if not pre:
        raise HTTPException(status_code=404, detail="QR no encontrado")
    now = datetime.now(timezone.utc)
    vigente = pre.activo and not pre.usado and pre.valido_desde <= now <= pre.valido_hasta
    return {"vigente": vigente, "prerregistro": pre}
