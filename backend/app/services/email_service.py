import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

def enviar_correo(destinatario: str, asunto: str, mensaje: str) -> tuple[str, str]:
    if settings.EMAIL_MODE.lower() == "console":
        print("==== CORREO SIMULADO ====")
        print("Para:", destinatario)
        print("Asunto:", asunto)
        print(mensaje)
        print("=========================")
        return "SIMULADO", "Correo simulado correctamente en consola del backend."
    try:
        msg = MIMEText(mensaje, "plain", "utf-8")
        msg["Subject"] = asunto
        msg["From"] = settings.SMTP_FROM
        msg["To"] = destinatario
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM, [destinatario], msg.as_string())
        return "ENVIADO", "Correo enviado correctamente por SMTP."
    except Exception as exc:
        return "ERROR", str(exc)
