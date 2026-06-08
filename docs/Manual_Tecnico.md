# Manual Técnico

## Arquitectura
El proyecto usa arquitectura cliente-servidor:

- Frontend: HTML, CSS y JavaScript.
- Backend: FastAPI.
- Base de datos: PostgreSQL.
- ORM: SQLAlchemy.
- Seguridad: JWT y bcrypt.
- QR: librería qrcode.
- Correo: SMTP o modo consola.

## Rutas principales

- `POST /api/auth/login`: autenticación.
- `GET /api/auth/me`: usuario actual.
- `POST /api/admin/usuarios`: crear usuario.
- `POST /api/admin/viviendas`: crear vivienda.
- `POST /api/admin/vecinos`: crear vecino y código único.
- `POST /api/visitas/normal`: registrar ingreso normal.
- `POST /api/visitas/qr/{token}`: registrar ingreso con QR.
- `PATCH /api/visitas/{id}/salida`: registrar salida.
- `GET /api/visitas/historial`: historial.
- `GET /api/visitas/placas/{placa}`: consulta de placa.
- `POST /api/prerregistros`: crear prerregistro QR.

## Seguridad
El usuario inicia sesión con correo y contraseña. El backend devuelve un token JWT. Cada ruta protegida valida el token y el rol correspondiente.

## Correo
Por defecto el proyecto utiliza `EMAIL_MODE=console`, por lo que el correo se imprime en consola. Para envío real se debe configurar SMTP en `.env`.

## Base de datos
Ejecutar `database/01_schema.sql` y `database/02_seed.sql` en PostgreSQL o levantar el proyecto con Docker Compose.
