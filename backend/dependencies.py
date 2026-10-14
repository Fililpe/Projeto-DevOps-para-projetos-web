"""Dependencias reutilizaveis das rotas da API."""

from fastapi import HTTPException, Request, status


def exigir_usuario_autenticado(request: Request) -> int:
    """Retorna o ID da sessao ou bloqueia o acesso anonimo."""
    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticacao necessaria",
        )

    return usuario_id
