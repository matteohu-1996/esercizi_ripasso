from rest_framework import serializers
from .models import Ingrediente, Pizza, Cliente, Ordine, VocePizzaOrdine

class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ["id", "nome", "prezzo_extra", "allergene", "vegetariano"]

class PizzaSerializer(serializers.ModelSerializer):
    ingredienti = IngredienteSerializer(many=True, read_only=True)
    ingredienti_id = serializers.PrimaryKeyRelatedField(
        many=True,queryset=Ingrediente.objects.all(),write_only=True,source="ingredienti",required=False
    )
    prezzo_totale = serializers.FloatField(read_only=True)

    class Meta:
        model = Pizza
        fields = ["id", "prezzo_base", "descrizione", "disponibilità", "prezzo_totale","ingredienti", "ingredienti_id"]


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nome", "telefono", "indirizzo"]



class VoceOrdineCreateSerializer(serializers.ModelSerializer):
    pizza_id = serializers.IntegerField()
    quantita = serializers.IntegerField(min_value=1)
    ingredienti_extra_ids = serializers.ListField(
        child=serializers.IntegerField(),
        default=list
    )

class VoceOrdineSerializer(serializers.ModelSerializer):
    pizza = PizzaSerializer(read_only=True)
    ingredienti_extra = IngredienteSerializer(many=True, read_only=True)

    class Meta:
        model = Ordine
        fields = ["id", "data_ora", "stato", "note", "cliente", "voci"]