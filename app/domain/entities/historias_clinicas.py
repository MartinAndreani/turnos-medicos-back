# app/domain/entities/historias_clinicas.py

from typing import Optional


class HistoriaClinica:
    def __init__(
        self,
        id_historia_clinica: str,
        id_paciente: str,
        id_medico: str,
        id_turno: Optional[str],
        fecha_registro,
        diagnostico: Optional[str] = None,
        tratamiento: Optional[str] = None,
        observaciones: Optional[str] = None,
        activo: bool = True,
    ):
        self.id_historia_clinica = id_historia_clinica
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.id_turno = id_turno
        self.fecha_registro = fecha_registro
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.observaciones = observaciones
        self.activo = activo

    # ========= REGLAS DE NEGOCIO =========

    def desactivar(self):
        if not self.activo:
            raise ValueError("La historia clínica ya está inactiva.")
        self.activo = False

    def activar(self):
        if self.activo:
            raise ValueError("La historia clínica ya está activa.")
        self.activo = True

    def actualizar_contenido(
        self,
        diagnostico: Optional[str] = None,
        tratamiento: Optional[str] = None,
        observaciones: Optional[str] = None,
        activo: Optional[bool] = None,
    ):
        # No se permite cambiar id_paciente, id_medico, id_turno, fecha_registro
        if diagnostico is not None:
            self.diagnostico = diagnostico
        if tratamiento is not None:
            self.tratamiento = tratamiento
        if observaciones is not None:
            self.observaciones = observaciones
        if activo is not None:
            self.activo = activo
