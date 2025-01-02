from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #telling passlib what hashing algorithm I want to use,it is bcrypt

def hash(password: str):
    return pwd_context.hash(password)

def verify_user(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass, hashed_pass)