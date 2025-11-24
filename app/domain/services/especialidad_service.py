from uuid import uuid4
from app.db.repositories.especialidad_repository import EspecialidadRepository
from app.domain.entities.especialidades import Especialidad
from app.api.schemas.especialidades import EspecialidadCreate, EspecialidadUpdate


class EspecialidadService:
    def __init__(self, repo: EspecialidadRepository):
        self.repo = repo

    # CREATE
    def create(self, dto: EspecialidadCreate):
        if self.repo.get_by_nombre(dto.nombre):
            raise ValueError("Ya existe una especialidad con ese nombre.")

        esp = Especialidad(
            id_especialidad=uuid4(),
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            activo=True
        )
        return self.repo.save(esp)

    # UPDATE
    def update(self, id_especialidad: str, dto: EspecialidadUpdate):
        esp = self.repo.get_by_id(id_especialidad)
        if not esp:
            raise ValueError("Especialidad no encontrada.")

        # Reglas
        if dto.nombre is not None:
            esp.nombre = dto.nombre
        if dto.descripcion is not None:
            esp.descripcion = dto.descripcion
        if dto.activo is not None:
            esp.activo = dto.activo

        return self.repo.save(esp)

    # DELETE (baja lógica)
    def delete(self, id_especialidad: str):
        return self.repo.delete(id_especialidad)

    # LIST & GET
    def list(self, skip=0, limit=100):
        return self.repo.list(skip=skip, limit=limit)

    def get(self, id_especialidad: str):
        return self.repo.get_by_id(id_especialidad)
