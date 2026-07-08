# Sticker Album API

API REST desenvolvida em **Python** com **FastAPI** para gerenciamento de álbuns de figurinhas. Possui autenticação JWT, controle de usuários e gerenciamento da coleção de figurinhas.

---

# 🚀 Funcionalidades

## 🔐 Autenticação

* Cadastro de usuários
* Login com JWT
* Login compatível com OAuth2 (Swagger)
* Refresh Token
* Rotas protegidas
* Validação de usuários ativos
* Senhas criptografadas com BCrypt

## 🎴 Figurinhas

* Adicionar figurinhas ao álbum
* Consultar uma figurinha específica
* Listar todas as figurinhas do usuário
* Atualizar automaticamente a quantidade de repetidas
* Remover figurinhas
* Listar figurinhas repetidas
* Calcular o progresso do álbum

## 🗄 Banco de Dados

* PostgreSQL (Desenvolvimento)
* Amazon RDS PostgreSQL (Produção)
* SQLAlchemy ORM
* Alembic (Migrations)

## 🐳 Docker

* Docker
* Docker Compose
* Ambiente de desenvolvimento (API + PostgreSQL)
* Ambiente de produção (API + Amazon RDS)

---

# 🛠 Tecnologias

* Python 3
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* Uvicorn
* Passlib
* BCrypt
* Python-Jose (JWT)
* Python-Dotenv
* Docker
* Docker Compose
* Amazon EC2
* Amazon RDS

---

# 📂 Estrutura do Projeto

```text
app/
├── routers/
│   ├── auth_routes.py
│   └── figurinha_routes.py
├── database.py
├── dependencies.py
├── models.py
├── schemas.py
└── main.py

alembic/
└── versions/

.env.example
Dockerfile
docker-compose.yml
docker-compose.aws.yml
requirements.txt
.gitignore
.dockerignore
```

---

# ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`.

```env
# Banco de Dados
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=db
DB_PORT=5432
DB_NAME=seu_banco

# JWT
SECRET_KEY=sua_chave
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **DB_HOST**
>
> * Desenvolvimento: `db`
> * Produção (AWS): endpoint do Amazon RDS

---

# 🐳 Executando Localmente

### Clonar o projeto

```bash
git clone https://github.com/LuisJunior0/album-figurinhas-api.git
cd album-figurinhas-api
```

### Configurar o `.env`

Mantenha:

```env
DB_HOST=db
```

### Subir os containers

```bash
docker compose up -d --build
```

### Executar as migrations

```bash
docker compose exec api alembic upgrade head
```

---

# ☁️ Executando na AWS

Configure o arquivo `.env` utilizando o endpoint do Amazon RDS.

Suba a aplicação:

```bash
docker compose -f docker-compose.aws.yml up -d --build
```

Execute as migrations:

```bash
docker compose -f docker-compose.aws.yml exec api alembic upgrade head
```

A API roda em um container Docker na **EC2**, enquanto o banco de dados utiliza o **Amazon RDS PostgreSQL**.

---

# 💻 Executando sem Docker

### Criar ambiente virtual

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar migrations

```bash
alembic upgrade head
```

### Iniciar a API

```bash
uvicorn app.main:app --reload
```

---

# 📚 Documentação

**Local**

* Swagger: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

**AWS**

* Swagger: `http://<IP_DA_EC2>/docs`

---

# 🔐 Endpoints

## Autenticação

| Método | Endpoint            | Descrição              |
| ------ | ------------------- | ---------------------- |
| POST   | `/auth/criar_conta` | Criar usuário          |
| POST   | `/auth/login`       | Login com JWT          |
| POST   | `/auth/login_form`  | Login OAuth2 (Swagger) |
| GET    | `/auth/refresh`     | Renovar token          |

## Figurinhas

> Requer `Authorization: Bearer <token>`

| Método | Endpoint                             | Descrição                 |
| ------ | ------------------------------------ | ------------------------- |
| GET    | `/figurinhas/listar`                 | Lista todas as figurinhas |
| GET    | `/figurinhas/{sigla}/{numero}`       | Busca uma figurinha       |
| POST   | `/figurinhas/criar_figurinha`        | Adiciona uma figurinha    |
| DELETE | `/figurinhas/remover_figurinha/{id}` | Remove uma figurinha      |
| GET    | `/figurinhas/repetidas`              | Lista repetidas           |
| GET    | `/figurinhas/progresso`              | Progresso do álbum        |

---

# 🔒 Segurança

* Senhas protegidas com BCrypt.
* Autenticação via JWT.
* Rotas protegidas por token.
* Na AWS, o acesso ao banco é realizado pelo Amazon RDS utilizando Security Groups.

---

# 👨‍💻 Autor

**Luis Junior**

Projeto desenvolvido para estudo de FastAPI, SQLAlchemy, Alembic, Docker e implantação em ambiente AWS (EC2 + RDS).
