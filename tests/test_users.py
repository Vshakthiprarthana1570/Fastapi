import pytest
from app import schemas
import jwt
from app.config import settings


def test_create_user(client):
    response = client.post("/users/",json={"email": "hello123@gmail.com", "password": "Kodekloud@123"})
    res = schemas.UserOut(**response.json())
    assert res.email == "hello123@gmail.com"
    assert response.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    assert test_user['id'] == payload.get("user_id")
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 404),
    ('sanjeev@gmail.com', 'wrongpassword', 404),
    ('wrongemail@gmail.com', 'wrongpassword', 404),
    (None, 'password123', 404),
    ('sanjeev@gmail.com', None, 404)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code