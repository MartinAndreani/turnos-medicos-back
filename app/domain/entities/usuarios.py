# app/domain/entities/usuarios.py

from typing import Optional


class Usuario:
    def __init__(
        self,
        id_usuario: str,
        email: str,
        password: str,
        activo: bool = True,
    ):
        self.id_usuario = id_usuario
        self.email = email
        self.password = password
        self.activo = activo

    # ====== REGLAS DE NEGOCIO ======

    def activar(self):
        if self.activo:
            raise ValueError("El usuario ya está activo.")
        self.activo = True

    def desactivar(self):
        if not self.activo:
            raise ValueError("El usuario ya está inactivo.")
        self.activo = False

    def actualizar_datos(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        activo: Optional[bool] = None,
    ):
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password
        if activo is not None:
            self.activo = activo
