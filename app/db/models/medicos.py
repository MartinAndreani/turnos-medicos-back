import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base

class Medico(Base):
    __tablename__ = "medicos"

    id_medico: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    matricula: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    dni: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    apellido: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str | None] = mapped_column(String, unique=True)
    telefono: Mapped[str | None]
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    especialidades = relationship("MedicoEspecialidad", back_populates="medico")
    disponibilidades = relationship("DisponibilidadConsultorio", back_populates="medico")
    turnos = relationship("Turno", back_populates="medico")
    historias = relationship("HistoriaClinica", back_populates="medico")
