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
    
    def save(self,medico:Medico)-> Medico:
        row = self.session.get(MedicoModel, medico.id_medico)
        if not row:
            row = MedicoModel(id_medico=medico.id_medico or str(uuid4()))
        row.matricula = medico.matricula
        row.dni = medico.dni
        row.nombre = medico.nombre
        row.apellido = medico.apellido
        row.telefono = medico.telefono
        row.activo = medico.activo
        
        try:
            self.session.add(row)
            self.session.commit()
            self.session.refresh(row)
        except:
            self.session.rollback()
            raise
        return _row_to_domain(row)


    def delete(self, id_medico: str) -> bool:
        row = self.session.get(MedicoModel, id_medico)
        if not row:
            return False
        try:
            row.activo = False
            self.session.commit()
            return True
        except:
            self.session.rollback()
            raise
        