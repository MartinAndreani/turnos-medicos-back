import uuid
from sqlalchemy import ForeignKey, String, Boolean, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.db.mixins import TimestampMixin

class MedicoModel(TimestampMixin, Base):
    __tablename__ = "medicos"

    id_medico: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    id_usuario: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), unique=True
    )
    matricula: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    dni: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    apellido: Mapped[str] = mapped_column(String, nullable=False)
    telefono: Mapped[str | None] = mapped_column(String)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    usuario = relationship("UsuarioModel")

    especialidades = relationship(
    "EspecialidadModel",
    secondary="medico_especialidad",
    back_populates="medicos"
    )   

    agendas = relationship("AgendaMedicoModel", back_populates="medico")
    turnos = relationship("TurnoModel", back_populates="medico")
    historias_clinicas = relationship("HistoriaClinicaModel", back_populates="medico")
    asignaciones = relationship("AsignacionConsultorioModel", back_populates="medico")
