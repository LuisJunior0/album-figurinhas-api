from fastapi import FastAPI

# Cria uma instância do FastAPI
app = FastAPI()

# Cria uma rota básica (endpoint)
@app.get("/")
def read_root():
    return {"mensagem": "Álbum de Figurinhas API rodando!"}
