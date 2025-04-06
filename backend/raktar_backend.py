from fastapi import FastAPI, HTTPException
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from services.user_service import UserService
from services.termek_service import TermekService
from services.beszallitas_service import BeszallitasService  
from models.models import Felhasznalo, Termek, Beszallitas 

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

class Termek_Pydantic(BaseModel):
    nev: str
    ar: float
    afa_kulcs: int

class TermekUpdate_Pydantic(BaseModel):
    nev: str = None
    ar: float = None
    afa_kulcs: int = None

class Beszallitas_Pydantic(BaseModel):
    termek_id: int
    mennyiseg: int
    beszallito_nev: str

class BeszallitasUpdate_Pydantic(BaseModel):
    termek_id: int = None
    mennyiseg: int = None
    beszallito_nev: str = None

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

# Termékek kezelése
@app.post("/termekek/")
async def add_termek(termek: Termek_Pydantic):
    new_termek = await TermekService.add_termek(
        nev=termek.nev,
        ar=termek.ar,
        afa_kulcs=termek.afa_kulcs
    )
    return {"message": "Termék hozzáadva", "termek_id": new_termek.id}

@app.get("/termekek/{termek_id}")
async def get_termek(termek_id: int):
    termek = await TermekService.get_termek(termek_id)
    if not termek:
        raise HTTPException(status_code=404, detail="Termék nem található")
    return {
        "id": termek.id,
        "nev": termek.nev,
        "ar": termek.ar,
        "afa_kulcs": termek.afa_kulcs
    }

@app.put("/termekek/{termek_id}")
async def update_termek(termek_id: int, termek: TermekUpdate_Pydantic):
    updated_termek = await TermekService.update_termek(
        termek_id=termek_id,
        nev=termek.nev,
        ar=termek.ar,
        afa_kulcs=termek.afa_kulcs
    )
    if not updated_termek:
        raise HTTPException(status_code=404, detail="Termék nem található")
    return {"message": "Termék frissítve", "termek_id": updated_termek.id}

@app.delete("/termekek/{termek_id}")
async def delete_termek(termek_id: int):
    success = await TermekService.delete_termek(termek_id)
    if not success:
        raise HTTPException(status_code=404, detail="Termék nem található")
    return {"message": "Termék törölve"}

# Beszállítások kezelése
@app.post("/beszallitasok/")
async def add_beszallitas(beszallitas: Beszallitas_Pydantic):
    new_beszallitas = await BeszallitasService.add_beszallitas(
        termek_id=beszallitas.termek_id,
        mennyiseg=beszallitas.mennyiseg,
        beszallito_nev=beszallitas.beszallito_nev
    )
    return {"message": "Beszállítás rögzítve", "beszallitas_id": new_beszallitas.id}

@app.get("/beszallitasok/{beszallitas_id}")
async def get_beszallitas(beszallitas_id: int):
    beszallitas = await BeszallitasService.get_beszallitas(beszallitas_id)
    if not beszallitas:
        raise HTTPException(status_code=404, detail="Beszállítás nem található")
    return {
        "id": beszallitas.id,
        "termek_id": beszallitas.termek_id,
        "mennyiseg": beszallitas.mennyiseg,
        "beszallito_nev": beszallitas.beszallito_nev
    }

@app.put("/beszallitasok/{beszallitas_id}")
async def update_beszallitas(beszallitas_id: int, beszallitas: BeszallitasUpdate_Pydantic):
    updated_beszallitas = await BeszallitasService.update_beszallitas(
        beszallitas_id=beszallitas_id,
        termek_id=beszallitas.termek_id,
        mennyiseg=beszallitas.mennyiseg,
        beszallito_nev=beszallitas.beszallito_nev
    )
    if not updated_beszallitas:
        raise HTTPException(status_code=404, detail="Beszállítás nem található")
    return {"message": "Beszállítás frissítve", "beszallitas_id": updated_beszallitas.id}

@app.delete("/beszallitasok/{beszallitas_id}")
async def delete_beszallitas(beszallitas_id: int):
    success = await BeszallitasService.delete_beszallitas(beszallitas_id)
    if not success:
        raise HTTPException(status_code=404, detail="Beszállítás nem található")
    return {"message": "Beszállítás törölve"}

# Adatbázis konfiguráció és migráció
TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {"models": ["models.models", "aerich.models"], "default_connection": "default"}
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