from datetime import time
import uuid
from sqlalchemy import Boolean, Date, ForeignKey, String, UniqueConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.db.mixins import TimestampMixin

class AsignacionConsultorioModel(TimestampMixin, Base):
    __tablename__ = "asignacion_consultorios"

    id_asignacion: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    id_medico: Mapped[uuid.UUID] = mapped_column(ForeignKey("medicos.id_medico"))
    id_consultorio: Mapped[uuid.UUID] = mapped_column(ForeignKey("consultorios.id_consultorio"))
    fecha_inicio: Mapped[Date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[Date] = mapped_column(Date, nullable=False)
    jornada: Mapped[str] = mapped_column(String, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("id_consultorio", "jornada", "fecha_inicio", "fecha_fin"),
    )

    medico = relationship("MedicoModel", back_populates="asignaciones")
    consultorio = relationship("ConsultorioModel", back_populates="asignaciones")
