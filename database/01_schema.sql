CREATE TYPE rol AS ENUM ('ADMIN','AGENTE','VECINO');
CREATE TYPE estado_visita AS ENUM ('PRERREGISTRADA','DENTRO','FINALIZADA','CANCELADA');
CREATE TYPE tipo_ingreso AS ENUM ('NORMAL','QR');
CREATE TYPE estado_correo AS ENUM ('PENDIENTE','ENVIADO','SIMULADO','ERROR');

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol rol NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS viviendas (
    id SERIAL PRIMARY KEY,
    direccion VARCHAR(180) NOT NULL UNIQUE,
    sector VARCHAR(80),
    numero_casa VARCHAR(30),
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vecinos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    vivienda_id INTEGER NOT NULL REFERENCES viviendas(id),
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL,
    telefono VARCHAR(30),
    codigo_unico VARCHAR(30) NOT NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS visitantes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(140) NOT NULL,
    dpi_licencia VARCHAR(40) NOT NULL UNIQUE,
    telefono VARCHAR(30),
    foto_url VARCHAR(255),
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vehiculos (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(20) NOT NULL UNIQUE,
    marca VARCHAR(60),
    color VARCHAR(50),
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS prerregistros (
    id SERIAL PRIMARY KEY,
    vecino_id INTEGER NOT NULL REFERENCES vecinos(id),
    visitante_nombre VARCHAR(140) NOT NULL,
    dpi_licencia VARCHAR(40) NOT NULL,
    placa VARCHAR(20),
    motivo VARCHAR(200),
    valido_desde TIMESTAMPTZ NOT NULL,
    valido_hasta TIMESTAMPTZ NOT NULL,
    token_qr VARCHAR(100) NOT NULL UNIQUE,
    qr_url VARCHAR(255),
    usado BOOLEAN NOT NULL DEFAULT FALSE,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_prerregistro_fechas CHECK (valido_hasta > valido_desde)
);

CREATE TABLE IF NOT EXISTS visitas (
    id SERIAL PRIMARY KEY,
    visitante_id INTEGER NOT NULL REFERENCES visitantes(id),
    vehiculo_id INTEGER REFERENCES vehiculos(id),
    vivienda_id INTEGER NOT NULL REFERENCES viviendas(id),
    vecino_id INTEGER NOT NULL REFERENCES vecinos(id),
    agente_id INTEGER NOT NULL REFERENCES usuarios(id),
    prerregistro_id INTEGER REFERENCES prerregistros(id),
    tipo_ingreso tipo_ingreso NOT NULL,
    estado estado_visita NOT NULL DEFAULT 'DENTRO',
    motivo VARCHAR(200),
    entrada_en TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    salida_en TIMESTAMPTZ,
    correo_estado estado_correo NOT NULL DEFAULT 'PENDIENTE',
    correo_detalle TEXT,
    CONSTRAINT chk_salida_mayor_entrada CHECK (salida_en IS NULL OR salida_en >= entrada_en)
);

CREATE TABLE IF NOT EXISTS auditoria (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    accion VARCHAR(80) NOT NULL,
    entidad VARCHAR(80) NOT NULL,
    entidad_id INTEGER,
    detalle TEXT,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_vecinos_codigo ON vecinos(codigo_unico);
CREATE INDEX IF NOT EXISTS idx_vehiculos_placa ON vehiculos(placa);
CREATE INDEX IF NOT EXISTS idx_visitas_entrada ON visitas(entrada_en);
CREATE INDEX IF NOT EXISTS idx_prerregistros_token ON prerregistros(token_qr);
