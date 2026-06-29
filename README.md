# Sticker Album API

API REST desenvolvida em Python com FastAPI para gerenciamento de álbuns de figurinhas, incluindo autenticação JWT, controle de usuários e gerenciamento completo das figurinhas de cada coleção.

## 🚀 Funcionalidades

### Autenticação

* Cadastro de usuários
* Login com JWT
* Login compatível com OAuth2
* Refresh Token
* Rotas protegidas por autenticação

### Gerenciamento de Figurinhas

* Adicionar figurinhas ao álbum
* Atualizar automaticamente a quantidade de figurinhas repetidas
* Remover figurinhas
* Consulta de figurinhas específicas
* Listagem completa do álbum
* Listagem de figurinhas repetidas
* Cálculo automático do progresso do álbum

### Banco de Dados

* PostgreSQL
* SQLAlchemy ORM
* Migrações com Alembic

---

## 🛠 Tecnologias Utilizadas

* Python 3
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* JWT (python-jose)
* Passlib + Bcrypt
* Pydantic
* Uvicorn
* Python Dotenv

---

## 📂 Estrutura do Projeto

```text
app/
├── routers/
│   ├── auth_routes.py
│   └── figurinha_routes.py
│
├── models.py
├── schemas.py
├── database.py
├── dependencies.py
├── main.py
│
.env
requirements.txt
```

---

## ⚙️ Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/album-figurinhas-api.git

cd album-figurinhas-api
```

### 2. Criar ambiente virtual

Windows:

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv

source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DATABASE_URL=postgresql://usuario:senha@localhost:5432/sticker_album
```

---

## ▶️ Executando a API

```bash
uvicorn app.main:app --reload
```

Após iniciar:

```text
http://127.0.0.1:8000
```

Documentação automática:

```text
http://127.0.0.1:8000/docs
```

Swagger ReDoc:

```text
http://127.0.0.1:8000/redoc
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
  "access_token": "...",
  "refresh_token": "...",
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

Todas as rotas abaixo exigem autenticação JWT.

---

## Listar Figurinhas

GET `/figurinhas/listar`

### Resposta

```json
[
  {
    "sigla": "BRA",
    "numero": 10,
    "quantidade": 2,
    "observacao": "Neymar"
  }
]
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

POST `/figurinhas/remover_figurinha`

### Exemplo

```json
{
  "sigla": "BRA",
  "numero": 10,
  "quantidade": 1
}
```

---

## Consultar Figurinha

GET `/figurinhas/{sigla}/{numero}`

### Exemplo

```text
/figurinhas/BRA/10
```

---

## Verificar Repetidas

GET `/figurinhas/repetidas`

### Resposta

```json
[
  {
    "sigla": "BRA",
    "numero": 10,
    "quantidade": 2,
    "observacao": "Neymar"
  }
]
```

---

## Progresso do Álbum

GET `/figurinhas/progresso`

### Resposta

```json
{
  "figurinhas": 450,
  "total_album": 980,
  "progresso_percentual": 45.92
}
```

---

## 🔒 Segurança

A autenticação é baseada em JWT.

Para acessar rotas protegidas:

```http
Authorization: Bearer SEU_TOKEN
```

---

## 📈 Melhorias Futuras

* Docker
* Testes automatizados
* Paginação de resultados
* Cache com Redis
* Deploy em nuvem
* Versionamento da API
* CI/CD com GitHub Actions

---

## 👨‍💻 Autor

Luis Junior

Projeto desenvolvido para estudos de FastAPI, SQLAlchemy, PostgreSQL e autenticação JWT.
