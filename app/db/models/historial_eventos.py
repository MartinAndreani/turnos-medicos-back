


from datetime import datetime
import uuid
from sqlalchemy import DateTime, ForeignKey, String, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.db.mixins import TimestampMixin


class HistorialEvento(TimestampMixin, Base):
    
    __tablename__ = "historial_eventos"

    id_evento: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_turno: Mapped[uuid.UUID] = mapped_column(ForeignKey("turnos.id_turno"))
    fecha_evento: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    tipo_evento: Mapped[str] = mapped_column(String, nullable=False)
    actor: Mapped[str] = mapped_column(String, nullable=False)
    id_usuario: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("usuarios.id_usuario"))
    motivo: Mapped[str | None] = mapped_column(String, nullable=False)


    turno = relationship("Turno")
    usuario = relationship("Usuario")