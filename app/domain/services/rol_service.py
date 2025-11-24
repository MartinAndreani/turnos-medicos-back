# app/domain/services/rol_service.py

from uuid import uuid4
from app.domain.entities.roles import Rol
from app.db.repositories.rol_repository import RolRepository
from app.api.schemas.roles import RolCreate, RolUpdate


class RolService:
    def __init__(self, repo: RolRepository):
        self.repo = repo

    def create(self, dto: RolCreate) -> Rol:
        if self.repo.get_by_nombre(dto.nombre):
            raise ValueError("Ya existe un rol con ese nombre.")

        rol = Rol(
            id_rol=str(uuid4()),
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            activo=True,
        )

        return self.repo.save(rol)

    def update(self, id_rol: str, dto: RolUpdate) -> Rol:
        rol = self.repo.get_by_id(id_rol)
        if not rol:
            raise ValueError("Rol no encontrado.")

        rol.actualizar(
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            activo=dto.activo,
        )

        return self.repo.save(rol)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip=skip, limit=limit)

    def get(self, id_rol: str) -> Rol | None:
        return self.repo.get_by_id(id_rol)
