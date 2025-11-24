from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.agendas_medicos import AgendaMedicoModel
from app.domain.entities.agendas_medicos import AgendaMedico

def _row_to_domain(row: AgendaMedicoModel) -> AgendaMedico:
    return AgendaMedico(
        id_agenda=str(row.id_agenda),
        id_medico=str(row.id_medico),
        fecha_inicio=row.fecha_inicio,
        fecha_fin=row.fecha_fin,
        dias_semana=list(row.dias_semana), # Convertimos a lista python
        hora_inicio=row.hora_inicio,
        hora_fin=row.hora_fin,
        duracion_turno=row.duracion_turno,
        jornada=row.jornada,
        activo=row.activo,
    )

class AgendaMedicoRepository:
    def __init__(self, session: Session):
        self.session = session

    def check_overlap(self, id_medico: str, dias_nuevos: List[int], hora_inicio, hora_fin, fecha_inicio, fecha_fin) -> bool:
        """
        Valida si CUALQUIERA de los días nuevos choca con alguna agenda existente.
        """
        exists = self.session.query(AgendaMedicoModel).filter(
            AgendaMedicoModel.id_medico == UUID(str(id_medico)),
            AgendaMedicoModel.activo == True,
            
            # --- VALIDACIÓN DE ARRAY (Postgres) ---
            # Verifica si hay intersección entre el array guardado y los días nuevos
            AgendaMedicoModel.dias_semana.overlap(dias_nuevos),
            
            # Hora
            AgendaMedicoModel.hora_inicio < hora_fin,
            AgendaMedicoModel.hora_fin > hora_inicio,
            
            # Fecha
            AgendaMedicoModel.fecha_inicio <= fecha_fin,
            AgendaMedicoModel.fecha_fin >= fecha_inicio
        ).first()
        return exists is not None

    def save(self, agenda: AgendaMedico) -> AgendaMedico:
        row = self.session.get(AgendaMedicoModel, UUID(agenda.id_agenda))
        if not row:
            row = AgendaMedicoModel(
                id_agenda=UUID(agenda.id_agenda),
                id_medico=UUID(agenda.id_medico),
                fecha_inicio=agenda.fecha_inicio,
                fecha_fin=agenda.fecha_fin,
                dias_semana=agenda.dias_semana, # Guardamos la lista directa
                hora_inicio=agenda.hora_inicio,
                hora_fin=agenda.hora_fin,
                duracion_turno=agenda.duracion_turno,
                jornada=agenda.jornada,
                activo=agenda.activo
            )
            self.session.add(row)
        else:
            # Update logic (si aplica)
            pass

        self.session.commit()
        self.session.refresh(row)
        return _row_to_domain(row)

    # get_by_id, list_by_medico, delete... (igual que antes)