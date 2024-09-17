from passlib.context import CryptContext
cwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash(password:str):
    return cwd_context.hash(password)

def verify(plain_pass,hassed_password):
    return cwd_context.verify(plain_pass,hassed_password)