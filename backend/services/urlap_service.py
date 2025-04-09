from tortoise.exceptions import DoesNotExist
from models.models import Urlap
from datetime import date


class UrlapService:
    @staticmethod
    async def add_urlap(beszallito_nev: str, datum: date, termekek: list):
        urlap = await Urlap.create(
            beszallito_nev=beszallito_nev,
            datum=datum,
            termekek=termekek
        )
        return urlap

    @staticmethod
    async def get_urlap(urlap_id: int):
        try:
            return await Urlap.get(id=urlap_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def update_urlap(urlap_id: int, **kwargs):
        try:
            urlap = await Urlap.get(id=urlap_id)
            await urlap.update_from_dict(kwargs).save()
            return urlap
        except DoesNotExist:
            return None

    @staticmethod
    async def delete_urlap(urlap_id: int):
        try:
            urlap = await Urlap.get(id=urlap_id)
            await urlap.delete()
            return True
        except DoesNotExist:
            return False
