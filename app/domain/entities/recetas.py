from typing import Optional
import uuid

class Receta:
    def __init__(self, id_receta: uuid.UUID,
        id_turno: uuid.UUID,
        fecha_emision: str,
        medicamentos: Optional[str] = None,
        descripcion: Optional[str] = None
        ):

        self.id_receta = id_receta
        self.id_turno = id_turno
        self.fecha_emision = fecha_emision
        self.medicamentos = medicamentos
        self.descripcion = descripcion
