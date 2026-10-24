# FluidMES 1.2 — receitas, tanques e previsão

## Atualizar

Pare o projeto com Ctrl+C e faça backup de `server/db.sqlite3`. Substitua o código pelo conteúdo deste ZIP, preservando banco, `.venv` e configurações locais. Execute o mesmo comando:

```powershell
.\.venv\Scripts\python.exe run_local.py
```

O iniciador aplica as migrações incrementais, inicia a API, a simulação e o frontend e mostra os endereços local e LAN. Veja GUIA_LAN.md para firewall e escolha de interface. A identidade visual, o auth original e o scroll da landing foram preservados.

## Plantas

No botão + de Plantas, cadastre nome, localização, capacidade útil em litros e reset em segundos. O reset é aplicado na troca de receita ou de sua versão. Na simulação, a repetição da mesma versão não acrescenta reset. Uma planta nova é considerada inicialmente preparada. Paradas abertas e CLPs ativos sem resposta recente impedem nova programação naquela planta.

As plantas existentes recebem inicialmente capacidade de 50 L e reset de 60 s. São parâmetros demonstrativos: ajuste os valores antes de usar a previsão. Não reduza a capacidade abaixo de um ciclo já reservado; o formulário informa esse impedimento.

## Receitas

Escolha dois ou três ingredientes. Para cada ingrediente, informe nome, quantidade em litros na composição de referência e vazão em L/min. Por exemplo: 40 L de água e 10 L de xarope representam uma composição de referência de 50 L. Para produzir 25 L, cada quantidade é proporcionalmente reduzida pela metade.

A sequência de dois ingredientes é: dosagem 1 → dosagem 2 → mistura 1.

Com três ingredientes: dosagem 1 → dosagem 2 → mistura 1 → dosagem 3 → mistura 2.

Cada mistura tem duração fixa por ciclo. Ela não é multiplicada pelos litros. O abastecimento depende do volume e da vazão:

```text
Tempo de dosagem (s) = volume do ingrediente no ciclo (L) ÷ vazão (L/min) × 60
Tempo de produção do ciclo = soma das dosagens + misturas fixas
Ocupação do tanque = produção do ciclo + reset, quando necessário
```

Portanto, 100 L e 200 L no mesmo tanque têm o mesmo tempo de mistura, mas podem ter tempos diferentes de abastecimento. Esta é a distinção usada para conciliar mistura fixa e previsão por vazão.

O valor inicial de 30 L/min é um exemplo de simulação, não uma média comprovada das indústrias. Cada ingrediente pode usar outra vazão. Consulte REFERENCIAS_MES_E_CLPS.md e use dados medidos no equipamento.

Receitas antigas preservam seus valores numéricos; os nomes aparecem inicialmente como Ingrediente 1/2/3 e a vazão de referência como 30 L/min. Revise esses cadastros. Os campos antigos tempo1/tempo2 passam a representar as misturas fixas; a migração não pode descobrir unidades ou nomes que não estavam cadastrados.

## Pedido e aprovação

Informe receita, litros, prazo e, opcionalmente, planta de preferência. O botão Calcular melhor distribuição mostra ciclos, volumes por tanque, início e conclusão estimados e as etapas de cada ciclo. O cálculo não reserva equipamentos.

O funcionário envia o pedido para aprovação. O Chefe ou o Preposto vê a distribuição antes de aprovar. Na aprovação, a disponibilidade é recalculada e as reservas são gravadas em transação; a previsão pode mudar. Pedidos de Chefe/Preposto já nascem aprovados. Não há uma escolha manual de fila na interface.

O planejador busca o menor término estimado nas condições modeladas. A preferência por um tanque serve de desempate, depois de considerar preparação. Um tanque com a mesma receita evita reset, mas pode perder para outro que termine antes. As reservas anteriormente aprovadas são respeitadas; o sistema não altera automaticamente a prioridade de outros pedidos.

Exemplo: 200 L em quatro tanques de 50 L podem usar quatro ciclos paralelos. Com somente um tanque elegível, são quatro ciclos sucessivos. O segundo ciclo e os seguintes da mesma receita não adicionam reset. Esperar a liberação de outro tanque pode ser mais rápido; o cálculo considera essa possibilidade.

O pedido só termina depois que todos os ciclos terminam. Clique no card para ver cada tanque, litros, início/fim previstos, preparação, dosagens e misturas. O histórico preserva a composição e a versão da receita usadas, mesmo se a receita for editada depois.

## Simulação, paradas e limites do modelo

A simulação usa as durações cadastradas, sem fixar os novos pedidos em dez segundos. Ela roda no servidor e pode retomar após reiniciar o iniciador. Paradas e perda de comunicação detectada suspendem a evolução da simulação e ajustam as reservas da planta na retomada. Durante uma pausa, a interface informa que a previsão está suspensa.

O algoritmo considera tanques independentes, sem competição por uma bomba compartilhada, disponibilidade infinita dos ingredientes, tempos determinísticos e volume nominal aditivo. Não estima perda real de líquido, CIP validado, descarregamento, envase ou liberação laboratorial. Se o equipamento exigir essas etapas, elas precisam ser modeladas antes de tratar a previsão como compromisso industrial.

A busca de término é feita para o novo pedido sem reorganizar pedidos já aprovados. O desempate por setup/preferência é determinístico, não um otimizador global de todos os pedidos da fábrica. A proteção de concorrência usa transações e bloqueios de linha; para uso multiusuário intenso, prefira PostgreSQL ao SQLite da demonstração.

Pedidos antigos já existentes sem plano por ciclos mantêm o processamento de compatibilidade anterior. Novos pedidos usam o modelo 1.2. O plano aceita até 2.000 ciclos e recusa previsões superiores a um ano, orientando revisar volume, vazão e capacidade.

## Roteiro para apresentar

1. Crie quatro plantas de 50 L e uma receita com dois ingredientes e mistura de 12 s. Para uma demonstração rápida, ajuste conscientemente a vazão; deixe claro que é um parâmetro de bancada.
2. Como Funcionário, peça 200 L e calcule a distribuição. Mostre os quatro tanques e seus 50 L.
3. Como Chefe, abra o pedido, confira as etapas e aprove.
4. Acompanhe os ciclos até o histórico. Compare o total de 200 L com os 50 L de cada planta.
5. Cadastre uma parada em três plantas e calcule novamente para demonstrar ciclos sucessivos em um tanque.
6. Compare repetição da receita e troca de produto para demonstrar o efeito do reset.

## CLP

Em Administração técnica → CLPs, clique no dispositivo e use Testar comunicação. Sem sensor cadastrado, o teste verifica apenas conexão TCP. Com um sensor, tenta validar uma leitura Modbus. O diagnóstico não envia comandos ao equipamento e não requer Redis.

Para atualização contínua, configure Redis como descrito em GUIA_EXECUCAO.md e rode `read_plants --interval 5`. Cadastre o IP/porta e os registros efetivamente usados no seu CLP. Leituras antigas deixam de indicar disponibilidade após 15 segundos; mantenha o intervalo de coleta em até 5 segundos nesta configuração.

`SIMULACAO_PRODUCAO=false` impede início/conclusão simulados. O teste de leitura não integra automaticamente as ordens ao comando físico de bombas e misturadores. Essa integração exige o mapa de registros e a confirmação de execução do programa do CLP; não foi presumida nesta versão.
