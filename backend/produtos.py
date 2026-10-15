"""Rotas de cadastro e consulta do estoque compartilhado."""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
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


@router.put("/{produto_id}", response_model=ProdutoResposta)
def editar_produto(
    produto_id: int,
    produto: ProdutoCadastro,
    _usuario_id: int = Depends(exigir_usuario_autenticado),
):
    """Atualiza todos os campos de um produto existente."""
    with engine.begin() as conexao:
        resultado = conexao.execute(
            text("""
                UPDATE produtos
                SET nome = :nome,
                    descricao = :descricao,
                    preco = :preco,
                    quantidade = :quantidade
                WHERE id = :id
                RETURNING id, nome, descricao, preco, quantidade
            """),
            {
                "id": produto_id,
                "nome": produto.nome,
                "descricao": produto.descricao,
                "preco": produto.preco,
                "quantidade": produto.quantidade,
            },
        ).mappings().first()

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto nao encontrado",
        )

    return dict(resultado)


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_produto(
    produto_id: int,
    _usuario_id: int = Depends(exigir_usuario_autenticado),
):
    """Remove um produto do estoque."""
    with engine.begin() as conexao:
        resultado = conexao.execute(
            text("DELETE FROM produtos WHERE id = :id RETURNING id"),
            {"id": produto_id},
        ).first()

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto nao encontrado",
        )
