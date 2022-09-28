from app import schemas
# from .database import client, session    
from jose import JWTError, jwt
from app.config import settings
import pytest
    
# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello Amma'
#     assert res.status_code == 200
    
def test_create_user(client):
    res = client.post("/users/", json={"email":"hello123@gmail.com", "password":"password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201
    
def test_login_user(test_user, client):
    res = client.post("/login", data={"username":test_user['email'], "password":test_user['password']})
    # here json is changed to data because we give it not in json form from postman but in "form-data" form
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=settings.algorithm)
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('eshaan049@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('eshaan049@gmail.com', None, 422)
])# we gave the right status codes for error type in the list so if all passed its working    
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data = {'username':email, 'password':password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == "Wrong credentials given, Please try agian" or "Wrong credentials, Try again"
    