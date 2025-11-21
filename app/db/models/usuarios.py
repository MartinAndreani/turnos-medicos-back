


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base
import uuid


class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    activo: Mapped[bool] = mapped_column(default=True)
    
    