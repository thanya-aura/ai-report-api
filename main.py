from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO

from report_standard.main import analyze as analyze_standard
from report_plus.main import analyze as analyze_plus
from report_premium.main import analyze as analyze_premium

app = FastAPI(title="Unified Financial Report API")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), agent: str = "standard"):
    if not file.filename.endswith((".csv", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only CSV or XLSX files supported.")

    if agent == "standard":
        return await analyze_standard(file)
    elif agent == "plus":
        return await analyze_plus(file)
    elif agent == "premium":
        return await analyze_premium(file)
    else:
        raise HTTPException(status_code=400, detail="Invalid agent specified. Choose from: standard, plus, premium.")
