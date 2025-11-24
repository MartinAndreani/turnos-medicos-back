from uuid import uuid4
from sqlalchemy.orm import Session

from app.db.models.especialidades import EspecialidadModel
from app.domain.entities.especialidades import Especialidad


def _row_to_domain(row: EspecialidadModel) -> Especialidad:
    return Especialidad(
        id_especialidad=row.id_especialidad,
        nombre=row.nombre,
        descripcion=row.descripcion,
        activo=row.activo,
    )


class EspecialidadRepository:
    def __init__(self, session: Session):
        self.session = session

    # GET BY ID
    def get_by_id(self, id_especialidad: str):
        row = self.session.get(EspecialidadModel, id_especialidad)
        return _row_to_domain(row) if row else None

    # GET BY NAME
    def get_by_nombre(self, nombre: str):
        row = (
            self.session.query(EspecialidadModel)
            .filter(EspecialidadModel.nombre == nombre)
            .first()
        )
        return _row_to_domain(row) if row else None

    # LIST (solo activas)
    def list(self, skip=0, limit=100):
        rows = (
            self.session.query(EspecialidadModel)
            .filter(EspecialidadModel.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [_row_to_domain(r) for r in rows]

    # CREATE / UPDATE
    def save(self, esp: Especialidad):
        row = self.session.get(EspecialidadModel, esp.id_especialidad)

        if not row:
            row = EspecialidadModel(id_especialidad=esp.id_especialidad or uuid4())

        row.nombre = esp.nombre
        row.descripcion = esp.descripcion
        row.activo = esp.activo

        try:
            self.session.add(row)
            self.session.commit()
            self.session.refresh(row)
        except Exception:
            self.session.rollback()
            raise

        return _row_to_domain(row)

    # BAJA LÓGICA
    def delete(self, id_especialidad: str):
        row = self.session.get(EspecialidadModel, id_especialidad)
        if not row:
            return False

        try:
            row.activo = False
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise
