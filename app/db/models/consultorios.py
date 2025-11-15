import uuid
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base

class Consultorio(Base):
    __tablename__ = "consultorios"

    id_consultorio: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    numero_consultorio: Mapped[str] = mapped_column(String, nullable=False)
    piso: Mapped[str | None]
    id_especialidad: Mapped[uuid.UUID] = mapped_column(ForeignKey("especialidades.id_especialidad"), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    especialidad = relationship("Especialidad", back_populates="consultorios")
    disponibilidades = relationship("DisponibilidadConsultorio", back_populates="consultorio")
    turnos = relationship("Turno", back_populates="consultorio")
