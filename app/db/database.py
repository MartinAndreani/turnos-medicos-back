

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings
# ---- Clase Singleton para la base de datos ---- # 
class Database:
    _intance = None
    _initialized = False
    
    def __new__(cls, database_url: str):
        # Metodo de creacion de la clase, controla que solo haya una instancia
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            
        return cls._instance     

    def __init__(self,database_url: str):
        #Metodo de inicialización: Solo ejecuta la lógica del motor la primera vez
        if not self._initialized: 
            print("Inicializando el motodr de la base de datos (Ejecucion Unica)")
            
            self.engine = create_engine(database_url, pool_pre_ping=True)
            
            self.SessionLocal = sessionmaker(autocommit = False,  autoflush= False, bind = self.engine)
            self._initialized = True
            
            
    def get_session(self):
        
        db =self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


db_manager = Database(settings.DATABASE_URL)

Base = declarative_base()