import asyncio
import httpx

from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Input, Label, Button, Static, DataTable, ListView, ListItem, Select
from textual.containers import Horizontal, Vertical, Container

API_URL = "http://127.0.0.1:8000"

class LoginScreen(ModalScreen):
    """Screen with a dialog to enter username and password."""

    def compose(self) -> ComposeResult:
        yield Static("Raktar Login", classes="header")
        yield Label("Username")
        yield Input(placeholder="Username", id="username")
        yield Label("Password")
        yield Input(placeholder="Password", password=True, id="password")
        yield Label("", id="login_status", classes="error")
        yield Button("Log In", variant="primary", id="login")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "login":
            username = self.query_one("#username", Input).value
            password = self.query_one("#password", Input).value
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{API_URL}/login/", json={"nev": username, "jelszo": password})
                    response.raise_for_status()
                    data = response.json()
                
                self.app.current_user = data["nev"]
                self.app.user_role = data["szerep"]
                self.app.user_id = data["user_id"]
                self.app.post_login_setup()
                self.app.pop_screen()
            except httpx.HTTPStatusError as e:
                try:
                    error_msg = e.response.json().get("detail", "Login failed")
                except:
                    error_msg = str(e)
                self.query_one("#login_status").update(f"Error: {error_msg}")
            except Exception as e:
                self.query_one("#login_status").update(f"Login failed: {e}")

class ProfileDialog(ModalScreen):
    """Dialog to edit user profile."""

    def compose(self) -> ComposeResult:
        yield Static("Profil Szerkesztése", classes="header")
        yield Label("Név")
        yield Input(id="nev", placeholder="Név")
        yield Label("Email")
        yield Input(id="email", placeholder="Email")
        yield Label("Telefonszám")
        yield Input(id="telefonszam", placeholder="Telefonszám")
        yield Label("Cím")
        yield Input(id="cim", placeholder="Cím")
        yield Label("Új Jelszó (hagyja üresen, ha nem változtatja)")
        yield Input(id="jelszo", placeholder="Új jelszó", password=True)
        yield Label("", id="profile_status", classes="error")
        yield Button("Mentés", variant="primary", id="save")
        yield Button("Mégse", variant="error", id="cancel")

    async def on_mount(self):
        """Fetch user data when the dialog is mounted."""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{API_URL}/felhasznalok/{self.app.user_id}")
                resp.raise_for_status()
                data = resp.json()
                self.query_one("#nev", Input).value = data.get("nev", "")
                self.query_one("#email", Input).value = data.get("email", "")
                self.query_one("#telefonszam", Input).value = data.get("telefonszam", "")
                self.query_one("#cim", Input).value = data.get("cim", "")
        except Exception as e:
            self.query_one("#profile_status").update(f"Hiba a betöltéskor: {e}")

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "cancel":
            self.app.pop_screen()
        elif event.button.id == "save":
            data_to_update = {
                "nev": self.query_one("#nev", Input).value,
                "email": self.query_one("#email", Input).value,
                "telefonszam": self.query_one("#telefonszam", Input).value,
                "cim": self.query_one("#cim", Input).value,
            }
            
            new_password = self.query_one("#jelszo", Input).value
            if new_password:
                data_to_update["jelszo"] = new_password

            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.put(
                        f"{API_URL}/felhasznalok/{self.app.user_id}",
                        json=data_to_update
                    )
                    resp.raise_for_status()
                
                self.app.notify("Profil sikeresen frissítve!")
                # Update current_user name if it changed
                if self.app.current_user != data_to_update["nev"]:
                    self.app.current_user = data_to_update["nev"]
                    self.app.notify(f"Bejelentkezve: {self.app.current_user} ({self.app.user_role})")
                
                self.app.pop_screen()
            except Exception as e:
                self.query_one("#profile_status").update(f"Hiba a mentéskor: {e}")


class OrderDialog(ModalScreen):
    """Dialog to place an order."""
    def __init__(self, product_id, product_name, product_price):
        super().__init__()
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price

    def compose(self) -> ComposeResult:
        yield Static(f"Rendelés: {self.product_name} ({self.product_price})", classes="header")
        yield Label("Mennyiség")
        yield Input(value="1", id="quantity")
        
        if self.app.user_role == "admin":
            yield Label("Rendelés leadása más nevében:")
            yield Select([], id="user_select", prompt="Válassz felhasználót")
        
        yield Button("Rendelés Leadása", variant="primary", id="submit")
        yield Button("Mégse", variant="error", id="cancel")

    async def on_mount(self):
        if self.app.user_role == "admin":
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(f"{API_URL}/tabla-tartalom/?table=Felhasznalok&rows=100")
                    if resp.status_code == 200:
                        users = resp.json()
                        options = [(f"{u['nev']} ({u['email']})", u['id']) for u in users]
                        self.query_one("#user_select").set_options(options)
            except:
                pass

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "cancel":
            self.app.pop_screen()
        elif event.button.id == "submit":
            try:
                qty = int(self.query_one("#quantity").value)
                user_id = self.app.user_id
                
                if self.app.user_role == "admin":
                    sel = self.query_one("#user_select")
                    if sel.value != Select.BLANK:
                        user_id = sel.value
                    else:
                        self.app.notify("Válassz felhasználót!", severity="error")
                        return

                async with httpx.AsyncClient() as client:
                    # Get user's address
                    user_resp = await client.get(f"{API_URL}/felhasznalok/{user_id}")
                    user_data = user_resp.json()
                    szallitasi_cim = user_data.get("cim") or "Nincs cím megadva"

                    await client.post(f"{API_URL}/rendelesek/", json={
                        "termek_id": self.product_id,
                        "mennyiseg": qty,
                        "allapot": "Leadva",
                        "megrendelo_id": user_id,
                        "szallitasi_cim": szallitasi_cim
                    })
                self.app.notify("Rendelés sikeresen leadva!")
                self.app.pop_screen()
            except Exception as e:
                self.app.notify(f"Hiba: {e}", severity="error")

class EditOrderDialog(ModalScreen):
    """Dialog to edit order status or delete."""
    def __init__(self, order_id, current_status):
        super().__init__()
        self.order_id = order_id
        self.current_status = current_status

    def compose(self) -> ComposeResult:
        yield Static(f"Rendelés szerkesztése #{self.order_id}", classes="header")
        
        role = self.app.user_role
        if role in ["admin", "storage"]:
            yield Label("Állapot")
            options = []
            if role == "admin":
                options = [("Leadva", "Leadva"), ("Folyamatban", "Folyamatban"), ("Előkészítve", "Előkészítve"), ("Kiszállítva", "Kiszállítva")]
            elif role == "storage":
                options = [("Folyamatban", "Folyamatban"), ("Előkészítve", "Előkészítve")]
            
            if self.current_status and self.current_status not in [opt[1] for opt in options]:
                options.append((self.current_status, self.current_status))

            yield Select(options, value=self.current_status, id="status_select")
        else:
            yield Label(f"Jelenlegi állapot: {self.current_status}")

        with Horizontal(classes="buttons"):
            if role in ["admin", "storage"]:
                yield Button("Mentés", variant="primary", id="save")
            if role == "admin":
                yield Button("Törlés", variant="error", id="delete")
            yield Button("Bezárás", id="close")

    async def on_button_pressed(self, event):
        if event.button.id == "close":
            self.app.pop_screen()
        elif event.button.id == "delete":
            async with httpx.AsyncClient() as client:
                await client.delete(f"{API_URL}/rendelesek/{self.order_id}")
            self.app.notify("Rendelés törölve")
            self.app.pop_screen()
        elif event.button.id == "save":
            new_status = self.query_one("#status_select").value
            if new_status != Select.BLANK:
                async with httpx.AsyncClient() as client:
                    await client.put(f"{API_URL}/rendelesek/{self.order_id}", json={"allapot": new_status})
                self.app.notify("Rendelés frissítve")
                self.app.pop_screen()

class EditStorageDialog(ModalScreen):
    """Dialog to edit storage quantity."""
    def __init__(self, storage_id, product_name, quantity):
        super().__init__()
        self.storage_id = storage_id
        self.product_name = product_name
        self.quantity = quantity

    def compose(self):
        yield Static(f"Raktár: {self.product_name}", classes="header")
        yield Label("Mennyiség (0 a törléshez)")
        yield Input(value=str(self.quantity), id="qty")
        yield Button("Mentés", variant="primary", id="save")
        yield Button("Mégse", id="cancel")

    async def on_button_pressed(self, event):
        if event.button.id == "cancel":
            self.app.pop_screen()
        elif event.button.id == "save":
            try:
                qty = int(self.query_one("#qty").value)
                async with httpx.AsyncClient() as client:
                    if qty <= 0:
                        await client.delete(f"{API_URL}/tarhelyek/{self.storage_id}")
                        self.app.notify("Tétel törölve a raktárból")
                    else:
                        await client.put(f"{API_URL}/tarhelyek/{self.storage_id}", json={"mennyiseg": qty})
                        self.app.notify("Raktárkészlet frissítve")
                self.app.pop_screen()
            except Exception as e:
                self.app.notify(f"Hiba: {e}")

class ProductView(Container):
    def compose(self):
        yield DataTable(cursor_type="row")

    async def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("ID", "Név", "Ár")
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API_URL}/termekek/")
            for p in resp.json():
                table.add_row(p["id"], p["nev"], f"{p['ar']} Ft")

    def on_data_table_row_selected(self, event):
        row = self.query_one(DataTable).get_row_at(event.cursor_row)
        self.app.push_screen(OrderDialog(row[0], row[1], row[2]))

class OrderView(Container):
    def compose(self):
        yield DataTable(cursor_type="row")
        yield Button("Frissítés", id="refresh")

    async def on_mount(self):
        await self.load_data()

    async def on_button_pressed(self, event):
        if event.button.id == "refresh":
            await self.load_data()

    async def load_data(self):
        table = self.query_one(DataTable)
        table.clear(columns=True)
        
        role = self.app.user_role
        if role == "customer":
            table.add_columns("Termék", "Mennyiség", "Állapot")
        else:
            table.add_columns("ID", "Felhasználó", "Termék", "Mennyiség", "Állapot")

        async with httpx.AsyncClient() as client:
            orders_resp = await client.get(f"{API_URL}/tabla-tartalom/?table=Rendelesek&rows=100")
            prod_resp = await client.get(f"{API_URL}/termekek/")
            products = {p["id"]: p["nev"] for p in prod_resp.json()}
            
            users = {}
            if role != "customer":
                user_resp = await client.get(f"{API_URL}/tabla-tartalom/?table=Felhasznalok&rows=100")
                users = {u["id"]: u["nev"] for u in user_resp.json()}

            for o in orders_resp.json():
                if role == "customer" and o["megrendelo_id"] != self.app.user_id:
                    continue
                
                p_name = products.get(o["termek_id"], str(o["termek_id"]))
                
                if role == "customer":
                    table.add_row(p_name, str(o["mennyiseg"]), o["allapot"], key=str(o["id"]))
                else:
                    u_name = users.get(o["megrendelo_id"], str(o["megrendelo_id"]))
                    table.add_row(str(o["id"]), u_name, p_name, str(o["mennyiseg"]), o["allapot"], key=str(o["id"]))

    def on_data_table_row_selected(self, event):
        if self.app.user_role == "customer":
            return
        
        row = self.query_one(DataTable).get_row_at(event.cursor_row)
        order_id = row[0]
        status = row[4]
        self.app.push_screen(EditOrderDialog(order_id, status))

class StorageView(Container):
    def compose(self):
        yield DataTable(cursor_type="row")
        yield Button("Frissítés", id="refresh")

    async def on_mount(self):
        await self.load_data()

    async def on_button_pressed(self, event):
        if event.button.id == "refresh":
            await self.load_data()

    async def load_data(self):
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns("Termék", "Mennyiség")
        
        async with httpx.AsyncClient() as client:
            storage_resp = await client.get(f"{API_URL}/tabla-tartalom/?table=Tarhelyek&rows=100")
            prod_resp = await client.get(f"{API_URL}/termekek/")
            products = {p["id"]: p["nev"] for p in prod_resp.json()}
            
            for s in storage_resp.json():
                p_name = products.get(s["termek_id"], str(s["termek_id"]))
                table.add_row(p_name, str(s["mennyiseg"]), key=str(s["id"]))

    def on_data_table_row_selected(self, event):
        row = self.query_one(DataTable).get_row(event.row_key)
        self.app.push_screen(EditStorageDialog(event.row_key, row[0], row[1]))

class RaktarApp(App):
    """A Textual TUI for the Raktar project."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("q", "quit", "Quit")]

    CSS = """
    .error {
        color: red;
    }
    #sidebar {
        width: 25;
        background: $panel;
        border-right: vkey $primary;
        dock: left;
        height: 100%;
    }
    #content {
        height: 100%;
        width: 1fr;
        padding: 1;
    }
    .header {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    .buttons {
        height: 3;
        margin-top: 1;
        align: center middle;
    }
    Button {
        margin: 0 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.current_user = None
        self.user_role = None
        self.user_id = None

    def on_mount(self) -> None:
        self.push_screen(LoginScreen())

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Horizontal(
            Vertical(
                ListView(
                    ListItem(Label("Termékek"), id="menu_products"),
                    ListItem(Label("Rendelések"), id="menu_orders"),
                    ListItem(Label("Raktár"), id="menu_storage"),
                    ListItem(Label("Profil"), id="menu_profile"),
                    id="main_menu"
                ),
                id="sidebar"
            ),
            Container(id="content")
        )
        yield Footer()

    def post_login_setup(self):
        """Adjust UI based on user role."""
        # Filter menu items based on role
        menu = self.query_one("#main_menu")
        # Everyone sees Products and Orders
        # Only Admin and Storage see Storage
        if self.user_role == "customer":
            # Hide storage menu item (index 2)
            # Textual ListView doesn't easily support hiding items, but we can just not mount the view if clicked
            # or rebuild the list. For simplicity, we'll just handle the click logic.
            pass
        
        # Load initial view
        self.query_one("#content").mount(ProductView())
        self.notify(f"Bejelentkezve: {self.current_user} ({self.user_role})")

    async def on_list_view_selected(self, event: ListView.Selected):
        content = self.query_one("#content")
        content.remove_children()
        
        if event.item.id == "menu_products":
            content.mount(ProductView())
        elif event.item.id == "menu_orders":
            content.mount(OrderView())
        elif event.item.id == "menu_storage":
            if self.user_role in ["admin", "storage"]:
                content.mount(StorageView())
            else:
                self.notify("Nincs jogosultságod ehhez a menüponthoz.", severity="warning")
                content.mount(Static("Hozzáférés megtagadva."))
        elif event.item.id == "menu_profile":
            self.push_screen(ProfileDialog())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

async def main():
    app = RaktarApp()
    await app.run_async()

if __name__ == "__main__":
    asyncio.run(main())
