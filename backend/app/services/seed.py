from sqlalchemy.orm import Session
from app.models.models import Usuario, Vivienda, Vecino
from app.models.enums import Rol
from app.core.security import hash_password

DEFAULTS = [
    ("Administrador", "admin@garita.com", "Admin123*", Rol.admin),
    ("Agente Principal", "agente@garita.com", "Agente123*", Rol.agente),
    ("Vecino Demo", "vecino@garita.com", "Vecino123*", Rol.vecino),
]

def seed_initial_data(db: Session):
    for nombre, email, password, rol in DEFAULTS:
        if not db.query(Usuario).filter(Usuario.email == email).first():
            db.add(Usuario(nombre=nombre, email=email, password_hash=hash_password(password), rol=rol))
    if not db.query(Vivienda).filter(Vivienda.direccion == "Casa 14, Sector B").first():
        db.add(Vivienda(direccion="Casa 14, Sector B", sector="Sector B", numero_casa="14"))
    if not db.query(Vivienda).filter(Vivienda.direccion == "Casa 25, Sector A").first():
        db.add(Vivienda(direccion="Casa 25, Sector A", sector="Sector A", numero_casa="25"))
    db.commit()
    vecino_user = db.query(Usuario).filter(Usuario.email == "vecino@garita.com").first()
    vivienda = db.query(Vivienda).filter(Vivienda.direccion == "Casa 14, Sector B").first()
    if vecino_user and vivienda and not db.query(Vecino).filter(Vecino.usuario_id == vecino_user.id).first():
        db.add(Vecino(usuario_id=vecino_user.id, vivienda_id=vivienda.id, nombre="Vecino Demo", email="vecino@garita.com", telefono="5555-0000", codigo_unico="VN-DEMO01"))
        db.commit()
