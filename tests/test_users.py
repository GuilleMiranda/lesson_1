import pytest
from jose import JWTError, jwt
from app import schemas
from app.config import settings

def test_create_user(client):
    res = client.post("/users", json={"email": "test@user.com", "password": "test123"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "test@user.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/auth/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, key=settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert res.status_code == 200
    assert id == test_user["id"]
    assert login_res.token_type == "Bearer"

@pytest.mark.parametrize("email, password, status_code", [
    ("wrong_email@email.com", "test123", 403),
    ("test@user.com", "wrong_password", 403),
    ("wrong_email@email.com", "wrong_password", 403),
    (None, "test123", 422),
    ("test@user.com", None, 422),

])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/auth/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"