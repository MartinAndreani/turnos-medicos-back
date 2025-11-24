# app/domain/entities/roles.py

class Rol:
    def __init__(
        self,
        id_rol: str,
        nombre: str,
        descripcion: str | None = None,
        activo: bool = True,
    ):
        self.id_rol = id_rol
        self.nombre = nombre
        self.descripcion = descripcion
        self.activo = activo

    def activar(self):
        if self.activo:
            raise ValueError("El rol ya está activo.")
        self.activo = True

    def desactivar(self):
        if not self.activo:
            raise ValueError("El rol ya está inactivo.")
        self.activo = False

    def actualizar(
        self,
        nombre: str | None = None,
        descripcion: str | None = None,
        activo: bool | None = None,
    ):
        if nombre is not None:
            self.nombre = nombre
        if descripcion is not None:
            self.descripcion = descripcion
        if activo is not None:
            self.activo = activo
