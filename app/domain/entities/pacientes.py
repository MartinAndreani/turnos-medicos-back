


from typing import Optional
import uuid


class Paciente:
    def __init__(self, id_paciente: uuid.UUID,
        dni:str,
        nombre:str,
        apellido:str,
        fecha_nacimiento:Optional[str]=None,
        direccion:Optional[str]=None,
        telefono:Optional[str]=None,
        activo:bool=True,
        id_usuario: Optional[uuid.UUID]=None,    
            ):
        
        self.id_paciente = id_paciente
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.telefono = telefono
        self.activo = activo
        self.id_usuario = id_usuario
        
    
    
    def activar(self):
        if self.activo:
            raise ValueError("El paciente ya está activo.")
        self.activo = True
        
    def desactivar(self):
        if not self.activo:
            raise ValueError("El paciente ya está inactivo.")
        self.activo = False
        