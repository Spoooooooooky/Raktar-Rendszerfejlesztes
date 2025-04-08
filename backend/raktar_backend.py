from fastapi import FastAPI, HTTPException
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from models.pydantic_models import (
    Felhasznalo_Pydantic,
    FelhasznaloUpdate_Pydantic,
    Termek_Pydantic,
    TermekUpdate_Pydantic,
    Beszallitas_Pydantic,
    BeszallitasUpdate_Pydantic,
)
from backend.services.felhasznalo_service import UserService
from services.termek_service import TermekService
from services.beszallitas_service import BeszallitasService
from models.models import Felhasznalo, Termek, Beszallitas
from services.urlap_service import UrlapService
from models.pydantic_models import Urlap_Pydantic, UrlapUpdate_Pydantic

app = FastAPI()

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

# Űrlapok kezelése


@app.post("/urlapok/")
async def add_urlap(urlap: Urlap_Pydantic):
    new_urlap = await UrlapService.add_urlap(
        beszallito_nev=urlap.beszallito_nev,
        datum=urlap.datum,
        termekek=urlap.termekek
    )
    return {"message": "Űrlap rögzítve", "urlap_id": new_urlap.id}

@app.get("/urlapok/{urlap_id}")
async def get_urlap(urlap_id: int):
    urlap = await UrlapService.get_urlap(urlap_id)
    if not urlap:
        raise HTTPException(404, "Űrlap nem található")
    return {
        "id": urlap.id,
        "beszallito_nev": urlap.beszallito_nev,
        "datum": urlap.datum.isoformat(),
        "termekek": urlap.termekek
    }

@app.put("/urlapok/{urlap_id}")
async def update_urlap(urlap_id: int, urlap: UrlapUpdate_Pydantic):
    updated = await UrlapService.update_urlap(
        urlap_id,
        **urlap.dict(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(404, "Űrlap nem található")
    return {"message": "Űrlap frissítve"}

@app.delete("/urlapok/{urlap_id}")
async def delete_urlap(urlap_id: int):
    success = await UrlapService.delete_urlap(urlap_id)
    if not success:
        raise HTTPException(404, "Űrlap nem található")
    return {"message": "Űrlap törölve"}


def start():
    uvicorn.run("raktar_backend:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    start()