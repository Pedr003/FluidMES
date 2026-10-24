# FluidMES 1.1.3 — acesso direto ao auth original

A tela adicional “Concluir cadastro da empresa” foi removida. O botão Acessar da landing abre o auth original, mesmo quando o navegador possui uma sessão autenticada. O auth não redireciona automaticamente para o painel; o acesso ocorre após enviar o login.

O cadastro continua no formulário original e cria empresa e Preposto juntos. O layout, campos, textos e CSS do auth foram preservados. O scroll da landing e as permissões da 1.1.2 permanecem.

Uma conta antiga sem empresa retorna ao auth com mensagem no formulário. Ela não recebe uma empresa fictícia nem acessa dados de outra empresa. O responsável pelo banco local pode corrigir o vínculo de uma conta específica com uma empresa existente:

```powershell
.\.venv\Scripts\python.exe server\manage.py definir_preposto --email "email-da-conta" --cnpj "CNPJ-da-empresa-existente"
```

## Executar

Encerre a versão anterior com Ctrl+C. Preserve e faça backup de `server/db.sqlite3` e das configurações locais antes de substituir o código. Na pasta FluidMES:

```powershell
.\.venv\Scripts\python.exe run_local.py
```

Abra http://127.0.0.1:5173. O guia completo de primeira instalação está em GUIA_EXECUCAO.md. Não houve migração adicional nesta correção.
