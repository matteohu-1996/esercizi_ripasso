# Cheatsheet Django + DRF

Riferimento rapido per esercizi tipo pizzeria / università.

---

## 0. Setup iniziale (LA sequenza giusta)

```bash
pip install Django djangorestframework mysqlclient python-dotenv

# 1. Crea il progetto (la cartella esterna NON viene creata, occhio al punto finale)
django-admin startproject pizzeria .

# 2. Crea l'app
python manage.py startapp api

# 3. (configura settings.py: INSTALLED_APPS + DATABASES)

# 4. Migrazioni
python manage.py makemigrations
python manage.py migrate

# 5. Superuser per /admin
python manage.py createsuperuser

# 6. Avvia
python manage.py runserver
```

Server su `http://localhost:8000`. DRF browsable API su ogni endpoint registrato.

### Albero risultante

```
pizzeria_django/
├── manage.py
├── .env
├── pizzeria/                ← project (config)
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py              ← URL globali del progetto
│   ├── asgi.py
│   └── wsgi.py
└── api/                     ← app (logica)
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py       ← solo con DRF
    ├── views.py
    ├── urls.py              ← URL della app (NON creato di default!)
    ├── tests.py
    └── migrations/
        └── __init__.py
```

---

## 1. `settings.py` — cose da modificare SEMPRE

### `INSTALLED_APPS`: aggiungere app + DRF

```python
INSTALLED_APPS = [
    # ... default ...
    'api',                # nome dell'app (deve matchare la cartella)
    'rest_framework',     # se si usa DRF
]
```

### `DATABASES`: connessione MySQL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),     # es: 'localhost'
        'PORT': os.getenv('DB_PORT'),     # es: '3306'
    }
}
```

ENGINE per altri DB:
- SQLite: `'django.db.backends.sqlite3'` + `'NAME': BASE_DIR / 'db.sqlite3'`
- PostgreSQL: `'django.db.backends.postgresql'`

### Variabili .env

In testa a `settings.py`:

```python
import os
from dotenv import load_dotenv
load_dotenv()
```

`.env` (stessa cartella di `manage.py`):

```
DB_NAME=pizzeria
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

Crea il database **prima** del migrate (`CREATE DATABASE pizzeria;`).

---

## 2. URL routing — i due `urls.py` (gotcha classico)

### Project urls (`pizzeria/urls.py`) — già esiste

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),   # delega tutto a api/urls.py
]
```

### App urls (`api/urls.py`) — **DA CREARE A MANO**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PizzaViewSet, CustomerViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'pizzas', PizzaViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

**Nome OBBLIGATORIO**: `urlpatterns` (lista). Senza, Django non trova le rotte.

### Endpoint generati dal router (`ModelViewSet`)

| Metodo | URL                          | Azione   |
|--------|------------------------------|----------|
| GET    | `/api/v1/pizzas/`            | list     |
| POST   | `/api/v1/pizzas/`            | create   |
| GET    | `/api/v1/pizzas/{id}/`       | retrieve |
| PUT    | `/api/v1/pizzas/{id}/`       | update   |
| PATCH  | `/api/v1/pizzas/{id}/`       | partial_update |
| DELETE | `/api/v1/pizzas/{id}/`       | destroy  |

---

## 3. `models.py` — ORM Django

### Tipi di campo comuni

| Python    | Django                                | Note                        |
|-----------|---------------------------------------|-----------------------------|
| str corta | `CharField(max_length=N)`             | `max_length` **obbligatorio** |
| str lunga | `TextField()`                         | senza limite                |
| int       | `IntegerField()`                      |                             |
| float     | `FloatField()`                        |                             |
| decimal   | `DecimalField(max_digits=, decimal_places=)` | per soldi precisi    |
| bool      | `BooleanField(default=False)`         |                             |
| date      | `DateField()`                         |                             |
| datetime  | `DateTimeField(auto_now_add=True)`    | `auto_now_add` = al create  |
| email     | `EmailField()`                        | con validator               |
| url       | `URLField()`                          |                             |

Opzioni comuni: `unique=True`, `blank=True` (form-level), `null=True` (DB-level), `default=...`, `choices=[...]`.

### Modello base

```python
from django.db import models

class Pizza(models.Model):
    name = models.CharField(max_length=80, unique=True)
    price = models.FloatField()

    def __str__(self):
        return self.name
```

`__str__` migliora `/admin` e debug (mostra l'oggetto leggibile).

### Foreign Key (1:N)

```python
class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,        # cliente eliminato -> ordini eliminati
        related_name='orders'            # accesso inverso: customer.orders
    )
    pizza = models.ForeignKey(
        Pizza,
        on_delete=models.PROTECT,        # blocca eliminazione se ci sono ordini
        related_name='orders'
    )
```

Valori `on_delete`:
- `CASCADE` — elimina anche i figli
- `PROTECT` — vieta l'eliminazione del padre
- `SET_NULL` — mette null nei figli (richiede `null=True`)
- `SET_DEFAULT` — usa il default
- `DO_NOTHING` — niente

### Many-to-Many

```python
class Corso(models.Model):
    studenti = models.ManyToManyField(
        Studente,
        blank=True,
        related_name='corsi_seguiti'
    )
```

Django crea **automaticamente** la tabella ponte. Niente da gestire.

### One-to-One

```python
profilo = models.OneToOneField(User, on_delete=models.CASCADE)
```

### Choices

```python
class Order(models.Model):
    STATUS_CHOICES = [
        ('ricevuto', 'Ricevuto'),
        ('pronto', 'Pronto'),
        ('consegnato', 'Consegnato'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ricevuto')
```

### Migrazioni (CICLO obbligato dopo ogni modifica ai modelli)

```bash
python manage.py makemigrations    # genera il file migration
python manage.py migrate           # lo applica al DB
```

Per vedere il SQL di una migrazione:
```bash
python manage.py sqlmigrate api 0001
```

---

## 4. `admin.py` — registra modelli per l'admin panel

```python
from django.contrib import admin
from .models import Pizza, Customer, Order

admin.site.register(Pizza)
admin.site.register(Customer)
admin.site.register(Order)
```

Versione avanzata:

```python
@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']
    list_filter = ['price']
```

---

## 5. `serializers.py` — DRF (l'equivalente Pydantic)

### Pattern base con `ModelSerializer`

```python
from rest_framework import serializers
from .models import Pizza, Customer, Order

class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['id', 'name', 'price']     # oppure '__all__'
```

### Campo calcolato

```python
class PizzaSerializer(serializers.ModelSerializer):
    numero_ordini = serializers.SerializerMethodField()

    class Meta:
        model = Pizza
        fields = ['id', 'name', 'price', 'numero_ordini']

    def get_numero_ordini(self, obj):
        # 'obj' è l'istanza Pizza. Usa il related_name='orders'
        return obj.orders.count()
```

Convenzione: `get_<nome_campo>(self, obj)`.

### Nested / relazioni

```python
class CustomerSerializer(serializers.ModelSerializer):
    # Relazione inversa (related_name='orders'): tutti gli ordini del cliente
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'orders']
```

Altre opzioni per relazioni:
- `serializers.StringRelatedField(many=True, read_only=True)` — usa `__str__`
- `serializers.PrimaryKeyRelatedField(many=True, read_only=True)` — solo gli id

### Validazione custom

```python
def validate_price(self, value):
    if value <= 0:
        raise serializers.ValidationError("Prezzo deve essere positivo")
    return value
```

---

## 6. `views.py` — DRF ViewSets

### `ModelViewSet` (CRUD completo gratis)

```python
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pizza
from .serializers import PizzaSerializer

class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
```

Genera in automatico: list, retrieve, create, update, partial_update, destroy.

### Ricerca + ordinamento

```python
class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'professore__cognome']   # __ per attraversare FK
    ordering_fields = ['price', 'name']
```

URL: `?search=marg&ordering=-price` (`-` = desc).

### Endpoint custom con `@action`

```python
class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer

    # detail=True  -> URL: /pizzas/{id}/orders/
    # detail=False -> URL: /pizzas/orders/
    @action(methods=['GET'], detail=True)
    def orders(self, request, pk=None):
        pizza = self.get_object()
        orders = pizza.orders.all()
        return Response(OrderSerializer(orders, many=True).data)

    @action(methods=['POST'], detail=True)
    def iscrivi(self, request, pk=None):
        corso = self.get_object()
        id_studente = request.data.get('id_studente')
        if not id_studente:
            return Response({"error": "ID mancante"}, status=status.HTTP_400_BAD_REQUEST)
        studente = get_object_or_404(Studente, pk=id_studente)
        corso.studenti.add(studente)
        return Response({"status": "ok"})
```

### View basata su funzione (alternativa light)

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello(request):
    return Response({"msg": "ciao"})
```

---

## 7. ORM Django — query base

```python
# Tutti
Pizza.objects.all()

# Filter (== AND)
Pizza.objects.filter(price__lt=10, name__icontains="marg")

# Singolo
Pizza.objects.get(pk=1)                  # solleva DoesNotExist se manca
Pizza.objects.filter(pk=1).first()       # None se manca

# Esiste?
Pizza.objects.filter(name="X").exists()

# Conteggio
Pizza.objects.count()

# Ordina
Pizza.objects.order_by('-price', 'name')

# Esclude
Pizza.objects.exclude(price=0)

# Slice
Pizza.objects.all()[:10]
```

### Field lookups (operatori filter)

| Lookup           | SQL equivalente             |
|------------------|----------------------------|
| `name="X"`       | `=`                        |
| `name__iexact="X"` | `LIKE` case-insensitive  |
| `name__contains="X"` | `LIKE %X%`             |
| `name__icontains="X"` | LIKE case-insensitive |
| `name__startswith="X"` |                       |
| `price__gt=5`    | `>`                        |
| `price__gte=5`   | `>=`                       |
| `price__lt=5`    | `<`                        |
| `price__lte=5`   | `<=`                       |
| `id__in=[1,2,3]` | `IN`                       |
| `name__isnull=True` | `IS NULL`               |
| `date__year=2025` |                           |

### Attraversare relazioni (doppio underscore)

```python
# Ordini il cui cliente si chiama "Mario"
Order.objects.filter(customer__name="Mario")

# Ordini di pizze sopra i 10€
Order.objects.filter(pizza__price__gt=10)
```

### OR e Q

```python
from django.db.models import Q
Pizza.objects.filter(Q(name="X") | Q(price__lt=5))
```

### Aggregazioni

```python
from django.db.models import Count, Sum, Avg, Min, Max

Pizza.objects.aggregate(media=Avg('price'))            # {'media': 7.5}
Pizza.objects.annotate(num=Count('orders')).order_by('-num')   # ogni pizza con conteggio
```

### Create / Update / Delete

```python
p = Pizza.objects.create(name="Margherita", price=6.0)   # save incluso
p.price = 7.0; p.save()
p.delete()
Pizza.objects.filter(price__lt=5).delete()               # bulk
```

### Add / remove su M:N

```python
corso.studenti.add(stud)
corso.studenti.remove(stud)
corso.studenti.clear()
corso.studenti.set([s1, s2, s3])
```

### Related name (relazione inversa)

```python
# se in Order: customer = ForeignKey(Customer, related_name='orders')
customer.orders.all()       # tutti gli ordini del cliente
customer.orders.count()
```

Senza `related_name`: si accede via `customer.order_set.all()`.

---

## 8. Comandi `manage.py` di salvataggio

```bash
python manage.py runserver               # avvia (default :8000)
python manage.py runserver 0.0.0.0:9000  # custom

python manage.py makemigrations          # genera migrazioni
python manage.py migrate                 # applica
python manage.py migrate api 0003        # specifica app/numero
python manage.py showmigrations          # lista
python manage.py sqlmigrate api 0001     # mostra SQL

python manage.py createsuperuser         # admin user
python manage.py changepassword <user>

python manage.py shell                   # shell con Django caricato
python manage.py dbshell                 # shell del DB

python manage.py startapp <nome>         # nuova app
python manage.py collectstatic           # raccoglie static (production)

python manage.py test                    # test
python manage.py loaddata fixture.json   # carica fixture
python manage.py dumpdata api > out.json # esporta dati
```

---

## 9. Errori frequenti & gotcha

| Sintomo | Causa | Fix |
|---------|-------|-----|
| `No module named 'api'` | app non registrata | aggiungere a `INSTALLED_APPS` |
| `Table 'xxx' doesn't exist` | migrazioni non applicate | `makemigrations` + `migrate` |
| `Unknown database 'xxx'` | DB non creato | crearlo lato server prima |
| `ImproperlyConfigured: settings` | `DJANGO_SETTINGS_MODULE` non set | `manage.py` lo fa per te, da shell `os.environ.setdefault(...)` |
| `404 al posto del browsable API` | `api/urls.py` non incluso o nome variabile sbagliato | deve chiamarsi `urlpatterns` |
| Endpoint URL senza slash finale dà 404 | DRF mette slash di default | metti `/` finale o `APPEND_SLASH=True` |
| `RelatedManager has no len()` nel serializer | passi il manager invece del queryset | usa `.all()` o `many=True` |
| `null` non accettato | manca `null=True` sul campo | aggiungilo + `makemigrations` |
| Migration conflict | due rami con migration con stesso numero | `makemigrations --merge` |
| `CSRF token missing` su POST da curl | sessione richiede CSRF | usa endpoint DRF (esenta) o `csrf_exempt` |
| Modifica modelli senza `makemigrations` | dimenticato | rifare il ciclo migrations |
| `__str__` mostra `Pizza object (1)` | non hai overridden | aggiungi `def __str__(self)` |
| `FieldError: Cannot resolve keyword` | nome campo errato in filter | controlla `__` e nomi |
| Foreign Key fallisce alla migrate | tabelle in ordine sbagliato (raro su MySQL) | rileggi traceback, di solito tipo dato |

---

## 10. DRF ulteriori dettagli

### Permessi

```python
from rest_framework.permissions import IsAuthenticated, AllowAny

class PizzaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]   # o AllowAny per pubblico
    ...
```

Globale in `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
}
```

### Paginazione globale

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### `get_queryset` dinamico

```python
def get_queryset(self):
    qs = Pizza.objects.all()
    veg = self.request.query_params.get('vegetariane')
    if veg:
        qs = qs.filter(is_vegetarian=True)
    return qs
```

---

## 11. Test rapidi

Browsable API: vai a `http://localhost:8000/api/v1/pizzas/` nel browser.

curl:
```bash
curl http://localhost:8000/api/v1/pizzas/
curl -X POST http://localhost:8000/api/v1/pizzas/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Margherita","price":6.0}'
```

Shell Django (popolare dati al volo):
```bash
python manage.py shell
>>> from api.models import Pizza
>>> Pizza.objects.create(name="Margherita", price=6.0)
```

---

## 12. Checklist prima di consegnare

- [ ] DB esistente sul server, credenziali in `.env`
- [ ] `'api'` e `'rest_framework'` in `INSTALLED_APPS`
- [ ] Project `urls.py` include `api.urls`
- [ ] `api/urls.py` esiste con variabile `urlpatterns`
- [ ] Tutti i `CharField` hanno `max_length=...`
- [ ] Ogni FK ha `on_delete=...` (e idealmente `related_name=...`)
- [ ] Ogni modello ha `__str__`
- [ ] `makemigrations` e `migrate` eseguiti dopo l'ultima modifica
- [ ] ViewSet definiscono `queryset` e `serializer_class`
- [ ] Ogni ViewSet è `router.register`-ato in `api/urls.py`
- [ ] Modelli registrati in `admin.py` (per testare via /admin)
- [ ] Server avviato: `python manage.py runserver`
- [ ] `/api/v1/<risorsa>/` risponde con la browsable API DRF

---

## 13. Confronto rapido FastAPI vs Django

| FastAPI                       | Django + DRF                          |
|------------------------------|---------------------------------------|
| `database.py` engine + Session | `settings.py` `DATABASES`            |
| `Base.metadata.create_all()` | `python manage.py migrate`            |
| SQLAlchemy `Column`          | `models.<X>Field()`                   |
| `relationship` + `back_populates` | `ForeignKey(related_name=...)`   |
| `Table` bridge per N:N       | `ManyToManyField` (auto)              |
| Pydantic `BaseModel`         | DRF `Serializer` / `ModelSerializer`  |
| `from_attributes = True`     | `class Meta: model = ...`             |
| `@app.get("/x")`             | `ViewSet` + `router.register`         |
| `Depends(get_db)`            | gestito da Django automaticamente     |
| `HTTPException(404)`         | `get_object_or_404` / `Response(status=...)` |
| `db.add` + `db.commit`       | `Model.objects.create(...)`           |
| `db.query(M).filter(...)`    | `M.objects.filter(...)`               |
| Niente admin built-in        | `/admin` gratis                       |
| Niente migrations (a mano o Alembic) | `makemigrations` + `migrate`  |
