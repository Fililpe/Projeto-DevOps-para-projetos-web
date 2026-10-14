
import re

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from backend.database import engine
from backend.security import gerar_hash_senha, verificar_senha


router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticacao"]
)


# -------------------------------
# MODELOS DE ENTRADA
# -------------------------------

class UsuarioCadastro(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    email: EmailStr
    senha: str

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError("O nome nao pode estar vazio")

        return valor

    @field_validator("email", mode="before")
    @classmethod
    def normalizar_email(cls, valor):
        if isinstance(valor, str):
            return valor.strip().lower()
        return valor

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, valor):
        if (
            len(valor) < 8
            or not re.search(r"[A-Z]", valor)
            or not re.search(r"[a-z]", valor)
            or not re.search(r"[0-9]", valor)
        ):
            raise ValueError(
                "A senha deve ter pelo menos 8 caracteres, "
                "uma letra maiuscula, uma minuscula e um numero"
            )

        if len(valor.encode("utf-8")) > 72:
            raise ValueError(
                "A senha excede o limite de 72 bytes"
            )

        return valor


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

    @field_validator("email", mode="before")
    @classmethod
    def normalizar_email(cls, valor):
        if isinstance(valor, str):
            return valor.strip().lower()
        return valor


# -------------------------------
# CADASTRO DE USUARIOS
# -------------------------------

@router.post("/register", status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(usuario: UsuarioCadastro):

    senha_hash = gerar_hash_senha(usuario.senha)

    try:
        with engine.begin() as conexao:
            resultado = conexao.execute(
                text("""
                    INSERT INTO usuarios (nome, email, senha_hash)
                    VALUES (:nome, :email, :senha_hash)
                    ON CONFLICT (email) DO NOTHING
                    RETURNING id, nome, email
                """),
                {
                    "nome": usuario.nome,
                    "email": str(usuario.email),
                    "senha_hash": senha_hash
                }
            ).mappings().first()

            if resultado is None:
                raise HTTPException(
                    status_code=409,
                    detail="O e-mail informado ja esta em uso"
                )

            return dict(resultado)

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="O e-mail informado ja esta em uso"
        )


# -------------------------------
# LOGIN DE USUARIOS
# -------------------------------

@router.post("/login")
def login(usuario: UsuarioLogin, request: Request):

    email = str(usuario.email)

    with engine.connect() as conexao:
        resultado = conexao.execute(
            text("""
                SELECT id, nome, email, senha_hash
                FROM usuarios
                WHERE email = :email
            """),
            {"email": email}
        ).mappings().first()

    if not resultado:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos"
        )

    if (
        len(usuario.senha.encode("utf-8")) > 72
        or not verificar_senha(
            usuario.senha, resultado["senha_hash"]
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos"
        )

    request.session.clear()
    request.session["usuario_id"] = resultado["id"]

    return {
        "mensagem": "Login realizado com sucesso",
        "usuario": {
            "id": resultado["id"],
            "nome": resultado["nome"],
            "email": resultado["email"]
        }
    }


# -------------------------------
# LOGOUT DE USUARIOS
# -------------------------------

@router.post("/logout")
def logout(request: Request):

    request.session.clear()

    return {
        "mensagem": "Logout realizado com sucesso"
    }
