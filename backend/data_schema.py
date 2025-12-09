from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    phone: int
    name: str