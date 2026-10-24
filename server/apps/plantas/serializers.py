import math
from rest_framework import serializers
from .models import Planta, Clp, Sensor


class PlantaSerializer(serializers.ModelSerializer):
    painel = serializers.SerializerMethodField()

    def get_painel(self, obj):
        if not hasattr(obj, "card_orders"):
            return None
        orders = [order for order in obj.card_orders if not order.receita_snapshot]
        lots = getattr(obj, "card_lots", [])
        running_lot = next(
            (batch for batch in lots if batch.status == "em_andamento"), None
        )
        running = next(
            (order for order in orders if order.status == "em_andamento"), None
        )
        latest = obj.card_oee[0] if obj.card_oee else None
        clps = [clp for clp in obj.card_clps if clp.ativo]
        from django.utils import timezone

        offline = any(
            clp.status != "online"
            or not clp.ultima_comunicacao
            or (timezone.now() - clp.ultima_comunicacao).total_seconds() > 15
            for clp in clps
        )
        from apps.producao.models import Parada

        stopped = Parada.objects.filter(planta=obj, fim__isnull=True).exists()
        return {
            "status": (
                "parada"
                if stopped
                else (
                    "offline"
                    if offline
                    else "produzindo" if running or running_lot else "disponivel"
                )
            ),
            "receita": (
                running_lot.pedido.receita_snapshot["nome"]
                if running_lot
                else running.receita.nome if running else None
            ),
            "pedido": (
                running_lot.pedido_id
                if running_lot
                else running.pk if running else None
            ),
            "iniciado_em": (
                running_lot.iniciado_em
                if running_lot
                else running.iniciado_em if running else None
            ),
            "duracao_seg": (
                running_lot.setup_seg + running_lot.duracao_producao_seg
                if running_lot
                else running.duracao_simulada_seg if running else None
            ),
            "quantidade_produzida": sum(
                o.quantidade for o in orders if o.status == "concluido"
            )
            + getattr(obj, "produzido_lotes", 0),
            "quantidade_planejada": sum(
                o.quantidade
                for o in orders
                if o.aprovacao == "aprovado" and o.status != "cancelado"
            )
            + getattr(obj, "planejado_lotes", 0),
            "oee": latest.oee if latest else None,
            "oee_data": latest.data if latest else None,
            "fila": sum(
                o.status == "pendente" and o.aprovacao == "aprovado" for o in orders
            )
            + sum(b.status == "planejado" for b in lots),
        }

    def validate(self, attrs):
        if (
            self.instance
            and "capacidade_l" in attrs
            and self.instance.lotes.exclude(status="concluido")
            .filter(quantidade__gt=attrs["capacidade_l"])
            .exists()
        ):
            raise serializers.ValidationError(
                {
                    "capacidade_l": "Há ciclos programados maiores que esta capacidade. Preserve a capacidade até concluir os ciclos."
                }
            )
        return attrs

    def validate_capacidade_l(self, value):
        if not math.isfinite(value) or not 0.01 <= value <= 1000000:
            raise serializers.ValidationError(
                "A capacidade deve estar entre 0,01 e 1.000.000 L."
            )
        return value

    def validate_tempo_reset_seg(self, value):
        if not math.isfinite(value) or not 0 <= value <= 604800:
            raise serializers.ValidationError(
                "Informe um tempo de reset entre 0 e 604.800 segundos."
            )
        return value

    class Meta:
        model = Planta
        fields = [
            "idplanta",
            "uuid",
            "nome",
            "localizacao",
            "capacidade_l",
            "tempo_reset_seg",
            "painel",
        ]
        read_only_fields = ["idplanta", "uuid"]


class ClpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clp
        fields = [
            "idclp",
            "nome",
            "ip",
            "porta",
            "ativo",
            "status",
            "ultima_comunicacao",
            "planta",
        ]
        read_only_fields = ["status", "ultima_comunicacao"]

    def validate_planta(self, value):
        if value.empresa_id != self.context["request"].user.empresa_id:
            raise serializers.ValidationError("Planta inválida.")
        return value

    def validate_porta(self, value):
        if not value.isdigit() or not 1 <= int(value) <= 65535:
            raise serializers.ValidationError("Use uma porta entre 1 e 65535.")
        return value


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"

    def validate_clp(self, value):
        if value.planta.empresa_id != self.context["request"].user.empresa_id:
            raise serializers.ValidationError("CLP inválido.")
        return value

    def validate(self, attrs):
        low = attrs.get("minimo", getattr(self.instance, "minimo", 0))
        high = attrs.get("maximo", getattr(self.instance, "maximo", 0))
        if not math.isfinite(low) or not math.isfinite(high) or low > high:
            raise serializers.ValidationError("Limites inválidos.")
        if attrs.get("endereco", 0) > 65535:
            raise serializers.ValidationError("Endereço fora da faixa Modbus.")
        return attrs
