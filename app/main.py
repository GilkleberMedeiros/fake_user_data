from fastapi import FastAPI
from pydantic import BaseModel

import secrets
from typing import TypeVar

from utils import generate_fake_names, generate_fake_email


app = FastAPI()

T = TypeVar("T")

# Models
class FakeUser(BaseModel):
    name: str
    email: str
    password: str

class SystemMessageResponse(BaseModel):
    system_message: str
    data: T

class FakeUserResponse(SystemMessageResponse):
    data: list[FakeUser]
    

@app.get("/")
async def fake_user_data(n: int, unique: bool = True) -> FakeUserResponse:
    names = generate_fake_names(n, unique=unique)

    fake_users = list(
        map(
            lambda i: 
                {
                "name": i, 
                "email": generate_fake_email(i), 
                "password": secrets.token_hex(16),
                }, 
            names
        )
    )
    
    if unique and len(fake_users) == 0:
        message = "couldn't generate users due unique constraint. Max unique users already generated."
    elif unique and len(fake_users) < n:
        message = f"couldn't generate {n} users due unique constraint. Max unique users generated."
    elif len(fake_users) < n:
        message = "couldn't generate suficient users due some reason."
    else:
        message = f"{n} fake users generated."

    return {"system_message": message, "data": fake_users}