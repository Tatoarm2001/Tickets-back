from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List

# 🎵 Modelo base para conciertos
class ConcertBase(BaseModel):
    name: str = Field(..., example="Concierto Rock")
    place: str = Field(..., example="Estadio Nacional")
    date: datetime = Field(..., example="2025-06-15T20:00:00")
    price: float = Field(..., example=99.99)
    stock: int = Field(..., example=6)

# 📩 Esquema para crear un nuevo concierto (mismo que ConcertBase)
class ConcertCreate(ConcertBase):
    pass

# 📤 Esquema de salida con ID incluido
class ConcertOut(ConcertBase):
    id: int
    model_config = ConfigDict(from_attributes=True)  # Para Pydantic v2

# 🎟️ Esquema para actualizar stock
class CartUpdate(BaseModel):
    id: int = Field(..., example=1)
    stock: int = Field(..., example=3)