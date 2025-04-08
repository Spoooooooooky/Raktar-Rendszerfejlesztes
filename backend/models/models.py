from tortoise import fields, models

class Felhasznalo(models.Model):
    id = fields.IntField(pk=True)
    telefonszam = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    nev = fields.CharField(max_length=100)
    szerep = fields.CharField(max_length=50)

    class Meta:
        table = "felhasznalok"

    def __str__(self):
        return f"{self.nev} ({self.email})"

class Termek(models.Model):
    id = fields.IntField(pk=True)
    nev = fields.CharField(max_length=100)
    ar = fields.FloatField()
    afa_kulcs = fields.IntField()

    class Meta:
        table = "termekek"

    def __str__(self):
        return f"{self.nev} - {self.ar} Ft (ÁFA: {self.afa_kulcs}%)"

class Beszallitas(models.Model):
    id = fields.IntField(pk=True)
    termek_id = fields.IntField()
    mennyiseg = fields.IntField()
    beszallito_nev = fields.CharField(max_length=100)

    class Meta:
        table = "beszallitasok"

    def __str__(self):
        return f"Beszállítás: {self.beszallito_nev}, Termék ID: {self.termek_id}, Mennyiség: {self.mennyiseg}"
    

# Fuvarok kezelése
class Fuvar(models.Model):
    id = fields.IntField(pk=True)
    statusz = fields.CharField(max_length=50, default="Feldolgozás alatt")  
    szallitas_datum = fields.DateField()
    beszallito_nev = fields.CharField(max_length=100)
    termekek = fields.JSONField()  

    class Meta:
        table = "fuvarok"

    def __str__(self):
        return f"Fuvar #{self.id} - {self.statusz}"
