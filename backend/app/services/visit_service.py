from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import Visitante, Vehiculo, Vecino, Visita, Prerregistro
from app.models.enums import TipoIngreso, EstadoVisita, EstadoCorreo
from app.services.email_service import enviar_correo


def limpiar_texto(valor: str | None) -> str | None:
    if valor is None:
        return None
    return valor.strip()


def normalizar_token(token: str) -> str:
    return token.strip().replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")


def fecha_sin_zona(fecha):
    if fecha is None:
        return None

    if fecha.tzinfo is not None:
        return fecha.astimezone(timezone.utc).replace(tzinfo=None)

    return fecha


def ahora_sin_zona():
    return datetime.now()


def get_or_create_visitante(
    db: Session,
    nombre: str,
    dpi_licencia: str,
    telefono: str | None = None
) -> Visitante:
    dpi_licencia = limpiar_texto(dpi_licencia)
    nombre = limpiar_texto(nombre)
    telefono = limpiar_texto(telefono)

    visitante = db.query(Visitante).filter(
        Visitante.dpi_licencia == dpi_licencia
    ).first()

    if visitante:
        visitante.nombre = nombre
        visitante.telefono = telefono
        return visitante

    visitante = Visitante(
        nombre=nombre,
        dpi_licencia=dpi_licencia,
        telefono=telefono
    )

    db.add(visitante)
    db.flush()

    return visitante


def get_or_create_vehiculo(
    db: Session,
    placa: str | None,
    marca: str | None = None,
    color: str | None = None
) -> Vehiculo | None:
    placa = limpiar_texto(placa)
    marca = limpiar_texto(marca)
    color = limpiar_texto(color)

    if not placa:
        return None

    placa = placa.upper().replace(" ", "")

    vehiculo = db.query(Vehiculo).filter(
        Vehiculo.placa == placa
    ).first()

    if vehiculo:
        if marca:
            vehiculo.marca = marca
        if color:
            vehiculo.color = color
        return vehiculo

    vehiculo = Vehiculo(
        placa=placa,
        marca=marca,
        color=color
    )

    db.add(vehiculo)
    db.flush()

    return vehiculo


def notificar_visita(visita: Visita, db: Session):
    mensaje = f"""Se ha registrado la llegada de un visitante para su residencia.

Nombre: {visita.visitante.nombre}
DPI/Licencia: {visita.visitante.dpi_licencia}
Placa: {visita.vehiculo.placa if visita.vehiculo else 'Sin vehículo'}
Hora de ingreso: {visita.entrada_en}
Tipo de ingreso: {visita.tipo_ingreso.value}
Dirección: {visita.vivienda.direccion}
Agente: {visita.agente.nombre}
"""

    estado, detalle = enviar_correo(
        visita.vecino.email,
        "Nueva visita registrada en garita",
        mensaje
    )

    visita.correo_estado = EstadoCorreo(estado)
    visita.correo_detalle = detalle

    db.commit()


def registrar_visita_normal(db: Session, data, agente):
    codigo = limpiar_texto(data.codigo_vecino)

    vecino = db.query(Vecino).filter(
        Vecino.codigo_unico == codigo,
        Vecino.activo == True
    ).first()

    if not vecino:
        raise HTTPException(
            status_code=404,
            detail="Código único del vecino inválido o inactivo"
        )

    visitante = get_or_create_visitante(
        db,
        data.visitante.nombre,
        data.visitante.dpi_licencia,
        data.visitante.telefono
    )

    vehiculo = get_or_create_vehiculo(
        db,
        data.vehiculo.placa if data.vehiculo else None,
        data.vehiculo.marca if data.vehiculo else None,
        data.vehiculo.color if data.vehiculo else None
    )

    visita = Visita(
        visitante_id=visitante.id,
        vehiculo_id=vehiculo.id if vehiculo else None,
        vivienda_id=vecino.vivienda_id,
        vecino_id=vecino.id,
        agente_id=agente.id,
        tipo_ingreso=TipoIngreso.normal,
        estado=EstadoVisita.dentro,
        motivo=limpiar_texto(data.motivo)
    )

    db.add(visita)
    db.commit()
    db.refresh(visita)

    notificar_visita(visita, db)

    db.refresh(visita)

    return visita


def registrar_visita_qr(db: Session, token: str, agente):
    token_limpio = normalizar_token(token)

    pre = db.query(Prerregistro).filter(
        Prerregistro.token_qr == token_limpio
    ).first()

    if not pre:
        raise HTTPException(
            status_code=404,
            detail="QR no encontrado. Verifica que el token esté completo y sin espacios."
        )

    if not pre.activo:
        raise HTTPException(
            status_code=400,
            detail="Este QR está inactivo"
        )

    if pre.usado:
        raise HTTPException(
            status_code=400,
            detail="Este QR ya fue utilizado"
        )

    ahora = ahora_sin_zona()
    valido_desde = fecha_sin_zona(pre.valido_desde)
    valido_hasta = fecha_sin_zona(pre.valido_hasta)

    if ahora < valido_desde:
        raise HTTPException(
            status_code=400,
            detail=f"El QR todavía no está vigente. Vigente desde: {valido_desde}"
        )

    if ahora > valido_hasta:
        raise HTTPException(
            status_code=400,
            detail=f"El QR ya venció. Vigente hasta: {valido_hasta}"
        )

    if not pre.vecino or not pre.vecino.activo:
        raise HTTPException(
            status_code=400,
            detail="El vecino asociado al QR está inactivo o no existe"
        )

    visitante = get_or_create_visitante(
        db,
        pre.visitante_nombre,
        pre.dpi_licencia
    )

    vehiculo = get_or_create_vehiculo(
        db,
        pre.placa
    )

    visita = Visita(
        visitante_id=visitante.id,
        vehiculo_id=vehiculo.id if vehiculo else None,
        vivienda_id=pre.vecino.vivienda_id,
        vecino_id=pre.vecino_id,
        agente_id=agente.id,
        prerregistro_id=pre.id,
        tipo_ingreso=TipoIngreso.qr,
        estado=EstadoVisita.dentro,
        motivo=pre.motivo
    )

    pre.usado = True

    db.add(visita)
    db.commit()
    db.refresh(visita)

    notificar_visita(visita, db)

    db.refresh(visita)

    return visita