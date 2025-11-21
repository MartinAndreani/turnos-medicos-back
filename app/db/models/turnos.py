from datetime import datetime
import uuid
from sqlalchemy import DateTime, ForeignKey, String, Text, Time, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.db.mixins import TimestampMixin

class Turno(TimestampMixin, Base):
    __tablename__ = "turnos"

    id_turno: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_paciente: Mapped[uuid.UUID] = mapped_column(ForeignKey("pacientes.id_paciente"))
    id_medico: Mapped[uuid.UUID] = mapped_column(ForeignKey("medicos.id_medico"))
    id_consultorio: Mapped[uuid.UUID] = mapped_column(ForeignKey("consultorios.id_consultorio"))
    fecha_hora_inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fecha_hora_fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    estado: Mapped[str] = mapped_column(String, nullable=False)
    motivo_consulta: Mapped[str | None] = mapped_column(Text)

    paciente = relationship("Paciente", back_populates="turnos")
    medico = relationship("Medico", back_populates="turnos")
    consultorio = relationship("Consultorio", back_populates="turnos")

    historia_clinica = relationship("HistoriaClinica", back_populates="turno", uselist=False)
    recetas = relationship("Receta", back_populates="turno")

    __table_args__ = (
        UniqueConstraint("id_medico", "fecha_hora_inicio"),
        UniqueConstraint("id_consultorio", "fecha_hora_inicio"),
    )
