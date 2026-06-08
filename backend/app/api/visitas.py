from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from datetime import datetime, timezone, date
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import require_roles, get_current_user
from app.models.models import Visita, Vehiculo, Prerregistro, Vecino, Visitante
from app.models.enums import Rol, EstadoVisita, TipoIngreso
from app.schemas.schemas import VisitaNormalCreate, SalidaRequest, PlacaOut, DashboardOut
from app.services.visit_service import registrar_visita_normal, registrar_visita_qr
from app.services.audit import log_audit


router = APIRouter(prefix="/visitas", tags=["Visitas"])


class QRIngresoRequest(BaseModel):
    token_qr: str


def visita_to_out(v: Visita):
    return {
        "id": v.id,
        "tipo_ingreso": v.tipo_ingreso,
        "estado": v.estado,
        "motivo": v.motivo,
        "entrada_en": v.entrada_en,
        "salida_en": v.salida_en,
        "correo_estado": v.correo_estado,
        "visitante": {
            "id": v.visitante.id,
            "nombre": v.visitante.nombre,
            "dpi_licencia": v.visitante.dpi_licencia
        },
        "vivienda": {
            "id": v.vivienda.id,
            "direccion": v.vivienda.direccion
        },
        "vecino": {
            "id": v.vecino.id,
            "nombre": v.vecino.nombre,
            "email": v.vecino.email
        },
        "vehiculo": {
            "id": v.vehiculo.id,
            "placa": v.vehiculo.placa,
            "marca": v.vehiculo.marca,
            "color": v.vehiculo.color
        } if v.vehiculo else None,
    }


@router.post("/normal")
def crear_visita_normal(
    data: VisitaNormalCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.agente, Rol.admin))
):
    visita = registrar_visita_normal(db, data, user)
    log_audit(db, user, "CREAR", "visitas", visita.id, "Ingreso normal")
    return visita_to_out(visita)


@router.post("/qr")
def crear_visita_qr_body(
    data: QRIngresoRequest,
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.agente, Rol.admin))
):
    visita = registrar_visita_qr(db, data.token_qr, user)
    log_audit(db, user, "CREAR", "visitas", visita.id, "Ingreso QR")
    return visita_to_out(visita)


@router.post("/qr/{token}")
def crear_visita_qr_url(
    token: str,
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.agente, Rol.admin))
):
    visita = registrar_visita_qr(db, token, user)
    log_audit(db, user, "CREAR", "visitas", visita.id, "Ingreso QR")
    return visita_to_out(visita)


@router.patch("/{visita_id}/salida")
def registrar_salida(
    visita_id: int,
    data: SalidaRequest,
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.agente, Rol.admin))
):
    visita = db.query(Visita).filter(Visita.id == visita_id).first()

    if not visita:
        raise HTTPException(status_code=404, detail="Visita no encontrada")

    if visita.estado == EstadoVisita.finalizada:
        raise HTTPException(status_code=400, detail="La visita ya tiene salida registrada")

    visita.estado = EstadoVisita.finalizada
    visita.salida_en = datetime.now(timezone.utc)

    db.commit()
    db.refresh(visita)

    log_audit(
        db,
        user,
        "ACTUALIZAR",
        "visitas",
        visita.id,
        data.observacion or "Salida registrada"
    )

    return visita_to_out(visita)


@router.get("/historial")
def historial(
    q: str | None = None,
    estado: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(Visita).order_by(Visita.entrada_en.desc())

    if user.rol == Rol.vecino:
        vecino = db.query(Vecino).filter(Vecino.usuario_id == user.id).first()

        if vecino:
            query = query.filter(Visita.vecino_id == vecino.id)
        else:
            return []

    if estado:
        query = query.filter(Visita.estado == estado)

    if q:
        like = f"%{q}%"

        query = (
            query
            .join(Visitante, Visita.visitante_id == Visitante.id)
            .outerjoin(Vehiculo, Visita.vehiculo_id == Vehiculo.id)
            .filter(
                or_(
                    Visitante.nombre.ilike(like),
                    Vehiculo.placa.ilike(like)
                )
            )
        )

    return [visita_to_out(v) for v in query.limit(200).all()]


@router.get("/placas/{placa}", response_model=PlacaOut)
def consultar_placa(
    placa: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    placa_norm = placa.upper().replace(" ", "")

    visita = (
        db.query(Visita)
        .join(Vehiculo)
        .filter(Vehiculo.placa == placa_norm)
        .order_by(Visita.entrada_en.desc())
        .first()
    )

    if not visita:
        return PlacaOut(placa=placa_norm, encontrada=False)

    if user.rol == Rol.vecino:
        vecino = db.query(Vecino).filter(Vecino.usuario_id == user.id).first()

        if not vecino or visita.vecino_id != vecino.id:
            raise HTTPException(
                status_code=403,
                detail="La placa no está asociada a su vivienda"
            )

    return PlacaOut(
        placa=placa_norm,
        encontrada=True,
        vivienda=visita.vivienda.direccion,
        vecino=visita.vecino.nombre,
        ultima_entrada=visita.entrada_en,
        estado=visita.estado.value
    )


@router.get("/dashboard", response_model=DashboardOut)
def dashboard(
    db: Session = Depends(get_db),
    user=Depends(require_roles(Rol.admin, Rol.agente))
):
    today = date.today()

    visitas_hoy = db.query(Visita).filter(func.date(Visita.entrada_en) == today).count()
    visitas_dentro = db.query(Visita).filter(Visita.estado == EstadoVisita.dentro).count()
    visitas_finalizadas = db.query(Visita).filter(Visita.estado == EstadoVisita.finalizada).count()
    prerregistros_activos = db.query(Prerregistro).filter(
        Prerregistro.activo == True,
        Prerregistro.usado == False
    ).count()
    visitas_normales = db.query(Visita).filter(Visita.tipo_ingreso == TipoIngreso.normal).count()
    visitas_qr = db.query(Visita).filter(Visita.tipo_ingreso == TipoIngreso.qr).count()

    return DashboardOut(
        visitas_hoy=visitas_hoy,
        visitas_dentro=visitas_dentro,
        visitas_finalizadas=visitas_finalizadas,
        prerregistros_activos=prerregistros_activos,
        visitas_normales=visitas_normales,
        visitas_qr=visitas_qr
    )