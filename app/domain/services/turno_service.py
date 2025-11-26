# app/domain/services/turno_service.py

from uuid import uuid4, UUID
from datetime import datetime
from app.api.schemas.turnos import TurnoCreate, TurnoUpdateEstado
from app.domain.entities.turnos import Turno

# Repositories
from app.db.repositories.turno_repository import TurnoRepository
from app.db.repositories.agenda_medico_repository import AgendaMedicoRepository
from app.db.repositories.asignacion_consultorio_repository import AsignacionConsultorioRepository
from app.db.repositories.medico_repository import MedicoRepository

# --- CORRECCIÓN AQUÍ: Importamos las nuevas clases específicas ---
from app.domain.entities.estados_turnos import (
    TurnoStateFactory, 
    EstadoPendiente, 
    EstadoConfirmado, 
    # EstadoCancelado,          <-- ESTO ERA LO QUE DABA ERROR (Bórralo)
    EstadoCanceladoPorPaciente, # <-- AGREGA ESTO
    EstadoCanceladoPorMedico,   # <-- AGREGA ESTO
    EstadoTurnoEnum
)

class TurnoService:
    def __init__(
        self, 
        turno_repo: TurnoRepository,
        agenda_repo: AgendaMedicoRepository,
        asignacion_repo: AsignacionConsultorioRepository,
        medico_repo: MedicoRepository
    ):
        self.turno_repo = turno_repo
        self.agenda_repo = agenda_repo
        self.asignacion_repo = asignacion_repo
        self.medico_repo = medico_repo
        
        
        
    def get_all(
        self, 
        id_medico: str = None, 
        id_paciente: str = None, 
        fecha_desde: datetime = None,
        fecha_hasta: datetime = None
    ) -> list[Turno]:
        """
        Obtiene lista de turnos con filtros opcionales.
        """
        return self.turno_repo.get_all(
            id_medico=id_medico, 
            id_paciente=id_paciente,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )
        
    
    def get_by_id(self, id_turno: str) -> Turno:
        """Obtiene un turno por su ID o lanza error si no existe."""
        turno = self.turno_repo.get_by_id(id_turno)
        if not turno:
            raise ValueError("El turno no existe.")
        return turno

    def create(self, dto: TurnoCreate) -> Turno:
        # ... (Toda tu lógica de create sigue igual, no cambies nada aquí) ...
        # ... (Resumen: validaciones, buscar consultorio, crear turno PENDIENTE) ...
        
        # Validar existencias
        if not self.medico_repo.get_by_id(str(dto.id_medico)): raise ValueError("Médico no existe.")
        
        # Validar overlaps
        if self.turno_repo.check_overlap_medico(str(dto.id_medico), dto.fecha_hora_inicio, dto.fecha_hora_fin):
            raise ValueError("El médico ya tiene un turno asignado.")
        if self.turno_repo.check_overlap_paciente(str(dto.id_paciente), dto.fecha_hora_inicio, dto.fecha_hora_fin):
            raise ValueError("El paciente ya tiene un turno asignado.")

        # Validar Agenda
        fecha_turno = dto.fecha_hora_inicio.date()
        dia_semana = fecha_turno.weekday()
        hora_turno = dto.fecha_hora_inicio.time()
        hora_fin_turno = dto.fecha_hora_fin.time()

        agenda_valida = self.agenda_repo.find_agenda_for_turn(
            str(dto.id_medico), fecha_turno, dia_semana, hora_turno, hora_fin_turno
        )
        if not agenda_valida:
            raise ValueError("El médico no tiene agenda disponible.")

        # Obtener Consultorio
        asignacion_real = self.asignacion_repo.find_for_turn(
            id_medico=str(dto.id_medico),
            fecha=fecha_turno,
            dia=dia_semana,
            start=hora_turno,
            end=hora_fin_turno
        )
        if not asignacion_real:
             raise ValueError("El médico tiene agenda pero no tiene consultorio asignado.")

        id_consultorio_asignado = asignacion_real.id_consultorio

        # Crear Turno
        nuevo_turno = Turno(
            id_turno=str(uuid4()),
            id_paciente=str(dto.id_paciente),
            id_medico=str(dto.id_medico),
            id_consultorio=str(id_consultorio_asignado),
            id_estado_turno=EstadoTurnoEnum.PENDIENTE, # Usamos el Enum
            fecha_hora_inicio=dto.fecha_hora_inicio,
            fecha_hora_fin=dto.fecha_hora_fin,
            motivo_consulta=dto.motivo_consulta
        )
        
        saved_turno = self.turno_repo.save(nuevo_turno)

        # Historial Inicial
        estado_inicial = EstadoPendiente(saved_turno, self.turno_repo)
        estado_inicial._registrar_historial(actor="Sistema", motivo="Creación de turno", tipo_evento="CREACION")

        self.turno_repo.commit()
        return saved_turno

    def change_state(self, id_turno: str, dto: TurnoUpdateEstado) -> Turno:
        turno = self.turno_repo.get_by_id(id_turno)
        if not turno: raise ValueError("Turno no encontrado")

        # Reconstruir estado actual
        estado_actual = TurnoStateFactory.get_state(turno, self.turno_repo)

        # --- CORRECCIÓN AQUÍ: Actualizamos el mapa con las clases nuevas ---
        mapa_estados = {
            EstadoTurnoEnum.PENDIENTE: EstadoPendiente,
            EstadoTurnoEnum.CONFIRMADO: EstadoConfirmado,
            # EstadoTurnoEnum.CANCELADO: EstadoCancelado, <-- ESTO YA NO SIRVE
            
            # Usamos los específicos:
            EstadoTurnoEnum.CANCELADO_POR_PACIENTE: EstadoCanceladoPorPaciente,
            EstadoTurnoEnum.CANCELADO_POR_MEDICO: EstadoCanceladoPorMedico,
            # Si tienes más (Atendido, Ausente, etc), agrégalos aquí también si el front los manda
        }
        
        clase_estado_destino = mapa_estados.get(str(dto.id_nuevo_estado))
        
        if not clase_estado_destino:
            raise ValueError(f"Estado destino no válido o no soportado en transición manual: {dto.id_nuevo_estado}")

        # Ejecutar transición
        estado_actual.transition_to(
            nuevo_estado_class=clase_estado_destino,
            actor=dto.actor,
            motivo=dto.motivo_cambio
        )

        self.turno_repo.commit()
        return turno