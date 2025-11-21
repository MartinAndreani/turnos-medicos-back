

import uuid

from sqlalchemy import String, Text
from app.db.base import Base
from app.db.mixins import TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

class EstadoTurno(TimestampMixin,Base):
    __tablename__ = "estados_turnos"
    
    id_estado_turno: Mapped[uuid.UUID] = mapped_column( primary_key=True, default=uuid.uuid4 )
    nombre: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column( nullable=False, default=True )
    
    
    turnos = relationship("Turno", back_populates="estado_turno")