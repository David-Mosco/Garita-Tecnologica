import secrets, string
from sqlalchemy.orm import Session
from app.models.models import Vecino

def generar_codigo_vecino(db: Session) -> str:
    alphabet = string.ascii_uppercase + string.digits
    while True:
        code = "VN-" + "".join(secrets.choice(alphabet) for _ in range(6))
        if not db.query(Vecino).filter(Vecino.codigo_unico == code).first():
            return code

def generar_token_qr() -> str:
    return secrets.token_urlsafe(32)
