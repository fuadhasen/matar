from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pass(password: str):
    """Hash the password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(non_hashed_pass, hashed_pass):
    """Verify the password using bcrypt"""
    return pwd_context.verify(non_hashed_pass, hashed_pass)
