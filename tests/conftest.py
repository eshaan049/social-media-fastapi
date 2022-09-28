from fastapi.testclient import TestClient

from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import pytest
# from alembic import command

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)# responsible for SQLAlchemy to connect with postgres or DB
# if we use SQlite DB then we add more parameters like: create_engine(SQ:AL..., connect_args={'check_same_thread':False})

# to talk to SQL DB we need make use of session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # command.upgrade("head")# alembic create db and below destroy that
    # command.downgrade('base')
    db = TestingSessionLocal()# commit we should do in main.py functions
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):# returns a response obj
    def override_get_db():# this is similar to conn.close() where we perform SQL and then close the connection in the end
        try:
            yield session
        finally:
            session.close()
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)# used to give import response obj type for further use
    

@pytest.fixture
def test_user2(client):
    user_data = {"email":"eshaan111@gmail.com", "password":"password123"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data['password']
    
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email":"eshaan@gmail.com", "password":"password123"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data['password']
    
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id':test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
        'title':'first title',
        'content':'first content',
        'owner_id':test_user['id']   
    }, {
        'title':'2nd title',
        'content':'2nd content',
        'owner_id':test_user['id']
    }, {
        'title':'3rd title',
        'content':'3rd content',
        'owner_id':test_user['id']
    }, {
        'title':'4th title',
        'content':'4th content',
        'owner_id':test_user2['id']
    }]
    
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    
    # session.add_all([models.Post(title='first title', content="first content", owner_id=test_user['id']),
                    #  models.Post(title='2nd title', content='2nd content', owner_id = test_user['id']),
                    #  models.Post(title='3rd title', content='3rd content', owner_id = test_user['id'])])
    
    session.commit()
    posts = session.query(models.Post).all()
    
    return posts