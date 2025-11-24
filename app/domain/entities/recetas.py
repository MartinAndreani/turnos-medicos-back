# app/domain/entities/recetas.py

from typing import Optional
from datetime import date
import uuid


class Receta:
    def __init__(
        self,
        id_receta: uuid.UUID,
        id_turno: uuid.UUID,
        fecha_emision: date,
        medicamentos: Optional[str] = None,
        descripcion: Optional[str] = None,
        activo: bool = True,
    ):
        self.id_receta = id_receta
        self.id_turno = id_turno
        self.fecha_emision = fecha_emision
        self.medicamentos = medicamentos
        self.descripcion = descripcion
        self.activo = activo

    # ===== LÓGICA DE NEGOCIO =====

    def anular(self):
        if not self.activo:
            raise ValueError("La receta ya está anulada.")
        self.activo = False
