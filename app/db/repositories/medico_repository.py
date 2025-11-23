# app/db/repositories/medico_repository.py

from uuid import uuid4
from sqlalchemy.orm import Session

from app.db.models.medicos import MedicoModel
from app.domain.entities.medicos import Medico


# ========================
#  MAPPER ORM → DOMAIN
# ========================
def _row_to_domain(row: MedicoModel) -> Medico:
    return Medico(
        id_medico=row.id_medico,
        matricula=row.matricula,
        dni=row.dni,
        nombre=row.nombre,
        apellido=row.apellido,
        telefono=row.telefono,
        activo=row.activo,
        id_usuario=row.id_usuario,
    )


# ========================
#  REPOSITORY
# ========================
class MedicoRepository:
    def __init__(self, session: Session):
        self.session = session

    # GET BY ID
    def get_by_id(self, id_medico: str) -> Medico | None:
        row = self.session.get(MedicoModel, id_medico)
        return _row_to_domain(row) if row else None

    # GET BY DNI
    def get_by_dni(self, dni: str) -> Medico | None:
        row = self.session.query(MedicoModel).filter_by(dni=dni).first()
        return _row_to_domain(row) if row else None

    # GET BY MATRICULA
    def get_by_matricula(self, matricula: str) -> Medico | None:
        row = self.session.query(MedicoModel).filter_by(matricula=matricula).first()
        return _row_to_domain(row) if row else None

    # LISTA SOLO ACTIVOS CON PAGINADO
    def list(self, skip: int = 0, limit: int = 100) -> list[Medico]:
        rows = (
            self.session.query(MedicoModel)
            .filter(MedicoModel.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [_row_to_domain(row) for row in rows]

    # LISTA TODOS (ACTIVOS E INACTIVOS)
    def list_all(self):
        return self.se
