from fastapi import FastAPI, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import models
import schemas
from typing import List, Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware  # Importar CORS

# Crea las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Carrito de Compras",
    description="API para gestionar la compra de entradas de conciertos.",
    version="1.0.0"
)

# Configuración de CORS
origins = [
    "http://localhost:5173",  # Para desarrollo con Vite
    "https://tudominio.com",  # Si tienes un frontend desplegado
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origen permitido
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de conciertos"}

# 🆕 Crear múltiples conciertos
@app.post("/concerts/", response_model=List[schemas.ConcertResponse])
def create_concerts(
    concerts: List[schemas.ConcertCreate] = Body(...),
    db: Session = Depends(get_db)
):
    return crud.create_concerts(db=db, concerts=concerts)

@app.get("/concerts/{concert_id}", response_model=schemas.ConcertResponse)
def get_concert(concert_id: int, db: Session = Depends(get_db)):
    concert = crud.get_concert(db, concert_id)
    if concert is None:
        raise HTTPException(status_code=404, detail="Concierto no encontrado")
    return concert

@app.get("/concerts/", response_model=List[schemas.ConcertResponse])
def get_concerts(db: Session = Depends(get_db)):
    return crud.get_concerts(db)

@app.get("/concerts/filtered/", response_model=List[schemas.ConcertResponse])
def search_concerts(
    event_name: Optional[str] = Query(None),
    place: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    db: Session = Depends(get_db),
):
    return crud.get_concerts_filtered(
        db, event_name, place, date_from, date_to, price_min, price_max
    )

@app.put("/concerts/{concert_id}", response_model=schemas.ConcertResponse)
def update_concert(
    concert_id: int,
    concert_update: schemas.ConcertCreate,
    db: Session = Depends(get_db)
):
    updated_concert = crud.update_concert(db, concert_id, concert_update)
    if updated_concert is None:
        raise HTTPException(status_code=404, detail="Concierto no encontrado")
    return updated_concert

@app.delete("/concerts/{concert_id}", response_model=schemas.ConcertResponse)
def delete_concert(concert_id: int, db: Session = Depends(get_db)):
    deleted_concert = crud.delete_concert(db, concert_id)
    if deleted_concert is None:
        raise HTTPException(status_code=404, detail="Concierto no encontrado")
    return deleted_concert

@app.put("/cart/update-stock/", response_model=List[schemas.ConcertResponse])
def update_cart_stock(
    concerts_data: List[dict] = Body(...),
    db: Session = Depends(get_db),
):
    updated_concerts = crud.update_concert_stock(db, concerts_data)
    if not updated_concerts:
        raise HTTPException(
            status_code=404, detail="No se encontraron conciertos para actualizar"
        )
    return updated_concerts

@app.get("/concerts/page/{page}", response_model=List[schemas.ConcertResponse])
def get_concerts_paginated(page: int, db: Session = Depends(get_db)):
    if page < 1:
        raise HTTPException(status_code=400, detail="La página debe ser 1 o mayor")
    return crud.get_concerts_paginated(db, page)