# app/domain/services/usuario_service.py

from uuid import uuid4
from typing import Optional, List

from app.domain.entities.usuarios import Usuario
from app.db.repositories.usuario_repository import UsuarioRepository
from app.db.repositories.rol_repository import RolRepository
from app.db.repositories.rol_x_usuario_repository import RolXUsuarioRepository
from app.api.schemas.usuarios import UsuarioCreate, UsuarioUpdate
from app.core.security import hash_password


class UsuarioService:
    def __init__(
        self,
        usuario_repo: UsuarioRepository,
        rol_repo: RolRepository,
        rxu_repo: RolXUsuarioRepository,
    ):
        self.usuario_repo = usuario_repo
        self.rol_repo = rol_repo
        self.rxu_repo = rxu_repo

    # ========== CREATE ==========

    def create(self, dto: UsuarioCreate) -> Usuario:
        # email único
        if self.usuario_repo.get_by_email(dto.email):
            raise ValueError("Ya existe un usuario con ese email.")

        # hashear password
        hashed = hash_password(dto.password)

        usuario = Usuario(
            id_usuario=str(uuid4()),
            email=dto.email,
            password=hashed,
            activo=True,
        )

        usuario = self.usuario_repo.save(usuario)

        # asignación de roles por IDs (opción B)
        if dto.roles_ids:
            self._set_roles_for_user(usuario.id_usuario, dto.roles_ids)

        return usuario

    # ========== UPDATE ==========

    def update(self, id_usuario: str, dto: UsuarioUpdate) -> Usuario:
        usuario = self.usuario_repo.get_by_id(id_usuario)
        if not usuario:
            raise ValueError("Usuario no encontrado.")

        # actualizar campos
        new_password = None
        if dto.password is not None:
            new_password = hash_password(dto.password)

        usuario.actualizar_datos(
            email=dto.email,
            password=new_password,
            activo=dto.activo,
        )

        usuario = self.usuario_repo.save(usuario)

        # si mandan roles_ids, REEMPLAZAMOS todas las asignaciones previas
        if dto.roles_ids is not None:
            self._set_roles_for_user(usuario.id_usuario, dto.roles_ids)

        return usuario

    # ========== DELETE (BAJA LÓGICA) ==========

    def delete(self, id_usuario: str) -> bool:
        return self.usuario_repo.delete(id_usuario)

    # ========== GET & LIST ==========

    def get(self, id_usuario: str) -> Optional[Usuario]:
        return self.usuario_repo.get_by_id(id_usuario)

    def list(self, skip: int = 0, limit: int = 100) -> list[Usuario]:
        return self.usuario_repo.list(skip=skip, limit=limit)

    # ========== HELPER P/ROLES ==========

    def _set_roles_for_user(self, id_usuario: str, roles_ids: List[str]) -> None:
        # valida que todos existan y estén activos
        for id_rol in roles_ids:
            rol = self.rol_repo.get_by_id(str(id_rol))
            if not rol or not rol.activo:
                raise ValueError(f"Rol inválido o inactivo: {id_rol}")

        # borra asignaciones previas
        self.rxu_repo.remove_all_for_user(id_usuario)

        # crea las nuevas
        for id_rol in roles_ids:
            self.rxu_repo.add(id_usuario, str(id_rol))
