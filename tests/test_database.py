import pytest
from sqlalchemy.exc import SQLAlchemyError

from backend import database


def test_conexao_postgresql():
    try:
        assert database.testar_conexao() is True
    except SQLAlchemyError as erro:
        pytest.fail(f"Falha na conexao PostgreSQL: {erro}")
