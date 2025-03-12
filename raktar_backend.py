from fastapi import FastAPI
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
    ar = fields.IntField()
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
class Rendeles_Pydantic(BaseModel):
    termek: int
    mennyiseg: int
    allapot: str
    megrendelo: int
    szallitasi_cim: str

@app.post("/rendelesek/")
async def create_order(rendeles: Rendeles_Pydantic):
    new_order = await Rendeles.create(**rendeles.dict())
    return {"message": "Rendelés létrehozva", "rendeles_id": new_order.id}

@app.get("/rendelesek/")
async def list_orders():
    rendelesek = await Rendeles.all().values()
    return rendelesek

@app.post("/termek-hozzaadasa/")
async def add_product(nev: str, ar: int, afa_kulcs: int):
    termek = await Termek.create(nev=nev, ar=ar, afa_kulcs=afa_kulcs)
    return {"message": "Termék hozzáadva", "termek_id": termek.id}

@app.delete("/adatok-torlese/")
async def clear_data():
    await Termek.all().delete()
    return {"message": "Minden adat törölve"}

# Adatbázis konfiguráció és migráció
TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
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