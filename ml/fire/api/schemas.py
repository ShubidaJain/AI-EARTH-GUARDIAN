from pydantic import BaseModel, Field


class LocationRequest(BaseModel):

    latitude: float = Field(
        ...,
        ge=-90,
        le=90
    )

    longitude: float = Field(
        ...,
        ge=-180,
        le=180
    )


class GridRequest(BaseModel):

    latitude: float = Field(
        ...,
        ge=-90,
        le=90
    )

    longitude: float = Field(
        ...,
        ge=-180,
        le=180
    )

    radius: float = Field(
        default=0.5,
        gt=0,
        le=2
    )

    points: int = Field(
        default=5,
        ge=3,
        le=9
    )