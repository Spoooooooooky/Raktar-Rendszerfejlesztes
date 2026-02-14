from tortoise.exceptions import DoesNotExist
from models.models import Tarhely

class TarhelyService:
    @staticmethod
    async def add_tarhely(termek_id: int, mennyiseg: int):
        tarhely = await Tarhely.create(
            termek_id=termek_id,
            mennyiseg=mennyiseg
        )
        return tarhely

    @staticmethod
    async def get_tarhely(tarhely_id: int):
        return await Tarhely.get_or_none(id=tarhely_id)

    @staticmethod
    async def delete_tarhely(tarhely_id: int):
        tarhely = await Tarhely.get_or_none(id=tarhely_id)
        if tarhely:
            await tarhely.delete()
            return True
        return False
