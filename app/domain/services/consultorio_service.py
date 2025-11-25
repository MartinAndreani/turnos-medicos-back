from uuid import uuid4
from app.db.repositories.consultorio_repository import ConsultorioRepository
from app.domain.entities.consultorios import Consultorio

class ConsultorioService:
    def __init__(self, repo: ConsultorioRepository):
        self.repo = repo
        
    def create(self, dto) -> Consultorio:
        # 1. ELIMINAMOS LA VALIDACIÓN POR ID (El DTO no tiene ID todavía)
        # Si quieres validar duplicados, tendrías que tener un método en el repo como:
        # if self.repo.get_by_numero_y_piso(dto.numero_consultorio, dto.piso):
        #     raise ValueError("Ya existe un consultorio con ese número en ese piso")

        # 2. Creamos la entidad generando el ID aquí
        consultorio = Consultorio(
            id_consultorio=str(uuid4()),  # Generamos el ID nuevo
            numero_consultorio=dto.numero_consultorio,
            piso=dto.piso,
            activo=True
        )
        
        # 3. Guardamos
        return self.repo.save(consultorio)
    
    def delete(self, id_consultorio: str) -> bool:
        # Aquí sí está bien usar el ID porque viene como argumento (string/uuid)
        if not self.repo.get_by_id(id_consultorio):
            raise ValueError("No existe consultorio")
        
        return self.repo.delete(id_consultorio)