# app/main.py

from fastapi import FastAPI

# Inicializa la DB (Singleton)
from app.db.database import db_manager, get_db, Base

# Importar modelos para que SQLAlchemy los registre
# (IMPORTANTE: cada archivo de modelo debe ser importado)
from app.db.models import pacientes as pacientes_model
from app.db.models import medicos as medicos_model
from app.db.models import turnos as turnos_model    
from app.db.models import recetas as recetas_model
from app.db.models import especialidades as especialidades_model
from app.db.models import medico_especialidad as medico_especialidad_model
from app.db.models import usuarios as usuarios_model
from app.db.models import roles as roles_model
from app.db.models import historias_clinicas as historias_clinicas_model    
# si tenés más modelos, agregalos igual:
# from app.db.models import usuarios, roles, medicos

# Importar routers
from app.api.routes.pacientes import router as pacientes_router
from app.api.routes.medicos import router as medicos_router
from app.api.routes.turnos import router as turnos_router
from app.api.routes.recetas import router as recetas_router
from app.api.routes.especialidades import router as especialidades_router
from app.api.routes.medico_especialidad import router as medico_especialidades_router
from app.api.routes.usuarios import router as usuarios_router
from app.api.routes.roles import router as roles_router
from app.api.routes.auth import router as auth_router
from app.api.routes.historias_clinicas import router as historias_clinicas_router


app = FastAPI(
    title="Turnos Médicos API",
    version="1.0.0"
)


# ---------------------------------------------------------
# EVENTO STARTUP (si querés logs o seeds futuros)
# ---------------------------------------------------------
@app.on_event("startup")
def startup_event():
    print("🔌 API inicializando...")
    engine = db_manager.engine
    print("✅ Conexión establecida")


# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "API funcionando 🚀"}


# ---------------------------------------------------------
# INCLUIR ROUTERS
# ---------------------------------------------------------
app.include_router(pacientes_router)
app.include_router(medicos_router)
app.include_router(turnos_router)
app.include_router(recetas_router)
app.include_router(especialidades_router)
app.include_router(medico_especialidades_router)
app.include_router(historias_clinicas_router)
app.include_router(usuarios_router)
app.include_router(roles_router)
app.include_router(auth_router)