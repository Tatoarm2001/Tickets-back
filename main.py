from fastapi import FastAPI, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import models
import schemas
from typing import List, Optional
from datetime import datetime

# Crea las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Carrito de Compras",
    description="API para gestionar la compra de entradas de conciertos.",
    version="1.0.0"
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


# Crear un nuevo concierto
@app.post("/concerts/", response_model=schemas.ConcertOut)
def create_concert(concert: schemas.ConcertCreate, db: Session = Depends(get_db)):
    return crud.create_concert(db=db, concert=concert)


# Obtener un concierto por ID
@app.get("/concerts/{concert_id}", response_model=schemas.ConcertOut)
def get_concert(concert_id: int, db: Session = Depends(get_db)):
    concert = crud.get_concert(db, concert_id)
    if concert is None:
        raise HTTPException(status_code=404, detail="Concierto no encontrado")
    return concert


# Obtener todos los conciertos
@app.get("/concerts/", response_model=List[schemas.ConcertOut])
def get_concerts(db: Session = Depends(get_db)):
    return crud.get_concerts(db)


# Obtener conciertos con filtros
@app.get("/concerts/filtered/", response_model=List[schemas.ConcertOut])
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


# Actualizar un concierto
@app.put("/concerts/{concert_id}", response_model=schemas.ConcertOut)
def update_concert(
    concert_id: int,
    concert_update: schemas.ConcertCreate,
    db: Session = Depends(get_db)
):
    updated_concert = crud.update_concert(db, concert_id, concert_update)
    if updated_concert is None:
        raise HTTPException(status_code=404, detail="Concierto no encontrado")
    return updated_concert


# Eliminar un concierto
@app.delete("/concerts/{concert_id}", response_model=schemas.ConcertOut)
def delete_concert(concert_id: int, db: Session = Depends(get_db)):
    deleted_concert = crud.delete_concert(db, concert_id)
    if deleted_concert is None:
        raise HTTPException(status_code=404, detail="Concierto no encontrado")
    return deleted_concert


# Actualizar el stock
@app.put("/cart/update-stock/", response_model=List[schemas.ConcertOut])
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

# 🎟️ Obtener conciertos paginados
@app.get("/concerts/page/{page}", response_model=List[schemas.ConcertOut])
def get_concerts_paginated(page: int, db: Session = Depends(get_db)):
    if page < 1:
        raise HTTPException(status_code=400, detail="La página debe ser 1 o mayor")
    return crud.get_concerts_paginated(db, page)