# 🌱 AgroTechHub - Plataforma Agrícola Inteligente

Um site profissional e interativo voltado para o setor agrícola, conectando produtores, compradores e tecnologia com dados meteorológicos reais de todo o mundo.

## 🚀 Deploy no Vercel

Este projeto está configurado para deploy automático no Vercel.

### 📋 Pré-requisitos

- Conta no [Vercel](https://vercel.com)
- Conta no [GitHub](https://github.com)

### 🔧 Passos para Deploy

1. **Fork ou Clone este repositório**
2. **Conecte ao Vercel:**
   - Acesse [vercel.com](https://vercel.com)
   - Clique em "New Project"
   - Importe seu repositório do GitHub
   - Configure as variáveis de ambiente (opcional)

3. **Deploy Automático:**
   - O Vercel detectará automaticamente que é um projeto Python/Flask
   - O deploy será feito automaticamente usando as configurações em `vercel.json`

### 🌐 URL de Produção

Após o deploy, seu site estará disponível em:
\`\`\`
https://seu-projeto.vercel.app
\`\`\`

## ✨ Funcionalidades

- **🏠 Página inicial** com design moderno e responsivo
- **👤 Sistema de autenticação** (login/cadastro)
- **📊 Dashboard** para produtores rurais
- **🛒 Marketplace** de produtos agrícolas
- **🌤️ Previsão do tempo global** com dados reais
- **📝 Blog** com conteúdo sobre agricultura
- **📱 Design responsivo** para todos os dispositivos

## 🌍 Sistema de Clima

- ✅ **Dados meteorológicos reais** de qualquer cidade do mundo
- ✅ **Múltiplas APIs** para garantir disponibilidade
- ✅ **Previsão de 5 dias** detalhada
- ✅ **Interface intuitiva** com exemplos de cidades

### APIs Utilizadas:
1. **wttr.in** - Principal fonte de dados
2. **OpenMeteo** - Backup científico gratuito
3. **Geocoding** - Para localização precisa

## 🛠️ Tecnologias

### Frontend
- HTML5 + CSS3 + JavaScript
- Font Awesome (ícones)
- Google Fonts (Poppins)
- Design responsivo com Flexbox/Grid

### Backend
- Python 3.8+
- Flask 2.3.3
- Requests (APIs externas)
- Jinja2 (templates)

### Deploy
- Vercel (serverless)
- Configuração automática
- HTTPS incluído

## 📁 Estrutura do Projeto

\`\`\`
agrotechhub/
├── app.py                 # Aplicação Flask principal
├── api/
│   └── index.py          # Entrada para Vercel
├── vercel.json           # Configuração Vercel
├── requirements.txt      # Dependências Python
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── weather.html
│   └── ...
├── static/               # Arquivos estáticos
│   ├── css/style.css
│   └── js/script.js
└── README.md
\`\`\`

## 🔐 Variáveis de Ambiente (Opcional)

No painel do Vercel, você pode configurar:

\`\`\`bash
SECRET_KEY=sua_chave_secreta_aqui
\`\`\`

## 🧪 Teste Local

Para testar localmente antes do deploy:

\`\`\`bash
# Clone o repositório
git clone <seu-repositorio>
cd agrotechhub

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
\`\`\`

Acesse: `http://localhost:5000`

## 📊 Dados de Teste

### Usuário Demo:
- **Email:** admin@agro.com
- **Senha:** 123456

### Cidades para Teste do Clima:
- São Paulo, Brasil
- Tokyo, Japan
- New York, USA
- Paris, France
- London, UK

## 🚀 Funcionalidades Futuras

- [ ] Banco de dados real (PostgreSQL)
- [ ] Sistema de upload de imagens
- [ ] Chat entre usuários
- [ ] Notificações push
- [ ] API própria
- [ ] App mobile

## 📞 Suporte

- **Email:** contato@agrotechhub.com
- **GitHub:** [Issues](https://github.com/seu-usuario/agrotechhub/issues)

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Desenvolvido com ❤️ para o agronegócio mundial** 🌍🚜
