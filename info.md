To run:
uvicorn main:app --reload

To make everything work, PIP these: New, as of Mar.11: aerich
pip install fastapi uvicorn tortoise-orm pydantic aerich tomli_w tomlkit


Before first run, run these in the folder you saved the project to:
aerich init -t raktar_backend.TORTOISE_ORM
aerich init-db

For migration afterwards:
aerich migrate
aerich upgrade

