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
            dto.dias_semana,   # Nuevo campo del DTO
            dto.hora_inicio,  # Nuevo campo del DTO
            dto.hora_fin,     # Nuevo campo del DTO
            dto.fecha_inicio, 
            dto.fecha_fin,
            dto.jornada
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
            "dias_semana": dto.dias_semana, 
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
        return self.repo.list(skip, limit)
        

    def update(self, id_asignacion, dto):
        # 1. Obtener la asignación actual
        asignacion_actual = self.repo.get_by_id(id_asignacion)
        if not asignacion_actual:
            raise ValueError("La asignación no existe")

        # 2. Crear un diccionario con los valores actuales
        data_actual = {
            "id_asignacion": asignacion_actual.id_asignacion,
            "id_medico": asignacion_actual.id_medico,
            "id_consultorio": asignacion_actual.id_consultorio,
            "fecha_inicio": asignacion_actual.fecha_inicio,
            "fecha_fin": asignacion_actual.fecha_fin,
            "dias_semana": asignacion_actual.dias_semana,
            "hora_inicio": asignacion_actual.hora_inicio,
            "hora_fin": asignacion_actual.hora_fin,
            "jornada": asignacion_actual.jornada,
            "activo": asignacion_actual.activo
        }

        # 3. Aplicar solo los cambios enviados en el DTO
        dto_dict = dto.dict(exclude_unset=True)

        for key, val in dto_dict.items():
            data_actual[key] = val

        # 4. Validar fechas
        if data_actual["fecha_inicio"] > data_actual["fecha_fin"]:
            raise ValueError("La fecha de inicio no puede ser mayor que la fecha de fin")

        # 5. Buscar overlap, ignorando la asignación actual
        overlap = self.repo.get_overlap_update(
            id_consultorio=data_actual["id_consultorio"],
            dias_nuevos=data_actual["dias_semana"],
            hora_inicio=data_actual["hora_inicio"],
            hora_fin=data_actual["hora_fin"],
            fecha_inicio=data_actual["fecha_inicio"],
            fecha_fin=data_actual["fecha_fin"],
            jornada=data_actual["jornada"],
            id_excluir=id_asignacion
        )

        if overlap:
            raise ValueError("El consultorio ya está asignado en ese horario, día y rango de fechas")

        # 6. Guardar cambios
        return self.repo.update(id_asignacion, data_actual)


    def delete(self, id_asignacion):
        return self.repo.delete(id_asignacion)