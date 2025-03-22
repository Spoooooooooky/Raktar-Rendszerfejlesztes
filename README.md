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
