"""Ponto de entrada da aplicacao. Rodar com: uvicorn backend.main:app --reload"""
from fastapi import FastAPI

app = FastAPI(title="Sistema de Estoque", version="0.1.0")


@app.get("/api/health", tags=["infra"])
def health():
    """Usado para saber se a API esta no ar (smoke test)."""
    return {"status": "ok"}
