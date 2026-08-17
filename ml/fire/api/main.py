from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import LocationRequest
from .predictor import predict_fire_risk

from .predictor import (
    predict_fire_risk,
    predict_live_fire_risk
)

app = FastAPI(
    title="AI Earth Guardian API",
    description="Wildfire risk prediction service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Health check
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "AI Earth Guardian API",
        "model": "XGBoost"
    }


# ============================================================
# Prediction
# ============================================================

@app.post("/predict/live")
def predict_live(
    request: LocationRequest
):

    try:

        result = predict_live_fire_risk(
            request.latitude,
            request.longitude
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )