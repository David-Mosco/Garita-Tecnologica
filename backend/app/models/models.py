from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.enums import Rol, EstadoVisita, TipoIngreso, EstadoCorreo

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    email = Column(String(160), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum(Rol, values_callable=lambda x: [e.value for e in x]), nullable=False)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    vecino = relationship("Vecino", back_populates="usuario", uselist=False)

class Vivienda(Base):
    __tablename__ = "viviendas"
    id = Column(Integer, primary_key=True, index=True)
    direccion = Column(String(180), nullable=False, unique=True)
    sector = Column(String(80), nullable=True)
    numero_casa = Column(String(30), nullable=True)
    activa = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    vecinos = relationship("Vecino", back_populates="vivienda")
    visitas = relationship("Visita", back_populates="vivienda")

class Vecino(Base):
    __tablename__ = "vecinos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    vivienda_id = Column(Integer, ForeignKey("viviendas.id"), nullable=False)
    nombre = Column(String(120), nullable=False)
    email = Column(String(160), nullable=False)
    telefono = Column(String(30), nullable=True)
    codigo_unico = Column(String(30), unique=True, nullable=False, index=True)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    usuario = relationship("Usuario", back_populates="vecino")
    vivienda = relationship("Vivienda", back_populates="vecinos")
    prerregistros = relationship("Prerregistro", back_populates="vecino")

class Visitante(Base):
    __tablename__ = "visitantes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(140), nullable=False)
    dpi_licencia = Column(String(40), nullable=False, index=True)
    telefono = Column(String(30), nullable=True)
    foto_url = Column(String(255), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("dpi_licencia", name="uq_visitante_documento"),)

class Vehiculo(Base):
    __tablename__ = "vehiculos"
    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(20), nullable=False, unique=True, index=True)
    marca = Column(String(60), nullable=True)
    color = Column(String(50), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    visitas = relationship("Visita", back_populates="vehiculo")

class Prerregistro(Base):
    __tablename__ = "prerregistros"
    id = Column(Integer, primary_key=True, index=True)
    vecino_id = Column(Integer, ForeignKey("vecinos.id"), nullable=False)
    visitante_nombre = Column(String(140), nullable=False)
    dpi_licencia = Column(String(40), nullable=False)
    placa = Column(String(20), nullable=True)
    motivo = Column(String(200), nullable=True)
    valido_desde = Column(DateTime(timezone=True), nullable=False)
    valido_hasta = Column(DateTime(timezone=True), nullable=False)
    token_qr = Column(String(100), unique=True, nullable=False, index=True)
    qr_url = Column(String(255), nullable=True)
    usado = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    vecino = relationship("Vecino", back_populates="prerregistros")
    visitas = relationship("Visita", back_populates="prerregistro")

class Visita(Base):
    __tablename__ = "visitas"
    id = Column(Integer, primary_key=True, index=True)
    visitante_id = Column(Integer, ForeignKey("visitantes.id"), nullable=False)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=True)
    vivienda_id = Column(Integer, ForeignKey("viviendas.id"), nullable=False)
    vecino_id = Column(Integer, ForeignKey("vecinos.id"), nullable=False)
    agente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    prerregistro_id = Column(Integer, ForeignKey("prerregistros.id"), nullable=True)
    tipo_ingreso = Column(Enum(TipoIngreso, values_callable=lambda x: [e.value for e in x]), nullable=False)
    estado = Column(Enum(EstadoVisita, values_callable=lambda x: [e.value for e in x]), default=EstadoVisita.dentro, nullable=False)
    motivo = Column(String(200), nullable=True)
    entrada_en = Column(DateTime(timezone=True), server_default=func.now())
    salida_en = Column(DateTime(timezone=True), nullable=True)
    correo_estado = Column(Enum(EstadoCorreo, values_callable=lambda x: [e.value for e in x]), default=EstadoCorreo.pendiente, nullable=False)
    correo_detalle = Column(Text, nullable=True)
    visitante = relationship("Visitante")
    vehiculo = relationship("Vehiculo", back_populates="visitas")
    vivienda = relationship("Vivienda", back_populates="visitas")
    vecino = relationship("Vecino")
    agente = relationship("Usuario")
    prerregistro = relationship("Prerregistro", back_populates="visitas")

class Auditoria(Base):
    __tablename__ = "auditoria"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    accion = Column(String(80), nullable=False)
    entidad = Column(String(80), nullable=False)
    entidad_id = Column(Integer, nullable=True)
    detalle = Column(Text, nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    usuario = relationship("Usuario")
