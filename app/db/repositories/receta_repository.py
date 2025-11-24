# app/db/repositories/receta_repository.py

from uuid import uuid4
from typing import Optional, List

from sqlalchemy.orm import Session

from app.db.models.recetas import RecetaModel
from app.domain.entities.recetas import Receta


def _row_to_domain(row: RecetaModel) -> Receta:
    return Receta(
        id_receta=row.id_receta,
        id_turno=row.id_turno,
        fecha_emision=row.fecha_emision,
        medicamentos=row.medicamentos,
        descripcion=row.descripcion,
        activo=row.activo,
    )


class RecetaRepository:
    def __init__(self, session: Session):
        self.session = session

    # GET BY ID
    def get_by_id(self, id_receta: str) -> Optional[Receta]:
        row = self.session.get(RecetaModel, id_receta)
        return _row_to_domain(row) if row else None

    # GET BY TURNO
    def get_by_turno(self, id_turno: str) -> Optional[Receta]:
        row = (
            self.session.query(RecetaModel)
            .filter(RecetaModel.id_turno == id_turno)
            .filter(RecetaModel.activo == True)
            .first()
        )
        return _row_to_domain(row) if row else None

    # LIST (solo activas)
    def list(self, skip: int = 0, limit: int = 100) -> List[Receta]:
        rows = (
            self.session.query(RecetaModel)
            .filter(RecetaModel.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [_row_to_domain(r) for r in rows]

    # LIST POR TURNO
    def list_by_turno(self, id_turno: str) -> List[Receta]:
        rows = (
            self.session.query(RecetaModel)
            .filter(RecetaModel.id_turno == id_turno)
            .filter(RecetaModel.activo == True)
            .all()
        )
        return [_row_to_domain(r) for r in rows]

    # SAVE (CREATE / UPDATE)
    def save(self, receta: Receta) -> Receta:
        row = self.session.get(RecetaModel, receta.id_receta)

        if not row:
            row = RecetaModel(id_receta=receta.id_receta or uuid4())

        row.id_turno = receta.id_turno
        row.fecha_emision = receta.fecha_emision
        row.medicamentos = receta.medicamentos
        row.descripcion = receta.descripcion
        row.activo = receta.activo

        try:
            self.session.add(row)
            self.session.commit()
            self.session.refresh(row)
        except Exception:
            self.session.rollback()
            raise

        return _row_to_domain(row)

    # BAJA LÓGICA
    def delete(self, id_receta: str) -> bool:
        row = self.session.get(RecetaModel, id_receta)
        if not row:
            return False

        try:
            row.activo = False
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise
