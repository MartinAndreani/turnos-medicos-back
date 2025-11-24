# app/domain/services/receta_service.py

from uuid import uuid4
from datetime import date
from typing import List, Optional

from app.db.repositories.receta_repository import RecetaRepository
from app.db.repositories.turno_repository import TurnoRepository
from app.domain.entities.recetas import Receta
from app.api.schemas.recetas import RecetaCreate, RecetaUpdate


class RecetaService:
    def __init__(self, receta_repo: RecetaRepository, turno_repo: TurnoRepository):
        self.receta_repo = receta_repo
        self.turno_repo = turno_repo

    # =============== CREATE ===================
    def create(self, dto: RecetaCreate) -> Receta:
        # 1) turno debe existir
        turno = self.turno_repo.get_by_id(str(dto.id_turno))
        if not turno:
            raise ValueError("El turno asociado a la receta no existe.")

        # 2) estado del turno debe ser válido
        if turno.id_estado not in ("CONFIRMADO", "FINALIZADO"):
            raise ValueError(
                "Solo se pueden emitir recetas para turnos confirmados o finalizados."
            )

        # 3) solo una receta activa por turno
        existente = self.receta_repo.get_by_turno(str(dto.id_turno))
        if existente:
            raise ValueError("Ya existe una receta para este turno.")

        # 4) debe haber medicamentos o descripción
        if not dto.medicamentos and not dto.descripcion:
            raise ValueError(
                "La receta debe incluir al menos medicamentos o una descripción."
            )

        receta = Receta(
            id_receta=uuid4(),
            id_turno=dto.id_turno,
            fecha_emision=date.today(),
            medicamentos=dto.medicamentos,
            descripcion=dto.descripcion,
            activo=True,
        )

        return self.receta_repo.save(receta)

    # =============== UPDATE ===================
    def update(self, id_receta: str, dto: RecetaUpdate) -> Receta:
        receta = self.receta_repo.get_by_id(id_receta)
        if not receta:
            raise ValueError("No existe la receta.")

        if dto.medicamentos is not None:
            receta.medicamentos = dto.medicamentos

        if dto.descripcion is not None:
            receta.descripcion = dto.descripcion

        if dto.activo is not None:
            receta.activo = dto.activo

        # Validación: no dejar receta vacía
        if not receta.medicamentos and not receta.descripcion:
            raise ValueError(
                "La receta no puede quedar sin medicamentos ni descripción."
            )

        return self.receta_repo.save(receta)

    # =============== DELETE (BAJA LÓGICA) =====
    def delete(self, id_receta: str) -> bool:
        return self.receta_repo.delete(id_receta)

    # =============== GET ======================
    def get(self, id_receta: str) -> Optional[Receta]:
        return self.receta_repo.get_by_id(id_receta)

    # =============== LIST =====================
    def list(self, skip: int = 0, limit: int = 100) -> List[Receta]:
        return self.receta_repo.list(skip=skip, limit=limit)

    # =============== LIST BY TURNO ============
    def list_by_turno(self, id_turno: str) -> List[Receta]:
        return self.receta_repo.list_by_turno(id_turno)
