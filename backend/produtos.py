"""Rotas de cadastro e consulta do estoque compartilhado."""

from decimal import Decimal

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import text

from backend.database import engine
from backend.dependencies import exigir_usuario_autenticado


router = APIRouter(
    prefix="/api/produtos",
    tags=["Produtos"],
)


class ProdutoCadastro(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    descricao: str | None = None
    preco: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    quantidade: int = Field(default=0, ge=0)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError("O nome nao pode estar vazio")

        return valor

    @field_validator("descricao")
    @classmethod
    def normalizar_descricao(cls, valor: str | None) -> str | None:
        if valor is None:
            return None

        valor = valor.strip()
        return valor or None


class ProdutoResposta(ProdutoCadastro):
    id: int


@router.post(
    "",
    response_model=ProdutoResposta,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_produto(
    produto: ProdutoCadastro,
    _usuario_id: int = Depends(exigir_usuario_autenticado),
):
    """Cadastra um produto no estoque global."""
    with engine.begin() as conexao:
        resultado = conexao.execute(
            text("""
                INSERT INTO produtos (nome, descricao, preco, quantidade)
                VALUES (:nome, :descricao, :preco, :quantidade)
                RETURNING id, nome, descricao, preco, quantidade
            """),
            {
                "nome": produto.nome,
                "descricao": produto.descricao,
                "preco": produto.preco,
                "quantidade": produto.quantidade,
            },
        ).mappings().one()

    return dict(resultado)


@router.get("", response_model=list[ProdutoResposta])
def listar_produtos(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    _usuario_id: int = Depends(exigir_usuario_autenticado),
):
    """Lista o estoque global com paginacao."""
    offset = (page - 1) * limit

    with engine.connect() as conexao:
        resultados = conexao.execute(
            text("""
                SELECT id, nome, descricao, preco, quantidade
                FROM produtos
                ORDER BY id
                LIMIT :limit OFFSET :offset
            """),
            {"limit": limit, "offset": offset},
        ).mappings().all()

    return [dict(produto) for produto in resultados]
