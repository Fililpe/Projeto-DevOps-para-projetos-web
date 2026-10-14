import uuid

from fastapi.testclient import TestClient

from backend.main import app


def autenticar_usuario(cliente: TestClient):
    email = f"produtos-{uuid.uuid4().hex}@example.com"
    senha = "Teste1234"

    cadastro = cliente.post(
        "/api/auth/register",
        json={
            "nome": "Usuario Produtos",
            "email": email,
            "senha": senha,
        },
    )
    assert cadastro.status_code == 201

    login = cliente.post(
        "/api/auth/login",
        json={"email": email, "senha": senha},
    )
    assert login.status_code == 200


def test_rotas_de_produtos_exigem_autenticacao():
    with TestClient(app) as cliente:
        consulta = cliente.get("/api/produtos")
        cadastro = cliente.post(
            "/api/produtos",
            json={
                "nome": "Produto sem sessao",
                "preco": "10.00",
                "quantidade": 1,
            },
        )

    assert consulta.status_code == 401
    assert cadastro.status_code == 401


def test_cadastro_consulta_e_paginacao_de_produtos():
    identificador = uuid.uuid4().hex

    with TestClient(app) as cliente:
        autenticar_usuario(cliente)

        primeiro = cliente.post(
            "/api/produtos",
            json={
                "nome": f"Produto {identificador} A",
                "descricao": "Produto criado no teste",
                "preco": "12.50",
                "quantidade": 3,
            },
        )
        segundo = cliente.post(
            "/api/produtos",
            json={
                "nome": f"Produto {identificador} B",
                "preco": "5.00",
            },
        )

        assert primeiro.status_code == 201
        assert primeiro.json()["nome"] == f"Produto {identificador} A"
        assert primeiro.json()["quantidade"] == 3
        assert segundo.status_code == 201
        assert segundo.json()["quantidade"] == 0

        consulta = cliente.get(
            "/api/produtos",
            params={"page": 1, "limit": 100},
        )
        pagina_um = cliente.get(
            "/api/produtos",
            params={"page": 1, "limit": 1},
        )
        pagina_dois = cliente.get(
            "/api/produtos",
            params={"page": 2, "limit": 1},
        )

        assert consulta.status_code == 200
        nomes = {produto["nome"] for produto in consulta.json()}
        assert f"Produto {identificador} A" in nomes
        assert f"Produto {identificador} B" in nomes

        assert pagina_um.status_code == 200
        assert pagina_dois.status_code == 200
        assert len(pagina_um.json()) == 1
        assert len(pagina_dois.json()) == 1
        assert pagina_um.json()[0]["id"] != pagina_dois.json()[0]["id"]


def test_produto_rejeita_preco_e_quantidade_negativos():
    with TestClient(app) as cliente:
        autenticar_usuario(cliente)

        preco_invalido = cliente.post(
            "/api/produtos",
            json={
                "nome": "Produto com preco invalido",
                "preco": "-0.01",
                "quantidade": 1,
            },
        )
        quantidade_invalida = cliente.post(
            "/api/produtos",
            json={
                "nome": "Produto com quantidade invalida",
                "preco": "1.00",
                "quantidade": -1,
            },
        )

    assert preco_invalido.status_code == 422
    assert quantidade_invalida.status_code == 422


def test_paginacao_rejeita_valores_fora_do_limite():
    with TestClient(app) as cliente:
        autenticar_usuario(cliente)

        pagina_invalida = cliente.get(
            "/api/produtos",
            params={"page": 0},
        )
        limite_invalido = cliente.get(
            "/api/produtos",
            params={"limit": 101},
        )

    assert pagina_invalida.status_code == 422
    assert limite_invalido.status_code == 422
