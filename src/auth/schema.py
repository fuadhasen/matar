from pydantic import BaseModel


class UserCreateModel(BaseModel):
    full_name: str
    email: str
    password: str
    phone_number: int
    role: str
