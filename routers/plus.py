from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO

from report_plus.utils.kpi import calculate_kpis
from report_plus.utils.sox import validate_sox_controls
from report_plus.utils.forecast import simple_forecast
from report_plus.utils.audit_log import log_action
from report_plus.utils.validation import validate_report_structure
from report_plus.utils.export import generate_pdf_summary

router = APIRouter(prefix="/plus", tags=["Report Plus Agent"])

@router.post("/analyze")
async def analyze_plus(file: UploadFile = File(...)):
    # ✅ Validate file format
    if not file.filename.endswith((".csv", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only CSV or XLSX files supported.")

    # ✅ Read file into DataFrame
    if file.filename.endswith(".csv"):
        df = pd.read_csv(BytesIO(await file.read()))
    else:
        df = pd.read_excel(BytesIO(await file.read()), engine="openpyxl")

    # ✅ Perform core analyses
    validation = validate_report_structure(df)
    kpis = calculate_kpis(df)
    sox = validate_sox_controls(df)
    forecast = simple_forecast(df)

    # ✅ Log and export
    log_action("analyze", "report_plus")
    pdf_summary = generate_pdf_summary(df)

    return JSONResponse(content={
        "Validation": validation,
        "KPIs": kpis,
        "SOX_Controls": sox,
        "Forecast": forecast,
        "PDF_Summary_Generated": pdf_summary  # Usually returns success status or filename
    })
