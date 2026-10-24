# FluidMES 1.1.2

A tela de login/cadastro volta à apresentação da versão 1.1. As regras de cadastro e permissões da 1.1.1 permanecem: cadastro público cria Preposto e o Preposto acessa todas as áreas de sua empresa.

Na landing, a roda do mouse, o trackpad, o teclado e o toque usam a rolagem do navegador. Após 240 ms sem rolagem, a página alinha suavemente à seção mais próxima. Um novo gesto interrompe esse alinhamento imediatamente. Durante um arrasto ou tecla de rolagem pressionada, o alinhamento aguarda a liberação. O meio de seções maiores que a tela permanece livre para leitura; o alinhamento ocorre próximo às suas bordas. Com movimento reduzido ativado no dispositivo, não há alinhamento automático.

## Atualizar e executar

Encerre o projeto com Ctrl+C. Faça backup de `server/db.sqlite3` e preserve o banco, `.env` e ambiente virtual ao substituir os arquivos do código. Nenhuma migração adicional foi criada nesta atualização.

No Windows, dentro da pasta FluidMES:

```powershell
.\.venv\Scripts\python.exe run_local.py
```

No Linux/macOS, com o ambiente virtual ativado:

```sh
python run_local.py
```

Abra http://127.0.0.1:5173. Para a primeira instalação, siga GUIA_EXECUCAO.md.

## Verificação

```sh
cd client
npm ci
npm run test:scroll
npm run lint
npm run build
```
