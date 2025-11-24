# app/db/repositories/agenda_medico_repository.py

from uuid import uuid4
from sqlalchemy.orm import Session

from app.db.models.agendas_medicos import AgendaMedicoModel
from app.domain.entities.agendas_medicos import AgendaMedico


def _row_to_domain(row: AgendaMedicoModel) -> AgendaMedico:
    return AgendaMedico(
        id_agenda=str(row.id_agenda),
        id_medico=str(row.id_medico),
        dia_semana=row.dia_semana,
        hora_inicio=row.hora_inicio,
        hora_fin=row.hora_fin,
        duracion_turno=row.duracion_turno,
        jornada=row.jornada,
        activo=row.activo,
    )


class AgendaMedicoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id_agenda: str):
        row = self.session.get(AgendaMedicoModel, id_agenda)
        return _row_to_domain(row) if row else None

    def list_by_medico(self, id_medico: str):
        rows = (
            self.session.query(AgendaMedicoModel)
            .filter(AgendaMedicoModel.id_medico == id_medico)
            .filter(AgendaMedicoModel.activo == True)
            .all()
        )
        return [_row_to_domain(r) for r in rows]

    def save(self, agenda: AgendaMedico):
        row = self.session.get(AgendaMedicoModel, agenda.id_agenda)

        if not row:
            row = AgendaMedicoModel(
                id_agenda=agenda.id_agenda or str(uuid4())
            )

        row.id_medico = agenda.id_medico
        row.dia_semana = agenda.dia_semana
        row.hora_inicio = agenda.hora_inicio
        row.hora_fin = agenda.hora_fin
        row.duracion_turno = agenda.duracion_turno
        row.jornada = agenda.jornada
        row.activo = agenda.activo

        try:
            self.session.add(row)
            self.session.commit()
            self.session.refresh(row)
        except Exception:
            self.session.rollback()
            raise

        return _row_to_domain(row)

    def delete(self, id_agenda: str) -> bool:
        row = self.session.get(AgendaMedicoModel, id_agenda)
        if not row:
            return False

        try:
            row.activo = False
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise
