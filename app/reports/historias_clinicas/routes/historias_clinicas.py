from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.db.database import get_db
from app.reports.historias_clinicas.services.historia_clinica_service import HistoriaClinicaReportsService
import io

router = APIRouter(prefix="/reportes/historia", tags=["Reportes Historia Clínica"])

@router.get("/diagnosticos")
def reporte_diagnosticos(db=Depends(get_db)):
    service = HistoriaClinicaReportsService(db)
    pdf_bytes = service.generar_reporte_diagnosticos()

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=diagnosticos.pdf"}
    )

@router.get("/tratamientos")
def reporte_tratamientos(db=Depends(get_db)):
    service = HistoriaClinicaReportsService(db)
    pdf_bytes = service.generar_reporte_tratamientos()

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=tratamientos.pdf"}
    )


@router.get("/registros/{id_paciente}")
def reporte_registros_paciente(id_paciente: str, db=Depends(get_db)):
    service = HistoriaClinicaReportsService(db)
    pdf_bytes = service.generar_reporte_registros_por_paciente(id_paciente)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=historia_clinica_{id_paciente}.pdf"
        }
    )
