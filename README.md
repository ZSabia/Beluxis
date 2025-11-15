# Beluxis

# Beluxis

Bem-vindo(a) ao Beluxis!

O seu salão de cabeleireira de confiança. Produtos e serviços de beleza para você.

Beluxis é um site que une e facilita o atendimento de salões de beleza. Permite o cadastro de clientes, produtos, serviços, agendamentos e inclui um painel administrativo para controle.

## Funcionalidades

- **Autenticação de Usuários**: Registro, login e logout de clientes.
- **Produtos**: Visualização de produtos disponíveis, com painel admin para CRUD (criar, ler, atualizar, deletar).
- **Serviços**: Visualização de serviços oferecidos, com painel admin para CRUD.
- **Agendamentos**: Clientes podem solicitar agendamentos de serviços, e admins podem aprovar ou negar.
- **Calendário**: Visualização de agendamentos em formato de calendário.
- **Perfil**: Clientes podem visualizar seus agendamentos e editar perfil.
- **Admin Panel**: Acesso restrito para admins gerenciarem produtos, serviços e agendamentos.

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Banco de Dados**: PostgreSQL (produção) ou SQLite (desenvolvimento)
- **ORM**: SQLAlchemy
- **Migrações**: Flask-Migrate
- **Autenticação**: Flask-Login
- **Formulários**: Flask-WTF
- **Deploy**: Gunicorn, Docker

## Instalação e Execução

### Pré-requisitos

- Python 3.11+
- PostgreSQL (opcional, para produção)
- Docker (opcional, para execução com container)

### Instalação Local (SQLite)

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd beluxis
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou venv\Scripts\activate no Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco de dados:
   ```bash
   flask db init  # se necessário
   flask db migrate
   flask db upgrade
   ```

5. Execute o aplicativo:
   ```bash
   python main.py
   ```

   O app estará disponível em `http://localhost:5000`.

### Execução com Docker

1. Certifique-se de ter Docker e Docker Compose instalados.

2. Execute:
   ```bash
   docker-compose up --build
   ```

   O app estará disponível em `http://localhost:8000`.

## Deploy

### Heroku

1. Crie um app no Heroku.
2. Configure variáveis de ambiente: `DATABASE_URL`, `SECRET_KEY`.
3. Faça push do código para o Heroku Git.

### Google Cloud Run

1. Build a imagem Docker.
2. Faça deploy no Cloud Run com a imagem.

## Estrutura do Projeto

- `beluxis/`: Código principal da aplicação.
  - `__init__.py`: Inicialização do app Flask.
  - `models.py`: Modelos do banco de dados.
  - `routes.py`: Rotas e lógica da aplicação.
  - `forms.py`: Formulários WTForms.
  - `calendario.py`: Lógica para geração do calendário.
  - `template_helpers.py`: Funções auxiliares para templates.
  - `templates/`: Templates HTML.
  - `static/`: Arquivos estáticos (CSS, imagens).
- `migrations/`: Migrações do banco de dados.
- `instance/`: Arquivos de instância (configurações, banco SQLite).
- `main.py`: Ponto de entrada.
- `requirements.txt`: Dependências Python.
- `Procfile`: Para deploy no Heroku.
- `Dockerfile`: Para containerização.
- `docker-compose.yml`: Para execução local com Docker.

## Contribuição

1. Fork o projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am "Adiciona nova feature"`.
4. Push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
