from uuid import UUID
from datetime import date, time
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.agendas_medicos import AgendaMedicoModel
from app.domain.entities.agendas_medicos import AgendaMedico

# ... (tu función _row_to_domain sigue igual) ...
def _row_to_domain(row: AgendaMedicoModel) -> AgendaMedico:
    return AgendaMedico(
        id_agenda=str(row.id_agenda),
        id_medico=str(row.id_medico),
        fecha_inicio=row.fecha_inicio,
        fecha_fin=row.fecha_fin,
        dias_semana=list(row.dias_semana),
        hora_inicio=row.hora_inicio,
        hora_fin=row.hora_fin,
        duracion_turno=row.duracion_turno,
        jornada=row.jornada,
        activo=row.activo,
    )

class AgendaMedicoRepository:
    def __init__(self, session: Session):
        self.session = session

    # ... (tus métodos existentes save, get_by_id, check_overlap siguen igual) ...
    
    def get_by_id(self, id_agenda: str) -> Optional[AgendaMedico]:
        row = self.session.get(AgendaMedicoModel, UUID(id_agenda))
        return _row_to_domain(row) if row else None

    def check_overlap(self, id_medico: str, dias_nuevos: List[int], hora_inicio, hora_fin, fecha_inicio, fecha_fin) -> bool:
        # ... (tu código existente de overlap) ...
        exists = self.session.query(AgendaMedicoModel).filter(
            AgendaMedicoModel.id_medico == UUID(str(id_medico)),
            AgendaMedicoModel.activo == True,
            AgendaMedicoModel.dias_semana.overlap(dias_nuevos),
            AgendaMedicoModel.hora_inicio < hora_fin,
            AgendaMedicoModel.hora_fin > hora_inicio,
            AgendaMedicoModel.fecha_inicio <= fecha_fin,
            AgendaMedicoModel.fecha_fin >= fecha_inicio
        ).first()
        return exists is not None

    def save(self, agenda: AgendaMedico) -> AgendaMedico:
        # ... (tu código existente de save) ...
        row = self.session.get(AgendaMedicoModel, UUID(agenda.id_agenda))
        if not row:
            row = AgendaMedicoModel(
                id_agenda=UUID(agenda.id_agenda),
                id_medico=UUID(agenda.id_medico),
                fecha_inicio=agenda.fecha_inicio,
                fecha_fin=agenda.fecha_fin,
                dias_semana=agenda.dias_semana,
                hora_inicio=agenda.hora_inicio,
                hora_fin=agenda.hora_fin,
                duracion_turno=agenda.duracion_turno,
                jornada=agenda.jornada,
                activo=agenda.activo
            )
            self.session.add(row)
        else:
            # Update logic (simplificado)
            row.dias_semana = agenda.dias_semana
            # ... mapear otros campos si es update ...
            pass

        self.session.commit()
        self.session.refresh(row)
        return _row_to_domain(row)

    def delete(self, id_agenda: str) -> bool:
        # ... (tu código existente de delete) ...
        row = self.session.get(AgendaMedicoModel, UUID(id_agenda))
        if not row: return False
        row.activo = False
        self.session.commit()
        return True

    # --- NUEVO MÉTODO PARA TURNOS ---
    def find_agenda_for_turn(self, id_medico: str, fecha: date, dia: int, start: time, end: time) -> Optional[AgendaMedico]:
        """
        Busca una agenda activa que contenga:
        1. La fecha del turno (dentro del mes).
        2. El día de la semana (dentro del array de días).
        3. El horario (el turno debe estar TOTALMENTE dentro del horario de agenda).
        """
        row = self.session.query(AgendaMedicoModel).filter(
            AgendaMedicoModel.id_medico == UUID(id_medico),
            AgendaMedicoModel.activo == True,
            
            # 1. Validar Vigencia Mensual
            AgendaMedicoModel.fecha_inicio <= fecha,
            AgendaMedicoModel.fecha_fin >= fecha,
            
            # 2. Validar Día de Semana (Array contains)
            # Verificamos si la lista de días contiene 'dia' (ej: 0 para Lunes)
            AgendaMedicoModel.dias_semana.contains([dia]),
            
            # 3. Validar Horario (Contención estricta)
            # La agenda debe empezar ANTES o IGUAL que el turno
            AgendaMedicoModel.hora_inicio <= start,
            # La agenda debe terminar DESPUÉS o IGUAL que el turno
            AgendaMedicoModel.hora_fin >= end
        ).first()

        return _row_to_domain(row) if row else None