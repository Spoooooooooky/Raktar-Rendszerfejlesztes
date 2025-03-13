import httpx
import asyncio

API_URL = "http://127.0.0.1:8000"

async def create_user(telefonszam, email, nev, szerep):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/felhasznalok/", json={"telefonszam": telefonszam, "email": email, "nev": nev, "szerep": szerep})
        print(response.json().get("message"))

async def create_product(nev, ar, afa_kulcs):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/termekek/", json={"nev": nev, "ar": ar, "afa_kulcs": afa_kulcs})
        print(response.json().get("message"))

async def main():
    # Create users
    await create_user("123456789", "admin@example.com", "Admin User", "admin")
    await create_user("234567890", "storage1@example.com", "Storage User 1", "storage")
    await create_user("345678901", "storage2@example.com", "Storage User 2", "storage")
    await create_user("456789012", "customer1@example.com", "Customer User 1", "customer")
    await create_user("567890123", "customer2@example.com", "Customer User 2", "customer")
    await create_user("678901234", "customer3@example.com", "Customer User 3", "customer")

    # Create products
    await create_product("Termék 1", 150000, 27)
    await create_product("Termék 2", 100000, 18)
    await create_product("Termék 3", 50000, 5)

if __name__ == "__main__":
    asyncio.run(main())