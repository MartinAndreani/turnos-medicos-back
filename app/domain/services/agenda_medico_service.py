# app/domain/services/agenda_medico_service.py

from uuid import uuid4
from datetime import time

from app.domain.entities.agendas_medicos import AgendaMedico
from app.api.schemas.agendas_medicos import AgendaMedicoCreate, AgendaMedicoUpdate
from app.db.repositories.agenda_medico_repository import AgendaMedicoRepository
from app.db.repositories.medico_repository import MedicoRepository


def _minutos(t: time):
    return t.hour * 60 + t.minute


class AgendaMedicoService:
    def __init__(self, agenda_repo: AgendaMedicoRepository, medico_repo: MedicoRepository):
        self.agenda_repo = agenda_repo
        self.medico_repo = medico_repo

    # ====== CREATE ======
    def create(self, dto: AgendaMedicoCreate) -> AgendaMedico:
        id_medico_str = str(dto.id_medico)

        # 1) Médico activo
        medico = self.medico_repo.get_by_id(id_medico_str)
        if not medico or not getattr(medico, "activo", True):
            raise ValueError("El médico no existe o está inactivo.")

        # 2) Validar horas
        if dto.hora_fin <= dto.hora_inicio:
            raise ValueError("La hora de fin debe ser mayor que la hora de inicio.")

        # 3) Validar duración dentro del intervalo
        intervalo_min = _minutos(dto.hora_fin) - _minutos(dto.hora_inicio)
        if dto.duracion_turno > intervalo_min:
            raise ValueError("La duración del turno no puede exceder el intervalo disponible.")

        # 4) Validar superposición en el mismo día
        agendas_existentes = self.agenda_repo.list_by_medico(id_medico_str)
        for a in agendas_existentes:
            if a.dia_semana == dto.dia_semana:
                # overlap check
                if not (dto.hora_fin <= a.hora_inicio or dto.hora_inicio >= a.hora_fin):
                    raise ValueError("La agenda se superpone con otra existente.")

        agenda = AgendaMedico(
            id_agenda=str(uuid4()),
            id_medico=id_medico_str,
            dia_semana=dto.dia_semana,
            hora_inicio=dto.hora_inicio,
            hora_fin=dto.hora_fin,
            duracion_turno=dto.duracion_turno,
            jornada=dto.jornada,
            activo=True,
        )

        return self.agenda_repo.save(agenda)

    # ====== UPDATE ======
    def update(self, id_agenda: str, dto: AgendaMedicoUpdate) -> AgendaMedico:
        agenda = self.agenda_repo.get_by_id(id_agenda)
        if not agenda:
            raise ValueError("Agenda no encontrada.")

        # No se puede cambiar el médico
        # Validación de horas si se cambian
        new_inicio = dto.hora_inicio or agenda.hora_inicio
        new_fin = dto.hora_fin or agenda.hora_fin

        if new_fin <= new_inicio:
            raise ValueError("La hora de fin debe ser mayor que la hora de inicio.")

        intervalo_min = _minutos(new_fin) - _minutos(new_inicio)
        new_duracion = dto.duracion_turno or agenda.duracion_turno
        if new_duracion > intervalo_min:
            raise ValueError("La duración del turno no puede exceder el intervalo.")

        # Validación de superposición si cambian horarios o día
        new_dia = dto.dia_semana or agenda.dia_semana
        agendas_existentes = self.agenda_repo.list_by_medico(agenda.id_medico)

        for a in agendas_existentes:
            if a.id_agenda == id_agenda:
                continue

            if a.dia_semana == new_dia:
                if not (new_fin <= a.hora_inicio or new_inicio >= a.hora_fin):
                    raise ValueError("La agenda se superpone con otra existente.")

        # Aplicar cambios
        agenda.actualizar(
            dia_semana=dto.dia_semana,
            hora_inicio=dto.hora_inicio,
            hora_fin=dto.hora_fin,
            duracion_turno=dto.duracion_turno,
            jornada=dto.jornada,
            activo=dto.activo,
        )

        return self.agenda_repo.save(agenda)

    # ====== DELETE ======
    def delete(self, id_agenda: str) -> bool:
        return self.agenda_repo.delete(id_agenda)
