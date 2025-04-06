from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction
from models.models import Felhasznalo

class UserService:
    @staticmethod
    async def add_user(telefonszam: str, email: str, nev: str, szerep: str):
        """Új felhasználó hozzáadása."""
        user = await Felhasznalo.create(
            telefonszam=telefonszam,
            email=email,
            nev=nev,
            szerep=szerep
        )
        return user

    @staticmethod
    async def get_user(user_id: int):
        """Felhasználó adatainak lekérdezése ID alapján."""
        try:
            user = await Felhasznalo.get(id=user_id)
            return user
        except DoesNotExist:
            return None

    @staticmethod
    async def update_user(user_id: int, telefonszam: str = None, email: str = None, nev: str = None, szerep: str = None):
        """Felhasználó adatainak módosítása."""
        async with in_transaction():
            try:
                user = await Felhasznalo.get(id=user_id)
                if telefonszam:
                    user.telefonszam = telefonszam
                if email:
                    user.email = email
                if nev:
                    user.nev = nev
                if szerep:
                    user.szerep = szerep
                await user.save()
                return user
            except DoesNotExist:
                return None

    @staticmethod
    async def delete_user(user_id: int):
        """Felhasználó törlése ID alapján."""
        try:
            user = await Felhasznalo.get(id=user_id)
            await user.delete()
            return True
        except DoesNotExist:
            return False