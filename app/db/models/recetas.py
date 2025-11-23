from datetime import date, datetime
import uuid
from sqlalchemy import ForeignKey, Date, JSON, Text, func, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.db.mixins import TimestampMixin

class RecetaModel(TimestampMixin, Base):
    __tablename__ = "recetas"

    id_receta: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    id_turno: Mapped[uuid.UUID] = mapped_column(ForeignKey("turnos.id_turno"))
    medicamentos: Mapped[dict | None] = mapped_column(JSON)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

    turno = relationship("TurnoModel", back_populates="recetas")
