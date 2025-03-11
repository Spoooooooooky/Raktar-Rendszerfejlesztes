import typer
import httpx

app = typer.Typer()

API_URL = "http://127.0.0.1:8000"

@app.command()
def add_data(name: str, stock: int):
    """Add a product to the database."""
    response = httpx.post(f"{API_URL}/add-product/", params={"name": name, "stock": stock})
    typer.echo(response.json())

@app.command()
def clear_data():
    """Delete all data from the database."""
    response = httpx.delete(f"{API_URL}/clear-data/")
    typer.echo(response.json())

if __name__ == "__main__":
    app()
