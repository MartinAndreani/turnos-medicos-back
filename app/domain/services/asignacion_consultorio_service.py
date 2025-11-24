# app/domain/services/asignacion_consultorio_service.py

from uuid import uuid4
from app.db.repositories.asignacion_consultorio_repository import AsignacionConsultorioRepository
from app.db.repositories.medico_repository import MedicoRepository
from app.db.repositories.consultorio_repository import ConsultorioRepository
from app.db.models.asignacion_consultorios import AsignacionConsultorioModel


class AsignacionConsultorioService:
    def __init__(self, repo: AsignacionConsultorioRepository, repo_medico: MedicoRepository, repo_consultorio: ConsultorioRepository):
        self.repo = repo
        self.repo_medico = repo_medico
        self.repo_consultorio = repo_consultorio

   
    def create(self, dto):
        # Validar médico
        if not self.repo_medico.get_by_id(dto.id_medico):
            raise ValueError("El médico no existe")

        # Validar consultorio
        if not self.repo_consultorio.get_by_id(dto.id_consultorio):
            raise ValueError("El consultorio no existe")

        # Validación de rango de fechas
        if dto.fecha_inicio > dto.fecha_fin:
            raise ValueError("La fecha de inicio no puede ser mayor que la fecha de fin")

        # Validar que el consultorio NO esté ocupado
        overlap = self.repo.get_overlap(dto.id_consultorio, dto.jornada, dto.fecha_inicio, dto.fecha_fin)
        if overlap:
            raise ValueError("El consultorio ya está asignado en esa jornada y rango de fechas")

        # Validar que el médico NO tenga dos consultorios a la vez
        overlap_medico = self.repo.get_overlap_medico(
            dto.id_medico,
            dto.jornada,
            dto.fecha_inicio,
            dto.fecha_fin
        )
        if overlap_medico:
            raise ValueError("El médico ya tiene un consultorio asignado en ese rango y jornada")

        # Crear asignación
        asignacion = AsignacionConsultorioModel(
            id_asignacion=uuid4(),
            id_medico=dto.id_medico,
            id_consultorio=dto.id_consultorio,
            fecha_inicio=dto.fecha_inicio,
            fecha_fin=dto.fecha_fin,
            jornada=dto.jornada,
            activo=True,
        )

        return self.repo.save(asignacion)

    def update(self, id_asignacion, dto):
        asignacion = self.repo.get_by_id(id_asignacion)
        if not asignacion:
            raise ValueError("No existe asignación")

        # Nuevos valores aplicados (fallback a los actuales)
        new_inicio = dto.fecha_inicio or asignacion.fecha_inicio
        new_fin = dto.fecha_fin or asignacion.fecha_fin
        new_jornada = dto.jornada or asignacion.jornada
        new_medico = dto.id_medico or asignacion.id_medico

        if new_inicio > new_fin:
            raise ValueError("Rango de fechas inválido")

        # =============================
        # Validar consultorio ocupado
        # =============================
        overlap = self.repo.get_overlap(
            asignacion.id_consultorio,
            new_jornada,
            new_inicio,
            new_fin,
        )

        if overlap and overlap.id_asignacion != asignacion.id_asignacion:
            raise ValueError("El consultorio ya tiene asignación en ese rango")

        # =============================
        # Validar médico ocupado
        # =============================
        overlap_medico = self.repo.get_overlap_medico(
            new_medico,
            new_jornada,
            new_inicio,
            new_fin
        )

        if overlap_medico and overlap_medico.id_asignacion != asignacion.id_asignacion:
            raise ValueError("El médico ya tiene un consultorio asignado en ese rango y jornada")

        # Guardar cambios
        asignacion.fecha_inicio = new_inicio
        asignacion.fecha_fin = new_fin
        asignacion.jornada = new_jornada
        
        if dto.id_medico:
            asignacion.id_medico = dto.id_medico

        if dto.activo is not None:
            asignacion.activo = dto.activo

        return self.repo.save(asignacion)


    def delete(self, id_asignacion):
        return self.repo.delete(id_asignacion)


    def get(self, id_asignacion):
        return self.repo.get_by_id(id_asignacion)

    def list(self, skip=0, limit=100):
        return self.repo.list(skip=skip, limit=limit)
