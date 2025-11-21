from datetime import date, datetime
import uuid
from sqlalchemy import ForeignKey, Date, JSON, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.db.mixins import TimestampMixin

class Receta(TimestampMixin, Base):
    __tablename__ = "recetas"

    id_receta: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_turno: Mapped[uuid.UUID] = mapped_column(ForeignKey("turnos.id_turno"))
    medicamentos: Mapped[dict | None] = mapped_column(JSON)

    turno = relationship("Turno", back_populates="recetas")
