To run:
uvicorn main:app --reload

To make everything work, PIP these: New, as of Mar.11: aerich
pip install fastapi uvicorn tortoise-orm pydantic aerich tomli_w tomlkit typer httpx

Before first run, run these in the folder you saved the project to:
aerich init -t raktar_backend.TORTOISE_ORM
aerich init-db

For migration afterwards:
aerich migrate
aerich upgrade

Ezekkel a módosításokkal most már hozzáadhatsz adatokat minden táblához a testfend.py fájl segítségével. Az adatok beviteléhez használd a következő parancsokat:

Felhasználó hozzáadása: python [testfend.py](http://_vscodecontentref_/5) add-felhasznalo --telefonszam "123456789" --email "example@example.com" --nev "John Doe" --szerep "admin"
Termék hozzáadása: python [testfend.py](http://_vscodecontentref_/6) add-termek --nev "Termék1" --ar 150000 --afa_kulcs 27
Rendelés hozzáadása: python [testfend.py](http://_vscodecontentref_/7) add-rendeles --termek 1 --mennyiseg 10 --allapot "új" --megrendelo 1 --szallitasi_cim "1234 Budapest, Fő utca 1"
Beszállítás hozzáadása: python [testfend.py](http://_vscodecontentref_/8) add-beszallitas --urlap 1 --beszallito 1
Űrlap hozzáadása: python [testfend.py](http://_vscodecontentref_/9) add-urlap --termek 1 --mennyiseg 100
Fuvar hozzáadása: python [testfend.py](http://_vscodecontentref_/10) add-fuvar --rendeles 1 --allapot "szállítás alatt" --fuvarozo 1
Tárolóhely hozzáadása: python [testfend.py](http://_vscodecontentref_/11) add-tarhely --termek 1 --mennyiseg 50
Adatok törlése: python [testfend.py](http://_vscodecontentref_/12) clear-data
Tábla tartalmának lekérdezése: python [testfend.py](http://_vscodecontentref_/13) get-table-content --table "felhasznalo" --rows 10
