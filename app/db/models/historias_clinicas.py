from datetime import datetime
import uuid
from sqlalchemy import ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base

class HistoriaClinica(Base):
    __tablename__ = "historias_clinicas"

    id_entrada_historia: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_paciente: Mapped[uuid.UUID] = mapped_column(ForeignKey("pacientes.id_paciente"), nullable=False)
    id_medico: Mapped[uuid.UUID] = mapped_column(ForeignKey("medicos.id_medico"), nullable=False)
    id_turno: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("turnos.id_turno"))

    fecha_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    diagnostico: Mapped[str | None] = mapped_column(Text)
    tratamiento: Mapped[str | None] = mapped_column(Text)
    observaciones: Mapped[str | None] = mapped_column(Text)

    paciente = relationship("Paciente", back_populates="historias")
    medico = relationship("Medico", back_populates="historial")
    turno = relationship("Turno", back_populates="historias")
