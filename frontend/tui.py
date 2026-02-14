from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, DataTable, Button, Label, ListView, ListItem, Static, Input
from textual.screen import Screen
import httpx
import json

API_URL = "http://127.0.0.1:8000"

class DataEntryScreen(Screen):
    def __init__(self, table_name: str, on_save: callable = None):
        super().__init__()
        self.table_name = table_name
        self.on_save = on_save
        self.inputs = {}

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Label(f"Add new item to {self.table_name}", classes="form-title")
            
            fields = self.get_fields(self.table_name)
            for field_key, field_label in fields.items():
                yield Label(field_label)
                inp = Input(placeholder=field_label, id=field_key)
                self.inputs[field_key] = inp
                yield inp

            with Horizontal(classes="buttons"):
                yield Button("Save", variant="success", id="save-btn")
                yield Button("Cancel", variant="error", id="cancel-btn")

    def get_fields(self, table_name):
        if table_name == "Felhasznalok":
            return {"telefonszam": "Telefonszám", "email": "Email", "nev": "Név", "szerep": "Szerep"}
        elif table_name == "Termekek":
            return {"nev": "Név", "ar": "Ár", "afa_kulcs": "ÁFA Kulcs"}
        elif table_name == "Rendelesek":
            return {"termek_id": "Termék ID", "mennyiseg": "Mennyiség", "allapot": "Állapot", "megrendelo_id": "Megrendelő ID", "szallitasi_cim": "Szállítási Cím"}
        elif table_name == "Beszallitasok":
            return {"termek_id": "Termék ID", "mennyiseg": "Mennyiség", "beszallito_nev": "Beszállító Neve"}
        elif table_name == "Urlapok":
            return {"beszallito_nev": "Beszállító Neve", "datum": "Dátum (YYYY-MM-DD)", "termekek": "Termékek (JSON List)"}
        elif table_name == "Fuvarok":
            return {"szallitas_datum": "Szállítás Dátum (YYYY-MM-DD)", "beszallito_nev": "Beszállító Neve", "termekek": "Termékek (JSON List)"}
        elif table_name == "Tarhelyek":
            return {"termek_id": "Termék ID", "mennyiseg": "Mennyiség"}
        return {}

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel-btn":
            self.app.pop_screen()
        elif event.button.id == "save-btn":
            self.save_data()

    def save_data(self):
        data = {}
        for key, inp in self.inputs.items():
            val = inp.value
            if key in ["ar"]:
                try: val = float(val)
                except: pass
            elif key in ["afa_kulcs", "termek_id", "mennyiseg", "megrendelo_id"]:
                try: val = int(val)
                except: pass
            elif key == "termekek":
                try: val = json.loads(val)
                except: pass 
            data[key] = val

        endpoint = self.table_name.lower() + "/"
        try:
            response = httpx.post(f"{API_URL}/{endpoint}", json=data)
            if 200 <= response.status_code < 300:
                self.notify("Item added successfully!")
                if self.on_save:
                    self.on_save()
                self.app.pop_screen()
            else:
                self.notify(f"Error: {response.text}", severity="error")
        except Exception as e:
            self.notify(f"Connection error: {e}", severity="error")

class TableView(Container):
    def __init__(self, table_name: str):
        super().__init__()
        self.table_name = table_name
        self.column_names = []

    def compose(self) -> ComposeResult:
        yield Label(f"Table: {self.table_name}", classes="table-title")
        yield DataTable(cursor_type="row")
        with Horizontal(classes="buttons"):
            yield Button("Add Item", variant="success", id="add-btn")
            yield Button("Delete Item", variant="warning", id="delete-btn")
            yield Button("Refresh", variant="primary", id="refresh-btn")
            yield Button("Clear All Data", variant="error", id="clear-btn")

    def on_mount(self) -> None:
        self.load_data()

    def load_data(self) -> None:
        table = self.query_one(DataTable)
        table.clear(columns=True)
        self.column_names = []
        
        try:
            response = httpx.get(f"{API_URL}/tabla-tartalom/", params={"table": self.table_name, "rows": 100})
            if response.status_code == 200:
                data = response.json()
                if data:
                    headers = list(data[0].keys())
                    self.column_names = headers
                    table.add_columns(*headers)
                    for row in data:
                        table.add_row(*[str(row.get(h)) for h in headers])
            else:
                table.add_column("Error")
                table.add_row(f"Failed to load: {response.text}")
        except Exception as e:
            table.add_column("Error")
            table.add_row(str(e))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-btn":
            self.app.push_screen(DataEntryScreen(self.table_name, self.load_data))
        elif event.button.id == "delete-btn":
            self.delete_selected_item()
        elif event.button.id == "refresh-btn":
            self.load_data()
        elif event.button.id == "clear-btn":
            try:
                httpx.delete(f"{API_URL}/adatok-torlese/")
                self.load_data()
            except:
                pass

    def delete_selected_item(self):
        table = self.query_one(DataTable)
        if table.cursor_row is None:
            self.app.notify("No item selected.", severity="warning")
            return

        try:
            row_index = table.cursor_row
            row_values = table.get_row_at(row_index)
            
            if "id" in self.column_names:
                id_idx = self.column_names.index("id")
                item_id = row_values[id_idx]
                
                endpoint = self.table_name.lower()
                response = httpx.delete(f"{API_URL}/{endpoint}/{item_id}")
                
                if 200 <= response.status_code < 300:
                    self.app.notify("Item deleted.")
                    self.load_data()
                else:
                    self.app.notify(f"Error: {response.text}", severity="error")
            else:
                self.app.notify("Cannot find ID column.", severity="error")
        except Exception as e:
            self.app.notify(f"Error: {e}", severity="error")

class RaktarApp(App):
    CSS = """
    Screen {
        layout: horizontal;
    }
    DataEntryScreen {
        align: center middle;
    }
    #dialog {
        layout: vertical;
        width: 60;
        height: auto;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }
    #sidebar {
        width: 30;
        background: $panel;
        border-right: vkey $primary;
        height: 100%;
    }
    #content {
        width: 1fr;
        height: 100%;
        padding: 1;
    }
    .table-title {
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
    .form-title {
        text-align: center;
        text-style: bold;
        margin: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="sidebar"):
            yield Label("Tables", classes="table-title")
            yield ListView(
                ListItem(Label("Felhasznalok"), id="Felhasznalok"),
                ListItem(Label("Termekek"), id="Termekek"),
                ListItem(Label("Rendelesek"), id="Rendelesek"),
                ListItem(Label("Beszallitasok"), id="Beszallitasok"),
                ListItem(Label("Urlapok"), id="Urlapok"),
                ListItem(Label("Fuvarok"), id="Fuvarok"),
                ListItem(Label("Tarhelyek"), id="Tarhelyek"),
            )
        with Container(id="content"):
            yield Static("Select a table from the sidebar to view contents.", id="placeholder")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        table_name = event.item.id
        content = self.query_one("#content")
        content.remove_children()
        content.mount(TableView(table_name))

if __name__ == "__main__":
    RaktarApp().run()
