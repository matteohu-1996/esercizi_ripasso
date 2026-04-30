from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredienteViewSet, PizzaViewSet

router = DefaultRouter()

router.register(r"ingredienti", IngredienteViewSet, basename="ingrediente")
router.register(r"pizze", PizzaViewSet, basename="pizza")

urlpatterns = [
    path("", include(router.urls)),
]
