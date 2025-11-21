



import uuid
from app.db.database import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.mixins import TimestampMixin

class Rol(TimestampMixin, Base):
    __tablename__ = "roles"
    
    id_rol: Mapped[uuid.UUID] = mapped_column(primary_key = True, default=uuid.uuid4, nullable=False)
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(default=True)
    

    roles_x_usuarios = relationship("RolXUsuario", back_populates="rol")