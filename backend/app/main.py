from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import Base, engine
from app.models import models
from app.api import auth, admin, visitas, prerregistros, vecinos

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version="1.0.0", description="API para control de ingreso de garita tecnológica residencial")

origins = [x.strip() for x in settings.CORS_ORIGINS.split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins or ["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(visitas.router, prefix="/api")
app.include_router(prerregistros.router, prefix="/api")
app.include_router(vecinos.router, prefix="/api")

@app.get("/")
def root():
    return {"mensaje": "Sistema de Garita Tecnológica funcionando", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

from app.core.database import SessionLocal
from app.services.seed import seed_initial_data

@app.on_event("startup")
def startup_seed():
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()
