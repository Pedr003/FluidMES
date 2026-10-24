# Guia de execução — FluidMES 1.2.0

Para contas antigas com erro de permissão, consulte **ATUALIZACAO_1.1.1.md**.

## 1. Preparar

Instale **Python 3.12** e **Node.js 22 ou superior** (com npm). Extraia o ZIP e abra o terminal na pasta `FluidMES`, que contém `client`, `server` e `run_local.py`. Não abra `index.html` diretamente.

No Windows, confira:

```powershell
py -3.12 --version
node --version
npm --version
```

## 2. Windows / PowerShell — primeira execução

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r server\requirements.txt
.\.venv\Scripts\python.exe run_local.py
```

Não precisa ativar a venv nem alterar a política de execução do PowerShell.

O iniciador instala o frontend com `npm ci` quando necessário, aplica as migrações e inicia três processos: API, simulador de produção e frontend. Aguarde o Vite informar que está pronto e abra:

**http://127.0.0.1:5173**

Nas próximas vezes, execute apenas:

```powershell
.\.venv\Scripts\python.exe run_local.py
```

Mantenha o terminal aberto. **Ctrl+C** encerra os processos. Se uma porta estiver ocupada, encerre a outra instância do projeto antes de iniciar novamente.

## Acesso pela rede local (LAN)

O mesmo comando de execução já habilita a LAN. Após iniciar, use em outro dispositivo da mesma rede o endereço mostrado no terminal em **Na rede LAN**, como `http://192.168.0.20:5173`. Permita Node.js nas redes privadas do Firewall do Windows. O computador e o terminal devem permanecer ligados. Consulte GUIA_LAN.md para escolher manualmente o IP quando houver várias conexões.

## 3. Linux / macOS

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r server/requirements.txt
python run_local.py
```

No Linux/Python 3.12, você também pode usar `server/requirements.lock` no lugar de `requirements.txt` para fixar todas as dependências transitivas da resolução revisada.

## 4. Criar o primeiro acesso

O botão **Acessar** abre sempre o login original. Não existe tela adicional para concluir cadastro de empresa. Uma conta antiga sem empresa recebe uma mensagem no auth e precisa de correção administrativa com `definir_preposto --email "conta" --cnpj "CNPJ-da-empresa-existente"`. O cadastro novo já cria o vínculo completo.


Entre em `/auth` e use o cadastro para criar sua empresa e seu usuário **Preposto**. CPF e CNPJ precisam ser válidos. O cadastro não envia convite nem exige OTP nesta versão. Depois entre com e-mail ou CPF e senha.

Para experimentar sem usar dados pessoais, interrompa o iniciador e rode os comandos opcionais abaixo. Eles criam uma empresa fictícia, plantas, receitas e três contas de demonstração com **senhas aleatórias exibidas no terminal**:

```powershell
.\.venv\Scripts\python.exe server\manage.py migrate
.\.venv\Scripts\python.exe server\manage.py seed_demo
.\.venv\Scripts\python.exe run_local.py
```

Contas criadas:

- `preposto@fluidmes.demo`
- `chefe@fluidmes.demo`
- `funcionario@fluidmes.demo`

Guarde as senhas mostradas no primeiro uso do comando. Repetir o comando preserva senhas existentes. As contas de demonstração não enviam e-mails para destinatários reais. Nenhuma conta ou senha de demonstração está pré-gravada no ZIP.

## 5. Experimentar os fluxos da 1.1

**Preposto:** visualize todas as áreas. Cadastre plantas, receitas e funcionários; consulte Rendimentos e Últimas atualizações. Em Administração técnica ficam CLPs, sensores e paradas.

**Chefe:** visualize Funcionários apenas para consulta, além de Home, Pedidos, Plantas, Receitas e suas preferências. Não há acesso a Rendimentos, Administração técnica ou Últimas atualizações.

**Funcionário:** consulte Plantas e Receitas e envie novos cadastros para aprovação. Em Pedidos veja apenas suas próprias solicitações. Não edite nem exclua plantas e receitas.

Para testar aprovação, entre como Funcionário e use o botão **+** em Plantas ou Receitas. O modal reúne os dados; ao enviar, a solicitação fica em Pedidos, mas o cadastro ainda não existe. Entre como Chefe ou Preposto e aprove. Só então a planta ou receita será criada. Recusar não cria o registro.

Para testar produção, tenha uma planta e uma receita cadastradas. Faça um pedido como Funcionário e aprove como Chefe. A produção começa automaticamente se a planta estiver livre. Se estiver ocupada, o planejador considera as reservas já aprovadas, capacidades e o tempo de troca, podendo repartir o volume entre plantas. Pedidos feitos por Chefe ou Preposto já nascem aprovados.

Novos pedidos são divididos em ciclos por tanque. A duração considera a dosagem de cada ingrediente (volume ÷ vazão), as misturas fixas por ciclo e o reset de troca de receita. O pedido termina após todos os seus ciclos. Veja **GUIA_PLANEJAMENTO_E_RECEITAS.md**. Ao concluir, vai para o filtro **Histórico**, os ciclos seguintes respeitam as reservas por planta e o OEE diário é recalculado para o volume efetivamente concluído em cada tanque. O processamento ocorre no servidor: fechar a aba não cancela a fila. Reiniciar o iniciador retoma pedidos em andamento. O simulador considera toda a quantidade produzida como boa; isso é uma convenção de demonstração, não medição de refugo real.

O Preposto pode corrigir ou excluir pedidos que ainda aguardam aprovação. Pedidos já em produção ou finalizados não são editáveis. O botão **Calcular melhor distribuição** antecipa tanques, volumes, etapas e previsão. A aprovação confirma as reservas. As cores dos pedidos de Chefe/Preposto identificam o tipo; para o Funcionário, identificam o status. Cores sempre vêm acompanhadas de texto/ícone.

Clicar em pessoas, plantas ou receitas abre os detalhes em modal. O ícone ao lado do fechar expande o modal até ocupar a tela. Escape fecha o modal e Tab mantém a navegação dentro dele.

## 6. Preferências e indicadores

Em **Configurações**, escolha tema do dispositivo, escuro ou claro e os modos de sidebar para computadores e telas menores. As escolhas são salvas por conta. O padrão é acompanhar o dispositivo; sem preferência identificável, o tema é escuro.

Em computadores, o menu vem aberto; há opções de ícones e expansão ao passar o mouse. Em telas menores, o padrão é o puxador lateral, com alternativas de ícones ou menu hambúrguer. O foco principal é o computador.

As Homes variam por cargo. Os gráficos respondem ao mouse e ao teclado. O gráfico de aprovações distingue solicitações aprovadas, aguardando e recusadas; as barras mostram receitas mais pedidas e, para o Preposto, produção por planta.

Últimas atualizações é exclusiva do Preposto e exclui ações realizadas pelo próprio usuário. Mostra autoria, cargo, horário e descrição. Eventos automáticos de produção aparecem como Sistema.

O perfil foi mantido simples, conforme a última definição. OEE fica sem medição até existir um registro; não são inventados percentuais para uma planta nova. `tempo1` e `tempo2` agora são durações fixas de mistura por ciclo; o ciclo ideal para OEE é ponderado pelo volume e pela duração de produção dos ciclos. O turno diário padrão é 480 minutos. Confirme as unidades e os turnos antes de usar os indicadores com equipamentos reais.

## 7. Banco e e-mail locais

SQLite persiste os dados em `server/db.sqlite3`. Não é preciso configurar banco remoto para a execução local. O link de recuperação de senha aparece no terminal da API, pois o modo local usa e-mail no console.

Faça backup do banco antes de aplicar esta versão sobre uma instalação existente. Migrações são incrementais; `run_local.py` aplica as pendentes. O timestamp de criação de pedidos anteriores à 1.1 recebe a data da migração quando não havia esse campo; não deve ser interpretado como uma data histórica real.

## 8. Redis e Modbus (opcionais)

A interface e a simulação de pedidos funcionam sem Redis. No modo local, WebSocket usa memória e não recebe telemetria de outros processos. Para sensores reais ou o simulador Modbus, use Redis e configure `REDIS_URL` tanto na API quanto no coletor, antes de iniciá-los.

Exemplo PowerShell (com Redis disponível em localhost:6379):

```powershell
$env:REDIS_URL="redis://127.0.0.1:6379/0"
.\.venv\Scripts\python.exe run_local.py
```

Em outro terminal, com a mesma variável:

```powershell
$env:REDIS_URL="redis://127.0.0.1:6379/0"
.\.venv\Scripts\python.exe server\manage.py read_plants --interval 5
```

Para testar um CLP simulado, inicie em um terceiro terminal:

```powershell
.\.venv\Scripts\python.exe server\services\server_temp.py --host 127.0.0.1 --port 5020
```

Na Administração técnica do Preposto, cadastre um CLP ativo com IP `127.0.0.1`, porta `5020`, e um sensor `holding_register` no endereço `0`: o valor inicial é `1000`. A telemetria aparece nos detalhes da planta. O coletor apenas lê; não controla máquinas nem envia receitas a CLPs. No Docker, `127.0.0.1` refere-se ao próprio contêiner, então use um endereço alcançável na rede.

`SIMULACAO_PRODUCAO=false` desativa o início e a conclusão automáticos; essa opção prepara a integração futura. Ainda é necessário implementar o adaptador de controle/estados dos tanques para produção real. Não basta desativar a simulação para que pedidos comandem hardware.

## 9. Docker, testes e produção

Alternativa local completa, incluindo PostgreSQL, Redis e processos auxiliares:

```sh
docker compose up --build
```

Abra **http://localhost:8080**. O Compose incluído é de desenvolvimento e não foi executado nesta revisão; o YAML foi validado. Os testes foram executados localmente com SQLite, ASGI e Chromium.

Verificações:

```sh
python server/manage.py check
python server/manage.py makemigrations --check --dry-run
python server/manage.py test apps
cd client
npm ci
npm run lint
npm run build
```

O build fica em `client/dist`. A configuração de CI está em `.github/workflows/ci.yml`.

Para publicar, use `config.settings.prod`, HTTPS, segredo forte, PostgreSQL e SMTP reais, Redis privado e processos persistentes para API/coleta/simulação. Veja `server/.env.example`: as variáveis devem ser injetadas pelo serviço; o arquivo não é carregado automaticamente. Sirva `client/dist`, estáticos Django e `/api`/`/ws` por proxy. Não use o iniciador de desenvolvimento como serviço público.

## 10. Se algo não iniciar

- **Python/Django não encontrado:** use o executável de `.venv` exatamente como nos comandos.
- **npm não encontrado:** instale Node.js e abra novamente o terminal.
- **Porta 8000 ou 5173 ocupada:** pare outra instância do projeto.
- **Pedido não termina:** mantenha `run_local.py` aberto; se iniciou manualmente, execute `python server/manage.py run_production`.
- **Não recebeu recuperação por e-mail:** no modo local, procure o link no terminal.
- **Monitor de sensores sem leituras:** configure Redis, coletor, CLP e sensores. Isso não é necessário para a simulação de pedidos.
- **Conta bloqueada temporariamente no login:** aguarde o limite de tentativas de autenticação; não há limite de leitura do token CSRF.
