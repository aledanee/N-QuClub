from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app  # Adjust the import according to your project structure
from app.db.base_class import Base  # Adjust the import

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_notification():
    response = client.post("/notifications/?user_id=4", json={"message": "Welcome!", "read_status": false})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome!"
    assert "notification_id" in data
