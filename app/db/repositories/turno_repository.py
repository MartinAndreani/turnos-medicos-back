# app/db/repositories/turno_repository.py

from uuid import uuid4
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.models.turnos import TurnoModel
from app.domain.entities.turnos import Turno


def _row_to_domain(row: TurnoModel) -> Turno:
    return Turno(
        id_turno=row.id_turno,
        id_paciente=row.id_paciente,
        id_medico=row.id_medico,
        id_consultorio=row.id_consultorio,
        fecha_hora_inicio=row.fecha_hora_inicio,
        fecha_hora_fin=row.fecha_hora_fin,
        id_estado=row.id_estado,
        motivo_consulta=row.motivo_consulta,
    )


class TurnoRepository:
    def __init__(self, session: Session):
        self.session = session

    # GET BY ID
    def get_by_id(self, id_turno: str) -> Optional[Turno]:
        row = self.session.get(TurnoModel, id_turno)
        return _row_to_domain(row) if row else None

    # LIST
    def list(self, skip: int = 0, limit: int = 100) -> List[Turno]:
        rows = (
            self.session.query(TurnoModel)
            .filter(TurnoModel.id_estado != "CANCELADO")   # excluir cancelados por defecto
            .order_by(TurnoModel.fecha_hora_inicio)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [_row_to_domain(r) for r in rows]

    # LIST POR MEDICO
    def list_by_medico(self, id_medico: str, skip: int = 0, limit: int = 100) -> List[Turno]:
        rows = (
            self.session.query(TurnoModel)
            .filter(TurnoModel.id_medico == id_medico)
            .filter(TurnoModel.id_estado != "CANCELADO")
            .order_by(TurnoModel.fecha_hora_inicio)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [_row_to_domain(r) for r in rows]

    # LIST POR PACIENTE
    def list_by_paciente(self, id_paciente: str, skip: int = 0, limit: int = 100) -> List[Turno]:
        rows = (
            self.session.query(TurnoModel)
            .filter(TurnoModel.id_paciente == id_paciente)
            .filter(TurnoModel.id_estado != "CANCELADO")
            .order_by(TurnoModel.fecha_hora_inicio)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [_row_to_domain(r) for r in rows]
    


    # ======================================================
    # VALIDACIÓN DE SUPERPOSICIÓN – MÉDICO
    # ======================================================
    def hay_superposicion_medico(
        self,
        id_medico: str,
        inicio,
        fin,
        excluir_id: str | None = None
    ) -> bool:

        query = (
            self.session.query(TurnoModel)
            .filter(TurnoModel.id_medico == id_medico)
            .filter(TurnoModel.id_estado != "CANCELADO")
            .filter(TurnoModel.fecha_hora_inicio < fin)
            .filter(TurnoModel.fecha_hora_fin > inicio)
        )

        if excluir_id:
            query = query.filter(TurnoModel.id_turno != excluir_id)

        return self.session.query(query.exists()).scalar()
    

    # ======================================================
    # VALIDACIÓN DE SUPERPOSICIÓN – CONSULTORIO
    # ======================================================
    def hay_superposicion_consultorio(
        self,
        id_consultorio: str,
        inicio,
        fin,
        excluir_id: str | None = None
    ) -> bool:

        query = (
            self.session.query(TurnoModel)
            .filter(TurnoModel.id_consultorio == id_consultorio)
            .filter(TurnoModel.id_estado != "CANCELADO")
            .filter(TurnoModel.fecha_hora_inicio < fin)
            .filter(TurnoModel.fecha_hora_fin > inicio)
        )

        if excluir_id:
            query = query.filter(TurnoModel.id_turno != excluir_id)

        return self.session.query(query.exists()).scalar()

    # SAVE (CREATE / UPDATE)
    def save(self, turno: Turno) -> Turno:
        row = self.session.get(TurnoModel, turno.id_turno)

        if not row:
            row = TurnoModel(id_turno=turno.id_turno or str(uuid4()))

        row.id_paciente = turno.id_paciente
        row.id_medico = turno.id_medico
        row.id_consultorio = turno.id_consultorio
        row.fecha_hora_inicio = turno.fecha_hora_inicio
        row.fecha_hora_fin = turno.fecha_hora_fin
        row.id_estado = turno.id_estado
        row.motivo_consulta = turno.motivo_consulta

        try:
            self.session.add(row)
            self.session.commit()
            self.session.refresh(row)
        except Exception:
            self.session.rollback()
            raise

        return _row_to_domain(row)

    # DELETE (BAJA LOGICA → CANCELADO)
    def delete(self, id_turno: str) -> bool:
        row = self.session.get(TurnoModel, id_turno)
        if not row:
            return False

        try:
            row.id_estado = "CANCELADO"    # BAJA LÓGICA
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise
