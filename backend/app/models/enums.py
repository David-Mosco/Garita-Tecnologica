import enum

class Rol(str, enum.Enum):
    admin = "ADMIN"
    agente = "AGENTE"
    vecino = "VECINO"

class EstadoVisita(str, enum.Enum):
    prerregistrada = "PRERREGISTRADA"
    dentro = "DENTRO"
    finalizada = "FINALIZADA"
    cancelada = "CANCELADA"

class TipoIngreso(str, enum.Enum):
    normal = "NORMAL"
    qr = "QR"

class EstadoCorreo(str, enum.Enum):
    pendiente = "PENDIENTE"
    enviado = "ENVIADO"
    simulado = "SIMULADO"
    error = "ERROR"
