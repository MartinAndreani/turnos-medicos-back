# app/domain/services/turno_service.py

from uuid import uuid4
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.db.repositories.turno_repository import TurnoRepository
from app.domain.entities.turnos import Turno


# Función auxiliar para convertir strings ISO a datetime
def _parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except Exception:
        raise ValueError(f"Formato de fecha inválido: {value}")


class TurnoService:
    def __init__(self, repo: TurnoRepository):
        self.repo = repo

    # ========================================================
    # CREATE
    # ========================================================
    def create(self, data: Dict[str, Any]) -> Turno:
        required = [
            "id_paciente",
            "id_medico",
            "id_consultorio",
            "fecha_hora_inicio",
            "fecha_hora_fin",
        ]

        for campo in required:
            if campo not in data:
                raise ValueError(f"Falta el campo requerido: {campo}")

        inicio = _parse_datetime(data["fecha_hora_inicio"])
        fin = _parse_datetime(data["fecha_hora_fin"])

        if fin <= inicio:
            raise ValueError("fecha_hora_fin debe ser mayor que fecha_hora_inicio.")

        turno = Turno(
            id_turno=str(uuid4()),
            id_paciente=data["id_paciente"],
            id_medico=data["id_medico"],
            id_consultorio=data["id_consultorio"],
            fecha_hora_inicio=inicio,
            fecha_hora_fin=fin,
            id_estado=data.get("id_estado", "PENDIENTE"),
            motivo_consulta=data.get("motivo_consulta"),
        )

        # Médico ocupado en ese horario
        if self.repo.hay_superposicion_medico(
            turno.id_medico,
            inicio,
            fin
        ):
            raise ValueError("El médico ya tiene un turno en ese horario.")

        # Consultorio ocupado en ese horario
        if self.repo.hay_superposicion_consultorio(
            turno.id_consultorio,
            inicio,
            fin
        ):
            raise ValueError("El consultorio ya está ocupado en ese horario.")

        return self.repo.save(turno)

    # ========================================================
    # UPDATE
    # ========================================================
    def update(self, id_turno: str, data: Dict[str, Any]) -> Turno:
        turno = self.repo.get_by_id(id_turno)
        if not turno:
            raise ValueError("No existe turno")

        # Campos simples
        if "id_paciente" in data and data["id_paciente"] is not None:
            turno.id_paciente = data["id_paciente"]

        if "id_medico" in data and data["id_medico"] is not None:
            turno.id_medico = data["id_medico"]

        if "id_consultorio" in data and data["id_consultorio"] is not None:
            turno.id_consultorio = data["id_consultorio"]

        if "motivo_consulta" in data:
            turno.motivo_consulta = data["motivo_consulta"]

        # Fechas
        if "fecha_hora_inicio" in data and data["fecha_hora_inicio"] is not None:
            turno.fecha_hora_inicio = _parse_datetime(data["fecha_hora_inicio"])

        if "fecha_hora_fin" in data and data["fecha_hora_fin"] is not None:
            turno.fecha_hora_fin = _parse_datetime(data["fecha_hora_fin"])

        if turno.fecha_hora_fin <= turno.fecha_hora_inicio:
            raise ValueError("fecha_hora_fin debe ser mayor que fecha_hora_inicio.")

        # Estado
        if "id_estado" in data and data["id_estado"] is not None:
            turno.id_estado = data["id_estado"]


        # ===== VALIDACIÓN DE SUPERPOSICIÓN =====

        if self.repo.hay_superposicion_medico(
            turno.id_medico,
            turno.fecha_hora_inicio,
            turno.fecha_hora_fin,
            excluir_id=id_turno
        ):
            raise ValueError("El médico ya tiene un turno en ese horario.")

        if self.repo.hay_superposicion_consultorio(
            turno.id_consultorio,
            turno.fecha_hora_inicio,
            turno.fecha_hora_fin,
            excluir_id=id_turno
        ):
            raise ValueError("El consultorio ya está ocupado en ese horario.")

        return self.repo.save(turno)

    # ========================================================
    # DELETE → CANCELA EL TURNO (BAJA LÓGICA)
    # ========================================================
    def delete(self, id_turno: str) -> bool:
        turno = self.repo.get_by_id(id_turno)
        if not turno:
            return False

        # Baja lógica → CANCELADO
        turno.cancelar()
        self.repo.save(turno)
        return True

    # ========================================================
    # GET
    # ========================================================
    def get(self, id_turno: str) -> Optional[Turno]:
        return self.repo.get_by_id(id_turno)

    # ========================================================
    # LIST
    # ========================================================
    def list(self, skip: int = 0, limit: int = 100) -> List[Turno]:
        return self.repo.list(skip=skip, limit=limit)

    # ========================================================
    # LIST POR MÉDICO
    # ========================================================
    def list_by_medico(self, id_medico: str, skip: int = 0, limit: int = 100) -> List[Turno]:
        return self.repo.list_by_medico(id_medico, skip=skip, limit=limit)

    # ========================================================
    # LIST POR PACIENTE
    # ========================================================
    def list_by_paciente(self, id_paciente: str, skip: int = 0, limit: int = 100) -> List[Turno]:
        return self.repo.list_by_paciente(id_paciente, skip=skip, limit=limit)
