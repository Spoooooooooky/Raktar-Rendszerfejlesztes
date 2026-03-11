import httpx
import asyncio

API_URL = "http://127.0.0.1:8000"

async def clear_all_data():
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{API_URL}/adatok-torlese/")
        print(f"Adatbázis törlése: {response.json().get('message')}")

async def create_user(telefonszam, email, nev, szerep, jelszo="admin"):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/felhasznalok/", json={"telefonszam": telefonszam, "email": email, "nev": nev, "szerep": szerep, "jelszo": jelszo})
        print(response.json().get("message"))

async def create_product(nev, ar, afa_kulcs):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/termekek/", json={"nev": nev, "ar": ar, "afa_kulcs": afa_kulcs})
        print(response.json().get("message"))

async def create_order(termek_id, mennyiseg, allapot, megrendelo_id, szallitasi_cim):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/rendelesek/", json={"termek_id": termek_id, "mennyiseg": mennyiseg, "allapot": allapot, "megrendelo_id": megrendelo_id, "szallitasi_cim": szallitasi_cim})
        print(response.json().get("message"))

async def create_delivery(termek_id, mennyiseg, beszallito_nev):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/beszallitasok/", json={"termek_id": termek_id, "mennyiseg": mennyiseg, "beszallito_nev": beszallito_nev})
        print(response.json().get("message"))

async def create_form(beszallito_nev, datum, termekek):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/urlapok/", json={"beszallito_nev": beszallito_nev, "datum": datum, "termekek": termekek})
        print(response.json().get("message"))

async def create_transport(szallitas_datum, beszallito_nev, termekek):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/fuvarok/", json={"szallitas_datum": szallitas_datum, "beszallito_nev": beszallito_nev, "termekek": termekek})
        print(response.json().get("message"))

async def create_storage(termek_id, mennyiseg):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/tarhelyek/", json={"termek_id": termek_id, "mennyiseg": mennyiseg})
        print(response.json().get("message"))

async def main():
    # Előző adatok törlése a tiszta lap érdekében
    await clear_all_data()

    # Create users
    await create_user("123456789", "admin@example.com", "admin", "admin")
    await create_user("234567890", "storage1@example.com", "Storage1", "storage")
    await create_user("345678901", "storage2@example.com", "Storage2", "storage")
    await create_user("456789012", "customer1@example.com", "Customer1", "customer")
    await create_user("567890123", "customer2@example.com", "Customer2", "customer")
    await create_user("678901234", "customer3@example.com", "Customer3", "customer")

    # Create products
    await create_product("Termék 1", 150000, 27)
    await create_product("Termék 2", 100000, 18)
    await create_product("Termék 3", 50000, 5)

    # Create orders
    await create_order(1, 5, "Leadva", 4, "1051 Budapest, Fő utca 1.")
    await create_order(2, 2, "Leadva", 5, "4024 Debrecen, Kossuth tér 5.")
    await create_order(3, 1, "Leadva", 6, "6720 Szeged, Dóm tér 1.")

    # Create deliveries
    await create_delivery(1, 100, "Beszállító Kft.")
    await create_delivery(2, 50, "TechWorld Zrt.")

    # Create forms
    await create_form("Beszállító Kft.", "2023-10-25", [{"termek_id": 1, "mennyiseg": 100}, {"termek_id": 2, "mennyiseg": 20}])
    await create_form("TechWorld Zrt.", "2023-10-26", [{"termek_id": 3, "mennyiseg": 50}])

    # Create transports
    await create_transport("2023-10-28", "Logisztika Express", [{"rendeles_id": 1, "statusz": "Uton"}])
    await create_transport("2023-10-29", "GyorsFuvar Kft.", [{"rendeles_id": 2, "statusz": "Kezbesitve"}])

    # Create storage entries
    await create_storage(1, 500)
    await create_storage(2, 200)
    await create_storage(3, 100)

if __name__ == "__main__":
    asyncio.run(main())