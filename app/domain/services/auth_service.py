# app/domain/services/auth_service.py

from app.db.repositories.usuario_repository import UsuarioRepository
from app.domain.entities.usuarios import Usuario
from app.core.security import verify_password


class AuthService:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo

    def authenticate(self, email: str, password: str) -> Usuario:
        """
        Valida las credenciales del usuario.
        Lanza ValueError si son inválidas.
        """
        usuario = self.usuario_repo.get_by_email(email)
        if not usuario or not usuario.activo:
            # No exponemos si el mail existe o no
            raise ValueError("Credenciales inválidas.")

        if not verify_password(password, usuario.password):
            raise ValueError("Credenciales inválidas.")

        return usuario
