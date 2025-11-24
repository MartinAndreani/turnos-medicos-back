
import uuid


class Consultorio:
    def __init__(self, id_consultorio:uuid.UUID,
                 numero_consultorio: int,
                 piso: int,
                activo: bool = True):
        self.id_consultorio = id_consultorio
        self.numero_consultorio = numero_consultorio
        self.piso = piso
        self.activo = activo
        
        
    def activar(self):
        if self.activo:
            raise ValueError("El consultorio ya está activo.")
        self.activo = True

    def desactivar(self):
        if not self.activo:
            raise ValueError("El consultorio ya está inactivo.")
        self.activo = False

                 