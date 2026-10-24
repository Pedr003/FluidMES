# Referências industriais e CLPs — FluidMES

Pesquisa em fontes primárias consultadas em 24/10/2026. As sugestões abaixo são análise para o TCC, sem afirmar equivalência entre este projeto e um MES industrial completo.

## O que aproveitar de cada sistema

| Referência | Recurso destacado pela fonte | Aplicação ao FluidMES |
|---|---|---|
| Siemens Opcenter Execution Process | Instruções de receita, rastreabilidade, execução de lotes e integração de planejamento com operação. | Receita versionada por pedido, instruções de dosagem/mistura e separação entre planejamento e execução. |
| Rockwell Plex MES para alimentos e bebidas | Programação de lotes, OEE, análise de ingredientes/fórmulas e recursos de qualidade/rastreabilidade. | Divisão do pedido em ciclos e tanques, produção/OEE por equipamento e detalhamento por etapa. Genealogia dos lotes físicos de matéria-prima e controle laboratorial são evoluções futuras. |
| GE Vernova Proficy — caso Coca-Cola Refreshments | O caso apresenta padronização de dados, histórico e comparação de indicadores entre equipamentos e plantas. | Cards com status e dados úteis, volume realmente concluído por tanque e histórico de receita. Evitar chamar uma estimativa de medição real. |
| AVEVA System Platform e MES | A fonte distingue a camada operacional de visualização/integração da camada MES de fluxo e execução; enfatiza modelos reutilizáveis. | Separar interface, domínio de produção e comunicação industrial; compartilhar componentes e não confundir conexão com o monitor com resposta do CLP. |

Fontes:

- [Siemens — Opcenter Execution Process 2301](https://blogs.sw.siemens.com/opcenter/whats-new-in-opcenter-execution-process-2301/)
- [Rockwell — Plex MES for Food & Beverage](https://www.rockwellautomation.com/en-us/products/software/factorytalk/operationsuite/mes/plex-mes/plex-mes-for-food-and-beverage.html)
- [GE Vernova — Coca-Cola e Proficy](https://www.gevernova.com/software/customer-stories/coca-cola-achieves-operational-excellence-with-proficy)
- [AVEVA — System Platform e sua relação com MES](https://www.aveva.com/en/products/system-platform/)

## Empresas e contextos semelhantes

A Coca-Cola Refreshments é um caso documentado pela GE Vernova para uso de Proficy em sistemas de informação de linha, histórico e dashboards. A fonte cita iFIX e Historian; isso não comprova a implantação de um módulo específico de MES em todas as unidades da marca.

A Schneider Electric apresenta a Danone Specialised Nutrition como caso de digitalização com AVEVA MES: [página oficial do fabricante](https://www.se.com/eg/en/product-range/63377170-aveva-manufacturing-execution-system/). O interesse para o TCC é padronizar execução e informação da operação, não copiar exigências de um processo industrial diferente.

Fabricantes de xaropes, bases de refrigerantes, sucos e bebidas com múltiplos tanques são perfis potenciais para uma evolução do FluidMES. Essa indicação é uma análise de adequação do modelo de produção por receitas e ciclos, não uma afirmação de que uma empresa específica usa este software.

## Vazão: por que não adotar uma média única

A Graco explica que a seleção depende de vazão, características do material e compatibilidade do equipamento; a viscosidade afeta o desempenho. [Fonte oficial](https://www.graco.com/us/en/in-plant-manufacturing/solutions/articles/selecting-the-right-food-and-beverage-pump.html).

A Alfa Laval oferece a linha sanitária LKH em diversos tamanhos, com capacidades máximas de até 500 m³/h. Isso é uma faixa de catálogo com modelos diferentes, não uma média de dosagem de ingredientes e tampouco a vazão recomendada para os tanques do TCC. [Fonte oficial](https://www.alfalaval.co.uk/products/fluid-handling/pumps/centrifugal-pumps/lkh/).

A pesquisa não sustenta uma média universal aplicável ao projeto. O padrão inicial de **30 L/min = 1.800 L/h** foi escolhido como parâmetro demonstrativo editável. Deve ser substituído pela vazão medida de cada ingrediente/equipamento. Não é apresentado como média industrial, dado de fabricante ou valor validado para Coca-Cola/guaraná.

## CLPs e sensores, de forma simples

Pense em três funções:

- **Sensor:** mede algo. Um sensor de nível informa quanto o tanque encheu; um de temperatura informa o aquecimento; um medidor de vazão informa quanto líquido passa por minuto.
- **CLP:** é o computador industrial que executa o programa da máquina. Ele recebe sinais e comanda saídas, como abrir uma válvula, ligar uma bomba ou manter o misturador funcionando pelo tempo definido.
- **MES:** organiza os pedidos, a receita, os tanques e o histórico. Solicita e acompanha o trabalho, usando os estados que a automação informa.

Exemplo: o MES planeja 50 L de guaraná no Tanque 1. O programa do CLP executa as dosagens, confere os sensores e aciona o misturador. Ao terminar, informa a conclusão para o MES registrar o ciclo. O programa e as permissões físicas do equipamento precisam estar configurados para esse fluxo.

A documentação Siemens recomenda definir entradas/saídas, operação, condições que permitem cada atuação e interfaces antes de programar o sistema: [guia oficial de projeto de um sistema CLP](https://docs.tia.siemens.cloud/r/simatic_s7_1200_manual_collection_enus_20/programming-concepts/guidelines-for-designing-a-plc-system).

Modbus é uma forma de comunicação. O endereço IP identifica o dispositivo na rede, a porta identifica o serviço, e o registro identifica o dado. Um registro só vira “litros” ou “temperatura” quando o endereço, tipo, escala e formato correspondem ao programa do CLP. O FluidMES atual lê coils, entradas digitais e holding registers simples; conversões de escala e valores de múltiplos registradores exigem adaptação ao mapa do equipamento.

Conectar ao WebSocket do site confirma apenas que o monitor web está aberto. Conectar por TCP ao CLP confirma que o serviço de rede aceitou uma conexão. Uma resposta Modbus válida confirma a leitura daquele registro. Nenhuma dessas confirmações, isoladamente, comprova a execução física de uma receita.

O novo botão Testar comunicação distingue conexão e leitura. A coleta contínua registra a última comunicação válida e acusa informação antiga. A produção entregue continua simulada; testes Modbus automatizados usam um servidor TCP local, não um CLP físico do laboratório.

## Próximos ganhos com maior impacto

1. Medir vazões e capacidade útil da bancada para reduzir erro de previsão.
2. Registrar estados reais de dosagem, mistura, bloqueio e conclusão do CLP.
3. Modelar bombas/tubulações compartilhadas se limitarem a produção paralela.
4. Incluir descarregamento e liberação de limpeza quando fizerem parte do ciclo real.
5. Adicionar rastreio dos lotes de matéria-prima e medição real de perdas antes de prometer otimização de desperdício.

Esses pontos decorrem da comparação e dos limites atuais do projeto. Menor duração estimada não prova menor perda de produto.
