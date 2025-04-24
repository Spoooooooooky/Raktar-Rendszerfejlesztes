from models.models import Fuvar
from tortoise.exceptions import DoesNotExist

class FuvarService:
    @staticmethod
    async def add_fuvar(szallitas_datum, beszallito_nev, termekek):
        """Add a new transport (fuvar)."""
        fuvar = await Fuvar.create(
            szallitas_datum=szallitas_datum,
            beszallito_nev=beszallito_nev,
            termekek=termekek
        )
        return fuvar

    @staticmethod
    async def get_fuvar(fuvar_id):
        """Retrieve a transport by ID."""
        try:
            fuvar = await Fuvar.get(id=fuvar_id)
            return fuvar
        except DoesNotExist:
            return None

    @staticmethod
    async def update_fuvar(fuvar_id, **kwargs):
        """Update a transport by ID."""
        try:
            fuvar = await Fuvar.get(id=fuvar_id)
            for key, value in kwargs.items():
                setattr(fuvar, key, value)
            await fuvar.save()
            return fuvar
        except DoesNotExist:
            return None

    @staticmethod
    async def delete_fuvar(fuvar_id):
        """Delete a transport by ID."""
        try:
            fuvar = await Fuvar.get(id=fuvar_id)
            await fuvar.delete()
            return True
        except DoesNotExist:
            return False