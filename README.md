To make everything work, PIP these: New, as of Mar.11: aerich

pip install fastapi uvicorn tortoise-orm pydantic aerich tomli_w tomlkit


Elso inditas elott a backend mappaban ezeket futtatsd:
-aerich init -t raktar_backend.TORTOISE_ORM
-aerich init-db

Kesobbi migraciok ugyan ott:
-aerich migrate
-aerich upgrade
