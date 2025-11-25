import uuid
from typing import List # Importar List
from sqlalchemy import ForeignKey, Integer, String, Time, Date, Boolean, UniqueConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY # <--- IMPORTANTE: Usar dialecto Postgres
from app.db.database import Base
from app.db.mixins import TimestampMixin

class AgendaMedicoModel(TimestampMixin, Base):
    __tablename__ = "agendas_medicos"

    id_agenda: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    id_medico: Mapped[uuid.UUID] = mapped_column(ForeignKey("medicos.id_medico"))
    
    fecha_inicio: Mapped[Date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[Date] = mapped_column(Date, nullable=False)

    # --- CAMBIO CRÍTICO: Ahora es una LISTA de enteros ---
    dias_semana: Mapped[List[int]] = mapped_column(ARRAY(Integer), nullable=False)
    # -----------------------------------------------------

    hora_inicio: Mapped[Time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[Time] = mapped_column(Time, nullable=False)
    duracion_turno: Mapped[int] = mapped_column(Integer, nullable=False)
    jornada: Mapped[str] = mapped_column(String, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    medico = relationship("MedicoModel", back_populates="agendas")

