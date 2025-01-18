# Inventory Management System

## Descrição

O Inventory Management System é uma aplicação web para gerenciar o inventário de produtos. A aplicação permite visualizar, adicionar, atualizar e deletar itens do inventário, bem como visualizar o histórico de movimentação dos produtos. A aplicação é composta por um backend desenvolvido com FastAPI e um frontend minimalista e moderno desenvolvido com Streamlit.

## Estrutura do Projeto

```
inventory_crud/
├── src/
│   ├── backend/
│   │   ├── controller/
│   │   │   ├── crud.py
│   │   │   └── routes.py
│   │   ├── models/
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── schemas/
│   │   │   └── schema.py
│   │   ├── main.py
│   │   └── Dockerfile
│   ├── frontend/
│   │   ├── app.py
│   │   └── Dockerfile
├── pyproject.toml
├── poetry.lock
├── docker-compose.yml
└── .env
```

## Tecnologias Utilizadas

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Banco de Dados**: PostgreSQL
- **Gerenciamento de Dependências**: Poetry
- **Containerização**: Docker e Docker Compose

## Pré-requisitos

- Docker
- Docker Compose

## Configuração do Ambiente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/inventory_crud.git
cd inventory_crud
```

2. Crie um arquivo .env na raiz do projeto e adicione as seguintes variáveis de ambiente:

```
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=seu_banco_de_dados
```

3. Construa e inicie os contêineres Docker:

```bash
docker-compose up --build
```

## Utilização

### Acessando o Frontend

Após iniciar os contêineres, você pode acessar o frontend do Streamlit no seu navegador:

```
http://localhost:8501
```

### Endpoints da API
A API FastAPI estará disponível em:

```
http://localhost:8000
```

### Endpoints Disponíveis

- **GET /api/items**: Retorna todos os itens do inventário.
- **GET /api/items/{item_id}**: Retorna um item específico pelo ID.
- **POST /api/items**: Adiciona um novo item ao inventário.
- **PUT /api/items/{item_id}**: Atualiza um item existente pelo ID.
- **DELETE /api/items/{item_id}**: Deleta um item pelo ID.
- **GET /api/movements/{product_id}**: Retorna o histórico de movimentação de um produto específico pelo ID.

### Funcionalidades do Frontend

- **Ver Itens**: Exibe todos os itens do inventário. Permite buscar um item específico pelo ID.
- **Adicionar Item**: Adiciona um novo item ao inventário.
- **Atualizar Item**: Atualiza um item existente. Os campos são pré-preenchidos com os valores atuais do item.
- **Deletar Item**: Deleta um item pelo ID.
- **Ver Histórico de Movimentação**: Exibe o histórico de movimentação de um produto específico pelo ID.

## Estrutura do Código

### Backend

- **backend/controller/crud.py**: Contém as funções CRUD para gerenciar os itens e o histórico de movimentação.
- **backend/controller/routes.py**: Define as rotas da API.
- **backend/model/database.py**: Configura a conexão com o banco de dados.
- **backend/model/models.py**: Define os modelos do banco de dados.
- **backend/schemas/schema.py**: Define os esquemas Pydantic para validação dos dados.
- **backend/main.py**: Inicializa a aplicação FastAPI e inclui as rotas.
- **backend/Dockerfile**: Define o Dockerfile para o backend.

### Frontend

- **frontend/app.py**: Contém a aplicação Streamlit para o frontend.
- **frontend/Dockerfile**: Define o Dockerfile para o frontend.