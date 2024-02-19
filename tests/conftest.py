import pytest
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app

from app.database import get_db
from app import models
from app.models import Base
from app.oauth2 import create_access_token

# from alembic import command

url = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/fastapi_test_db"

engine = create_engine(
    url=url,
    # echo=True,  # Prints to standard output the operations (statements) performed.
)

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # command.upgrade("head")
    # command.downgrade("base")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def get_testing_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_testing_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@user.com", "password": "test123"}
    res = client.post("/users", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user_2(client):
    user_data = {"email": "test2@user.com", "password": "test123"}
    res = client.post("/users", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, session, test_user_2):
    posts_data = [
        {"title": "1st title", "content": "1st content", "user_id": test_user["id"]},
        {"title": "2st title", "content": "2st content", "user_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "user_id": test_user["id"]},
        {"title": "4th title", "content": "4th content", "user_id": test_user_2["id"]},
    ]

    post_map = map(lambda post: models.Post(**post), posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
