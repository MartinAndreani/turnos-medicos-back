# app/api/dependencies/roles.py

from fastapi import Depends, HTTPException, status
from app.api.dependencies.auth import get_current_user
from app.domain.entities.usuarios import Usuario
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db.repositories.rol_x_usuario_repository import RolXUsuarioRepository


def require_role(role_name: str):
    """
    Verifica que el usuario tenga un rol específico.
    Devuelve una dependencia que se puede usar con Depends().
    """
    def dependency(
        current_user: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        rxu = RolXUsuarioRepository(db)
        roles = rxu.list_roles_for_user(current_user.id_usuario)
        nombres = [r.nombre for r in roles]

        if role_name not in nombres:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere el rol '{role_name}' para acceder a este recurso."
            )

        return current_user

    return dependency


def require_admin(
    current_user: Usuario = Depends(require_role("ADMIN"))
):
    """
    Convenience dependency:
    require_role("ADMIN") ya hace todo.
    """
    return current_user
