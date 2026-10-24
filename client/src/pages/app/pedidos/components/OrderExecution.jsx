import useData from "../../shared/useData";
import { DataState } from "../../shared/UI";
import BatchPlan from "./BatchPlan";

export default function OrderExecution({ id }) {
  const { data, error, loading, reload } = useData(
    [`/api/pedidos/${id}/`],
    1500,
  );
  const order = data?.[0];
  return (
    <>
      <DataState loading={loading} error={error} reload={reload} />
      {order && (
        <>
          {order.em_pausa && (
            <p className="form-error" role="status">
              Produção pausada: uma planta está indisponível. A previsão será
              atualizada na retomada.
            </p>
          )}
          {order.aviso_previsao && (
            <p className="form-error">{order.aviso_previsao}</p>
          )}
          <p className="info-note">
            Receita: {order.receita_snapshot?.nome || order.receita_nome} ·
            versão {order.receita_snapshot?.versao || "anterior"}.{" "}
            {order.simulado
              ? "Execução simulada com as durações da receita."
              : "Simulação desligada; este plano não envia comandos ao equipamento."}
          </p>
          <BatchPlan plan={order.plano} lots={order.lotes} />
        </>
      )}
    </>
  );
}
