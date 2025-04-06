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