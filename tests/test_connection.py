from database import engine

def test_connection():
    try:
        with engine.connect() as connection:
            assert connection is not None  # Verifica que la conexión no es None
    except Exception as e:
        assert False, f"❌ Error al conectar a MySQL: {e}"