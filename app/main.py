from fastapi import FastAPI

# 1. Importación para inicializar el Singleton
# Al importar 'db_manager', Python ejecuta todo el código de database.py,
# incluyendo la línea 'db_manager = Database(settings.database_url)', 
# creando el único motor de conexión a la BD.
from db.database import db_manager 

# 2. Importación de la Base (opcional pero recomendada)
# Esto garantiza que la Base de SQLAlchemy esté disponible si la necesitas.
from db.database import Base 

# 3. Importación de Modelos (CRUCIAL para SQLAlchemy)
# Si tienes tus modelos definidos en una carpeta 'db/models/', por ejemplo:
# import db.models.pacientes
# import db.models.medicos

app = FastAPI()

@app.get("/")
def root():
    """Ruta de salud básica de la API."""
    return {"msg": "API está operativa"}

# Ejemplo de ruta que usa la conexión Singleton
# Para probar, necesitarías importar una ruta de tu api/routes/

# from app.api.routes import pacientes_router # Asumiendo que tienes un router
# app.include_router(pacientes_router, prefix="/pacientes", tags=["Pacientes"])