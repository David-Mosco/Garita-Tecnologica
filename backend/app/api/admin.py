from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, require_roles
from app.models.models import Usuario, Vivienda, Vecino
from app.models.enums import Rol
from app.schemas.schemas import (
    UsuarioCreate,
    UsuarioOut,
    ViviendaCreate,
    ViviendaOut,
    VecinoCreate,
    VecinoOut,
)
from app.services.code_service import generar_codigo_vecino
from app.services.audit import log_audit


router = APIRouter(prefix="/admin", tags=["Administración"])


@router.post("/usuarios", response_model=UsuarioOut)
def crear_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.admin)),
):
    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(status_code=400, detail="El correo ya existe")

    item = Usuario(
        nombre=data.nombre,
        email=data.email,
        password_hash=hash_password(data.password),
        rol=data.rol,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    log_audit(db, user, "CREAR", "usuarios", item.id, f"Usuario {item.email}")

    return item


@router.get("/usuarios", response_model=list[UsuarioOut])
def listar_usuarios(
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.admin)),
):
    return db.query(Usuario).order_by(Usuario.id).all()


@router.post("/viviendas", response_model=ViviendaOut)
def crear_vivienda(
    data: ViviendaCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.admin)),
):
    if db.query(Vivienda).filter(Vivienda.direccion == data.direccion).first():
        raise HTTPException(status_code=400, detail="La vivienda ya existe")

    item = Vivienda(**data.model_dump())

    db.add(item)
    db.commit()
    db.refresh(item)

    log_audit(db, user, "CREAR", "viviendas", item.id, item.direccion)

    return item


@router.get("/viviendas", response_model=list[ViviendaOut])
def listar_viviendas(
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.admin, Rol.agente, Rol.vecino)),
):
    return (
        db.query(Vivienda)
        .order_by(Vivienda.sector, Vivienda.numero_casa, Vivienda.direccion)
        .all()
    )


@router.delete("/viviendas/{vivienda_id}")
def desactivar_vivienda(
    vivienda_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.admin)),
):
    vivienda = db.query(Vivienda).filter(Vivienda.id == vivienda_id).first()

    if not vivienda:
        raise HTTPException(status_code=404, detail="Vivienda no encontrada")

    vivienda.activa = False
    db.commit()

    log_audit(db, user, "DESACTIVAR", "viviendas", vivienda.id, vivienda.direccion)

    return {"mensaje": "Vivienda desactivada correctamente"}


@router.post("/vecinos", response_model=VecinoOut)
def crear_vecino(
    data: VecinoCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.admin)),
):
    vivienda = (
        db.query(Vivienda)
        .filter(Vivienda.id == data.vivienda_id, Vivienda.activa == True)
        .first()
    )

    if not vivienda:
        raise HTTPException(status_code=404, detail="Vivienda no encontrada")

    if db.query(Vecino).filter(Vecino.email == data.email, Vecino.activo == True).first():
        raise HTTPException(status_code=400, detail="El correo del vecino ya existe")

    codigo = generar_codigo_vecino(db)

    vecino = Vecino(**data.model_dump(), codigo_unico=codigo)

    db.add(vecino)
    db.commit()
    db.refresh(vecino)

    log_audit(db, user, "CREAR", "vecinos", vecino.id, f"Código {codigo}")

    return vecino


@router.get("/vecinos", response_model=list[VecinoOut])
def listar_vecinos(
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.admin, Rol.agente)),
):
    return db.query(Vecino).order_by(Vecino.nombre).all()


@router.delete("/vecinos/{vecino_id}")
def desactivar_vecino(
    vecino_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.admin)),
):
    vecino = db.query(Vecino).filter(Vecino.id == vecino_id).first()

    if not vecino:
        raise HTTPException(status_code=404, detail="Vecino no encontrado")

    vecino.activo = False
    db.commit()

    log_audit(db, user, "DESACTIVAR", "vecinos", vecino.id, vecino.codigo_unico)

    return {"mensaje": "Vecino desactivado correctamente"}