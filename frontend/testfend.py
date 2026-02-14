import typer
import httpx
from rich.console import Console
from rich.table import Table
from rich import box

app = typer.Typer()
console = Console()

API_URL = "http://127.0.0.1:8000"

def handle_response(response):
    try:
        if 200 <= response.status_code < 300:
            data = response.json()
            console.print(f"[bold green]Success:[/bold green] {data.get('message', 'Operation successful')}")
        else:
            console.print(f"[bold red]Error {response.status_code}:[/bold red] {response.text}")
    except Exception as e:
        console.print(f"[bold red]Error processing response:[/bold red] {e}")

@app.command()
def add_felhasznalo(
    telefonszam: str = typer.Option(..., prompt="Telefonszám"),
    email: str = typer.Option(..., prompt="Email"),
    nev: str = typer.Option(..., prompt="Név"),
    szerep: str = typer.Option(..., prompt="Szerep")
):
    """Add a user to the database."""
    try:
        response = httpx.post(f"{API_URL}/felhasznalok/", json={"telefonszam": telefonszam, "email": email, "nev": nev, "szerep": szerep})
        handle_response(response)
    except httpx.RequestError as e:
        console.print(f"[bold red]Connection Error:[/bold red] {e}")

@app.command()
def add_termek(
    nev: str = typer.Option(..., prompt="Termék neve"),
    ar: int = typer.Option(..., prompt="Ár"),
    afa_kulcs: int = typer.Option(..., prompt="ÁFA kulcs")
):
    """Add a product to the database."""
    try:
        response = httpx.post(f"{API_URL}/termekek/", json={"nev": nev, "ar": ar, "afa_kulcs": afa_kulcs})
        handle_response(response)
    except httpx.RequestError as e:
        console.print(f"[bold red]Connection Error:[/bold red] {e}")

@app.command()
def add_rendeles(
    termek: int = typer.Option(..., prompt="Termék ID"),
    mennyiseg: int = typer.Option(..., prompt="Mennyiség"),
    allapot: str = typer.Option(..., prompt="Állapot"),
    megrendelo: int = typer.Option(..., prompt="Megrendelő ID"),
    szallitasi_cim: str = typer.Option(..., prompt="Szállítási cím")
):
    """Add an order to the database."""
    try:
        response = httpx.post(f"{API_URL}/rendelesek/", json={"termek": termek, "mennyiseg": mennyiseg, "allapot": allapot, "megrendelo": megrendelo, "szallitasi_cim": szallitasi_cim})
        handle_response(response)
    except httpx.RequestError as e:
        console.print(f"[bold red]Connection Error:[/bold red] {e}")

@app.command()
def add_beszallitas(
    urlap: int = typer.Option(..., prompt="Űrlap ID"),
    beszallito: int = typer.Option(..., prompt="Beszállító ID")
):
    """Add a delivery to the database."""
    try:
        response = httpx.post(f"{API_URL}/beszallitasok/", json={"urlap": urlap, "beszallito": beszallito})
        handle_response(response)
    except httpx.RequestError as e:
        console.print(f"[bold red]Connection Error:[/bold red] {e}")

@app.command()
def add_urlap(
    termek: int = typer.Option(..., prompt="Termék ID"),
    mennyiseg: int = typer.Option(..., prompt="Mennyiség")
):
    """Add a form to the database."""
    try:
        response = httpx.post(f"{API_URL}/urlapok/", json={"termek": termek, "mennyiseg": mennyiseg})
        handle_response(response)
    except httpx.RequestError as e:
        console.print(f"[bold red]Connection Error:[/bold red] {e}")

@app.command()
def add_fuvar(
    rendeles: int = typer.Option(..., prompt="Rendelés ID"),
    allapot: str = typer.Option(..., prompt="Állapot"),
    fuvarozo: int = typer.Option(..., prompt="Fuvarozó ID")
):
    """Add a transport to the database."""
    try:
        response = httpx.post(f"{API_URL}/fuvarok/", json={"rendeles": rendeles, "allapot": allapot, "fuvarozo": fuvarozo})
        handle_response(response)
    except httpx.RequestError as e:
        console.print(f"[bold red]Connection Error:[/bold red] {e}")

@app.command()
def add_tarhely(
    termek: int = typer.Option(..., prompt="Termék ID"),
    mennyiseg: int = typer.Option(..., prompt="Mennyiség")
):
    """Add a storage to the database."""
    try:
        response = httpx.post(f"{API_URL}/tarhelyek/", json={"termek": termek, "mennyiseg": mennyiseg})
        handle_response(response)
    except httpx.RequestError as e:
        console.print(f"[bold red]Connection Error:[/bold red] {e}")

@app.command()
def clear_data():
    """Delete all data from the database."""
    try:
        response = httpx.delete(f"{API_URL}/adatok-torlese/")
        handle_response(response)
    except httpx.RequestError as e:
        console.print(f"[bold red]Connection Error:[/bold red] {e}")

@app.command()
def list_tables():
    """List available tables."""
    try:
        response = httpx.get(f"{API_URL}/tablak/")
        if response.status_code == 200:
            tables = response.json()
            rich_table = Table(title="Available Tables", box=box.ROUNDED)
            rich_table.add_column("Table Name", style="cyan")
            for table in tables:
                rich_table.add_row(table)
            console.print(rich_table)
        else:
            console.print(f"[bold red]Error {response.status_code}:[/bold red] {response.text}")
    except httpx.RequestError as e:
        console.print(f"[bold red]Connection Error:[/bold red] {e}")

@app.command()
def get_table_content(
    table: str = typer.Option(..., prompt="Tábla neve"),
    rows: int = typer.Option(10)
):
    """Get content of a table."""
    try:
        response = httpx.get(f"{API_URL}/tabla-tartalom/", params={"table": table, "rows": rows})
        if response.status_code == 200:
            data = response.json()
            if not data:
                console.print(f"[yellow]A(z) '{table}' tábla üres.[/yellow]")
                return

            rich_table = Table(title=f"Tábla: {table}", box=box.ROUNDED)
            
            # Create headers from the first item keys
            headers = list(data[0].keys())
            for header in headers:
                rich_table.add_column(str(header), style="cyan")
            
            for row in data:
                rich_table.add_row(*[str(row.get(h, "")) for h in headers])
            
            console.print(rich_table)
        else:
            console.print(f"[bold red]Error {response.status_code}:[/bold red] {response.text}")
    except httpx.RequestError as e:
        console.print(f"[bold red]Connection Error:[/bold red] {e}")

if __name__ == "__main__":
    app()