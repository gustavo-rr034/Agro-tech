# AgroTechHub

Um site profissional e interativo voltado para o setor agrícola, conectando produtores, compradores e tecnologia.

## Funcionalidades

- **Página inicial atrativa** com banner sobre agricultura moderna e sustentável
- **Sistema de login e cadastro** para produtores e compradores
- **Painel de controle** para cadastro de plantações com:
  - Nome da plantação
  - Tipo de cultura (soja, milho, café, etc.)
  - Localização
  - Previsão de colheita
  - Imagens da lavoura
- **Página de compras** com listagem de produtos agrícolas
- **Previsão do tempo** integrada via API
- **Blog** com dicas sobre agricultura inteligente e sustentável
- **Design responsivo** com animações suaves e esquema de cores verde/terra

## Tecnologias Utilizadas

### Frontend
- HTML5
- CSS3 com Flexbox e Grid
- JavaScript ES6+
- Font Awesome (ícones)
- Google Fonts (Poppins)

### Backend
- Python 3.8+
- Flask 2.3.3
- Jinja2 (templates)

## Instalação e Execução

1. **Clone o repositório**
\`\`\`bash
git clone <url-do-repositorio>
cd agrotechhub
\`\`\`

2. **Crie um ambiente virtual**
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
\`\`\`

3. **Instale as dependências**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Execute a aplicação**
\`\`\`bash
python app.py
\`\`\`

5. **Acesse no navegador**
\`\`\`
http://localhost:5000
\`\`\`

## Estrutura do Projeto

\`\`\`
agrotechhub/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── README.md             # Documentação
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página inicial
│   ├── login.html        # Página de login
│   ├── register.html     # Página de cadastro
│   ├── dashboard.html    # Painel do usuário
│   ├── add_plantation.html # Cadastro de plantação
│   ├── products.html     # Página de produtos
│   ├── weather.html      # Previsão do tempo
│   └── blog.html         # Blog
└── static/               # Arquivos estáticos
    ├── css/
    │   └── style.css     # Estilos CSS
    ├── js/
    │   └── script.js     # JavaScript
    └── images/           # Imagens (placeholder)
\`\`\`

## Funcionalidades Detalhadas

### Sistema de Autenticação
- Cadastro de usuários (produtores e compradores)
- Login com validação
- Sessões seguras
- Logout

### Dashboard do Produtor
- Visualização de estatísticas
- Listagem de plantações cadastradas
- Cadastro de novas plantações
- Edição e exclusão de plantações

### Produtos Agrícolas
- Catálogo de produtos (sementes, insumos, equipamentos)
- Filtros por categoria
- Informações de contato dos vendedores
- Design responsivo com cards

### Previsão do Tempo
- Busca por cidade
- Informações meteorológicas atuais
- Previsão para os próximos dias
- Interface intuitiva

### Blog
- Artigos sobre agricultura inteligente
- Design moderno com cards
- Informações do autor e data

## Dados de Teste

### Usuário de Teste
- **Email:** admin@agro.com
- **Senha:** 123456
- **Tipo:** Produtor

### Produtos Pré-cadastrados
- Sementes de Soja Premium
- Fertilizante NPK 20-05-20
- Trator Compacto 75CV

## Personalização

### Cores do Tema
As cores podem ser alteradas no arquivo `static/css/style.css`:
\`\`\`css
:root {
    --primary-color: #2d5016;    /* Verde escuro */
    --secondary-color: #4a7c59;  /* Verde médio */
    --accent-color: #8fbc8f;     /* Verde claro */
    --earth-color: #8b4513;      /* Cor terra */
    --light-green: #f0f8f0;      /* Verde muito claro */
}
\`\`\`

### Adicionando Novas Funcionalidades
1. Crie novas rotas no `app.py`
2. Adicione templates correspondentes em `templates/`
3. Implemente o JavaScript necessário em `static/js/script.js`
4. Adicione estilos em `static/css/style.css`

## Melhorias Futuras

- Integração com banco de dados real (PostgreSQL/MySQL)
- API de clima real (OpenWeatherMap)
- Sistema de upload de imagens
- Chat entre usuários
- Sistema de avaliações
- Integração com mapas
- Notificações push
- App mobile

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

- **Email:** contato@agrotechhub.com
- **Telefone:** (11) 99999-0000
- **Endereço:** São Paulo, SP

---

Desenvolvido com ❤️ para o agronegócio brasileiro.
