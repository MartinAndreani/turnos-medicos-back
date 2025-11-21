



import uuid
from app.db.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class Rol(Base):
    __tablename__ = "roles"
    
    id_rol: Mapped[uuid.UUID] = mapped_column(primary_key = True, default=uuid.uuid4, nullable=False)
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String, nullable=True)
    activo: Mapped[bool] = mapped_column(default=True)
    
