
import uuid

from fastapi.testclient import TestClient

from backend.main import app


def test_fluxo_autenticacao():
    email = f"teste-{uuid.uuid4().hex}@example.com"

    with TestClient(app) as cliente:

        # Cadastro
        cadastro = cliente.post(
            "/api/auth/register",
            json={
                "nome": "Usuario Teste",
                "email": email,
                "senha": "Teste1234"
            }
        )

        assert cadastro.status_code == 201
        assert cadastro.json()["email"] == email
        assert "senha_hash" not in cadastro.json()

        # Cadastro duplicado
        duplicado = cliente.post(
            "/api/auth/register",
            json={
                "nome": "Outro Usuario",
                "email": email,
                "senha": "Teste1234"
            }
        )

        assert duplicado.status_code == 409

        # Login com senha incorreta
        invalido = cliente.post(
            "/api/auth/login",
            json={
                "email": email,
                "senha": "SenhaErrada123"
            }
        )

        assert invalido.status_code == 401

        # Login correto
        login = cliente.post(
            "/api/auth/login",
            json={
                "email": email,
                "senha": "Teste1234"
            }
        )

        assert login.status_code == 200
        assert login.json()["usuario"]["email"] == email
        assert "estoque_session" in cliente.cookies

        # Logout
        logout = cliente.post("/api/auth/logout")

        assert logout.status_code == 200
        assert "estoque_session" not in cliente.cookies
