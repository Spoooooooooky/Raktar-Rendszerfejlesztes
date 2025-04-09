from tortoise.exceptions import DoesNotExist
from models.models import Fuvar

class FuvarService:
    @staticmethod
    async def add_fuvar(szallitas_datum: date, beszallito_nev: str, termekek: list):
        fuvar = await Fuvar.create(
            szallitas_datum=szallitas_datum,
            beszallito_nev=beszallito_nev,
            termekek=termekek
        )
        return fuvar

    @staticmethod
    async def get_fuvar(fuvar_id: int):
        try:
            return await Fuvar.get(id=fuvar_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def update_fuvar(fuvar_id: int, **kwargs):
        try:
            fuvar = await Fuvar.get(id=fuvar_id)
            await fuvar.update_from_dict(kwargs).save()
            return fuvar
        except DoesNotExist:
            return None

    @staticmethod
    async def delete_fuvar(fuvar_id: int):
        try:
            fuvar = await Fuvar.get(id=fuvar_id)
            await fuvar.delete()
            return True
        except DoesNotExist:
            return False
