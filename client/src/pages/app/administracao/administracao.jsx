import ClpConnectionTest from "./components/ClpConnectionTest";
import { dateTime } from "../shared/format";
import { useState } from "react";
import EntityList from "../shared/EntityList";
import { clpFields, sensorFields, stopFields } from "../shared/resources";
export default function Administracao() {
  const [tab, setTab] = useState("clps");
  const configs = {
    clps: ["CLPs", "idclp", clpFields],
    sensores: ["Sensores", "idsensor", sensorFields],
    paradas: ["Paradas", "idparada", stopFields],
  };
  const [title, id, fields] = configs[tab];
  return (
    <div>
      <div className="admin-tabs segmented">
        {Object.entries(configs).map(([key, [label]]) => (
          <button
            key={key}
            className={tab === key ? "active" : ""}
            onClick={() => setTab(key)}
          >
            {label}
          </button>
        ))}
      </div>
      <EntityList
        key={tab}
        title={`Administração · ${title}`}
        description="Configuração técnica da operação. Acesso exclusivo do Preposto."
        endpoint={`/api/${tab}/`}
        idField={id}
        fields={fields}
        createLabel={`Adicionar ${title === "Paradas" ? "parada" : title === "Sensores" ? "sensor" : "CLP"}`}
        renderRow={(item) => (
          <>
            <div className="entity-avatar">
              <i
                aria-hidden="true"
                className={`bi ${tab === "clps" ? "bi-hdd-network" : tab === "sensores" ? "bi-broadcast" : "bi-pause-circle"}`}
              />
            </div>
            <div className="row-main">
              <strong>{item.nome || `Parada #${item.idparada}`}</strong>
              <span>
                {tab === "clps"
                  ? `${item.ip}:${item.porta}`
                  : tab === "sensores"
                    ? `${item.tipo} · ${item.unidade}`
                    : new Date(item.inicio).toLocaleString("pt-BR")}
              </span>
            </div>
          </>
        )}
        renderDetailExtra={
          tab === "clps"
            ? (item) => <ClpConnectionTest clp={item} />
            : undefined
        }
        details={(item) => [
          ...(tab === "clps"
            ? [
                ["Comunicação", item.status || "Não testada"],
                ["Última leitura válida", dateTime(item.ultima_comunicacao)],
              ]
            : []),
          ...fields
            .filter((f) => f.type !== "password")
            .map((f) => [f.label, String(item[f.name] ?? "—")]),
        ]}
      />
    </div>
  );
}
