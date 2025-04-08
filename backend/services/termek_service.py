from tortoise.exceptions import DoesNotExist
from models.models import Termek

class TermekService:
    @staticmethod
    async def add_termek(nev: str, ar: float, afa_kulcs: int):
        """Új termék hozzáadása."""
        termek = await Termek.create(
            nev=nev,
            ar=ar,
            afa_kulcs=afa_kulcs
        )
        return termek

    @staticmethod
    async def get_termek(termek_id: int):
        """Termék adatainak lekérdezése ID alapján."""
        try:
            termek = await Termek.get(id=termek_id)
            return termek
        except DoesNotExist:
            return None

    @staticmethod
    async def update_termek(termek_id: int, nev: str = None, ar: float = None, afa_kulcs: int = None):
        """Termék adatainak módosítása."""
        try:
            termek = await Termek.get(id=termek_id)
            if nev:
                termek.nev = nev
            if ar:
                termek.ar = ar
            if afa_kulcs:
                termek.afa_kulcs = afa_kulcs
            await termek.save()
            return termek
        except DoesNotExist:
            return None

    @staticmethod
    async def delete_termek(termek_id: int):
        """Termék törlése ID alapján."""
        try:
            termek = await Termek.get(id=termek_id)
            await termek.delete()
            return True
        except DoesNotExist:
            return False