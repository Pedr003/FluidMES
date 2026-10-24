from django.db import transaction
from django.db.models import Prefetch, Sum, Q, Value
from django.db.models.functions import Coalesce
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from asgiref.sync import async_to_sync
from rest_framework.exceptions import ValidationError
from apps.accounts.permissions import RequestCreateAccess, OwnerAccess
from apps.accounts.audit import AuditMixin, record
from apps.producao.models import Pedido, OEERegistro, LoteProducao
from apps.producao.workflow import enqueue_request
from .models import Planta, Clp, Sensor
from .serializers import PlantaSerializer, ClpSerializer, SensorSerializer


class PlantasView(AuditMixin, ModelViewSet):
    serializer_class = PlantaSerializer
    permission_classes = [RequestCreateAccess]
    audit_resource = "planta"

    def get_queryset(self):
        return (
            Planta.objects.filter(empresa=self.request.user.empresa)
            .annotate(
                produzido_lotes=Coalesce(
                    Sum("lotes__quantidade", filter=Q(lotes__status="concluido")),
                    Value(0.0),
                ),
                planejado_lotes=Coalesce(Sum("lotes__quantidade"), Value(0.0)),
            )
            .order_by("idplanta")
            .prefetch_related(
                Prefetch(
                    "pedidos",
                    queryset=Pedido.objects.select_related("receita").order_by(
                        "-idpedido"
                    ),
                    to_attr="card_orders",
                ),
                Prefetch(
                    "oee_registros",
                    queryset=OEERegistro.objects.order_by("-data")[:1],
                    to_attr="card_oee",
                ),
                Prefetch(
                    "clps", queryset=Clp.objects.order_by("idclp"), to_attr="card_clps"
                ),
                Prefetch(
                    "lotes",
                    queryset=LoteProducao.objects.exclude(status="concluido")
                    .select_related("pedido")
                    .order_by("inicio_previsto"),
                    to_attr="card_lots",
                ),
            )
        )

    def create(self, request, *args, **kwargs):
        if request.user.role == 3:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return enqueue_request(request, "planta", serializer)
        return super().create(request, *args, **kwargs)

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa)
        record(
            self.request.user,
            self.request.user.empresa_id,
            "criou",
            "planta",
            serializer.instance.nome,
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        if instance.pedidos.exists() or instance.lotes.exists():
            raise ValidationError("Planta possui pedidos; exclusão não permitida.")
        label = instance.nome
        instance.delete()
        record(
            self.request.user, self.request.user.empresa_id, "excluiu", "planta", label
        )


class ClpView(AuditMixin, ModelViewSet):
    serializer_class = ClpSerializer
    permission_classes = [OwnerAccess]
    audit_resource = "CLP"

    @action(detail=True, methods=["post"])
    def testar(self, request, pk=None):
        from services.clp_probe import probe

        clp = self.get_object()
        sensor = (
            clp.sensores.order_by("pk")
            .values("nome", "tipo_registro", "endereco")
            .first()
        )
        result = async_to_sync(probe)(clp.ip, clp.porta, sensor)
        clp.status = (
            "online"
            if result["leitura_validada"]
            else "conectado" if result["conectado"] else "offline"
        )
        fields = ["status"]
        if result["leitura_validada"]:
            clp.ultima_comunicacao = timezone.now()
            fields.append("ultima_comunicacao")
        clp.save(update_fields=fields)
        result["ultima_comunicacao"] = clp.ultima_comunicacao
        return Response(result)

    def get_queryset(self):
        return Clp.objects.filter(
            planta__empresa=self.request.user.empresa
        ).select_related("planta")


class SensoresView(AuditMixin, ModelViewSet):
    serializer_class = SensorSerializer
    permission_classes = [OwnerAccess]
    audit_resource = "sensor"

    def get_queryset(self):
        return Sensor.objects.filter(
            clp__planta__empresa=self.request.user.empresa
        ).select_related("clp__planta")
