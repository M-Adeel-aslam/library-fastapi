from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hased_password(password:str):
    return pwd_context.hash(password)

def verify_password(plainPassword, encrypedPassword):
    return pwd_context.verify(plainPassword, encrypedPassword)