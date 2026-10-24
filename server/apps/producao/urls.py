from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    PedidosView,
    ReceitasView,
    RendimentosView,
    ParadasView,
    SolicitacoesView,
)

router = SimpleRouter()
router.register("pedidos", PedidosView, basename="pedido")
router.register("receitas", ReceitasView, basename="receita")
router.register("rendimentos", RendimentosView, basename="rendimento")
router.register("paradas", ParadasView, basename="parada")
router.register("solicitacoes", SolicitacoesView, basename="solicitacao")
urlpatterns = [path("api/", include(router.urls))]
