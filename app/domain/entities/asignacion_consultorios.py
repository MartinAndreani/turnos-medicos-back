from uuid import UUID
from datetime import date


class AsignacionConsultorio:
    def __init__(
        self,
        id_asignacion: UUID,
        id_medico: UUID,
        id_consultorio: UUID,
        fecha_inicio: date,
        fecha_fin: date,
        jornada: str,
        activo: bool = True,
    ):
        self.id_asignacion = id_asignacion
        self.id_medico = id_medico
        self.id_consultorio = id_consultorio
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.jornada = jornada
        self.activo = activo

