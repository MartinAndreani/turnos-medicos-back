# app/domain/entities/medicos.py

from typing import Optional
import uuid


class Medico:
    def __init__(
        self,
        id_medico: uuid.UUID,
        matricula: str,
        dni: str,
        nombre: str,
        apellido: str,
        telefono: Optional[str] = None,
        activo: bool = True,
        id_usuario: Optional[uuid.UUID] = None,
    ):

        self.id_medico = id_medico
        self.matricula = matricula
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.activo = activo
        self.id_usuario = id_usuario

    # === MÉTODOS DE DOMINIO =======================

    def activar(self):
        if self.activo:
            raise ValueError("El médico ya está activo.")
        self.activo = True

    def desactivar(self):
        if not self.activo:
            raise ValueError("El médico ya está inactivo.")
        self.activo = False
