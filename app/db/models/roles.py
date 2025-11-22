



import uuid
from app.db.database import Base
from sqlalchemy import String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.mixins import TimestampMixin

class RolModel(TimestampMixin, Base):
    __tablename__ = "roles"
    
    id_rol: Mapped[uuid.UUID] = mapped_column(primary_key = True, default=uuid.uuid4, nullable=False, server_default=text("gen_random_uuid()"))
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(default=True)
    

    roles_x_usuarios = relationship("RolXUsuarioModel", back_populates="rol")