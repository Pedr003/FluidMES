# Atualização 1.1.1 — cadastro e acesso do Preposto

1. Pare a versão anterior com Ctrl+C.
2. Extraia este ZIP. Preserve seu `server/db.sqlite3` se quiser continuar com os dados existentes: faça uma cópia antes de atualizar e leve-a para a pasta `server` da nova instalação. Não copie `node_modules` nem a venv entre instalações diferentes.
3. Execute o projeto com os comandos de `GUIA_EXECUCAO.md`. Não há novas migrações de banco nesta correção.
4. O cadastro do auth sempre cria a empresa e seu Preposto. Chefes e funcionários continuam sendo cadastrados na plataforma pelo Preposto.
5. O Preposto tem acesso às telas e ações operacionais de sua empresa. Não é necessário marcar `is_staff` ou `is_superuser` no Django para isso.

## Se sua conta foi criada numa versão anterior com cargo incorreto

Na pasta do projeto, com o sistema parado, execute no PowerShell:

```powershell
.\.venv\Scripts\python.exe server\manage.py definir_preposto --email "seu-email-cadastrado"
.\.venv\Scripts\python.exe run_local.py
```

O comando ajusta somente a conta informada; preserva senha, empresa e dados. Saia e entre novamente no site para atualizar a sessão exibida.

**Atualização da 1.1.3:** a tela adicional de conclusão de cadastro foi removida. Contas antigas sem empresa retornam ao auth original com mensagem de vínculo pendente. O administrador local deve corrigir o vínculo explicitamente pelo comando abaixo. Novos cadastros já criam empresa e Preposto no auth.

Se você administra o banco local e precisa vincular explicitamente uma conta a uma empresa já existente nele, use:

```powershell
.\.venv\Scripts\python.exe server\manage.py definir_preposto --email "seu-email-cadastrado" --cnpj "CNPJ-da-empresa-existente"
```

Depois entre novamente no site. O comando não cria nem apaga empresas e não troca a senha.

## O que foi verificado

- Cadastro real no auth cria Preposto mesmo se uma requisição tentar enviar outro cargo.
- Login do Preposto mostra todas as áreas e permite criar, editar e excluir receitas/plantas disponíveis para essas operações.
- Criação da receita `coca-cola`, com todos os valores em 2, salva sem 403 no navegador.
- Criação de planta aparece como card.
- Na 1.1.1, contas sem empresa tinham um fluxo adicional de configuração, removido da interface na 1.1.3.
- Chefes/funcionários e o isolamento entre empresas continuam cobertos pelos testes.

**48 testes automatizados aprovados**, lint e build aprovados, além do fluxo em Chromium. O perfil de uma conta já existente no seu computador só é alterado quando você executa o comando administrativo acima; o ZIP não contém banco ou credenciais de demonstração.
