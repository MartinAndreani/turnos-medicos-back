# app/domain/entities/turnos.py

from typing import Optional
from datetime import datetime
import uuid


class Turno:
    def __init__(
        self,
        id_turno: uuid.UUID,
        id_paciente: uuid.UUID,
        id_medico: uuid.UUID,
        id_consultorio: uuid.UUID,
        fecha_hora_inicio: datetime,
        fecha_hora_fin: datetime,
        id_estado: str = "PENDIENTE",
        motivo_consulta: Optional[str] = None,
    ):
        self.id_turno = id_turno
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.id_consultorio = id_consultorio
        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin = fecha_hora_fin
        self.id_estado = id_estado
        self.motivo_consulta = motivo_consulta

    # ===== LÓGICA DE NEGOCIO =====

    def confirmar(self):
        if self.id_estado == "CONFIRMADO":
            raise ValueError("El turno ya está confirmado.")
        if self.id_estado == "CANCELADO":
            raise ValueError("No se puede confirmar un turno cancelado.")
        self.id_estado = "CONFIRMADO"

    def cancelar(self):
        if self.id_estado == "CANCELADO":
            raise ValueError("El turno ya está cancelado.")
        if self.id_estado == "FINALIZADO":
            raise ValueError("No se puede cancelar un turno finalizado.")
        self.id_estado = "CANCELADO"

    def finalizar(self):
        if self.id_estado != "CONFIRMADO":
            raise ValueError("Solo un turno confirmado puede finalizarse.")
        self.id_estado = "FINALIZADO"
