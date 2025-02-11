from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Concert
import schemas

# 🆕 Crear un nuevo concierto
def create_concert(db: Session, concert: schemas.ConcertCreate):
    db_concert = Concert(**concert.model_dump())  # Convierte Pydantic a diccionario
    db.add(db_concert)
    db.commit()
    db.refresh(db_concert)  # Recarga para obtener el ID asignado
    return db_concert

# 🔍 Obtener un concierto por ID
def get_concert(db: Session, concert_id: int):
    return db.query(Concert).filter(Concert.id == concert_id).first()

# 📋 Obtener todos los conciertos
def get_concerts(db: Session):
    return db.query(Concert).all()

# 🚀 Obtener conciertos con filtros dinámicos
def get_concerts_filtered(
    db: Session,
    eventName: str = None,
    place: str = None,
    dateTime_from: str = None,
    dateTime_to: str = None,
    priceMin: float = None,
    priceMax: float = None,
):

    # Inicia la consulta
    query = db.query(Concert)

    # Construye filtros dinámicos
    filters = []
    
    if eventName:
        filters.append(Concert.eventName.ilike(f"%{eventName}%"))  # Búsqueda parcial
    if place:
        filters.append(Concert.place.ilike(f"%{place}%"))  # Búsqueda parcial
    if dateTime_from:
        filters.append(Concert.dateTime >= dateTime_from)
    if dateTime_to:
        filters.append(Concert.dateTime <= dateTime_to)
    if priceMin:
        filters.append(Concert.price >= priceMin)
    if priceMax:
        filters.append(Concert.price <= priceMax)

    # Aplica los filtros si hay alguno
    if filters:
        query = query.filter(and_(*filters))

    # Ejecuta la consulta y devuelve los resultados
    return query.all()

# ✏️ Actualizar un concierto
def update_concert(db: Session, concert_id: int, concert_update: schemas.ConcertCreate):
    db_concert = db.query(Concert).filter(Concert.id == concert_id).first()
    if db_concert:
        for key, value in concert_update.model_dump().items():
            setattr(db_concert, key, value)  # Asigna los nuevos valores
        db.commit()
        db.refresh(db_concert)
    return db_concert

# ❌ Eliminar un concierto
def delete_concert(db: Session, concert_id: int):
    db_concert = db.query(Concert).filter(Concert.id == concert_id).first()
    if db_concert:
        db.delete(db_concert)
        db.commit()
    return db_concert

# ✏️ Actualiza el stock
def update_concert_stock(db: Session, concerts_data: list[dict]):
    updated_concerts = []

    for concert_data in concerts_data:
        concert = db.query(Concert).filter(Concert.id == concert_data["id"]).first()
        if concert:
            concert.stock = concert_data["stock"]
            updated_concerts.append(concert)

    db.commit()
    return updated_concerts

# 📜 Obtener conciertos paginados
def get_concerts_paginated(db: Session, page: int, page_size: int = 6):
    offset = (page - 1) * page_size
    return db.query(Concert).offset(offset).limit(page_size).all()