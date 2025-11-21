from datetime import datetime
import uuid
from sqlalchemy import DateTime, ForeignKey, String, Text, Time, UniqueConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.db.mixins import TimestampMixin

class Turno(TimestampMixin, Base):
    __tablename__ = "turnos"

    id_turno: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    id_paciente: Mapped[uuid.UUID] = mapped_column(ForeignKey("pacientes.id_paciente"))
    id_medico: Mapped[uuid.UUID] = mapped_column(ForeignKey("medicos.id_medico"))
    id_consultorio: Mapped[uuid.UUID] = mapped_column(ForeignKey("consultorios.id_consultorio"))
    id_estado_turno: Mapped[uuid.UUID] = mapped_column(ForeignKey("estados_turnos.id_estado_turno"))
    
    fecha_hora_inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fecha_hora_fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    motivo_consulta: Mapped[str | None] = mapped_column(Text)

    paciente = relationship("Paciente", back_populates="turnos")
    medico = relationship("Medico", back_populates="turnos")
    consultorio = relationship("Consultorio", back_populates="turnos")

    historia_clinica = relationship("HistoriaClinica", back_populates="turno", uselist=False)
    estado_turno = relationship("EstadoTurno", back_populates="turnos")
    recetas = relationship("Receta", back_populates="turno")

    __table_args__ = (
        UniqueConstraint("id_medico", "fecha_hora_inicio"),
        UniqueConstraint("id_consultorio", "fecha_hora_inicio"),
        
    )
