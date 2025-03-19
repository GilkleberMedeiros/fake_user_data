from fastapi import FastAPI, Response, status
from pydantic import BaseModel, field_validator

import secrets
from typing import TypeVar

from utils import generate_fake_names, generate_fake_email


app = FastAPI()

T = TypeVar("T")

# Models
class FakeUser(BaseModel, frozen=True):
    name: str
    email: str
    password: str

class SystemMessageResponse(BaseModel):
    system_message: str
    generate_target: int
    generated: int
    data: T

class FakeUserResponse(SystemMessageResponse):
    data: list[FakeUser]


    @field_validator("data", mode="before")
    @classmethod
    def data_validator(cls, v: T) -> T:
        data = set(v)

        if len(data) != len(v):
            raise Exception("Values in data aren't unique.")
        
        return v
    

@app.get("/")
async def fake_user_data(n: int, response: Response, unique: bool = True) -> FakeUserResponse:
    names = generate_fake_names(n, unique=unique)

    fake_users = list(
        map(
            lambda i: 
            FakeUser(
            **{
                "name": i, 
                "email": generate_fake_email(i), 
                "password": secrets.token_hex(16),
            }
            ), 
            names
        )
    )
    len_fake_users = len(fake_users)
    
    if unique and len_fake_users == 0:
        message = "couldn't generate users due unique constraint. Max unique users already generated."
        response.status_code = status.HTTP_429_TOO_MANY_REQUESTS
    elif unique and len_fake_users < n:
        message = f"couldn't generate {n} users due unique constraint. Max unique users generated."
    elif len_fake_users < n:
        message = "couldn't generate suficient users due some reason."
    else:
        message = f"{len_fake_users} fake users generated."

    return {"system_message": message, "generate_target": n, "generated": len_fake_users, "data": fake_users}