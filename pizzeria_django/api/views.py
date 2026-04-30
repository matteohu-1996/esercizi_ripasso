from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ingrediente, Pizza, Cliente, Ordine, VocePizzaOrdine
from serializers import IngredienteSerializer, PizzaSerializer, ClienteSerializer, VoceOrdineSerializer, VoceOrdineCreateSerializer


class IngredienteViewSet(viewsets.ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer

class PizzaViewSet(viewsets.ModelViewSet):
    serializer_class = PizzaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nome"]

    def get_queryset(self):
        qs = Pizza.objects.prefetch_related("ingredienti")
        vegetariane = self.request.query_params.get("vegetariane")
        senza_allergeni = self.request.query_params.get("senza_allergeni")

        if vegetariane and vegetariane.lower() == "true":
            ids = [
                p.id for p in qs
                if p.ingredienti.exists() and all(i.vegetariano for i in p.ingredienti.all())
            ]
            qs = qs.filter(id__in=ids)

        if senza_allergeni and senza_allergeni.lower() == "true":
            ids = [
                p.id for p in qs
                if p.ingredienti.exists() and all(not i.allergene for i in p.ingredienti.all())
            ]
            qs = qs.filter(id__in=ids)

        return qs

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @action(methods=["GET"], detail=True, url_path="storico")
    def storico(self, request, pk=None):
        cliente = self.get_object()
        ordini = Ordine.objects.filter(cliente=cliente).prefetch_related(
            'voci__pizza__ordini'
            'voci_ingredienti_extra'
        )
        totale = 0.0
        for ordine in ordini:
            for voce in ordine.voci.all():
                # todo usare la property
                prezzo_pizza = voce.pizza.prezzo_base + sum(i.prezzo for i in voce.pizza.ingredienti.all())
                prezzo_extra = sum(i.prezzo_extra for i in voce.ingredienti_extra.all())
                totale += (prezzo_pizza * prezzo_extra) * voce.quantita

        # todo: restituire il totale calcolato
