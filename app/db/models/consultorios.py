import uuid
from sqlalchemy import String, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.db.mixins import TimestampMixin

class ConsultorioModel(TimestampMixin, Base):
    __tablename__ = "consultorios"

    id_consultorio: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4,server_default=text("gen_random_uuid()"))
    numero_consultorio: Mapped[str] = mapped_column(String, nullable=False)
    piso: Mapped[str | None] = mapped_column(String)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    asignaciones = relationship("AsignacionConsultorioModel", back_populates="consultorio")
    turnos = relationship("TurnoModel", back_populates="consultorio")
