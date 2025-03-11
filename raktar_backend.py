from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import fields, models
from pydantic import BaseModel

# !!! OLVASD EL AZ info.md FILE-T !!!

app = FastAPI()

# Modellek
class Customer(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    phone = fields.CharField(max_length=20, unique=True)

class Supplier(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    contact_email = fields.CharField(max_length=100, unique=True)

class Carrier(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    vehicle_number = fields.CharField(max_length=50, unique=True)

class WarehouseWorker(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    employee_id = fields.CharField(max_length=50, unique=True)

class Product(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    stock = fields.IntField(default=0)

class Order(models.Model):
    id = fields.IntField(pk=True)
    customer = fields.ForeignKeyField("models.Customer", related_name="orders")
    product = fields.ForeignKeyField("models.Product", related_name="orders")
    quantity = fields.IntField()
    status = fields.CharField(max_length=50, default="pending")
    created_at = fields.DatetimeField(auto_now_add=True)

# Pydantic modellek
class Order_Pydantic(BaseModel):
    customer: int
    product: int
    quantity: int
    status: str

@app.post("/orders/")
async def create_order(order: Order_Pydantic):
    new_order = await Order.create(**order.dict())
    return {"message": "Order created", "order_id": new_order.id}

@app.get("/orders/")
async def list_orders():
    orders = await Order.all().values()
    return orders

# Adatbázis konfiguráció és migráció
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": [__name__]},
    generate_schemas=False,  # Mivel aerich-t használunk migrációra
    add_exception_handlers=True,
)
