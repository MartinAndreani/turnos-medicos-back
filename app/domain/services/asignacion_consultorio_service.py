from uuid import uuid4
from app.db.repositories.asignacion_consultorio_repository import AsignacionConsultorioRepository
from app.db.repositories.medico_repository import MedicoRepository
from app.db.repositories.consultorio_repository import ConsultorioRepository
# Asegúrate de importar tu DTO actualizado si usas type hinting

class AsignacionConsultorioService:
    def __init__(self, repo: AsignacionConsultorioRepository, repo_medico: MedicoRepository, repo_consultorio: ConsultorioRepository):
        self.repo = repo
        self.repo_medico = repo_medico
        self.repo_consultorio = repo_consultorio
   
    def create(self, dto):
        # 1. Validar existencias
        if not self.repo_medico.get_by_id(str(dto.id_medico)):
            raise ValueError("El médico no existe")

        if not self.repo_consultorio.get_by_id(str(dto.id_consultorio)):
            raise ValueError("El consultorio no existe")

        if dto.fecha_inicio > dto.fecha_fin:
            raise ValueError("La fecha de inicio no puede ser mayor que la fecha de fin")

        # 2. Validar OVERLAP (Enviamos los 6 parámetros necesarios)
        overlap = self.repo.get_overlap(
            dto.id_consultorio, 
            dto.jornada, 
            dto.dia_semana,   # Nuevo campo del DTO
            dto.hora_inicio,  # Nuevo campo del DTO
            dto.hora_fin,     # Nuevo campo del DTO
            dto.fecha_inicio, 
            dto.fecha_fin
        )
        if overlap:
            raise ValueError("El consultorio ya está asignado en ese horario, día y rango de fechas")

        # 3. Crear diccionario con TODOS los datos
        asignacion_data = {
            "id_asignacion": uuid4(),
            "id_medico": dto.id_medico,
            "id_consultorio": dto.id_consultorio,
            "fecha_inicio": dto.fecha_inicio,
            "fecha_fin": dto.fecha_fin,
            "dia_semana": dto.dia_semana, 
            "hora_inicio": dto.hora_inicio,
            "hora_fin": dto.hora_fin,
            "jornada": dto.jornada,
            "activo": True
        }

        return self.repo.create(asignacion_data)

    def get(self, id_asignacion):
        return self.repo.get_by_id(id_asignacion)

    def list(self, skip=0, limit=100):
        # Asegúrate de tener el método list en tu repositorio o ajusta esto
        # return self.repo.list(skip, limit)
        pass 

    def update(self, id_asignacion, dto):
        # Implementar lógica de update similar al create validando overlap
        pass

    def delete(self, id_asignacion):
        return self.repo.delete(id_asignacion)