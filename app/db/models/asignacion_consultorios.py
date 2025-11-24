import uuid
from typing import List
from datetime import time
from sqlalchemy import Boolean, Date, ForeignKey, String, UniqueConstraint, text, Integer, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY # <--- NECESARIO
from app.db.database import Base
from app.db.mixins import TimestampMixin

class AsignacionConsultorioModel(TimestampMixin, Base):
    __tablename__ = "asignacion_consultorios"

    id_asignacion: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    id_medico: Mapped[uuid.UUID] = mapped_column(ForeignKey("medicos.id_medico"))
    id_consultorio: Mapped[uuid.UUID] = mapped_column(ForeignKey("consultorios.id_consultorio"))
    
    fecha_inicio: Mapped[Date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[Date] = mapped_column(Date, nullable=False)
    
    # --- AHORA ES UNA LISTA ---
    dias_semana: Mapped[List[int]] = mapped_column(ARRAY(Integer), nullable=False)
    # --------------------------
    
    hora_inicio: Mapped[Time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[Time] = mapped_column(Time, nullable=False)
    
    jornada: Mapped[str] = mapped_column(String, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    medico = relationship("MedicoModel", back_populates="asignaciones")
    consultorio = relationship("ConsultorioModel", back_populates="asignaciones")