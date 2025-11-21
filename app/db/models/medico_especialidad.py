import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.db.mixins import TimestampMixin

class MedicoEspecialidad(TimestampMixin, Base):
    __tablename__ = "medico_especialidad"
    
    id_medico_especialidad: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    
    id_medico: Mapped[uuid.UUID] = mapped_column(ForeignKey("medicos.id_medico"))
    id_especialidad: Mapped[uuid.UUID] = mapped_column(ForeignKey("especialidades.id_especialidad"))

    medico = relationship("Medico", back_populates="especialidades")
    especialidad = relationship("Especialidad", back_populates="medicos")
