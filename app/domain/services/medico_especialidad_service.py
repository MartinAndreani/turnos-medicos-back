# app/domain/services/medico_especialidad_service.py

from typing import List

from app.db.repositories.medico_especialidad_repository import MedicoEspecialidadRepository
from app.db.repositories.medico_repository import MedicoRepository
from app.db.repositories.especialidad_repository import EspecialidadRepository
from app.domain.entities.especialidades import Especialidad


class MedicoEspecialidadService:
    def __init__(
        self,
        me_repo: MedicoEspecialidadRepository,
        medico_repo: MedicoRepository,
        especialidad_repo: EspecialidadRepository,
    ):
        self.me_repo = me_repo
        self.medico_repo = medico_repo
        self.especialidad_repo = especialidad_repo

    # Asignar una especialidad a un médico
    def asignar(self, id_medico: str, id_especialidad: str) -> Especialidad:
        medico = self.medico_repo.get_by_id(id_medico)
        if not medico or not medico.activo:
            raise ValueError("El médico no existe o está inactivo.")

        especialidad = self.especialidad_repo.get_by_id(id_especialidad)
        if not especialidad or not especialidad.activo:
            raise ValueError("La especialidad no existe o está inactiva.")

        if self.me_repo.exists(id_medico, id_especialidad):
            raise ValueError("La especialidad ya está asignada a este médico.")

        self.me_repo.add(id_medico, id_especialidad)
        return especialidad

    # Quitar una especialidad de un médico
    def quitar(self, id_medico: str, id_especialidad: str) -> None:
        medico = self.medico_repo.get_by_id(id_medico)
        if not medico:
            raise ValueError("Médico no encontrado.")

        especialidad = self.especialidad_repo.get_by_id(id_especialidad)
        if not especialidad:
            raise ValueError("Especialidad no encontrada.")

        ok = self.me_repo.remove(id_medico, id_especialidad)
        if not ok:
            raise ValueError("La especialidad no estaba asignada a este médico.")

    # Listar especialidades de un médico
    def listar_especialidades(self, id_medico: str) -> List[Especialidad]:
        medico = self.medico_repo.get_by_id(id_medico)
        if not medico:
            raise ValueError("Médico no encontrado.")

        return self.me_repo.list_especialidades_por_medico(id_medico)
