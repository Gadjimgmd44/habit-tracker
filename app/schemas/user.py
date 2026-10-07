from pydantic import BaseModel, EmailStr, Field,field_validator

class UserEmailBase(BaseModel):
    email: EmailStr 
    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls,v):
        if isinstance(v,str):
            return v.strip().lower()
        return v

class UserCreate(UserEmailBase):
    password: str = Field(min_length=8, max_length=72)

class UserLogin(UserEmailBase):
    password: str
    
