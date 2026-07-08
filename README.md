# Sticker Album API

API REST desenvolvida em Python com FastAPI para gerenciamento de álbuns de figurinhas, incluindo autenticação JWT, controle de usuários e gerenciamento completo das figurinhas de cada coleção.

---

# 🚀 Funcionalidades

## 🔐 Autenticação e Autorização

* Cadastro de usuários
* Login com JWT
* Login compatível com OAuth2
* Refresh Token
* Rotas protegidas por autenticação
* Validação de usuários ativos
* Controle de acesso baseado no usuário autenticado
* Senhas protegidas utilizando BCrypt

## 🎴 Gerenciamento de Figurinhas

* Adicionar figurinhas ao álbum
* Consultar figurinhas específicas
* Listar todas as figurinhas do usuário
* Atualização automática da quantidade de figurinhas repetidas
* Remover figurinhas da coleção
* Listagem de figurinhas repetidas
* Cálculo automático do progresso do álbum
* Associação automática das figurinhas ao usuário autenticado

## 🗄 Banco de Dados

* PostgreSQL
* SQLAlchemy ORM
* Alembic para versionamento do banco de dados
* Migrations automatizadas
* Criação e atualização controlada do schema

## 🐳 Containerização

* Docker
* Docker Compose
* API e banco executando em containers independentes
* Comunicação interna via rede Docker
* Configuração através de variáveis de ambiente
* Ambiente reproduzível em qualquer máquina com Docker

---

# 🛠 Tecnologias Utilizadas

* Python 3
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* Uvicorn
* Python Dotenv
* Passlib
* BCrypt
* Python-Jose (JWT)
* Docker
* Docker Compose

---

# 📂 Estrutura do Projeto

```text
app/
├── routers/
│   ├── auth_routes.py
│   └── figurinha_routes.py
│
├── database.py
├── dependencies.py
├── models.py
├── schemas.py
├── main.py
│
alembic/
├── versions/
│
.env.example
Dockerfile
docker-compose.yml
requirements.txt
.gitignore
.dockerignore
```

---

# ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto utilizando o modelo abaixo:

```env
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=db
DB_PORT=5432
DB_NAME=album_db

SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# 🐳 Executando com Docker

## Pré-requisitos

* Docker Desktop instalado

## 1. Clonar o repositório

```bash
git clone https://github.com/LuisJunior0/album-figurinhas-api.git

cd album-figurinhas-api
```

## 2. Criar o arquivo .env

Utilize o `.env.example` como referência.

## 3. Construir e iniciar os containers

```bash
docker compose up -d --build
```

## 4. Executar as migrations

Após os containers iniciarem:

```bash
docker compose exec api alembic upgrade head
```

O Alembic aplicará todas as migrations pendentes ao banco de dados.

## 5. Verificar os containers

```bash
docker ps
```

---

# 📚 Documentação da API

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# 💻 Executando Localmente

## Criar ambiente virtual

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

## Instalar dependências

```bash
pip install -r requirements.txt
```

## Aplicar migrations

```bash
alembic upgrade head
```

## Executar aplicação

```bash
uvicorn app.main:app --reload
```

---

# 🔐 Endpoints de Autenticação

## Criar Conta

POST `/auth/criar_conta`

### Exemplo

```json
{
  "nome": "Luis",
  "email": "luis@email.com",
  "senha": "123456"
}
```

---

## Login

POST `/auth/login`

### Exemplo

```json
{
  "email": "luis@email.com",
  "senha": "123456"
}
```

### Resposta

```json
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "token_type": "Bearer"
}
```

---

## Login OAuth2

POST `/auth/login_form`

---

## Refresh Token

GET `/auth/refresh`

---

# 🎴 Endpoints de Figurinhas

Todas as rotas exigem autenticação JWT.

## Listar Figurinhas

GET `/figurinhas/listar`

---

## Consultar Figurinha

GET `/figurinhas/{sigla}/{numero}`

Exemplo:

```text
/figurinhas/BRA/10
```

---

## Adicionar Figurinha

POST `/figurinhas/criar_figurinha`

### Exemplo

```json
{
  "sigla": "BRA",
  "numero": 10,
  "quantidade": 1,
  "observacao": "Neymar"
}
```

---

## Remover Figurinha

DELETE `/figurinhas/remover_figurinha/{id}`

---

## Listar Figurinhas Repetidas

GET `/figurinhas/repetidas`

---

## Consultar Progresso do Álbum

GET `/figurinhas/progresso`

### Exemplo de resposta

```json
{
  "figurinhas": 450,
  "total_album": 980,
  "progresso_percentual": 45.92
}
```

---

# 🔒 Segurança

A API utiliza autenticação baseada em JWT.

Para acessar endpoints protegidos:

```http
Authorization: Bearer SEU_TOKEN
```

As senhas dos usuários são armazenadas utilizando hash BCrypt e nunca são persistidas em texto puro.

---

# 🗃 Migrations com Alembic

Criar uma nova migration:

```bash
alembic revision --autogenerate -m "descricao_da_migration"
```

Ou utilizando Docker:

```bash
docker compose exec api alembic revision --autogenerate -m "descricao_da_migration"
```

Aplicar migrations:

```bash
alembic upgrade head
```

Ou utilizando Docker:

```bash
docker compose exec api alembic upgrade head
```

---

# 📈 Melhorias Futuras

* Testes automatizados
* Paginação de resultados
* Cache com Redis
* CI/CD com GitHub Actions
* Deploy em nuvem
* Monitoramento e observabilidade
* Versionamento da API

---

# 👨‍💻 Autor

Luis Junior

Projeto desenvolvido para estudos de FastAPI, SQLAlchemy, PostgreSQL, autenticação JWT, Alembic e Docker.
