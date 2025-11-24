# app/domain/services/historia_clinica_service.py

from uuid import uuid4
from typing import List, Optional

from app.domain.entities.historias_clinicas import HistoriaClinica
from app.api.schemas.historias_clinicas import (
    HistoriaClinicaCreate,
    HistoriaClinicaUpdate,
)
from app.db.repositories.historia_clinica_repository import HistoriaClinicaRepository
from app.db.repositories.paciente_repository import PacienteRepository
from app.db.repositories.medico_repository import MedicoRepository
from app.db.repositories.turno_repository import TurnoRepository


class HistoriaClinicaService:
    def __init__(
        self,
        hc_repo: HistoriaClinicaRepository,
        paciente_repo: PacienteRepository,
        medico_repo: MedicoRepository,
        turno_repo: TurnoRepository,
    ):
        self.hc_repo = hc_repo
        self.paciente_repo = paciente_repo
        self.medico_repo = medico_repo
        self.turno_repo = turno_repo

    # ========== CREATE ==========

    def create(self, dto: HistoriaClinicaCreate) -> HistoriaClinica:
        id_paciente_str = str(dto.id_paciente)
        id_medico_str = str(dto.id_medico)
        id_turno_str = str(dto.id_turno) if dto.id_turno is not None else None

        # 1) Paciente debe existir y estar activo
        paciente = self.paciente_repo.get_by_id(id_paciente_str)
        if not paciente or not getattr(paciente, "activo", True):
            raise ValueError("El paciente no existe o está inactivo.")

        # 2) Médico debe existir y estar activo
        medico = self.medico_repo.get_by_id(id_medico_str)
        if not medico or not getattr(medico, "activo", True):
            raise ValueError("El médico no existe o está inactivo.")

        # 3) Si hay turno asociado, deben cumplirse reglas extra
        if id_turno_str is not None:
            turno = self.turno_repo.get_by_id(id_turno_str)
            if not turno or not getattr(turno, "activo", True):
                raise ValueError("El turno asociado a la historia clínica no existe o está inactivo.")

            # 3.a) El turno debe pertenecer al mismo paciente
            if str(getattr(turno, "id_paciente", "")) != id_paciente_str:
                raise ValueError("El turno no pertenece al mismo paciente.")

            # 3.b) El turno debe pertenecer al mismo médico
            if str(getattr(turno, "id_medico", "")) != id_medico_str:
                raise ValueError("El turno no pertenece al mismo médico.")

            # 3.c) Si el turno tiene estado, debe estar finalizado/atendido
            estado = getattr(turno, "estado", None)
            if estado is not None and estado not in ("Finalizado", "Atendido"):
                raise ValueError("El turno aún no está finalizado/atendido.")

            # 3.d) Diagnóstico y tratamiento obligatorios si hay turno
            if not dto.diagnostico or not dto.tratamiento:
                raise ValueError(
                    "Si la historia clínica se asocia a un turno, diagnóstico y tratamiento son obligatorios."
                )

        # Crear entidad de dominio
        hc = HistoriaClinica(
            id_historia_clinica=str(uuid4()),
            id_paciente=id_paciente_str,
            id_medico=id_medico_str,
            id_turno=id_turno_str,
            fecha_registro=None,  # la pone el modelo/DB (default DateTime)
            diagnostico=dto.diagnostico,
            tratamiento=dto.tratamiento,
            observaciones=dto.observaciones,
            activo=True,
        )

        return self.hc_repo.save(hc)

    # ========== UPDATE ==========

    def update(self, id_historia_clinica: str, dto: HistoriaClinicaUpdate) -> HistoriaClinica:
        hc = self.hc_repo.get_by_id(id_historia_clinica)
        if not hc:
            raise ValueError("Historia clínica no encontrada.")

        # No se permite cambiar paciente, médico ni turno.
        # Solo contenido y activo.
        hc.actualizar_contenido(
            diagnostico=dto.diagnostico,
            tratamiento=dto.tratamiento,
            observaciones=dto.observaciones,
            activo=dto.activo,
        )

        # Regla adicional: si tiene turno asociado y está activa,
        # se mantiene la obligación de tener diagnóstico y tratamiento.
        if hc.id_turno is not None and hc.activo:
            if not hc.diagnostico or not hc.tratamiento:
                raise ValueError(
                    "Historias clínicas asociadas a un turno deben tener diagnóstico y tratamiento."
                )

        return self.hc_repo.save(hc)

    # ========== DELETE (BAJA LÓGICA) ==========

    def delete(self, id_historia_clinica: str) -> bool:
        return self.hc_repo.delete(id_historia_clinica)

    # ========== GET/LIST ==========

    def get(self, id_historia_clinica: str) -> Optional[HistoriaClinica]:
        return self.hc_repo.get_by_id(id_historia_clinica)

    def list(self, skip: int = 0, limit: int = 100) -> List[HistoriaClinica]:
        return self.hc_repo.list(skip=skip, limit=limit)

    def list_by_paciente(
        self, id_paciente: str, skip: int = 0, limit: int = 100
    ) -> List[HistoriaClinica]:
        return self.hc_repo.list_by_paciente(id_paciente, skip=skip, limit=limit)
