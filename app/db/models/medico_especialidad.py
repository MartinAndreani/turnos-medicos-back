from sqlalchemy import Table, Column, ForeignKey
from app.db.database import Base

medico_especialidad = Table(
    "medico_especialidad",
    Base.metadata,
    Column("id_medico", ForeignKey("medicos.id_medico"), primary_key=True),
    Column("id_especialidad", ForeignKey("especialidades.id_especialidad"), primary_key=True),
)