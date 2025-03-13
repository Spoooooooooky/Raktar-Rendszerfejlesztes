from fastapi import FastAPI, HTTPException
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from tortoise import fields, models
from pydantic import BaseModel

app = FastAPI()

# Modellek
class Felhasznalo(models.Model):
    id = fields.IntField(pk=True)
    telefonszam = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    nev = fields.CharField(max_length=100)
    szerep = fields.CharField(max_length=50)

class Termek(models.Model):
    id = fields.IntField(pk=True)
    nev = fields.CharField(max_length=100)
    ar = fields.FloatField()  # Módosítva int-ről float-ra
    afa_kulcs = fields.IntField()

class Rendeles(models.Model):
    id = fields.IntField(pk=True)
    termek = fields.ForeignKeyField("models.Termek", related_name="rendelesek")
    mennyiseg = fields.IntField()
    allapot = fields.CharField(max_length=50)
    megrendelo = fields.ForeignKeyField("models.Felhasznalo", related_name="rendelesek")
    szallitasi_cim = fields.CharField(max_length=255)

class Beszallitas(models.Model):
    id = fields.IntField(pk=True)
    urlap = fields.ForeignKeyField("models.Urlap", related_name="beszallitasok")
    beszallito = fields.ForeignKeyField("models.Felhasznalo", related_name="beszallitasok")

class Urlap(models.Model):
    id = fields.IntField(pk=True)
    idopont = fields.DatetimeField(auto_now_add=True)
    termek = fields.ForeignKeyField("models.Termek", related_name="urlapok")
    mennyiseg = fields.IntField()

class Fuvar(models.Model):
    id = fields.IntField(pk=True)
    rendeles = fields.ForeignKeyField("models.Rendeles", related_name="fuvarok")
    allapot = fields.CharField(max_length=50)
    fuvarozo = fields.ForeignKeyField("models.Felhasznalo", related_name="fuvarok")

class Tarhely(models.Model):
    id = fields.IntField(pk=True)
    termek = fields.ForeignKeyField("models.Termek", related_name="tarhelyek")
    mennyiseg = fields.IntField()
    beerkezes_datuma = fields.DatetimeField(auto_now_add=True)

# Pydantic modellek
class Felhasznalo_Pydantic(BaseModel):
    telefonszam: str
    email: str
    nev: str
    szerep: str

class Termek_Pydantic(BaseModel):
    nev: str
    ar: float  # Módosítva int-ről float-ra
    afa_kulcs: int

class Rendeles_Pydantic(BaseModel):
    termek: int
    mennyiseg: int
    allapot: str
    megrendelo: int
    szallitasi_cim: str

class Beszallitas_Pydantic(BaseModel):
    urlap: int
    beszallito: int

class Urlap_Pydantic(BaseModel):
    termek: int
    mennyiseg: int

class Fuvar_Pydantic(BaseModel):
    rendeles: int
    allapot: str
    fuvarozo: int

class Tarhely_Pydantic(BaseModel):
    termek: int
    mennyiseg: int

# API végpontok meg nem kellenek, es csak teszt celjabol vannak. Nem veglegesek.
""" @app.post("/felhasznalok/")
async def add_felhasznalo(felhasznalo: Felhasznalo_Pydantic):
    new_felhasznalo = await Felhasznalo.create(**felhasznalo.dict())
    return {"message": "Felhasználó hozzáadva", "felhasznalo_id": new_felhasznalo.id}

@app.post("/termekek/")
async def add_termek(termek: Termek_Pydantic):
    new_termek = await Termek.create(**termek.dict())
    return {"message": "Termék hozzáadva", "termek_id": new_termek.id}

@app.post("/rendelesek/")
async def create_order(rendeles: Rendeles_Pydantic):
    new_order = await Rendeles.create(**rendeles.dict())
    return {"message": "Rendelés létrehozva", "rendeles_id": new_order.id}

@app.post("/beszallitasok/")
async def add_beszallitas(beszallitas: Beszallitas_Pydantic):
    new_beszallitas = await Beszallitas.create(**beszallitas.dict())
    return {"message": "Beszállítás hozzáadva", "beszallitas_id": new_beszallitas.id}

@app.post("/urlapok/")
async def add_urlap(urlap: Urlap_Pydantic):
    new_urlap = await Urlap.create(**urlap.dict())
    return {"message": "Űrlap hozzáadva", "urlap_id": new_urlap.id}

@app.post("/fuvarok/")
async def add_fuvar(fuvar: Fuvar_Pydantic):
    new_fuvar = await Fuvar.create(**fuvar.dict())
    return {"message": "Fuvar hozzáadva", "fuvar_id": new_fuvar.id}

@app.post("/tarhelyek/")
async def add_tarhely(tarhely: Tarhely_Pydantic):
    new_tarhely = await Tarhely.create(**tarhely.dict())
    return {"message": "Tárolóhely hozzáadva", "tarhely_id": new_tarhely.id}

@app.delete("/adatok-torlese/")
async def clear_data():
    await Termek.all().delete()
    await Felhasznalo.all().delete()
    await Rendeles.all().delete()
    await Beszallitas.all().delete()
    await Urlap.all().delete()
    await Fuvar.all().delete()
    await Tarhely.all().delete()
    return {"message": "Minden adat törölve"}

@app.get("/tabla-tartalom/")
async def get_table_content(table: str, rows: int = 10):
    model_map = {
        "felhasznalo": Felhasznalo,
        "termek": Termek,
        "rendeles": Rendeles,
        "beszallitas": Beszallitas,
        "urlap": Urlap,
        "fuvar": Fuvar,
        "tarhely": Tarhely
    }
    model = model_map.get(table.lower())
    if not model:
        raise HTTPException(status_code=400, detail="Érvénytelen tábla név")
    content = await model.all().limit(rows).values()
    return content """

# Adatbázis konfiguráció és migráció
TORTOISE_ORM = {
    "connections": {"default": "sqlite://./db.sqlite3"},
    "apps": {
        "models": {"models": ["raktar_backend", "aerich.models"], "default_connection": "default"}
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