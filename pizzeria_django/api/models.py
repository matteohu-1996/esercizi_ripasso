from django.db import models


class Ingrediente(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    prezzo_extra = models.FloatField(default=0.0)
    allergene = models.BooleanField(default=False)
    vegetariano =models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    telefono = models.CharField(max_length=30, unique=True)
    indirizzo = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Ordine(models.Model):
    POSSIBILI_STATI = [
        ("ricevuto", "Ricevuto"),
        ("in_preparazione", "In preparazione"),
        ("pronto", "Pronto"),
        ("consegnato", "Consegnato"),
    ]

    data_ora = models.DateTimeField()
    stato = models.CharField(max_length=10, choices=POSSIBILI_STATI, default="ricevuto")
    note = models.TextField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, related_name="ordini")

    def __str__(self):
        return f"Ordine #{self.pk} - {self.cliente.nome} - {self.stato}"


class Pizza(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    prezzo_base = models.FloatField()
    descrizione = models.CharField(max_length=100, blank=True, null=True)
    disponibile = models.BooleanField(default=True)
    ingredienti = models.ManyToManyField(Ingrediente, blank=True, related_name="pizze")

    @property
    def prezzo_totale(self):
        return self.prezzo_base + sum(i.prezzo for i in self.ingredienti.all())

    def __str__(self):
        return self.nome

class VocePizzaOrdine(models.Model):
    ordine = models.ForeignKey(Ordine, on_delete=models.CASCADE, related_name="voci")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="voci")
    quantita = models.IntegerField(default=1)
    ingredienti_extra = models.ManyToManyField(Ingrediente, blank=True, related_name="voci_extra")

    def __str__(self):
        return f"{self.pizza.nome} - {self.quantita}"