from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.db.models.turnos import TurnoModel 
from app.db.models.historial_eventos import HistorialEventoModel # Ajusta import
from app.domain.entities.turnos import Turno

def _row_to_domain(row: TurnoModel) -> Turno:
    return Turno(
        id_turno=str(row.id_turno),
        id_paciente=str(row.id_paciente),
        id_medico=str(row.id_medico),
        id_consultorio=str(row.id_consultorio),
        id_estado_turno=str(row.id_estado_turno),
        fecha_hora_inicio=row.fecha_hora_inicio,
        fecha_hora_fin=row.fecha_hora_fin,
        motivo_consulta=row.motivo_consulta
    )

class TurnoRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, turno: Turno) -> Turno:
        row = self.session.get(TurnoModel, UUID(turno.id_turno))
        if not row:
            row = TurnoModel(
                id_turno=UUID(turno.id_turno),
                id_paciente=UUID(turno.id_paciente),
                id_medico=UUID(turno.id_medico),
                id_consultorio=UUID(turno.id_consultorio),
                id_estado_turno=UUID(turno.id_estado_turno),
                fecha_hora_inicio=turno.fecha_hora_inicio,
                fecha_hora_fin=turno.fecha_hora_fin,
                motivo_consulta=turno.motivo_consulta
            )
            self.session.add(row)
        else:
            row.id_estado_turno = UUID(turno.id_estado_turno)
            # Actualizar otros campos si fuera necesario

        self.session.flush() # Flush para obtener IDs si fuera autoincremental (aquí es UUID)
        return _row_to_domain(row)

    def check_overlap_medico(self, id_medico: str, inicio, fin) -> bool:
        """Valida si el médico ya tiene turno en ese horario"""
        exists = self.session.query(TurnoModel).filter(
            TurnoModel.id_medico == UUID(id_medico),
            # Filtra solo turnos activos (ej: no cancelados)
            # Aquí deberías filtrar por estados que "ocupan" lugar.
            # Asumiremos que todos ocupan salvo 'Cancelado'.
            # TurnoModel.id_estado_turno != ID_CANCELADO (Mejor manejar lógica en Service)
            
            TurnoModel.fecha_hora_inicio < fin,
            TurnoModel.fecha_hora_fin > inicio
        ).first()
        return exists is not None

    def check_overlap_paciente(self, id_paciente: str, inicio, fin) -> bool:
        """Valida si el paciente ya tiene turno en ese horario"""
        exists = self.session.query(TurnoModel).filter(
            TurnoModel.id_paciente == UUID(id_paciente),
            TurnoModel.fecha_hora_inicio < fin,
            TurnoModel.fecha_hora_fin > inicio
        ).first()
        return exists is not None

    def add_history(self, historial_data: dict):
        """Agrega una entrada al historial de eventos"""
        row = HistorialEventoModel(**historial_data)
        self.session.add(row)
    
    def commit(self):
        self.session.commit()

    def get_by_id(self, id_turno: str):
        row = self.session.get(TurnoModel, UUID(id_turno))
        return _row_to_domain(row) if row else None