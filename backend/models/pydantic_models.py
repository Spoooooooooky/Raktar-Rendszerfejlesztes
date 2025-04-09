from pydantic import BaseModel
from datetime import date

# Felhasználók Pydantic modellek
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

# Termékek Pydantic modellek
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
    
class Fuvar_Pydantic(BaseModel):
    szallitas_datum: date
    beszallito_nev: str
    termekek: list[dict]

class FuvarUpdate_Pydantic(BaseModel):
    statusz: str = None
    szallitas_datum: date = None
    beszallito_nev: str = None

class Urlap_Pydantic(BaseModel):
    beszallito_nev: str
    datum: date
    termekek: list[dict]

class UrlapUpdate_Pydantic(BaseModel):
    beszallito_nev: str = None
    datum: date = None
    termekek: list[dict] = None
