from sqlalchemy.orm import Session
from app.models.models import Auditoria, Usuario

def log_audit(db: Session, usuario: Usuario | None, accion: str, entidad: str, entidad_id: int | None = None, detalle: str | None = None):
    item = Auditoria(usuario_id=usuario.id if usuario else None, accion=accion, entidad=entidad, entidad_id=entidad_id, detalle=detalle)
    db.add(item)
    db.commit()
