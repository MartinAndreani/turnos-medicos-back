# app/domain/services/medico_service.py

from uuid import uuid4
from typing import Optional, List

from app.db.repositories.medico_repository import MedicoRepository
from app.domain.entities.medicos import Medico


class MedicoService:
    def __init__(self, repo: MedicoRepository):
        self.repo = repo

    # =======================
    #   ALTA (CREATE)
    # =======================
    def create(self, dto) -> Medico:
        """
        Crea un médico nuevo a partir de un DTO de entrada.
        Reglas de negocio:
        - El DNI no puede repetirse.
        - La matrícula no puede repetirse.
        """
        # Validación de unicidad de DNI
        if self.repo.get_by_dni(dto.dni):
            raise ValueError("DNI ya registrado")

        # Validación de unicidad de matrícula
        if self.repo.get_by_matricula(dto.matricula):
            raise ValueError("Matrícula ya registrada")

        medico = Medico(
            id_medico=str(uuid4()),
            matricula=dto.matricula,
            dni=dto.dni,
            nombre=dto.nombre,
            apellido=dto.apellido,
            telefono=getattr(dto, "telefono", None),
            activo=True,
        )

        return self.repo.save(medico)

    # =======================
    #   MODIFICACIÓN (UPDATE)
    # =======================
    def update(self, id_medico: str, dto) -> Medico:
        """
        Actualiza parcialmente un médico existente.
        Solo modifica los campos presentes en el DTO.
        Además valida:
        - Cambio de DNI: no debe quedar duplicado.
        - Cambio de matrícula: no debe quedar duplicada.
        """
        medico = self.repo.get_by_id(id_medico)
        if not medico:
            raise ValueError("No existe médico")

        # Si se envía DNI y cambia, validar unicidad
        if hasattr(dto, "dni") and dto.dni is not None and dto.dni != medico.dni:
            existente = self.repo.get_by_dni(dto.dni)
            if existente and existente.id_medico != medico.id_medico:
                raise ValueError("DNI ya registrado para otro médico")
            medico.dni = dto.dni

        # Si se envía matrícula y cambia, validar unicidad
        if hasattr(dto, "matricula") and dto.matricula is not None and dto.matricula != medico.matricula:
            existente = self.repo.get_by_matricula(dto.matricula)
            if existente and existente.id_medico != medico.id_medico:
                raise ValueError("Matrícula ya registrada para otro médico")
            medico.matricula = dto.matricula

        # Campos simples
        if hasattr(dto, "nombre") and dto.nombre is not None:
            medico.nombre = dto.nombre

        if hasattr(dto, "apellido") and dto.apellido is not None:
            medico.apellido = dto.apellido

        if hasattr(dto, "telefono") and dto.telefono is not None:
            medico.telefono = dto.telefono

        if hasattr(dto, "activo") and dto.activo is not None:
            medico.activo = dto.activo

        

        return self.repo.save(medico)

    # =======================
    #   BAJA (DELETE / SOFT)
    # =======================
    def delete(self, id_medico: str) -> bool:
        """
        Baja lógica del médico (soft delete).
        Implementación delegada al repositorio (activo=False).
        """
        return self.repo.delete(id_medico)

    # =======================
    #   CONSULTAS (READ)
    # =======================
    def get(self, id_medico: str) -> Optional[Medico]:
        """
        Obtiene un médico por ID. Devuelve None si no existe.
        """
        return self.repo.get_by_id(id_medico)

    def list(self, skip: int = 0, limit: int = 100) -> List[Medico]:
        """
        Lista médicos activos, paginados.
        """
        return self.repo.list(skip=skip, limit=limit)

    # =======================
    #   OPERACIONES DE ESTADO
    # =======================
    def activar(self, id_medico: str) -> Medico:
        """
        Usa la lógica de dominio (método activar del Medico)
        y persiste el cambio.
        """
        medico = self.repo.get_by_id(id_medico)
        if not medico:
            raise ValueError("No existe médico")

        medico.activar()
        return self.repo.save(medico)
    