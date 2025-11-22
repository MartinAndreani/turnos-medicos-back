


from sqlalchemy import Boolean, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
import uuid

from app.db.mixins import TimestampMixin


class UsuarioModel(TimestampMixin, Base):
    __tablename__ = "usuarios"
    
    
    id_usuario: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    roles_x_usuarios = relationship("RolXUsuarioModel", back_populates="usuario")
    
    
    