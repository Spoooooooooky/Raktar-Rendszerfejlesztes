import typer
import httpx

app = typer.Typer()

API_URL = "http://127.0.0.1:8000"

@app.command()
def add_felhasznalo(telefonszam: str = typer.Option(...), email: str = typer.Option(...), nev: str = typer.Option(...), szerep: str = typer.Option(...)):
    """Add a user to the database."""
    response = httpx.post(f"{API_URL}/felhasznalok/", json={"telefonszam": telefonszam, "email": email, "nev": nev, "szerep": szerep})
    typer.echo(response.json().get("message"))

@app.command()
def add_termek(nev: str = typer.Option(...), ar: int = typer.Option(...), afa_kulcs: int = typer.Option(...)):
    """Add a product to the database."""
    response = httpx.post(f"{API_URL}/termekek/", json={"nev": nev, "ar": ar, "afa_kulcs": afa_kulcs})
    typer.echo(response.json().get("message"))

@app.command()
def add_rendeles(termek: int = typer.Option(...), mennyiseg: int = typer.Option(...), allapot: str = typer.Option(...), megrendelo: int = typer.Option(...), szallitasi_cim: str = typer.Option(...)):
    """Add an order to the database."""
    response = httpx.post(f"{API_URL}/rendelesek/", json={"termek": termek, "mennyiseg": mennyiseg, "allapot": allapot, "megrendelo": megrendelo, "szallitasi_cim": szallitasi_cim})
    typer.echo(response.json().get("message"))

@app.command()
def add_beszallitas(urlap: int = typer.Option(...), beszallito: int = typer.Option(...)):
    """Add a delivery to the database."""
    response = httpx.post(f"{API_URL}/beszallitasok/", json={"urlap": urlap, "beszallito": beszallito})
    typer.echo(response.json().get("message"))

@app.command()
def add_urlap(termek: int = typer.Option(...), mennyiseg: int = typer.Option(...)):
    """Add a form to the database."""
    response = httpx.post(f"{API_URL}/urlapok/", json={"termek": termek, "mennyiseg": mennyiseg})
    typer.echo(response.json().get("message"))

@app.command()
def add_fuvar(rendeles: int = typer.Option(...), allapot: str = typer.Option(...), fuvarozo: int = typer.Option(...)):
    """Add a transport to the database."""
    response = httpx.post(f"{API_URL}/fuvarok/", json={"rendeles": rendeles, "allapot": allapot, "fuvarozo": fuvarozo})
    typer.echo(response.json().get("message"))

@app.command()
def add_tarhely(termek: int = typer.Option(...), mennyiseg: int = typer.Option(...)):
    """Add a storage to the database."""
    response = httpx.post(f"{API_URL}/tarhelyek/", json={"termek": termek, "mennyiseg": mennyiseg})
    typer.echo(response.json().get("message"))

@app.command()
def clear_data():
    """Delete all data from the database."""
    response = httpx.delete(f"{API_URL}/adatok-torlese/")
    typer.echo(response.json().get("message"))

@app.command()
def get_table_content(table: str = typer.Option(...), rows: int = typer.Option(10)):
    """Get content of a table."""
    response = httpx.get(f"{API_URL}/tabla-tartalom/", params={"table": table, "rows": rows})
    data = response.json()
    for row in data:
        typer.echo(", ".join(f"{key}: {value}" for key, value in row.items()))

if __name__ == "__main__":
    app()