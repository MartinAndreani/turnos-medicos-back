import uuid
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.db.mixins import TimestampMixin

class MedicoEspecialidadModel(TimestampMixin, Base):
    __tablename__ = "medico_especialidad"
    
    id_medico_especialidad: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"))
    
    id_medico: Mapped[uuid.UUID] = mapped_column(ForeignKey("medicos.id_medico"))
    id_especialidad: Mapped[uuid.UUID] = mapped_column(ForeignKey("especialidades.id_especialidad"))

    medico = relationship("MedicoModel", back_populates="especialidades")
    especialidad = relationship("EspecialidadModel", back_populates="medicos")
