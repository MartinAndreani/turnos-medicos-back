# app/domain/entities/agenda_medico.py

from datetime import time
from typing import Optional


class AgendaMedico:
    def __init__(
        self,
        id_agenda: str,
        id_medico: str,
        dia_semana: int,
        hora_inicio: time,
        hora_fin: time,
        duracion_turno: int,
        jornada: str,
        activo: bool = True,
    ):
        self.id_agenda = id_agenda
        self.id_medico = id_medico
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.duracion_turno = duracion_turno
        self.jornada = jornada
        self.activo = activo

    # ====== REGLAS ======

    def desactivar(self):
        if not self.activo:
            raise ValueError("La agenda ya está inactiva.")
        self.activo = False

    def activar(self):
        if self.activo:
            raise ValueError("La agenda ya está activa.")
        self.activo = True

    def actualizar(
        self,
        dia_semana: Optional[int] = None,
        hora_inicio: Optional[time] = None,
        hora_fin: Optional[time] = None,
        duracion_turno: Optional[int] = None,
        jornada: Optional[str] = None,
        activo: Optional[bool] = None,
    ):
        if dia_semana is not None:
            self.dia_semana = dia_semana
        if hora_inicio is not None:
            self.hora_inicio = hora_inicio
        if hora_fin is not None:
            self.hora_fin = hora_fin
        if duracion_turno is not None:
            self.duracion_turno = duracion_turno
        if jornada is not None:
            self.jornada = jornada
        if activo is not None:
            self.activo = activo
