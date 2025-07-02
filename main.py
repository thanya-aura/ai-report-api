from fastapi import FastAPI
from report_standard.main import router as standard_router
from report_plus.main import router as plus_router
from report_premium.main import router as premium_router

app = FastAPI(title="AI Report API")

app.include_router(standard_router, prefix="/standard", tags=["Standard Report"])
app.include_router(plus_router, prefix="/plus", tags=["Plus Report"])
app.include_router(premium_router, prefix="/premium", tags=["Premium Report"])

@app.get("/")
def root():
    return {"message": "AI Report API is live"}
