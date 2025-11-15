import uuid
from sqlalchemy import String, Boolean, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id_paciente: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    dni: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    apellido: Mapped[str] = mapped_column(String, nullable=False)
    fecha_nacimiento: Mapped[Date] = mapped_column(Date)

    direccion: Mapped[str | None]
    email: Mapped[str | None] = mapped_column(String, unique=True)
    telefono: Mapped[str | None]
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    turnos = relationship("Turno", back_populates="paciente")
    historias = relationship("HistoriaClinica", back_populates="paciente")
