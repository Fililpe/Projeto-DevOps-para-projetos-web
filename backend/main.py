
"""Ponto de entrada da aplicacao FastAPI."""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from backend.auth import router as auth_router
from backend.produtos import router as produtos_router

from pathlib import Path
from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

load_dotenv()

app = FastAPI(
    title="Sistema de Estoque",
    version="0.1.0"
)

secret_key = os.environ["SECRET_KEY"]

if len(secret_key) < 32:
    raise RuntimeError(
        "SECRET_KEY deve ter pelo menos 32 caracteres"
    )

# Configuracao das sessoes de autenticacao
app.add_middleware(
    SessionMiddleware,
    secret_key=secret_key,
    session_cookie="estoque_session",
    max_age=3600,
    same_site="lax",
    https_only=False
)

# Registra as rotas de autenticacao
app.include_router(auth_router)
app.include_router(produtos_router)


@app.get("/api/health", tags=["infra"])
def health():
    """Verifica se a API esta funcionando."""
    return {"status": "ok"}

# Precisa ficar sempre no final do arquivo
app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend"
)
