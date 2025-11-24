# app/domain/services/paciente_service.py
from app.db.repositories.paciente_repository import PacienteRepository
from app.domain.entities.pacientes import Paciente
from uuid import uuid4

class PacienteService:
    def __init__(self, repo: PacienteRepository):
        self.repo = repo

    def create(self, dto) -> Paciente:
        # validaciones de negocio
        if self.repo.get_by_dni(dto.dni):
            raise ValueError("DNI ya registrado")
        paciente = Paciente(
            id_paciente=str(uuid4()),
            dni=dto.dni,
            nombre=dto.nombre,
            apellido=dto.apellido,
            fecha_nacimiento=dto.fecha_nacimiento,
            direccion=dto.direccion,
            telefono=dto.telefono,
            activo=True
        )
        return self.repo.save(paciente)

    def update(self, id_paciente: str, dto) -> Paciente:
        paciente = self.repo.get_by_id(id_paciente)
        if not paciente:
            raise ValueError("No existe paciente")
        # aplicar cambios permitidos
        if dto.nombre is not None:
            paciente.nombre = dto.nombre
        if dto.apellido is not None:
            paciente.apellido = dto.apellido
        if dto.fecha_nacimiento is not None:
            paciente.fecha_nacimiento = dto.fecha_nacimiento
        if dto.direccion is not None:
            paciente.direccion = dto.direccion
        if dto.telefono is not None:
            paciente.telefono = dto.telefono
        if dto.activo is not None:
            paciente.activo = dto.activo
        return self.repo.save(paciente)

    def delete(self, id_paciente: str) -> bool:
        if not self.repo.get_by_id(id_paciente):
            raise ValueError("No existe paciente")
        return self.repo.delete(id_paciente)

    def list(self, skip=0, limit=100):
        return self.repo.list(skip=skip, limit=limit)
