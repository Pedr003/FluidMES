# FluidMES 1.2.1

MES em React/Vite e Django/DRF, com identidade visual baseada na landing page original, cards operacionais e permissões por cargo.

Leia também **ATUALIZACAO_1.1.1.md** se estiver atualizando uma conta antiga com erro de permissão.

## Publicar e acessar o admin

Leia **GUIA_VERCEL_ADMIN.md**. Esta atualização prepara frontend na Vercel, API/worker em servidor persistente e PostgreSQL online. Inclui configuração HTTPS, arquivos estáticos do Django Admin, script de rotas da Vercel e referência render.yaml. Nenhum recurso foi publicado automaticamente.

## Executar

Leia **GUIA_EXECUCAO.md** para o passo a passo completo. No Windows, a partir desta pasta:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r server\requirements.txt
.\.venv\Scripts\python.exe run_local.py
```

Abra **http://127.0.0.1:5173**. O iniciador instala o frontend quando necessário, aplica as migrações e inicia API, simulador persistente e Vite. Ctrl+C encerra os processos. Não é preciso Redis para a interface e a simulação básica.

## Produção por ciclos — versão 1.2

- Pedidos repartidos entre tanques e ciclos conforme capacidade, disponibilidade e reset; previsão e etapas por tanque.
- Receitas com dois ou três ingredientes, nomes, quantidades, vazões e misturas fixas por ciclo.
- Botões, campos e formulários compartilhados; botão flutuante mostra somente +; versão removida da sidebar.
- Snapshot de receita e parâmetros de execução por pedido; edição posterior não altera os ciclos já aprovados.
- Diagnóstico de CLP distingue conexão TCP de leitura Modbus válida; coleta contínua continua separada.

Leia **GUIA_PLANEJAMENTO_E_RECEITAS.md**, **REFERENCIAS_MES_E_CLPS.md** e **RELATORIO_1.2.md**.

## Ajustes da 1.1.4 — rede LAN

Execute `run_local.py`: o terminal mostra os endereços local e da LAN. O IP é detectado automaticamente e as configurações de host, CSRF e CORS são definidas no modo local. O frontend atende a rede na porta 5173 e encaminha a API internamente. Veja GUIA_LAN.md para acesso por outro computador ou celular.

A configuração local define ALLOWED_HOSTS integralmente, corrigindo o erro de inicialização reportado. Notificações funcionam por HTTP pelo IP, sem depender de crypto.randomUUID.

## Ajustes da 1.1.3

- Acessar abre o login original, mesmo com uma sessão salva.
- Tela adicional de conclusão de empresa removida. Contas antigas sem vínculo retornam ao auth com mensagem no formulário original.
- Cadastro completo continua no auth e cria empresa e Preposto.

## Ajustes da 1.1.2

- Tela de autenticação restaurada ao visual original, preservando cadastro exclusivo de Preposto e suas permissões.
- Landing com rolagem nativa e alinhamento suave à seção mais próxima após uma pausa de 240 ms; novos gestos interrompem o alinhamento.
- Seções longas continuam legíveis no celular; a preferência de movimento reduzido desativa o alinhamento automático.

## O que muda na 1.1

- Plantas em cards com faixa de status, OEE e quantidade produzida/planejada.
- Pedidos em cards, com cores por tipo para gestores e por status para funcionários; filtros de ativos e histórico.
- Receitas e funcionários em listas; detalhes e formulários em modais expansíveis até ocupar a tela.
- Sidebar conforme os cargos: só Preposto acessa tudo; Chefe não vê Rendimentos; Funcionário não vê Rendimentos nem Funcionários.
- Solicitações de plantas/receitas feitas por funcionários só criam registros após aprovação.
- Aprovação reserva os ciclos calculados; a execução persistente no servidor usa os tempos da receita.
- Configurações contém apenas preferências; Administração técnica e Últimas atualizações são exclusivas do Preposto.
- Preferências de tema e sidebar salvas por conta; gráficos interativos e Homes por cargo.
- Perfil mantido sem ampliação de escopo.

A hipótese adotada para a regra que ficou em aberto é: Chefe pode consultar Funcionários, mas só Preposto administra pessoas. Pedidos finalizados vão para Histórico. O planejador respeita as reservas de pedidos aprovados anteriormente.

Leia **RELATORIO_TECNICO.md** para arquitetura, evidências e limites. A pasta `quality/` guarda resultados das verificações; não contém contas ou banco de demonstração.
