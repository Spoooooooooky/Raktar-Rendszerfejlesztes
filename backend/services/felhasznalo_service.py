from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction
from models.models import Felhasznalo
import hashlib

class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Egyszerű SHA-256 hash."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    async def add_user(telefonszam: str, email: str, nev: str, szerep: str, jelszo: str, cim: str):
        """Új felhasználó hozzáadása."""
        hashed_pw = UserService.hash_password(jelszo)
        user = await Felhasznalo.create(
            telefonszam=telefonszam,
            email=email,
            nev=nev,
            szerep=szerep,
            jelszo=hashed_pw,
            cim=cim
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
    async def verify_user(nev: str, jelszo: str):
        """Felhasználó ellenőrzése név és jelszó alapján."""
        try:
            user = await Felhasznalo.get(nev=nev)
            if user.jelszo == UserService.hash_password(jelszo):
                return user
        except DoesNotExist:
            pass
        return None

    @staticmethod
    async def update_user(user_id: int, telefonszam: str = None, email: str = None, nev: str = None, szerep: str = None, jelszo: str = None, cim: str = None):
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
                if jelszo:
                    user.jelszo = UserService.hash_password(jelszo)
                if cim:
                    user.cim = cim
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