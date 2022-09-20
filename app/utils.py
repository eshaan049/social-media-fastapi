from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password : str):
    return pwd_context.hash(password)

def verify(passsword, hashed_password):
    return pwd_context.verify(passsword, hashed_password)