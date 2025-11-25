from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4, UUID

# 1. ENUM CON TUS UUIDS REALES
class EstadoTurnoEnum:
    AGENDADO = "43c5db27-dfbb-4b78-b2f3-562e2c2cceb4"
    PENDIENTE = "15d2c416-3b46-449d-ba9f-b1457269d5c2"
    CONFIRMADO = "235e44eb-b5dd-46f6-9965-7d8d990d9823"
    EN_SALA_DE_ESPERA = "d5703c83-0a67-40ec-bf70-df82cdf59f7d"
    EN_ATENCION = "279c6fff-6ee6-4d17-a63f-1d7eb06220be"
    ATENDIDO = "e6e5c959-a899-42cc-b154-ce46e6d99634"
    AUSENTE = "c16e89f6-8fc4-4b14-b34e-3ac42738fa0f"
    CANCELADO_POR_PACIENTE = "0e80543d-111c-4a40-8113-08e01f0576ba"
    CANCELADO_POR_MEDICO = "6fb4a9b6-557b-43cf-8ca3-7d07d03cb8c6" 

class TurnoState(ABC):
    def __init__(self, turno_entity, repository):
        self.turno = turno_entity
        self.repo = repository

    @abstractmethod
    def nombre_estado(self) -> str: pass

    @property
    @abstractmethod
    def id_estado(self) -> str: pass

    def _registrar_historial(self, actor: str, motivo: str, tipo_evento: str):
        # FIX: Eliminamos la clave 'estado_nuevo' que daba error.
        # Agregamos el nombre del estado al motivo por si acaso.
        motivo_enriquecido = f"{motivo} (Estado actual: {self.nombre_estado()})"
        
        historial_entry = {
            "id_evento": uuid4(),
            "id_turno": UUID(str(self.turno.id_turno)),
            "fecha_evento": datetime.now(),
            "tipo_evento": tipo_evento, # Aquí guardaremos ej: "PASO_A_CONFIRMADO"
            "actor": actor,
            "id_usuario": None,
            "motivo": motivo_enriquecido,
        }
        self.repo.add_history(historial_entry)

    def transition_to(self, nuevo_estado_class, actor: str, motivo: str):
        # 1. Instanciar
        nuevo_estado = nuevo_estado_class(self.turno, self.repo)
        
        # 2. Validar
        if not self.puede_transicionar(nuevo_estado):
             raise ValueError(f"No se puede pasar de {self.nombre_estado()} a {nuevo_estado.nombre_estado()}")

        # 3. Guardar en Entidad
        self.turno.id_estado_turno = nuevo_estado.id_estado
        self.repo.save(self.turno)
        
        # 4. Historial Dinámico
        # Generamos un tipo de evento único, ej: "PASO_A_EN_ATENCION"
        # Reemplazamos espacios por guiones bajos para que sea limpio en BD
        nombre_evento = f"{nuevo_estado.nombre_estado().replace(' ', '_')}"
        
        nuevo_estado._registrar_historial(actor, motivo, nombre_evento)
        
        return nuevo_estado

    def puede_transicionar(self, nuevo_estado) -> bool:
        # Por defecto permitimos todo. Las clases hijas restringen.
        return True

# --- IMPLEMENTACIONES CONCRETAS (Todas mapeadas) ---

class EstadoAgendado(TurnoState):
    def nombre_estado(self): return "AGENDADO"
    @property
    def id_estado(self): return EstadoTurnoEnum.AGENDADO

class EstadoPendiente(TurnoState):
    def nombre_estado(self): return "PENDIENTE"
    @property
    def id_estado(self): return EstadoTurnoEnum.PENDIENTE

class EstadoConfirmado(TurnoState):
    def nombre_estado(self): return "CONFIRMADO"
    @property
    def id_estado(self): return EstadoTurnoEnum.CONFIRMADO

class EstadoEnSalaDeEspera(TurnoState):
    def nombre_estado(self): return "EN SALA DE ESPERA"
    @property
    def id_estado(self): return EstadoTurnoEnum.EN_SALA_DE_ESPERA

class EstadoEnAtencion(TurnoState):
    def nombre_estado(self): return "EN ATENCION"
    @property
    def id_estado(self): return EstadoTurnoEnum.EN_ATENCION

class EstadoAtendido(TurnoState):
    def nombre_estado(self): return "ATENDIDO"
    @property
    def id_estado(self): return EstadoTurnoEnum.ATENDIDO
    # Regla de negocio: Un turno finalizado no debería cambiar más
    def puede_transicionar(self, nuevo_estado) -> bool: return False 

class EstadoAusente(TurnoState):
    def nombre_estado(self): return "AUSENTE"
    @property
    def id_estado(self): return EstadoTurnoEnum.AUSENTE
    def puede_transicionar(self, nuevo_estado) -> bool: return False 

class EstadoCanceladoPorPaciente(TurnoState):
    def nombre_estado(self): return "CANCELADO POR PACIENTE"
    @property
    def id_estado(self): return EstadoTurnoEnum.CANCELADO_POR_PACIENTE
    def puede_transicionar(self, nuevo_estado) -> bool: return False 

class EstadoCanceladoPorMedico(TurnoState):
    def nombre_estado(self): return "CANCELADO POR MEDICO"
    @property
    def id_estado(self): return EstadoTurnoEnum.CANCELADO_POR_MEDICO
    def puede_transicionar(self, nuevo_estado) -> bool: return False 

# --- FACTORY COMPLETO ---
class TurnoStateFactory:
    @staticmethod
    def get_state(turno_entity, repository) -> TurnoState:
        mapping = {
            EstadoTurnoEnum.AGENDADO: EstadoAgendado,
            EstadoTurnoEnum.PENDIENTE: EstadoPendiente,
            EstadoTurnoEnum.CONFIRMADO: EstadoConfirmado,
            EstadoTurnoEnum.EN_SALA_DE_ESPERA: EstadoEnSalaDeEspera,
            EstadoTurnoEnum.EN_ATENCION: EstadoEnAtencion,
            EstadoTurnoEnum.ATENDIDO: EstadoAtendido,
            EstadoTurnoEnum.AUSENTE: EstadoAusente,
            EstadoTurnoEnum.CANCELADO_POR_PACIENTE: EstadoCanceladoPorPaciente,
            EstadoTurnoEnum.CANCELADO_POR_MEDICO: EstadoCanceladoPorMedico,
        }
        
        # Obtenemos el ID actual (convertido a string para comparar con el Enum)
        id_actual = str(turno_entity.id_estado_turno)
        
        state_class = mapping.get(id_actual)
        
        # Fallback de seguridad: Si el ID no está en el mapa, devolvemos AGENDADO o lanzamos error
        if not state_class:
            # Opción A: Devolver un estado por defecto (útil para datos viejos corruptos)
            return EstadoAgendado(turno_entity, repository)
            # Opción B: Lanzar error para detectar inconsistencias
            # raise ValueError(f"Estado desconocido en base de datos: {id_actual}")

        return state_class(turno_entity, repository)