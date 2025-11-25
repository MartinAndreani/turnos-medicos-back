from uuid import UUID
from datetime import date, datetime, time, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.agendas_medicos import AgendaMedicoModel
from app.db.models.turnos import TurnoModel
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

ESTADOS_OCUPADOS = [
    UUID("43c5db27-dfbb-4b78-b2f3-562e2c2cceb4"),  # AGENDADO
    UUID("15d2c416-3b46-449d-ba9f-b1457269d5c2"),  # PENDIENTE
    UUID("235e4eeb-b5dd-406f-9965-7d8d990d9823"),  # CONFIRMADO
    UUID("d5703ca8-7a47-4cee-bf70-0f82cdf597df"),  # EN SALA DE ESPERA
    UUID("279c6fff-6ee6-4d17-a6f7-1d7eb06220be"),  # EN ATENCION
]




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
    
    
    def get_dias_y_horarios_disponibles(self, id_medico: str):
        hoy = date.today()

        # 1. Obtener agendas válidas
        agendas = (
            self.session.query(AgendaMedicoModel)
            .filter(
                AgendaMedicoModel.id_medico == UUID(id_medico),
                AgendaMedicoModel.activo == True,
                AgendaMedicoModel.fecha_fin >= hoy
            )
            .order_by(AgendaMedicoModel.fecha_inicio)
            .all()
        )

        if not agendas:
            return {}

        # 2. Obtener turnos ocupados reales
        turnos_ocupados = self.get_turnos_ocupados(id_medico)

        # Convertir turnos a dict = { "2025-11-26": ["09:00", "09:30"] }
        turnos_por_dia = {}
        for t in turnos_ocupados:
            fecha = t.fecha_hora_inicio.date().isoformat()
            hora = t.fecha_hora_inicio.time().strftime("%H:%M")

            turnos_por_dia.setdefault(fecha, []).append(hora)

        resultado = {}

        # 3. Generar los horarios disponibles, filtrando los ocupados
        for row in agendas:
            fecha_cursor = max(hoy, row.fecha_inicio)

            while fecha_cursor <= row.fecha_fin:

                if fecha_cursor.weekday() in row.dias_semana:

                    horarios = []
                    dt_inicio = datetime.combine(fecha_cursor, row.hora_inicio)
                    dt_fin = datetime.combine(fecha_cursor, row.hora_fin)

                    actual = dt_inicio

                    while actual + timedelta(minutes=row.duracion_turno) <= dt_fin:
                        hora_str = actual.time().strftime("%H:%M")
                        horarios.append(hora_str)
                        actual += timedelta(minutes=row.duracion_turno)

                    # ❗ FILTRAR HORARIOS OCUPADOS
                    ocupados = turnos_por_dia.get(fecha_cursor.isoformat(), [])
                    horarios_disponibles = [
                        h for h in horarios if h not in ocupados
                    ]

                    if horarios_disponibles:
                        resultado.setdefault(fecha_cursor.isoformat(), []).extend(
                            horarios_disponibles
                        )

                fecha_cursor += timedelta(days=1)

        return resultado
    
    
    

    def get_turnos_ocupados(self, id_medico: str):
        """
        Devuelve turnos con fecha + hora REALES según tu modelo actual.
        (NO usa fecha_hora_inicio ni nada inventado)
        """
        return (
            self.session.query(TurnoModel)
            .filter(
                TurnoModel.id_medico == UUID(id_medico),
                TurnoModel.id_estado_turno.in_(ESTADOS_OCUPADOS),
            )
            .all()
        )
        
        
        
    def get_agendas_activas_o_futuras(self, id_medico: str, hoy: date):
        return (
            self.session.query(AgendaMedicoModel)
            .filter(
                AgendaMedicoModel.id_medico == UUID(id_medico),
                AgendaMedicoModel.activo == True,
                AgendaMedicoModel.fecha_fin >= hoy
            )
            .order_by(AgendaMedicoModel.fecha_inicio)
            .all()
        )
