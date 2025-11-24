from datetime import time, date
from typing import List, Optional

class AgendaMedico:
    def __init__(
        self,
        id_agenda: str,
        id_medico: str,
        fecha_inicio: date,
        fecha_fin: date,
        dias_semana: List[int], # <--- Ahora es una lista
        hora_inicio: time,
        hora_fin: time,
        duracion_turno: int,
        jornada: str,
        activo: bool = True,
    ):
        self.id_agenda = id_agenda
        self.id_medico = id_medico
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.dias_semana = dias_semana # Lista
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.duracion_turno = duracion_turno
        self.jornada = jornada
        self.activo = activo
        
        
    def actualizar(self, dias_semana=None, hora_inicio=None, hora_fin=None, 
                   duracion_turno=None, jornada=None, activo=None):
        if dias_semana is not None: self.dias_semana = dias_semana
        if hora_inicio is not None: self.hora_inicio = hora_inicio
        if hora_fin is not None: self.hora_fin = hora_fin
        if duracion_turno is not None: self.duracion_turno = duracion_turno
        if jornada is not None: self.jornada = jornada
        if activo is not None: self.activo = activo