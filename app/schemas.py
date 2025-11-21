from pydantic import BaseModel, Field
from typing import Literal

class DiamondFeatures(BaseModel):
    carat: float = Field(..., gt=0, description="Carat weight")
    cut: Literal['Fair', 'Good', 'Very Good', 'Premium', 'Ideal']
    color: Literal['J', 'I', 'H', 'G', 'F', 'E', 'D']
    clarity: Literal['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']
    depth: float = Field(..., gt=0, lt=100)
    table: float = Field(..., gt=0, lt=100)
    x: float = Field(..., gt=0)
    y: float = Field(..., gt=0)
    z: float = Field(..., gt=0)

class PredictionResponse(BaseModel):
    predicted_price: float
    model_version: str