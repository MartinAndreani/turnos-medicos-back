import uuid
from sqlalchemy import ForeignKey, String, Boolean, Date, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.database import Base
from app.db.mixins import TimestampMixin

class PacienteModel(TimestampMixin, Base):
    __tablename__ = "pacientes"

    
    id_paciente: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    id_usuario: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), unique=True
    )
    dni: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    apellido: Mapped[str] = mapped_column(String, nullable=False)
    fecha_nacimiento: Mapped[Date | None] = mapped_column(Date, nullable=False)
    direccion: Mapped[str | None] = mapped_column(String, nullable=False)
    telefono: Mapped[str | None] = mapped_column(String, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    usuario = relationship("UsuarioModel")
    turnos = relationship("TurnoModel", back_populates="paciente")
    historias_clinicas = relationship("HistoriaClinicaModel", back_populates="paciente")

