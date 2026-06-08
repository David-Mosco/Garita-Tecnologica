from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.enums import Rol, TipoIngreso, EstadoVisita, EstadoCorreo

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: Rol
    nombre: str
    email: EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6)
    rol: Rol

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: Rol
    activo: bool
    class Config: from_attributes = True

class ViviendaCreate(BaseModel):
    direccion: str
    sector: Optional[str] = None
    numero_casa: Optional[str] = None

class ViviendaOut(ViviendaCreate):
    id: int
    activa: bool
    class Config: from_attributes = True

class VecinoCreate(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    vivienda_id: int
    usuario_id: Optional[int] = None

class VecinoOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    telefono: Optional[str]
    codigo_unico: str
    activo: bool
    vivienda: ViviendaOut
    class Config: from_attributes = True

class VisitanteIn(BaseModel):
    nombre: str
    dpi_licencia: str
    telefono: Optional[str] = None

class VehiculoIn(BaseModel):
    placa: Optional[str] = None
    marca: Optional[str] = None
    color: Optional[str] = None

class VisitaNormalCreate(BaseModel):
    visitante: VisitanteIn
    vehiculo: Optional[VehiculoIn] = None
    codigo_vecino: str
    motivo: Optional[str] = None

class PrerregistroCreate(BaseModel):
    vecino_id: Optional[int] = None
    visitante_nombre: str
    dpi_licencia: str
    placa: Optional[str] = None
    motivo: Optional[str] = None
    valido_desde: datetime
    valido_hasta: datetime

class PrerregistroOut(BaseModel):
    id: int
    vecino_id: int
    visitante_nombre: str
    dpi_licencia: str
    placa: Optional[str]
    motivo: Optional[str]
    valido_desde: datetime
    valido_hasta: datetime
    token_qr: str
    qr_url: Optional[str]
    usado: bool
    activo: bool
    class Config: from_attributes = True

class VisitaOut(BaseModel):
    id: int
    tipo_ingreso: TipoIngreso
    estado: EstadoVisita
    motivo: Optional[str]
    entrada_en: datetime
    salida_en: Optional[datetime]
    correo_estado: EstadoCorreo
    visitante: dict
    vivienda: dict
    vecino: dict
    vehiculo: Optional[dict]
    class Config: from_attributes = True

class SalidaRequest(BaseModel):
    observacion: Optional[str] = None

class PlacaOut(BaseModel):
    placa: str
    encontrada: bool
    vivienda: Optional[str] = None
    vecino: Optional[str] = None
    ultima_entrada: Optional[datetime] = None
    estado: Optional[str] = None

class DashboardOut(BaseModel):
    visitas_hoy: int
    visitas_dentro: int
    visitas_finalizadas: int
    prerregistros_activos: int
    visitas_normales: int
    visitas_qr: int
