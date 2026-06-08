# Sistema de Control de Ingreso para Garita Tecnológica Residencial

Proyecto completo desarrollado con **FastAPI + PostgreSQL + Frontend HTML/CSS/JavaScript**, listo para abrir en Visual Studio Code.

## Funcionalidades principales

- Login con JWT y manejo de roles: Administrador, Agente de Garita y Vecino.
- Registro de viviendas, vecinos, visitantes, vehículos y usuarios.
- Generación automática de código único por vecino.
- Registro de ingreso normal usando código único del vecino.
- Prerregistro de visitas con generación de código QR.
- Validación de QR vigente para registrar ingreso.
- Registro de hora de entrada y salida.
- Consulta de placas vehiculares y vivienda asociada.
- Historial completo con filtros.
- Dashboard estadístico.
- Bitácora de auditoría.
- Correo electrónico funcional mediante SMTP o simulado en consola.
- Documentación técnica, manual de usuario y script SQL.

## Credenciales iniciales

| Rol | Correo | Contraseña |
|---|---|---|
| Administrador | admin@garita.local | Admin123* |
| Agente | agente@garita.local | Agente123* |
| Vecino | vecino@garita.local | Vecino123* |

## Ejecución rápida con Docker

1. Abrir la carpeta en Visual Studio Code.
2. Crear el archivo `.env` copiando `.env.example`.
3. Ejecutar:

```bash
docker compose up --build
```

4. Abrir:

- Frontend: http://localhost:8080
- API: http://localhost:8000/docs
- pgAdmin: http://localhost:5050

Credenciales pgAdmin:

- Correo: admin@admin.com
- Contraseña: admin

## Ejecución manual sin Docker

1. Crear base de datos PostgreSQL llamada `garita_db`.
2. Ejecutar `database/01_schema.sql` y luego `database/02_seed.sql` desde pgAdmin 4.
3. Entrar a backend:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

4. Abrir `frontend/index.html` con Live Server o usar:

```bash
cd frontend
python -m http.server 8080
```

## Entregables incluidos

- `database/01_schema.sql`: estructura completa PostgreSQL.
- `database/02_seed.sql`: datos iniciales.
- `backend/`: API completa con FastAPI.
- `frontend/`: interfaz funcional conectada al backend.
- `docs/`: documento del proyecto, manual técnico, manual de usuario y diagrama.
- `postman/`: colección de pruebas.
- `evidencias/`: guía para capturas y video.
