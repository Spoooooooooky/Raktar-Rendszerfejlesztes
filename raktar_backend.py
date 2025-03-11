from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from tortoise import fields, models
from pydantic import BaseModel

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

@app.post("/add-product/")
async def add_product(name: str, stock: int):
    product = await Product.create(name=name, stock=stock)
    return {"message": "Product added", "product_id": product.id}

@app.delete("/clear-data/")
async def clear_data():
    await Product.all().delete()
    return {"message": "All data cleared"}

# Adatbázis konfiguráció és migráció
TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {"models": ["raktar_backend", "aerich.models"], "default_connection": "default"}
    }
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
def start():
    uvicorn.run("raktar_backend:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    start()
