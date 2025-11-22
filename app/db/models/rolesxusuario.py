


import uuid

from sqlalchemy import ForeignKey, text
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.mixins import TimestampMixin

class RolXUsuarioModel(TimestampMixin, Base):
    __tablename__ = "roles_x_usuarios"
    
    id_roles_x_usuario: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    id_usuario: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuarios.id_usuario"))
    id_rol: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id_rol"))

    
    usuario = relationship("UsuarioModel", back_populates="roles_x_usuarios")
    rol = relationship("RolModel", back_populates="roles_x_usuarios")
    