



import uuid
from app.db.database import Base
from app.db.mixins import TimestampMixin
from sqlalchemy import ForeignKey, Integer, String, Time, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

class AgendaMedico(TimestampMixin, Base):
    __tablename__ = "agendas_medicos"

    id_agenda: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_medico: Mapped[uuid.UUID] = mapped_column(ForeignKey("medicos.id_medico"))
    dia_semana: Mapped[int] = mapped_column(Integer, nullable=False)
    hora_inicio: Mapped[Time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[Time] = mapped_column(Time, nullable=False)
    duracion_turno: Mapped[int] = mapped_column(Integer, nullable=False)
    jornada: Mapped[str] = mapped_column(String, nullable=False)

    medico = relationship("Medico", back_populates="agendas")

    __table_args__ = (
        UniqueConstraint("id_medico", "dia_semana", "hora_inicio"),
    )