from datetime import datetime
from uuid import UUID
from typing import Optional

class Turno:
    def __init__(
        self,
        id_turno: str,
        id_paciente: str,
        id_medico: str,
        id_consultorio: str,
        id_estado_turno: str,
        fecha_hora_inicio: datetime,
        fecha_hora_fin: datetime,
        motivo_consulta: Optional[str] = None,
    ):
        self.id_turno = id_turno
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.id_consultorio = id_consultorio
        self.id_estado_turno = id_estado_turno
        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin = fecha_hora_fin
        self.motivo_consulta = motivo_consulta

    def cambiar_estado(self, nuevo_estado_id: str):
        self.id_estado_turno = nuevo_estado_id