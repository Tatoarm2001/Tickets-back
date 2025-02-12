from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Pydantic model para la creación de conciertos
class ConcertCreate(BaseModel):
    eventName: str  # Nombre del evento
    img: str  # URL de la imagen del concierto
    description: str  # Descripción del concierto
    dateTime: datetime  # Fecha y hora del evento
    place: str  # Lugar del evento
    price: float  # Precio del ticket
    stock: Optional[int] = 6  # Stock por defecto 6
    body: str  # Descripción adicional del evento

    class Config:
        orm_mode = True  # Permite que Pydantic pueda trabajar con modelos de SQLAlchemy

# Pydantic model para la respuesta al consultar conciertos
class ConcertResponse(BaseModel):
    id: int  # ID del concierto
    eventName: str  # Nombre del evento
    img: str  # URL de la imagen del concierto
    description: str  # Descripción del concierto
    dateTime: datetime  # Fecha y hora del evento
    place: str  # Lugar del evento
    price: float  # Precio del ticket
    stock: int  # Stock disponible
    body: str  # Descripción adicional

    class Config:
        orm_mode = True  # Permite que Pydantic pueda trabajar con modelos de SQLAlchemy