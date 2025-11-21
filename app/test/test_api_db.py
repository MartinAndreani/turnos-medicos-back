from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from app.db.database import Base, db_manager
from app.main import app

# Definimos el motor de prueba fuera de la función de prueba, pero NO lo inicializamos
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función de dependencia de prueba, igual que antes
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# ----------------------------------------------------------------------

# El TestClient y la ruta temporal DEBEN estar dentro de la función
def test_read_data_with_db_dependency():
    """
    Prueba que el Singleton de DB se puede sobrescribir y usar para obtener
    una sesión válida de una BD temporal (SQLite).
    """
    
    # 1. SETUP TEMPORAL: Sobrescribe la dependencia para el test.
    # Usamos un bloque try/finally para garantizar que la dependencia se restablezca.
    app.dependency_overrides[db_manager.get_session_dependency] = override_get_db
    
    # 2. CONFIGURACIÓN DEL CLIENTE Y RUTA DE PRUEBA
    # Crea las tablas de los modelos en la BD de prueba (SQLite)
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    router = APIRouter()
    
    # Endpoint de prueba que usa la dependencia Singleton
    @router.get("/health")
    def health_check(db: Session = Depends(db_manager.get_session_dependency)):
        try:
            # Prueba de fuego: ejecutar una consulta simple
            db.execute("SELECT 1")
            return {"status": "ok", "db_connected": True}
        except Exception as e:
            return {"status": "error", "db_connected": False, "detail": str(e)}

    # Añadimos la ruta temporal a la aplicación
    app.include_router(router)

    try:
        # 3. EJECUCIÓN DEL TEST
        response = client.get("/health")
        
        # 4. VERIFICACIÓN
        assert response.status_code == 200
        assert response.json()["db_connected"] == True
        
    finally:
        # 5. LIMPIEZA GARANTIZADA
        
        # Elimina la ruta temporal
        app.routes.pop()
        
        # Restaura la dependencia ORIGINAL del Singleton (CRUCIAL)
        app.dependency_overrides[db_manager.get_session_dependency] = db_manager.get_session_dependency

        # Opcional: Elimina las tablas de la BD de prueba
        Base.metadata.drop_all(bind=engine)