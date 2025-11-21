from datetime import datetime
import uuid
from sqlalchemy import ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.db.mixins import TimestampMixin

class HistoriaClinica(TimestampMixin, Base):
    __tablename__ = "historias_clinicas"

    id_historia_clinica: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_paciente: Mapped[uuid.UUID] = mapped_column(ForeignKey("pacientes.id_paciente"))
    id_medico: Mapped[uuid.UUID] = mapped_column(ForeignKey("medicos.id_medico"))
    id_turno: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("turnos.id_turno"))
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    diagnostico: Mapped[str | None] = mapped_column(Text)
    tratamiento: Mapped[str | None] = mapped_column(Text)
    observaciones: Mapped[str | None] = mapped_column(Text)

    paciente = relationship("Paciente", back_populates="historias_clinicas")
    medico = relationship("Medico", back_populates="historias_clinicas")
    turno = relationship("Turno", back_populates="historia_clinica")
