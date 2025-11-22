import uuid
from sqlalchemy import String, Text, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.db.mixins import TimestampMixin

class EspecialidadModel(TimestampMixin, Base):
    __tablename__ = "especialidades"

    id_especialidad: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text)

    medicos = relationship(
        "MedicoModel",
        secondary="medico_especialidad",
        back_populates="especialidades"
    )