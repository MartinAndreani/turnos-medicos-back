# app/reports/pacientes/routes/patients_reports.py

from io import BytesIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.reports.pacientes.services.patients_reports_service import PatientsReportsService

router = APIRouter(prefix="/reportes/pacientes", tags=["Reportes Pacientes"])


@router.get("/resumen", response_class=StreamingResponse)
def generar_reporte_pacientes(db: Session = Depends(get_db)):
    """
    Genera un PDF con:
    - Pacientes nuevos por mes
    - Ranking de pacientes por consultas
    - Pacientes inactivos

    El PDF se descarga como archivo adjunto.
    """
    service = PatientsReportsService()
    pdf_bytes = service.generar_pdf_reportes(db)

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="reporte_pacientes.pdf"'
        },
    )
