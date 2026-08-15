from fastapi import FastAPI, HTTPException

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


# ============================================================
# Health check
# ============================================================

@app.get("/")
def root():

    return {
        "status": "online",
        "service": "AI Earth Guardian",
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