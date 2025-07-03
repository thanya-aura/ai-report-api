from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd

router = APIRouter()


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.endswith((".xlsx", ".xls", ".csv")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to read file")

    # Placeholder result
    result = {"status": "success", "message": "Standard report analyzed"}
    return result
