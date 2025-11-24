



from uuid import uuid4
from app.db.repositories.consultorio_repository import ConsultorioRepository
from app.domain.entities.consultorios import Consultorio


class ConsultorioService:
    def __init__(self, repo: ConsultorioRepository):
        self.repo = repo
        
    def create(self,dto) -> Consultorio:
        if self.repo.get_by_id(dto.id_consultorio):
            raise ValueError("Consultorio ya registrado")
        consultorio = Consultorio(
            id_consultorio = str(uuid4()),
            numero_consultorio=dto.numero_consultorio,
            piso=dto.piso,
            activo=True
        )
        return self.repo.save(consultorio)
    
    def delete(self, id_consultorio: str) -> bool:
        if not self.repo.get_by_id(id_consultorio):
            raise ValueError("No existe consultorio")
        
        return self.repo.delete(id_consultorio)