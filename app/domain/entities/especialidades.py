from typing import Optional
import uuid

class Especialidad:
    def __init__(
        self,
        id_especialidad: uuid.UUID,
        nombre: str,
        descripcion: Optional[str] = None,
        activo: bool = True,
    ):
        self.id_especialidad = id_especialidad
        self.nombre = nombre
        self.descripcion = descripcion
        self.activo = activo

    # ======= REGLAS DE NEGOCIO =======

    def activar(self):
        if self.activo:
            raise ValueError("La especialidad ya está activa.")
        self.activo = True

    def desactivar(self):
        if not self.activo:
            raise ValueError("La especialidad ya está inactiva.")
        self.activo = False

    def actualizar(self, nombre: Optional[str], descripcion: Optional[str]):
        if nombre is not None:
            self.nombre = nombre
        if descripcion is not None:
            self.descripcion = descripcion
