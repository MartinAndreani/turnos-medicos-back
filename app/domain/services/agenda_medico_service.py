from datetime import date, datetime, timedelta
from uuid import uuid4
from typing import List
from app.api.schemas.agendas_medicos import AgendaMedicoCreate # Asegurate que sea singular
from app.domain.entities.agendas_medicos import AgendaMedico
# Imports repos...

class AgendaMedicoService:
    def __init__(self, agenda_repo, asignacion_repo, medico_repo):
        self.agenda_repo = agenda_repo
        self.asignacion_repo = asignacion_repo
        self.medico_repo = medico_repo

    # Devuelve UN SOLO objeto AgendaMedico (no una lista)
    def create_masivo(self, dto: AgendaMedicoCreate) -> AgendaMedico:
        
        if not self.medico_repo.get_by_id(str(dto.id_medico)):
            raise ValueError("Médico no existe.")

        # 1. Validar Agenda del Médico (Array overlap)
        if self.agenda_repo.check_overlap(
            str(dto.id_medico), 
            dto.dias_semana, # Lista completa
            dto.hora_inicio, 
            dto.hora_fin, 
            dto.fecha_inicio, 
            dto.fecha_fin
        ):
            raise ValueError("El médico ya tiene agenda ocupada en esos días y horarios.")

        # 2. Validar Consultorio (Array overlap)
        if self.asignacion_repo.get_overlap(
            dto.id_consultorio, 
            dto.dias_semana, # Lista completa
            dto.hora_inicio, 
            dto.hora_fin, 
            dto.fecha_inicio, 
            dto.fecha_fin,
            dto.jornada
        ):
            raise ValueError("El consultorio está ocupado en esos días y horarios.")

        # 3. Crear Agenda (1 Fila con array de días)
        nueva_agenda = AgendaMedico(
            id_agenda=str(uuid4()),
            id_medico=str(dto.id_medico),
            fecha_inicio=dto.fecha_inicio,
            fecha_fin=dto.fecha_fin,
            dias_semana=dto.dias_semana, # Lista [0, 2, 4]
            hora_inicio=dto.hora_inicio,
            hora_fin=dto.hora_fin,
            duracion_turno=dto.duracion_turno,
            jornada=dto.jornada,
            activo=True
        )
        agenda_guardada = self.agenda_repo.save(nueva_agenda)

        # 4. Crear Asignación (1 Fila con array de días)
        self.asignacion_repo.create({
            "id_asignacion": uuid4(),
            "id_medico": dto.id_medico,
            "id_consultorio": dto.id_consultorio,
            "fecha_inicio": dto.fecha_inicio,
            "fecha_fin": dto.fecha_fin,
            "dias_semana": dto.dias_semana, # Lista [0, 2, 4]
            "hora_inicio": dto.hora_inicio,
            "hora_fin": dto.hora_fin,
            "jornada": dto.jornada,
            "activo": True
        })
        
        return agenda_guardada
    
    
    def get_dias_y_horarios_disponibles(self, id_medico: str):

        # 1. Verificar que existe
        if not self.medico_repo.get_by_id(str(id_medico)):
            raise ValueError("Médico no existe.")

        hoy = date.today()

        # 2. Traer agendas válidas
        agendas = self.agenda_repo.get_agendas_activas_o_futuras(id_medico, hoy)
        if not agendas:
            return {}

        # 3. Traer turnos ocupados reales
        turnos_ocupados = self.agenda_repo.get_turnos_ocupados(id_medico)

        # Mapa: "2025-11-26": {"09:00", "09:30"}
        turnos_map = {}
        for t in turnos_ocupados:
            fecha = t.fecha_hora_inicio.date().isoformat()
            hora = t.fecha_hora_inicio.time().strftime("%H:%M")
            turnos_map.setdefault(fecha, set()).add(hora)

        resultado = {}

        # 4. Procesar cada agenda
        for ag in agendas:
            cursor = max(hoy, ag.fecha_inicio)

            while cursor <= ag.fecha_fin:

                if cursor.weekday() in ag.dias_semana:

                    dt_inicio = datetime.combine(cursor, ag.hora_inicio)
                    dt_fin = datetime.combine(cursor, ag.hora_fin)
                    actual = dt_inicio

                    horarios_disponibles = []

                    while actual + timedelta(minutes=ag.duracion_turno) <= dt_fin:
                        hora_str = actual.time().strftime("%H:%M")

                        if hora_str not in turnos_map.get(cursor.isoformat(), []):
                            horarios_disponibles.append(hora_str)

                        actual += timedelta(minutes=ag.duracion_turno)

                    if horarios_disponibles:
                        resultado.setdefault(cursor.isoformat(), []).extend(
                            horarios_disponibles
                        )

                cursor += timedelta(days=1)

        return resultado