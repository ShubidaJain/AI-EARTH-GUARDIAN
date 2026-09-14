from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import time 
import asyncio

from .schemas import (
    LocationRequest,
    GridRequest
)

from .predictor import (
    predict_fire_risk,
    predict_live_fire_risk,
    predict_fire_risk_grid,
    clear_grid_cache,
    get_grid_cache_info,
    THRESHOLD
)

from .weather_service import (
    clear_weather_cache,
    get_weather_cache_info
)

# ============================================================
# Batch prediction schemas
# ============================================================

class BatchLocationRequest(BaseModel):
    latitude: float
    longitude: float


class BatchPredictionRequest(BaseModel):
    locations: list[BatchLocationRequest]

app = FastAPI(
    title="AI Earth Guardian API",
    description="Wildfire risk prediction service",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Request timing middleware
# ============================================================

@app.middleware("http")
async def request_timing(request: Request, call_next):

    start_time = time.perf_counter()

    response = await call_next(request)

    processing_time = (
        time.perf_counter() - start_time
    ) * 1000

    response.headers["X-Process-Time-ms"] = (
        f"{processing_time:.2f}"
    )

    print(
        f"⏱️ {request.method} "
        f"{request.url.path} "
        f"{processing_time:.2f} ms"
    )

    return response

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
# System status
# ============================================================

@app.get("/status")
def status():

    weather_cache = get_weather_cache_info()
    grid_cache = get_grid_cache_info()

    return {
        "service": "AI Earth Guardian API",
        "status": "operational",

        "model": {
            "type": "XGBoost",
            "threshold": THRESHOLD
        },

        "cache": {
            "weather": weather_cache,
            "grid": grid_cache
        }
    }

#============================================================
#Info
#===========================================================

@app.get("/info")
def info():
    return {
        "service": "AI Earth Guardian API",
        "version": "1.0.0",
        "model": {
            "type": "XGBoost",
            "threshold": THRESHOLD
        },
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "live_prediction": "/predict/live",
            "grid_prediction": "/predict/grid",
            "cache_clear": "/cache/clear"
        },
        "performance": {
            "weather_cache": get_weather_cache_info(),
            "grid_cache": get_grid_cache_info()
        }
    }

# ============================================================
# Clear caches
# ============================================================

@app.post("/cache/clear")
def clear_cache():

    clear_weather_cache()
    clear_grid_cache()

    return {
        "status": "success",
        "message": "Weather and grid caches cleared"
    }


# ============================================================
# Live prediction
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


# ============================================================
# Grid prediction
# ============================================================

@app.post("/predict/grid")
async def predict_grid(
    request: GridRequest
):

    try:

        results = await predict_fire_risk_grid(
            latitude=request.latitude,
            longitude=request.longitude,
            radius=request.radius,
            points=request.points
        )

        return {
            "center": {
                "latitude": request.latitude,
                "longitude": request.longitude
            },

            "radius": request.radius,

            "points": request.points,

            "count": len(results),

            "results": results
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# Batch prediction
# ============================================================

# ============================================================
# Batch prediction
# ============================================================

@app.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):

    async def predict_location(location):

        try:

            prediction = await asyncio.to_thread(
                predict_live_fire_risk,
                location.latitude,
                location.longitude
            )

            return {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "prediction": prediction
            }

        except Exception as error:

            return {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "error": str(error)
            }

    tasks = [
        predict_location(location)
        for location in request.locations
    ]

    results = await asyncio.gather(*tasks)

    return {
        "count": len(results),
        "results": results
    }