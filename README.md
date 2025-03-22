To make everything work, PIP these:

pip install fastapi uvicorn tortoise-orm pydantic aerich tomli_w tomlkit

Automatikus inditasra:
- Linux:
    - Elso alkalommal:
        - chmod +x start.sh
        - ./start.sh
    - Utana:
        - ./start.sh
- Windows:
    - start.bat


Manualis elsoinditasi lepes sorozat:
- Kodszerkesztovel iditsd el a programot.
- aerich init -t raktar_backend.TORTOISE_ORM
- aerich init-db

Kesobbi manualis migracioknal:
- Kodszerkesztivel inditsd el a programot.
- aerich migrate
- aerich upgrade

Felhasználó hozzáadása:             python testfend.py add-felhasznalo --telefonszam "123456789" --email "example@example.com" --nev "John Doe" --szerep "admin"
Termék hozzáadása:                  python testfend.py add-termek --nev "Termék1" --ar 150000 --afa_kulcs 27
Rendelés hozzáadása:                python testfend.py add-rendeles --termek 1 --mennyiseg 10 --allapot "új" --megrendelo 1 --szallitasi_cim "1234 Budapest, Fő utca 1"
Beszállítás hozzáadása:             python testfend.py add-beszallitas --urlap 1 --beszallito 1
Űrlap hozzáadása:                   python testfend.py add-urlap --termek 1 --mennyiseg 100
Fuvar hozzáadása:                   python testfend.py add-fuvar --rendeles 1 --allapot "szállítás alatt" --fuvarozo 1
Tárolóhely hozzáadása:              python testfend.py add-tarhely --termek 1 --mennyiseg 50
Adatok törlése:                     python testfend.py clear-data
Tábla tartalmának lekérdezése:      python testfend.py get-table-content --table "felhasznalo" --rows 10
