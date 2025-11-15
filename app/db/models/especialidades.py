import uuid
from sqlalchemy import String, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base

class Especialidad(Base):
    __tablename__ = "especialidades"

    id_especialidad: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text)

    medicos = relationship("MedicoEspecialidad", back_populates="especialidad")
    consultorios = relationship("Consultorio", back_populates="especialidad")
