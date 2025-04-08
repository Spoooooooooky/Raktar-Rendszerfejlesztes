from tortoise.exceptions import DoesNotExist
from models.models import Beszallitas

class BeszallitasService:
    @staticmethod
    async def add_beszallitas(termek_id: int, mennyiseg: int, beszallito_nev: str):
        """Új beszállítás rögzítése."""
        beszallitas = await Beszallitas.create(
            termek_id=termek_id,
            mennyiseg=mennyiseg,
            beszallito_nev=beszallito_nev
        )
        return beszallitas

    @staticmethod
    async def get_beszallitas(beszallitas_id: int):
        """Beszállítás adatainak lekérdezése ID alapján."""
        try:
            beszallitas = await Beszallitas.get(id=beszallitas_id)
            return beszallitas
        except DoesNotExist:
            return None

    @staticmethod
    async def update_beszallitas(beszallitas_id: int, termek_id: int = None, mennyiseg: int = None, beszallito_nev: str = None):
        """Beszállítás adatainak módosítása."""
        try:
            beszallitas = await Beszallitas.get(id=beszallitas_id)
            if termek_id:
                beszallitas.termek_id = termek_id
            if mennyiseg:
                beszallitas.mennyiseg = mennyiseg
            if beszallito_nev:
                beszallitas.beszallito_nev = beszallito_nev
            await beszallitas.save()
            return beszallitas
        except DoesNotExist:
            return None

    @staticmethod
    async def delete_beszallitas(beszallitas_id: int):
        """Beszállítás törlése ID alapján."""
        try:
            beszallitas = await Beszallitas.get(id=beszallitas_id)
            await beszallitas.delete()
            return True
        except DoesNotExist:
            return False