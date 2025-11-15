from datetime import date
import uuid
from sqlalchemy import ForeignKey, Date, JSON, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base

class Receta(Base):
    __tablename__ = "recetas"

    id_receta: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_turno: Mapped[uuid.UUID] = mapped_column(ForeignKey("turnos.id_turno"), nullable=False)

    fecha_emision: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.now())
    medicamentos: Mapped[dict | None] = mapped_column(JSON)

    turno = relationship("Turno", back_populates="recetas")
