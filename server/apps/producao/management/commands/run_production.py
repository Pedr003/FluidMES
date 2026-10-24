import time
import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import close_old_connections
from apps.producao.models import Pedido, LoteProducao
from apps.producao.workflow import advance_plant

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Executa os ciclos programados com tempos de dosagem, mistura e preparação."

    def add_arguments(self, parser):
        parser.add_argument("--once", action="store_true")

    def handle(self, *args, **options):
        if not settings.SIMULACAO_PRODUCAO:
            self.stdout.write(
                "Simulação desativada. Nenhum pedido será concluído automaticamente."
            )
            return
        try:
            while True:
                close_old_connections()
                plants = list(
                    Pedido.objects.filter(
                        status__in=["pendente", "em_andamento"], aprovacao="aprovado"
                    )
                    .values_list("planta_id", flat=True)
                    .distinct()
                )
                plants = sorted(
                    set(plants)
                    | set(
                        LoteProducao.objects.exclude(status="concluido").values_list(
                            "planta_id", flat=True
                        )
                    )
                )
                for plant_id in plants:
                    try:
                        advance_plant(plant_id)
                    except Exception:
                        logger.exception(
                            "Falha no processamento da planta %s", plant_id
                        )
                if options["once"]:
                    return
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass
