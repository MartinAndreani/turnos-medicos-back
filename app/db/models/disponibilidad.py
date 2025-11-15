from datetime import time
import uuid
from sqlalchemy import ForeignKey, Integer, Time, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base

class DisponibilidadConsultorio(Base):
    __tablename__ = "disponibilidad_consultorios"

    id_disponibilidad: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_medico: Mapped[uuid.UUID] = mapped_column(ForeignKey("medicos.id_medico"), nullable=False)
    id_consultorio: Mapped[uuid.UUID] = mapped_column(ForeignKey("consultorios.id_consultorio"), nullable=False)
    dia_semana: Mapped[int] = mapped_column(Integer, nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)

    __table_args__ = (
        UniqueConstraint("id_consultorio", "dia_semana", "hora_inicio"),
    )

    medico = relationship("Medico", back_populates="disponibilidades")
    consultorio = relationship("Consultorio", back_populates="disponibilidades")
