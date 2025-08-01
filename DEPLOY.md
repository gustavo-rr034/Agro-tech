# Deploy AgroTechHub no Vercel

## Estrutura do Projeto para Vercel

\`\`\`
agrotechhub/
├── api/
│   └── index.py          # Aplicação Flask principal
├── templates/            # Templates HTML
├── static/              # CSS, JS, imagens
├── vercel.json          # Configuração Vercel
├── requirements.txt     # Dependências Python
├── runtime.txt          # Versão Python
└── .vercelignore        # Arquivos a ignorar
\`\`\`

## Passos para Deploy

1. **Certifique-se que tem APENAS estes arquivos:**
   - ✅ `api/index.py`
   - ✅ `vercel.json`
   - ✅ `requirements.txt`
   - ✅ `runtime.txt`
   - ✅ `.vercelignore`
   - ✅ Pasta `templates/`
   - ✅ Pasta `static/`

2. **NÃO deve ter:**
   - ❌ `app.py` na raiz
   - ❌ `package.json`
   - ❌ `next.config.js`
   - ❌ Pasta `node_modules/`
   - ❌ Pasta `.next/`

3. **Upload no Vercel:**
   - Faça upload de todos os arquivos
   - Vercel deve detectar automaticamente como Python
   - Deploy será feito usando `@vercel/python`

## Verificação

Se o deploy funcionar, você verá:
- ✅ "Build completed"
- ✅ Site funcionando em https://seu-projeto.vercel.app
- ✅ Todas as páginas carregando
- ✅ Sistema de clima funcionando

## Troubleshooting

Se ainda der erro:
1. Delete o projeto no Vercel
2. Certifique-se que não há arquivos Node.js
3. Crie novo projeto
4. Faça upload apenas dos arquivos listados acima
