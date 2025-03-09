from fastapi import FastAPI
from pydantic import BaseModel

from utils import generate_fake_names

app = FastAPI()

# Models
class FakeUser(BaseModel):
    name: str
    email: str
    password: str

@app.get("/")
async def fake_user_data(n: int, unique: bool = True) -> list[FakeUser]:
    names = generate_fake_names(n, unique=unique)

    return list(map(lambda i: {"name": i, "email": "email", "password": "password"}, names))
    pass