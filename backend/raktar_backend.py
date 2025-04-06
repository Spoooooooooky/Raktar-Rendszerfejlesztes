from fastapi import FastAPI, HTTPException
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from services.user_service import UserService
from models.models import Felhasznalo  # A modellek importálása a külön fájlból

app = FastAPI()

# Pydantic modellek
class Felhasznalo_Pydantic(BaseModel):
    telefonszam: str
    email: str
    nev: str
    szerep: str

class FelhasznaloUpdate_Pydantic(BaseModel):
    telefonszam: str = None
    email: str = None
    nev: str = None
    szerep: str = None

# Felhasználók kezelése
@app.post("/felhasznalok/")
async def add_felhasznalo(felhasznalo: Felhasznalo_Pydantic):
    user = await UserService.add_user(
        telefonszam=felhasznalo.telefonszam,
        email=felhasznalo.email,
        nev=felhasznalo.nev,
        szerep=felhasznalo.szerep
    )
    return {"message": "Felhasználó hozzáadva", "felhasznalo_id": user.id}

@app.get("/felhasznalok/{user_id}")
async def get_felhasznalo(user_id: int):
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")
    return {
        "id": user.id,
        "telefonszam": user.telefonszam,
        "email": user.email,
        "nev": user.nev,
        "szerep": user.szerep
    }

@app.put("/felhasznalok/{user_id}")
async def update_felhasznalo(user_id: int, felhasznalo: FelhasznaloUpdate_Pydantic):
    user = await UserService.update_user(
        user_id=user_id,
        telefonszam=felhasznalo.telefonszam,
        email=felhasznalo.email,
        nev=felhasznalo.nev,
        szerep=felhasznalo.szerep
    )
    if not user:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")
    return {"message": "Felhasználó frissítve", "felhasznalo_id": user.id}

@app.delete("/felhasznalok/{user_id}")
async def delete_felhasznalo(user_id: int):
    success = await UserService.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")
    return {"message": "Felhasználó törölve"}

# Adatbázis konfiguráció és migráció
TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {"models": ["models", "aerich.models"], "default_connection": "default"}
    }
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

def start():
    uvicorn.run("raktar_backend:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    start()