from pathlib import Path
import qrcode
from app.core.config import settings

QR_DIR = Path("static/qr")
QR_DIR.mkdir(parents=True, exist_ok=True)

def crear_qr(token: str) -> str:
    url_validacion = f"{settings.FRONTEND_URL}/qr.html?token={token}"
    img = qrcode.make(url_validacion)
    filename = f"qr_{token[:16]}.png"
    path = QR_DIR / filename
    img.save(path)
    return f"/static/qr/{filename}"
