from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction
from models.models import Rendeles

class RendelesService:
    @staticmethod
    async def add_rendeles(termek_id: int, mennyiseg: int, allapot: str, megrendelo_id: int, szallitasi_cim: str):
        rendeles = await Rendeles.create(
            termek_id=termek_id,
            mennyiseg=mennyiseg,
            allapot=allapot,
            megrendelo_id=megrendelo_id,
            szallitasi_cim=szallitasi_cim
        )
        return rendeles

    @staticmethod
    async def get_rendeles(rendeles_id: int):
        return await Rendeles.get_or_none(id=rendeles_id)

    @staticmethod
    async def update_rendeles(rendeles_id: int, **kwargs):
        async with in_transaction():
            rendeles = await Rendeles.get_or_none(id=rendeles_id)
            if not rendeles:
                return None
            rendeles.update_from_dict(kwargs)
            await rendeles.save()
            return rendeles

    @staticmethod
    async def delete_rendeles(rendeles_id: int):
        rendeles = await Rendeles.get_or_none(id=rendeles_id)
        if rendeles:
            await rendeles.delete()
            return True
        return False
