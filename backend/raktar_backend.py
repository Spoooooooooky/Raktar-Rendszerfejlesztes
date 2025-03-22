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

# Eredetileg itt int-kent volt az ar, es a tort forinokat csak az utolso ket pozicioban tartottunk, de Noel jogos kerdese utan lebegopontos adatta valt.
class Termek(models.Model):
    id = fields.IntField(pk=True)
    nev = fields.CharField(max_length=100)
    ar = fields.FloatField()
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

# A modelleket a Pydantic-nek is frissiteni kellett.
class Termek_Pydantic(BaseModel):
    nev: str
    ar: float
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
