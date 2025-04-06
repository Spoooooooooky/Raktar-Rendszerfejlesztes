Ezekket pip-el kell telepiteni:
- pip install fastapi uvicorn tortoise-orm pydantic aerich tomli_w tomlkit httpx

Linuxon a gtk grafikus rendszer telepitese:
- sudo dnf install python3-gobject gtk3

Windows
- Telepítsd a GTK-t a hivatalos oldalról: https://www.gtk.org/download/windows.php.
- Győződj meg róla, hogy a GTK binárisok elérhetők a PATH környezeti változóban.
- Telepítsd a Python csomagokat:
    - pip install pycairo PyGObject


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