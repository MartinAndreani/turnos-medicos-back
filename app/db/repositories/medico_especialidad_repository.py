# app/db/repositories/medico_especialidad_repository.py

from typing import List

from sqlalchemy import select, insert, delete
from sqlalchemy.orm import Session

from app.db.models.medico_especialidad import medico_especialidad
from app.db.models.especialidades import EspecialidadModel
from app.domain.entities.especialidades import Especialidad


def _row_to_especialidad(row: EspecialidadModel) -> Especialidad:
    return Especialidad(
        id_especialidad=row.id_especialidad,
        nombre=row.nombre,
        descripcion=row.descripcion,
        activo=row.activo,
    )


class MedicoEspecialidadRepository:
    def __init__(self, session: Session):
        self.session = session

    # ¿Existe ya la asociación?
    def exists(self, id_medico: str, id_especialidad: str) -> bool:
        stmt = (
            select(medico_especialidad)
            .where(medico_especialidad.c.id_medico == id_medico)
            .where(medico_especialidad.c.id_especialidad == id_especialidad)
        )
        result = self.session.execute(stmt).first()
        return result is not None

    # Crear asociación
    def add(self, id_medico: str, id_especialidad: str) -> None:
        stmt = insert(medico_especialidad).values(
            id_medico=id_medico,
            id_especialidad=id_especialidad,
        )
        try:
            self.session.execute(stmt)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    # Eliminar asociación
    def remove(self, id_medico: str, id_especialidad: str) -> bool:
        stmt = (
            delete(medico_especialidad)
            .where(medico_especialidad.c.id_medico == id_medico)
            .where(medico_especialidad.c.id_especialidad == id_especialidad)
        )
        try:
            result = self.session.execute(stmt)
            self.session.commit()
            # rowcount indica cuántas filas se borraron
            return result.rowcount > 0
        except Exception:
            self.session.rollback()
            raise

    # Listar especialidades de un médico
    def list_especialidades_por_medico(self, id_medico: str) -> List[Especialidad]:
        rows = (
            self.session.query(EspecialidadModel)
            .join(
                medico_especialidad,
                EspecialidadModel.id_especialidad == medico_especialidad.c.id_especialidad,
            )
            .filter(medico_especialidad.c.id_medico == id_medico)
            .filter(EspecialidadModel.activo == True)
            .all()
        )
        return [_row_to_especialidad(r) for r in rows]
