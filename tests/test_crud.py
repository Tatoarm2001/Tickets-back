import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from crud import get_concerts_filtered
from models import Concert
from datetime import datetime

# Configuración de la base de datos MySQL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost/ticket_store"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)  # Asegura que las tablas existen
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)  # Limpia la base de datos después de los tests

# Datos de prueba
def create_test_concerts(db):
    concert1 = Concert(eventName="Jazz Night", img="img1.jpg", description="A night of jazz", 
                       dateTime=datetime(2025, 3, 15, 20, 0), place="New York", price=50)
    concert2 = Concert(eventName="Rock Fest", img="img2.jpg", description="Rock legends", 
                       dateTime=datetime(2025, 4, 20, 19, 30), place="Los Angeles", price=80)
    db.add_all([concert1, concert2])
    db.commit()

def test_get_concerts_filtered_name(db):
    create_test_concerts(db)
    result = get_concerts_filtered(db, eventName="Jazz Night")
    assert len(result) == 1
    assert result[0].eventName == "Jazz Night"

def test_get_concerts_filtered_place(db):
    result = get_concerts_filtered(db, place="Los Angeles")
    assert len(result) == 1
    assert result[0].place == "Los Angeles"

def test_get_concerts_filtered_price_min(db):
    result = get_concerts_filtered(db, priceMin=60)
    assert len(result) == 1
    assert result[0].price == 80

def test_get_concerts_filtered_price_max(db):
    result = get_concerts_filtered(db, priceMax=60)
    assert len(result) == 1
    assert result[0].price == 50

def test_get_concerts_filtered_date_from(db):
    result = get_concerts_filtered(db, dateTime_from=datetime(2025, 4, 1)) 
    assert len(result) == 1
    assert result[0].dateTime == datetime(2025, 4, 20, 19, 30)

def test_get_concerts_filtered_date_to(db):
    result = get_concerts_filtered(db, dateTime_to=datetime(2025, 3, 30)) 
    assert len(result) == 1
    assert result[0].dateTime == datetime(2025, 3, 15, 20, 0)

def test_get_concerts_filtered_date_range(db):
    result = get_concerts_filtered(db, dateTime_from=datetime(2025, 3, 1), dateTime_to=datetime(2025, 4, 30))  
    assert len(result) == 2
