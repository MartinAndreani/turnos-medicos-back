


import uuid
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class RolXUsuario(Base):
    __tablename__ = "roles_x_usuarios"
    
    id_roles_x_usuario: Mapped[uuid.UUID] = mapped_column(primary_key = True, default=uuid.uuid4, nullable=False)
    id_usuario: Mapped[uuid.UUID] = mapped_column(nullable=False)
    id_rol: Mapped[uuid.UUID] = mapped_column(nullable=False)
    
    