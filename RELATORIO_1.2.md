# FluidMES 1.2 — sumário executivo e arquitetura

## Resultado

O pedido deixa de representar um único ciclo em uma única planta. Passa a registrar volume total, receita congelada e uma programação de ciclos por tanque. Capacidade, disponibilidade futura, reset e etapas da receita determinam a previsão de término. A aprovação consolida reservas; o histórico só registra conclusão do pedido após todos os ciclos.

A identidade visual foi preservada. As mudanças de interface se concentram na informação necessária aos novos fluxos: capacidade/reset nas plantas, ingredientes e misturas na receita e previsão/etapas no pedido. A sidebar não exibe identificação da versão e os botões flutuantes mostram apenas +, com nome acessível e descrição ao passar o mouse.

## Organização do código

| Responsabilidade | Local |
|---|---|
| Botão e campo compartilhados | client/src/pages/app/shared/controls |
| Modal de formulário, envio, bloqueio e erro | client/src/pages/app/shared/FormModal.jsx |
| Cadastros comuns | shared/EntityForm.jsx e shared/EntityList.jsx |
| Edição da receita de duas/três dosagens | receitas/components/RecipeForm.jsx |
| Pedido e consulta de distribuição | pedidos/components/ProductionOrderForm.jsx |
| Plano, ciclos, fases e histórico | pedidos/components/BatchPlan.jsx e OrderExecution.jsx |
| Normalização de cards e descrições de solicitações | pedidos/orderModel.js e requestDetails.js |
| Cálculo de tempos e snapshots | server/apps/producao/services/recipes.py |
| Algoritmo independente da API | server/apps/producao/services/planner.py |
| Reservas, execução simulada e retomada | server/apps/producao/services/production.py |
| Aprovação e compatibilidade anterior | server/apps/producao/workflow.py |
| Diagnóstico de CLP somente leitura | server/services/clp_probe.py |

Views e serializers validam o contrato e o acesso por empresa/cargo. O algoritmo recebe parâmetros explícitos e não acessa a interface. Snapshots são somente leitura para clientes. O serviço de execução não depende da aba aberta.

## Cálculo e persistência

A produção por ciclo soma a dosagem sequencial dos ingredientes e as misturas fixas. A composição é escalada proporcionalmente para o volume de cada ciclo. A mistura ocorre depois do segundo ingrediente e, se houver terceiro, uma segunda mistura depois dele.

Uma busca de viabilidade encontra o menor horizonte em que os tanques independentes conseguem concluir todo o volume. Considera a capacidade útil, reservas existentes, preparação e ciclos repetidos. O desempate prioriza menos preparação e a planta preferida. Não reorganiza outros pedidos já aprovados.

A gravação dos ciclos usa bulk_create dentro de transação. A aprovação bloqueia as plantas da empresa em ordem consistente e impede aprovação repetida. Os ciclos armazenam os litros e etapas usados, os horários previstos e os timestamps de execução. O snapshot da receita preserva a versão original diante de futuras edições.

Cards de plantas agregam volumes de ciclos no banco e carregam os ciclos ativos. A listagem de pedidos evita serializar todas as etapas; elas são carregadas no detalhe. OEE usa o volume e a duração de produção de cada ciclo concluído no tanque correspondente, evitando atribuir o pedido inteiro à primeira planta.

## Paradas, comunicação e compatibilidade

Paradas abertas ou comunicação de CLP ativa sem leitura recente impedem nova programação. Durante a simulação, a indisponibilidade detectada suspende a evolução e desloca a previsão da planta na retomada. A interface sinaliza previsão pausada.

As migrações são incrementais. Plantas existentes recebem capacidade de 50 L/reset de 60 s como valores demonstrativos a revisar. Receitas anteriores preservam os números e recebem nomes genéricos/vazão inicial na representação até revisão pelo usuário. Pedidos antigos sem snapshots continuam no fluxo de compatibilidade anterior; novos pedidos usam ciclos.

A comunicação industrial diferencia conexão TCP, leitura Modbus válida e conexão do monitor web. O diagnóstico não escreve registros. A coleta contínua continua usando Redis e o comando read_plants. A produção física não foi ligada automaticamente ao relógio da simulação.

## Hipóteses e limites

O modelo considera tanques e abastecimento independentes, quantidades nominais em litros, ingredientes disponíveis e tempos conhecidos. Não inclui bomba compartilhada, descarregamento/envase, ordem de prioridades por prazo, perdas físicas nem liberação laboratorial/CIP. A eliminação de reset na mesma receita é uma convenção da simulação, não uma validação sanitária.

A regra de 30 L/min é um parâmetro demonstrativo editável; a pesquisa não sustenta uma média industrial universal. Configure os valores medidos. Leia REFERENCIAS_MES_E_CLPS.md.

O SQLite facilita a demonstração. Para concorrência elevada e bloqueios de linha efetivos, utilize PostgreSQL. Não foram executados testes com CLP físico, Redis/PostgreSQL externos ou Windows nesta entrega. Testes de Modbus usam um servidor TCP local. O fallback temporário de enumeração de interfaces do Node.js foi necessário neste ambiente isolado para executar o Vite em 0.0.0.0; não faz parte do produto.

Há limites explícitos de 2.000 ciclos por plano e previsão de até um ano para evitar processamento ou datas inválidos por parâmetros extremos. Um plano estimado não mede desperdício real nem garante a melhor programação global da fábrica.

## Validação e execução

O CI foi atualizado para executar explicitamente as suítes de contas, plantas, produção, rede local e geometria de scroll.

**74 testes Django, quatro testes de geometria, lint e build passaram.** O fluxo real em Chromium cobriu cadastro de planta/receitas, prévia de 200 L em quatro tanques de 50 L, envio pelo Funcionário, aprovação do Chefe, duração de 12,5 segundos derivada da receita, conclusão e histórico. Houve verificação em viewport móvel e zero erros JavaScript não tratados nessa sequência.

As evidências finais ficam em quality/tests-1.2.txt, frontend-1.2.txt, browser-1.2.txt e migration-1.2.txt. Elas incluem testes de algoritmo, API, permissões, isolamento entre empresas, receitas, migração e Modbus, além dos fluxos em Chromium.

Para executar após instalar as dependências, use `python run_local.py` no ambiente virtual. O guia para Windows está em GUIA_EXECUCAO.md e a atualização/roteiro de demonstração em GUIA_PLANEJAMENTO_E_RECEITAS.md. Faça backup do banco antes de aplicar a atualização.
