# app/db/repositories/historia_clinica_repository.py

from uuid import uuid4
from typing import Optional, List

from sqlalchemy.orm import Session

from app.db.models.historias_clinicas import HistoriaClinicaModel
from app.domain.entities.historias_clinicas import HistoriaClinica


def _row_to_domain(row: HistoriaClinicaModel) -> HistoriaClinica:
    return HistoriaClinica(
        id_historia_clinica=str(row.id_historia_clinica),
        id_paciente=str(row.id_paciente),
        id_medico=str(row.id_medico),
        id_turno=str(row.id_turno) if row.id_turno is not None else None,
        fecha_registro=row.fecha_registro,
        diagnostico=row.diagnostico,
        tratamiento=row.tratamiento,
        observaciones=row.observaciones,
        activo=row.activo,
    )


class HistoriaClinicaRepository:
    def __init__(self, session: Session):
        self.session = session

    # ========== GETS ==========

    def get_by_id(self, id_historia_clinica: str) -> Optional[HistoriaClinica]:
        row = self.session.get(HistoriaClinicaModel, id_historia_clinica)
        return _row_to_domain(row) if row else None

    def list(self, skip: int = 0, limit: int = 100) -> List[HistoriaClinica]:
        rows = (
            self.session.query(HistoriaClinicaModel)
            .filter(HistoriaClinicaModel.activo == True)
            .order_by(HistoriaClinicaModel.fecha_registro.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [_row_to_domain(r) for r in rows]

    def list_by_paciente(
        self, id_paciente: str, skip: int = 0, limit: int = 100
    ) -> List[HistoriaClinica]:
        rows = (
            self.session.query(HistoriaClinicaModel)
            .filter(HistoriaClinicaModel.id_paciente == id_paciente)
            .filter(HistoriaClinicaModel.activo == True)
            .order_by(HistoriaClinicaModel.fecha_registro.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [_row_to_domain(r) for r in rows]

    # ========== SAVE (CREATE/UPDATE) ==========

    def save(self, hc: HistoriaClinica) -> HistoriaClinica:
        row = self.session.get(HistoriaClinicaModel, hc.id_historia_clinica)

        if not row:
            row = HistoriaClinicaModel(
                id_historia_clinica=hc.id_historia_clinica or uuid4()
            )

        row.id_paciente = hc.id_paciente
        row.id_medico = hc.id_medico
        row.id_turno = hc.id_turno
        row.diagnostico = hc.diagnostico
        row.tratamiento = hc.tratamiento
        row.observaciones = hc.observaciones
        row.activo = hc.activo

        try:
            self.session.add(row)
            self.session.commit()
            self.session.refresh(row)
        except Exception:
            self.session.rollback()
            raise

        return _row_to_domain(row)

    # ========== BAJA LÓGICA ==========

    def delete(self, id_historia_clinica: str) -> bool:
        row = self.session.get(HistoriaClinicaModel, id_historia_clinica)
        if not row:
            return False

        try:
            row.activo = False
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise
